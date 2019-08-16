from datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from LabManager import db
from LabManager.dbModels import (Person, Inventory, FieldEvent,
    helper_field_person, helper_field_equips)
from LabManager.maSchemas import (people_schema, equipments_schema,
    field_schema, fields_schema)
from LabManager.auth.utils import token_required
from LabManager.equipments.utils import (update_status,
    query_all_field_eligible, query_all_field_available)


fieldtrips = Blueprint("fieldtrips", __name__)


@fieldtrips.route("/fieldtrips/all", methods=["GET"])
@token_required
def fieldtrips_all(current_user):
    fieldtrips = FieldEvent.query.all()

    return jsonify(fields_schema.dump(fieldtrips).data)


@fieldtrips.route("/fieldtrips/<int:id>", methods=["GET"])
@token_required
def fieldtrips_fetch(current_user, id):
    fieldtrip = FieldEvent.query.get(id)
    if fieldtrip is None:
        return make_response("Field trip entry does not exist.", 404)

    return jsonify(field_schema.dump(fieldtrip).data)


# Backend route to be deleted on the future
@fieldtrips.route("/fieldtrips/backend1", methods=["GET"])
def backend1():
    helper_field_person_data = db.session.query(helper_field_person).all()
    data = []
    for row in helper_field_person_data:
        data.append({
            "APrimaryKeyIForgotToAdd": "An int",
            "person_id": f"{row[0]}",
            "fieldevent_id": f"{row[1]}"
        })

    return jsonify(data)


# Backend route to be deleted on the future
@fieldtrips.route("/fieldtrips/backend2", methods=["GET"])
def backend2():
    helper_field_equips_data = db.session.query(helper_field_equips).all()
    data = []
    for row in helper_field_equips_data:
        data.append({
            "APrimaryKeyIForgotToAdd": "An int",
            "equips_id": f"{row[0]}",
            "fieldevent_id": f"{row[1]}"
        })
    return jsonify(data)


@fieldtrips.route("/fieldtrips/post", methods=["GET"])
@token_required
def fieldtrips_post(current_user):
    personnel = Person.query.fiter_by(type_id=1).all()
    equips_field_available = query_all_field_available()
    equips_field_eligible = query_all_field_eligible()

    return jsonify({
            "personnel": people_schema.dump(personnel).data,
            "equips_field_available": equipments_schema.dump(equips_field_available).data,
            "equips_field_eligible": equipments_schema.dump(equips_field_eligible).data,
        })


@fieldtrips.route("/fieldtrips/post/add", methods=["POST"])
@token_required
def fieldtrips_add(current_user):
    location = request.json["location"]
    date_start = datetime.strptime(request.json["date_start"],
        "%Y-%m-%d")
    date_end_expected = datetime.strptime(request.json["date_end_expected"],
        "%Y-%m-%d")
    observations = request.json["observations"]
    personnel = request.json["personnel"]
    equipments = request.json["equipments"]
    
    # Check 'date_end_done' info and update equip status if present
    if request.json["date_end_done"]:
        date_end_done = datetime.strptime(request.json["date_end_done"],
            "%Y-%m-%d")
    else:
        date_end_done = None
        for inventory_id in equipments:
            update_status(inventory_id, "on_trip")

    new_trip = FieldEvent(
        location = location,
        date_start = date_start,
        date_end_expected = date_end_expected,
        date_end_done = date_end_done,
        observations = observations
    )

    db.session.add(new_trip)
    db.session.commit()
    
    for key in personnel:
        insert = helper_field_person.insert().values(Person=key,
            FieldEvent=new_trip.id)
        db.session.execute(insert)
        
    for key in equipments:
        insert = helper_field_equips.insert().values(Inventory=key,
            FieldEvent=new_trip.id)
        db.session.execute(insert)
            
    db.session.commit()

    return jsonify(field_schema.dump(new_trip).data)


@fieldtrips.route("/fieldtrips/update/<int:id>", methods=["PUT"])
@token_required
def fieldtrips_update(current_user, id):
    fieldtrip = FieldEvent.query.get(id)
    if fieldtrip is None:
        return make_response("Field trip entry does not exist.", 404)

    location = request.json["location"]
    date_start = datetime.strptime(request.json["date_start"],
        "%Y-%m-%d")
    date_end_expected = datetime.strptime(request.json["date_end_expected"],
        "%Y-%m-%d")
    observations = request.json["observations"]
    personnel = request.json["personnel"]
    equipments = request.json["equipments"]
    
    # Check if 'date_end_done' info on request, update equip status if present
    if request.json["date_end_done"]:
        date_end_done = datetime.strptime(request.json["date_end_done"],
            "%Y-%m-%d")
        for inventory_id in equipments:
            update_status(inventory_id, "on_trip")
    else:
        date_end_done = date_end_done

    fieldtrip.location = location
    fieldtrip.date_start = date_start
    fieldtrip.date_end_expected = date_end_expected
    fieldtrip.date_end_done = date_end_done
    fieldtrip.observations = observations

    db.session.commit()

    db.session.execute(helper_field_person.delete().where(
        helper_field_person.c.FieldEvent == id
    ))
    db.session.commit()
    
    db.session.execute(helper_field_equips.delete().where(
        helper_field_equips.c.FieldEvent == id
    ))
    db.session.commit()

    for key in personnel:
        insert = helper_field_person.insert().values(Person=key,
            FieldEvent=fieldtrip.id)
        db.session.execute(insert)

    for key in equipments:
        insert = helper_field_equips.insert().values(Inventory=key,
            FieldEvent=fieldtrip.id)
        db.session.execute(insert)
    
    db.session.commit()
    
    return jsonify(field_schema.dump(fieldtrip).data)

@fieldtrips.route("/fieldtrips/delete/<int:id>", methods=["DELETE"])
@token_required
def fieldtrips_delete(current_user, id):
    fieldtrip = FieldEvent.query.get(id)
    if fieldtrip is None:
        return make_response("Field trip entry does not exist.", 404)

    response = field_schema.dump(fieldtrip).data

    # Ensure equipments status is reverted to default 'available'
    for inventory_id in FieldEvent.equipments:
        update_status(inventory_id, "available")

    db.session.execute(helper_field_person.delete().where(
        helper_field_person.c.FieldEvent == id
    ))
    db.session.commit()

    db.session.execute(helper_field_equips.delete().where(
        helper_field_equips.c.FieldEvent == id
    ))
    db.session.commit()

    db.session.delete(fieldtrip)
    db.session.commit()

    return jsonify(response)
