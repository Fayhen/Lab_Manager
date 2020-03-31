from flask import Blueprint, request, make_response, jsonify
from LabManager import db
from LabManager.dbModels import PersonType, Gender, Person, FrequencyEvent
from LabManager.maSchemas import (type_schema, types_schema, gender_schema,
    genders_schema, person_schema, people_schema, frequency_schema,
    frequencies_schema)
from LabManager.auth.utils import token_required


personnel = Blueprint("personnel", __name__)


# Backend ops, might be erased upon deployement in favor of pre-populating SQL scripts
@personnel.route("/genders", methods=["GET"])
def gender_list():
    genders = {}

    for gender in Gender.query.all():
        genders[gender.gender_name] = gender.id

    return jsonify(genders)

@personnel.route("/genders/all", methods=["GET"])
def gender_all():
    genders = Gender.query.all()

    return jsonify(genders_schema.dump(genders))

@personnel.route("/genders/add", methods=["POST"])
def gender_add():
    gender_name = request.json["gender_name"]
    new_gender = Gender(gender_name=gender_name)
    db.session.add(new_gender)
    db.session.commit()

    return jsonify(gender_schema.dump(new_gender))

@personnel.route("/genders/<int:id>", methods=["GET"])
def gender_fetch(id):
    gender = Gender.query.get(id)

    return jsonify(gender_schema.dump(gender))

@personnel.route("/genders/update/<int:id>", methods=["PUT"])
def gender_update(id):
    gender = Gender.query.get(id)
    gender_name = request.json(["gender_name"])
    gender.gender_name = gender_name
    db.session.commit()

    return jsonify(gender_schema.dump(gender))

@personnel.route("/genders/delete/<int:id>", methods=["DELETE"])
def gender_delete(id):
    gender = Gender.query.get(id)
    response = gender_schema.dump(gender)
    db.session.delete(gender)
    db.session.commit()

    return jsonify(response)

@personnel.route("/persontypes", methods=["GET"])
def type_list():
    types = {}

    for person_type in PersonType.query.all():
        types[person_type.type_name] = person_type.id

    return jsonify(types)

@personnel.route("/persontypes/all", methods=["GET"])
def type_all():
    types = PersonType.query.all()

    return jsonify(types_schema.dump(types))

@personnel.route("/persontypes/add", methods=["POST"])
def type_add():
    type_name = request.json["type_name"]
    new_type = PersonType(type_name=type_name)
    db.session.add(new_type)
    db.session.commit()

    return jsonify(type_schema.dump(new_type))

@personnel.route("/persontypes/<int:id>", methods=["POST"])
def type_fetch(id):
    persontype = PersonType.query.get(id)

    return jsonify(type_schema.dump(persontype))

@personnel.route("/persontypes/update/<int:id>", methods=["PUT"])
def type_update(id):
    persontype = PersonType.query.get(id)
    type_name = request.json(["type_name"])
    persontype.type_name = type_name
    db.session.commit()

    return jsonify(type_schema.dump(persontype))

@personnel.route("/persontypes/delete/<int:id>", methods=["DELETE"])
def type_delete(id):
    persontype = PersonType.query.get(id)
    response = type_schema.dump(persontype)
    db.session.delete(persontype)
    db.session.commit()

    return jsonify(response)


# Personnel ops
@personnel.route("/personnel", methods=["GET"])
def personnel_get():
    if not request.args.get('visitors'):
        return make_response("Missing required query parameter 'visitors'", 400)

    visitors = request.args.get('visitors') == 'true'
    personnel = Person.query.filter(Person.is_visitor == visitors)
    
    return jsonify(people_schema.dump(personnel))


@personnel.route("/personnel/all", methods=["GET"])
# @token_required
# def personnel_all(current_user):
def personnel_all():
    personnel = Person.query.all()

    return jsonify(people_schema.dump(personnel))


@personnel.route("/personnel/add", methods=["POST"])
@token_required
def personnel_add(current_user):
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    middle_name = request.json["middle_name"]
    phone = request.json["phone"]
    birthday = request.json["birthday"]
    occupation = request.json["occupation"]
    institution = request.json["institution"]
    type_id = request.json["type_id"]
    gender_id = request.json["gender_id"]
    # Create instance
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
    # Commit instance
    db.session.add(new_person)
    db.session.commit()

    return jsonify(person_schema.dump(new_person))


@personnel.route("/personnel/<int:id>", methods=["GET", "PUT", "DELETE"])
# @token_required
# def personnel_ops(current_user, id):
def personnel_ops( id):
    person = Person.query.get(id)
    if person is None:
        return make_response("Person entry does not exist.", 404)
        

    if request.method == "GET":
        return jsonify(person_schema.dump(person))
    
    if request.method == "PUT":
        # Modify instance
        person.first_name = request.json["first_name"]
        person.last_name = request.json["last_name"]
        person.middle_name = request.json["middle_name"]
        person.phone = request.json["phone"]
        person.birthday = request.json["birthday"]
        person.occupation = request.json["occupation"]
        person.institution = request.json["institution"]
        person.type_id = request.json["type_id"]
        person.gender_id = request.json["gender_id"]
        # Commit instance
        db.session.commit()

        return jsonify(person_schema.dump(person))
    
    if request.method == "DELETE":
        response = person_schema.dump(person)
        db.session.delete(person)
        db.session.commit()

        return jsonify(response)


# Frequency events ops
@personnel.route("/frequency/all", methods=["GET"])
@token_required
def frequency_all(current_user):
    frequencies = FrequencyEvent.query.all()

    return jsonify(frequencies_schema.dump(frequencies))


@personnel.route("/frequency/add", methods=["POST"])
@token_required
def frequency_add(current_user):
    date = request.json["date"]
    entry_time = request.json["entry_time"]
    exit_time = request.json["exit_time"]
    person_id = request.json["person_id"]

    frequency = FrequencyEvent(
        date=date,
        entry_time=entry_time, 
        xit_time=exit_time,
        person_id=person_id
        )

    db.session.add(frequency)
    db.session.commit()

    return jsonify(frequency_schema.dump(frequency))


@personnel.route("/frequency/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def frequency_ops(current_user, id):
    frequency = FrequencyEvent.query.get(id)
    if frequency is None:
        return make_response("This frequency entry does not exist.", 404)

    if request.method == "GET":
        return jsonify(frequency_schema.dump(frequency))
    
    if request.method == "PUT":
        date = request.json["date"]
        entry_time = request.json["entry_time"]
        exit_time = request.json["exit_time"]
        person_id = request.json["person_id"]

        frequency.date = date
        frequency.entry_time = entry_time
        frequency.exit_time = exit_time
        frequency.person_id = person_id

        db.session.commit()

        return jsonify(frequency_schema.dump(frequency))
    
    if request.method == "DELETE":
        response = frequency_schema.dump(frequency)
        db.session.delete(frequency)
        db.session.commit()

        return jsonify(response)
