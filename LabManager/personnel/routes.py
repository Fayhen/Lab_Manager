from datetime import datetime, date, time
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from LabManager import db
from LabManager.dbModels import PersonType, Gender, Person, FrequencyEvent
from LabManager.maSchemas import type_schema, types_schema, gender_schema, genders_schema, person_schema, people_schema, frequency_schema, frequencies_schema


personnel = Blueprint("personnel", __name__)


# Backend ops, might be erased upon deployement in favor of pre-populating SQL scripts
@personnel.route("/genders/all", methods=["GET"])
def gender_all():
    genders = Gender.query.all()

    return jsonify(genders_schema.dump(genders).data)

@personnel.route("/genders/add", methods=["POST"])
def gender_add():
    gender_name = request.json["gender_name"]
    new_gender = Gender(gender_name=gender_name)
    db.session.add(new_gender)
    db.session.commit()

    return jsonify(gender_schema.dump(new_gender).data)

@personnel.route("/genders/<int:id>", methods=["POST"])
def gender_fetch(id):
    gender = Gender.query.get(id)

    return jsonify(gender_schema.dump(gender).data)

@personnel.route("/genders/update/<int:id>", methods=["PUT"])
def gender_update(id):
    gender = Gender.query.get(id)
    gender_name = request.json(["gender_name"])
    gender.gender_name = gender_name
    db.session.commit()

    return jsonify(gender_schema.dump(gender).data)

@personnel.route("/genders/delete/<int:id>", methods=["DELETE"])
def gender_delete(id):
    gender = Gender.query.get(id)
    response = gender_schema.dump(gender).data
    db.session.delete(gender)
    db.session.commit()

    return jsonify(response)

@personnel.route("/persontypes/all", methods=["GET"])
def type_all():
    types = PersonType.query.all()

    return jsonify(types_schema.dump(types).data)

@personnel.route("/persontypes/add", methods=["POST"])
def type_add():
    type_name = request.json["type_name"]
    new_type = PersonType(type_name=type_name)
    db.session.add(new_type)
    db.session.commit()

    return jsonify(type_schema.dump(new_type).data)

@personnel.route("/persontypes/<int:id>", methods=["POST"])
def type_fetch(id):
    persontype = PersonType.query.get(id)

    return jsonify(type_schema.dump(persontype).data)

@personnel.route("/persontypes/update/<int:id>", methods=["PUT"])
def type_update(id):
    persontype = PersonType.query.get(id)
    type_name = request.json(["type_name"])
    persontype.type_name = type_name
    db.session.commit()

    return jsonify(type_schema.dump(persontype).data)

@personnel.route("/persontypes/delete/<int:id>", methods=["DELETE"])
def type_delete(id):
    persontype = PersonType.query.get(id)
    response = type_schema.dump(persontype).data
    db.session.delete(persontype)
    db.session.commit()

    return jsonify(response)

# Personnel ops
@personnel.route("/personnel")
@login_required
def lab_personnel():
    return render_template("personnel.html", title="Laboratory Personnel")


@personnel.route("/personnel/all", methods=["GET"])
@token_required
def personnel_all(current_user):
    personnel = Person.query.all()

    return jsonify(people_schema.dump(personnel).data)

@personnel.route("/personnel/add", methods=["POST"])
@token_required
def personnel_add(current_user):
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    middle_name = request.json["middle_name"]
    phone = request.json["phone"]
    occupation = request.json["occupation"]
    institution = request.json["institution"]
    type_id = request.json["type_id"]
    gender_id = request.json["gender_id"]
    # Parse dates
    if request.json["birthday"]:
        birthday = datetime.strptime(request.json["birthday"], "%Y-%m-%d")
    else:
        birthday = None

    new_person = Person(
        first_name = first_name,
        last_name = last_name,
        middle_name = middle_name,
        phone = phone,
        birthday = birthday,
        occupation = occupation,
        institution = institution,
        type_id = type_id,
        gender_id = gender_id
    )

    db.session.add(new_person)
    db.session.commit()

    return jsonify(person_schema.dump(new_person).data)


@personnel.route("/personnel/<int:id>", methods=["GET"])
@token_required
def personnel_fetch(current_user, id):
    person = Person.query.get(id)
    if person is None:
        response = {
                 'message': 'This person entry does not exist.'
                   }
        return jsonify(response), 404
    
    return jsonify(person_schema.dump(person).data)


@personnel.route("/personnel/update/<int:id>", methods=["PUT"])
@token_required
def personnel_update(current_user, id):
    person = Person.query.get(id)
    if person is None:
        response = {
                 'message': 'This person entry does not exist.'
                   }
        return jsonify(response), 404

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    middle_name = request.json["middle_name"]
    phone = request.json["phone"]
    occupation = request.json["occupation"]
    institution = request.json["institution"]
    type_id = request.json["type_id"]
    gender_id = request.json["gender_id"]
    # Parse dates
    if request.json["birthday"]:
        birthday = datetime.strptime(request.json["birthday"], "%Y-%m-%d")
    else:
        birthday = None

    person.first_name = first_name
    person.last_name = last_name
    person.middle_name = middle_name
    person.phone = phone
    person.birthday = birthday
    person.occupation = occupation
    person.institution = institution
    person.type_id = type_id
    person.gender_id = gender_id

    db.session.commit()

    return jsonify(person_schema.dump(person).data)


@personnel.route("/personnel/delete/<int:id>", methods=["DELETE"])
@token_required
def personnel_delete(current_user, id):
    person = Person.query.get(id)
    if person is None:
        response = {
                 'message': 'This person entry does not exist.'
                   }
        return jsonify(response), 404
    
    response = person_schema.dump(person).data
    db.session.delete(person)
    db.session.commit()

    return jsonify(response)


# Frequency events ops
@personnel.route("/frequency")
@login_required
def frequency():
    return render_template("frequency.html", title="Laboratory Frequency")

@personnel.route("/frequency/all", methods=["GET"])
@token_required
def frequency_all(current_user):
    frequencies = FrequencyEvent.query.all()

    return jsonify(frequencies_schema.dump(frequencies).data)


@personnel.route("/frequency/add", methods=["POST"])
@token_required
def frequency_add(current_user):
    date = datetime.strptime(request.json["date"], "%Y-%m-%d")
    entry_time = time.fromisoformat(request.json["entry_time"])
    exit_time = time.fromisoformat(request.json["exit_time"])
    person_id = request.json["person_id"]

    new_frequency = FrequencyEvent(date=date, entry_time=entry_time, exit_time=exit_time, person_id=person_id)

    db.session.add(new_frequency)
    db.session.commit()

    return jsonify(frequency_schema.dump(new_frequency).data)


@personnel.route("/frequency/<int:id>", methods=["GET"])
@token_required
def frequency_fetch(current_user, id):
    frequency = FrequencyEvent.query.get(id)
    if frequency is None:
        response = {
                 'message': 'This frequency event does not exist.'
                   }
        return jsonify(response), 404

    return jsonify(frequency_schema.dump(frequency).data)


@personnel.route("/frequency/update/<int:id>", methods=["PUT"])
@token_required
def frequency_update(current_user, id):
    frequency = FrequencyEvent.query.get(id)
    if frequency is None:
        response = {
                 'message': 'This frequency event does not exist.'
                   }
        return jsonify(response), 404
    
    date = datetime.strptime(request.json["date"], "%Y-%m-%d")
    entry_time = time.fromisoformat(request.json["entry_time"])
    exit_time = time.fromisoformat(request.json["exit_time"])
    person_id = request.json["person_id"]

    frequency.date = date
    frequency.entry_time = entry_time
    frequency.exit_time = exit_time
    frequency.person_id = person_id

    db.session.commit()

    return jsonify(frequency_schema.dump(frequency).data)


@personnel.route("/frequency/delete/<int:id>", methods=["DELETE"])
@token_required
def frequency_delete(current_user, id):
    frequency = FrequencyEvent.query.get(id)
    if frequency is None:
        response = {
                 'message': 'This frequency event does not exist.'
                   }
        return jsonify(response), 404

    response = frequency_schema.dump(frequency).data
    db.session.delete(frequency)
    db.session.commit()

    return jsonify(response)
