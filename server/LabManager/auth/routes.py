import os
import jwt
import datetime
from flask import Blueprint, request, make_response, jsonify
from LabManager import app, db, bcrypt
from LabManager.dbModels import PersonType, Gender, Person, User
from LabManager.maSchemas import user_schema, users_schema, person_schema
from LabManager.auth.utils import save_profile_picture, token_required


auth = Blueprint("auth", __name__)


@auth.route("/auth/users", methods=["GET"])
@token_required
def users_all(current_user):
    users = User.query.all()

    return jsonify(users_schema.dump(users).data)


@auth.route("/auth/add", methods=["POST"])
def users_add():
    username = request.json["username"]
    email = request.json["email"]
    raw_password = request.json["password"]
    password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    if request.json["person_id"]:
        person_id = request.json["person_id"]
    else:
        new_person = Person(
            type_id = 1,
            gender_id = 3
        )
        db.session.add(new_person)
        db.session.commit()
        person_id = new_person.id
    
    new_user = User(
        username=username,
        email=email,
        password=password,
        person_id=person_id
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user).data)


@auth.route("/auth/<int:id>", methods=["GET"])
@token_required
def users_fetch(current_user, id):
    user = User.query.get(id)
    if user is None:
        return make_response("Field trip entry does not exist.", 404)

    return jsonify(user_schema.dump(user).data)


@auth.route("/auth/update/<int:id>", methods=["PUT"])
@token_required
def users_update(current_user, id):
    user = User.query.get(id)
    if user is None:
        return make_response("Field trip entry does not exist.", 404)

    username = request.json["username"]
    email = request.json["email"]
    raw_password = request.json["password"]
    password = bcrypt.generate_password_hash(raw_password).decode("utf-8")
    person_id = request.json["person_id"]

    user.username = username
    user.email = email
    user.password = password
    user.person_id=person_id

    db.session.commit()

    return jsonify(user_schema.dump(user).data)


@auth.route("/auth/delete/<int:id>", methods=["DELETE"])
@token_required
def users_delete(current_user, id):
    user = User.query.get(id)
    person_id = user.person_id
    if user is None:
        return make_response("Field trip entry does not exist.", 404)

    delete_person = request.json["delete_person"]
    response = user_schema.dump(user).data

    data=[]
    data.append({"delete_person": delete_person})
    data.append(response)

    db.session.delete(user)
    db.session.commit()

    # Add boolean on request to determine wheter 'Person' data should also be erased
    if delete_person == "true":
        person = Person.query.get(person_id)
        data.append(person_schema.dump(person).data)
        db.session.delete(person)
        db.session.commit()

    return jsonify(data)


@auth.route("/auth/login", methods=["POST"])
def auth_login():
    auth = request.authorization
    
    # Check if data is present
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify.", 401, {"WWW-Authenticate": "Basic-realm='Login required."})

    # Query user from db
    user = User.query.filter_by(username=auth.username).first()
    if user is None:
        return make_response("Field trip entry does not exist.", 404)

    # Check password and generate token
    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({
            "id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config["SECRET_KEY"])

        return jsonify({"token": token.decode("UTF-8")})

    return make_response("Could not verify.", 401, {"WWW-Authenticate": "Basic-realm='Login required."})


