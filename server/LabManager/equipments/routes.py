import time
from flask import Blueprint, request, make_response, jsonify
from LabManager import db
from LabManager.dbModels import Inventory, Lendings, TechnicalIssues
from LabManager.maSchemas import (equipment_schema, equipments_schema,
    lending_schema, lendings_schema, issue_schema, issues_schema)
from LabManager.auth.utils import token_required
from LabManager.equipments.utils import (update_status, query_all_available,
    query_all_lended, query_all_ontrip, query_all_broken)


equipments = Blueprint("equips", __name__)


# Inventory operations
@equipments.route("/inventory/all", methods=["GET"])
@token_required
def inventory_all(current_user):
    inventory = Inventory.query.all()
    result = equipments_schema.dump(inventory)

    return jsonify(result)


@equipments.route("/inventory/available", methods=["GET"])
@token_required
def inventory_available(current_user):
    available = query_all_available()

    return equipments_schema.dump(available)

@equipments.route("/inventory/lended", methods=["GET"])
@token_required
def inventory_lended(current_user):
    lended = query_all_lended()

    return equipments_schema.dump(lended)


@equipments.route("/inventory/ontrip", methods=["GET"])
@token_required
def inventory_ontrip(current_user):
    ontrip = query_all_ontrip()

    return equipments_schema.dump(ontrip)


@equipments.route("/inventory/broken", methods=["GET"])
@token_required
def inventory_broken(current_user):
    broken = query_all_broken()

    return equipments_schema.dump(broken)


@equipments.route("/inventory/add", methods=["POST"])
@token_required
def inventory_add(current_user):
    name = request.json["name"]
    description = request.json["description"]
    buy_date = request.json["buy_date"]
    field_eligible = request.json["field_eligible"]
    new_equip = Inventory(
        name = name,
        description = description,
        buy_date = buy_date,
        field_eligible = field_eligible,
        status = "available"
        )
    db.session.add(new_equip)
    db.session.commit()

    return jsonify(equipment_schema.dump(new_equip))


@equipments.route("/inventory/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def inventory_ops(current_user, id):
    equipment = Inventory.query.get(id).first()
    if equipment is None:
        return make_response("Inventory item does not exist.", 404)

    if request.method == "GET":
        return jsonify(equipment_schema.dump(equipment))
    
    if request.method == "PUT":
        name = request.json["name"]
        description = request.json["description"]
        buy_date = request.json["buy_date"]
        field_eligible = request.json["field_eligible"]

        equipment.name = name
        equipment.description = description
        equipment.buy_date = buy_date
        equipment.field_eligible = field_eligible

        db.session.commit()

        return jsonify(equipment_schema.dump(equipment))

    if request.method == "DELETE":
        response = equipment_schema.dump(equipment)
        db.session.delete(equipment)
        db.session.commit()

        return jsonify(response)


# Lendings operations
@equipments.route("/lendings/all", methods=["GET"])
@token_required
def lendings_all(current_user):
    lendings = Lendings.query.all()

    return jsonify(lendings_schema.dump(lendings))


@equipments.route("/lendings/add", methods=["POST"])
@token_required
def lendings_add(current_user):
    lender = request.json["lender"]
    observations =  request.json["observations"]
    inventory_id =  request.json["inventory_id"]
    lend_date = request.json["lend_date"]
    return_expected = request.json["return_expected"]
    return_done = request.json["return_done"]
    new_lending = Lendings(
        lender = lender,
        lend_date = lend_date,
        return_expected = return_expected,
        return_done = return_done,
        observations = observations,
        inventory_id = inventory_id
        )
    # Add 'lended' status to the equipment
    update_status(new_lending.inventory_id, "lended")
    
    db.session.add(new_lending)
    db.session.commit()

    return jsonify(lending_schema.dump(new_lending))


@equipments.route("/lendings/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def lendings_ops(current_user, id):
    lending = Lendings.query.get(id)
    if lending is None:
        return make_response("Lending entry does not exist.", 404)
    
    if request.method == "GET":
        return jsonify(lending_schema.dump(lending))

    if request.method == "PUT":
        lender = request.json["lender"]
        lend_date = request.json["lend_date"]
        return_expected = request.json["return_expected"]
        return_done = request.json["return_done"]
        observations =  request.json["observations"]
        inventory_id =  request.json["inventory_id"]

        lending.lender = lender
        lending.observations = observations
        lending.inventory_id = inventory_id
        lending.lend_date = lend_date
        lending.return_expected = return_expected
        
        # Check if 'return_done' exists and update equip status accordingly
        if return_done:
            lending.return_done = return_done
            update_status(lending.new_lending.inventory_id, "available")
        
        db.session.commit()

        return jsonify(lending_schema.dump(lending))

    if request.method == "DELETE":
        response = lending_schema.dump(lending)

        # Ensure equipments status is reverted to default 'available'
        update_status(lending.inventory_id, "available")

        db.session.delete(lending)
        db.session.commit()

        return jsonify(response)


# Technical issues operations
@equipments.route("/technical/all", methods=["GET"])
@token_required
def technical_all(current_user):
    issues = TechnicalIssues.query.all()

    return jsonify(issues_schema.dump(issues))


@equipments.route("/technical/add", methods=["POST"])
@token_required
def technical_add(current_user):
    description = request.json["description"]
    inventory_id = request.json["inventory_id"]
    report_date = str(time.time())
    solution_date = request.json["solution_date"]
    
    new_issue = TechnicalIssues(
        description = description,
        report_date = report_date,
        solution_date = solution_date,
        inventory_id = inventory_id
        )
    # Add 'broken' status to equipment
    update_status(new_issue.inventory_id, "broken")

    db.session.add(new_issue)
    db.session.commit()

    return jsonify(issue_schema.dump(new_issue))



@equipments.route("/technical/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def issue_ops(current_user, id):
    issue = TechnicalIssues.query.get(id)
    if issue is None:
        return make_response("Technical issue entry does not exist.", 404)

    if request.method == "GET":
        return jsonify(issue_schema.dump(issue))
    
    if request.method == "PUT":
        description = request.json["description"]
        inventory_id = request.json["inventory_id"]
        report_date = request.json["report_date"]

        # Check 'solution_date' info and update equip status if present
        if request.json["solution_date"]:
            solution_date = request.json["solution_date"]
            update_status(issue.inventory_id, "available") 

        issue.description = description
        issue.report_date = report_date
        issue.solution_date = solution_date
        issue.inventory_id = inventory_id

        db.session.commit()

        return jsonify(issue_schema.dump(issue))
    
    if request.method == "DELETE":
        response = issue_schema.dump(issue)
        # Ensure equipments status is reverted to default 'available'
        update_status(issue.inventory_id, "available")

        db.session.delete(issue)
        db.session.commit()

        return jsonify(response)
