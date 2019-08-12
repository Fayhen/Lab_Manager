import os
import jwt
import datetime
from flask import Blueprint, render_template, redirect, url_for, request, make_response, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from LabManager import app, db, bcrypt
from LabManager.dbModels import PersonType, Gender, Person, User
from LabManager.maSchemas import user_schema, users_schema, person_schema
from LabManager.auth.forms import RegistrationForm, LoginForm, UpdateAccountForm
from LabManager.auth.utils import save_profile_picture, token_required


auth = Blueprint("auth", __name__)


@auth.route("/logon", methods=["GET", "POST"])
def logon():
    form_signUp = RegistrationForm()
    form_signIn = LoginForm()

    # Account successfully created
    if form_signUp.submit_signUp.data and form_signUp.validate():
        new_person = Person(first_name=None, last_name=None, middle_name=None,
                            sex=None, birthday=None, occupation=None, institution=None,
                            timedelta=None)
        db.session.add(new_person)
        db.session.commit()

        hashed_password = bcrypt.generate_password_hash(form_signUp.password.data).decode("utf-8")
        new_user = User(username=form_signUp.username.data, email=form_signUp.email.data,
                        password=hashed_password, own_info=new_person)
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"Account created for {form_signUp.username.data}. You can now Log In.", "success")
        return redirect(url_for("main.home"))
    
    # User successfully logged in
    if form_signIn.submit_signIn.data and form_signIn.validate():
        user = User.query.filter_by(email=form_signIn.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_signIn.password.data):
            login_user(user, remember=form_signIn.remember_me.data)
            next_page = request.args.get("next")
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Invalid credentials. Please check your email and password.", "error")

    return render_template("logon.html", title="User Login",
                            form_signUp=form_signUp, form_signIn=form_signIn)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    user = User.query.filter_by(username=current_user.username).first()
    person_data = user.own_info

    requires_update = True if (person_data.first_name == None) else False


    if form.submit.data and form.validate():

        if form.picture.data:
            image_filepath = os.path.join(app.root_path, person_data.image_filepath)
            picture, path = save_profile_picture(form.picture.data, image_filepath)
            person_data.image_file = picture
            person_data.image_filepath = path

        current_user.username = form.username.data
        current_user.email = form.email.data
        person_data.first_name = form.first_name.data
        person_data.middle_name = form.middle_name.data
        person_data.last_name = form.last_name.data
        person_data.sex = form.sex.data
        person_data.birthday = form.birthday.data
        person_data.phone = form.phone.data
        person_data.occupation = form.occupation.data
        person_data.institution = form.institution.data

        db.session.add(current_user)
        db.session.add(person_data)
        db.session.commit()
        flash("You account information has been updated.", "success")

        return redirect(url_for("auth.account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = person_data.first_name
        form.middle_name.data = person_data.middle_name
        form.last_name.data = person_data.last_name
        form.birthday.data = person_data.birthday
        form.sex.data = person_data.sex
        form.phone.data = person_data.phone
        form.occupation.data = person_data.occupation
        form.institution.data = person_data.institution


    image_file = url_for("static", filename="profile_pics/" + person_data.image_file)

    return render_template("account.html", title="User Account",
                            image_file=image_file, form=form,
                            requires_update=requires_update)


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
        response = {
                 'message': 'Field trip entry does not exist.'
                   }
        return jsonify(response), 404

    return jsonify(user_schema.dump(user).data)


@auth.route("/auth/update/<int:id>", methods=["PUT"])
@token_required
def users_update(current_user, id):
    user = User.query.get(id)
    if user is None:
        response = {
                 'message': 'Field trip entry does not exist.'
                   }
        return jsonify(response), 404

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
    # Require bollean input to determine whete Person data should also be erased
    user = User.query.get(id)
    person_id = user.person_id
    if user is None:
        response = {
                 'message': 'Field trip entry does not exist.'
                   }
        return jsonify(response), 404

    delete_person = request.json["delete_person"]
    response = user_schema.dump(user).data

    data=[]
    data.append({"delete_person": delete_person})
    data.append(response)

    db.session.delete(user)
    db.session.commit()

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
        response = {
                 'message': 'User entry does not exist.'
                   }
        return jsonify(response), 404

    # Check password and generate token
    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({
            "id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }, app.config["SECRET_KEY"])

        return jsonify({"token": token.decode("UTF-8")})

    return make_response("Could not verify.", 401, {"WWW-Authenticate": "Basic-realm='Login required."})



