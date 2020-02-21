import os
import jwt
import datetime, time
from flask import Blueprint, request, make_response, jsonify
from LabManager import app, db, bcrypt
from LabManager.dbModels import PersonType, Gender, Person, User
from LabManager.maSchemas import user_schema, users_schema, person_schema, profile_schema
from LabManager.auth.utils import token_required


auth = Blueprint("auth", __name__)


@auth.route("/auth/users", methods=["GET"])
@token_required
def users_all(current_user):
    users = User.query.all()

    return jsonify(users_schema.dump(users))


@auth.route("/auth/add", methods=["POST"])
def users_add():
    username = request.json["username"]
    query_name = User.query.filter_by(username=username).first()
    if query_name is not None:
        return make_response("Resource already exists.", 409)
    
    email = request.json["email"]
    query_email = User.query.filter_by(email=email).first()
    if query_email is not None:
        return make_response("Resource already exists.", 409)

    raw_password = request.json["password"]
    password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    # if request.json["person_id"]:
    #     person_id = request.json["person_id"]
    # else:
    new_person = Person()
    db.session.add(new_person)
    db.session.commit()
    person_id = new_person.id
    
    new_user = User(
        username = username,
        email = email,
        password = password,
        created = str(time.time()),
        last_modified = str(time.time()),
        person_id=person_id
        )

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify(user_schema.dump(new_user)), 201)


@auth.route("/auth/user", methods=["GET"])
@token_required
def user_fetch(current_user):

    return make_response(jsonify(user_schema.dump(current_user)), 200)


@auth.route("/auth/profile", methods=["GET"])
@token_required
def get_profile(current_user):

    return make_response(jsonify(profile_schema.dump(current_user)), 200)


@auth.route("/auth/profile", methods=["PUT"])
@token_required
def profile_update(current_user):
    username = request.json["username"]
    email = request.json["email"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    middle_name = request.json["middle_name"]
    phone = request.json["phone"]
    birthday = request.json["birthday"]
    occupation = request.json["occupation"]
    institution = request.json["institution"]
    type_id = request.json["type_id"]
    gender_id = request.json["gender_id"]

    # Add data changes to User table
    current_user.username = username
    current_user.email = email

    # Verify and add password change
    if request.json["password"]:
        raw_password = request.json["password"]
        password = bcrypt.generate_password_hash(raw_password).decode("utf-8")
        current_user.password = password

    # Query for User's corresponding Person object by its ID
    person = Person.query.get(current_user.person_id)

    # Add data changes to Person table
    person.first_name = first_name
    person.last_name = last_name
    person.middle_name = middle_name
    person.phone = phone
    person.birthday = birthday
    person.occupation = occupation
    person.institution = institution
    person.type_id = type_id
    person.gender_id = gender_id

    # Commit changes
    db.session.commit()

    return make_response(jsonify(profile_schema.dump(current_user)), 202)


@auth.route("/auth/delete", methods=["DELETE"])
@token_required
def user_delete(current_user):

    delete_person = request.json["delete_person"]
    user_data = user_schema.dump(current_user)
    person_id = current_user.person_id

    response={}
    response["delete_person"] = delete_person
    response["user"] = user_data

    db.session.delete(current_user)
    db.session.commit()

    # Add boolean on request to determine wheter 'Person' data should also be erased
    if delete_person == True:
        person = Person.query.get(person_id)
        response["personnel"] = person_schema.dump(person)
        db.session.delete(person)
        db.session.commit()

    return jsonify(response)


@auth.route("/auth/login", methods=["POST"])
def auth_login():
    auth = request.json["user"]
    
    # Check if data is present
    if not auth or not auth["email"] or not auth["password"]:
        return make_response("Absent credentials.", 400, {"WWW-Authenticate": "Basic-realm='Login required."})

    # Query user from db
    user = User.query.filter_by(email=auth["email"]).first()
    if user is None:
        return make_response("Invalid credentials.", 401)

    # Check password and generate token
    if bcrypt.check_password_hash(user.password, auth["password"]):
        token = jwt.encode({
            "id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config["SECRET_KEY"])

        return jsonify({"token": token.decode("UTF-8")})

    return make_response("Invalid credentials.", 401, {"WWW-Authenticate": "Basic-realm='Login required."})


@auth.route("/auth/test", methods=["GET"])
def auth_test():
    
    return make_response("Python server says 'hi'. :D", 200)
