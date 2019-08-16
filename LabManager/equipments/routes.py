from datetime import datetime, date
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from LabManager import db
from LabManager.dbModels import Inventory, Lendings, TechnicalIssues
from LabManager.maSchemas import equipment_schema, equipments_schema, lending_schema, lendings_schema, issue_schema, issues_schema
from LabManager.auth.utils import token_required
from LabManager.equipments.utils import update_status, query_all_available, query_all_lended, query_all_ontrip, query_all_broken


equipments = Blueprint("equips", __name__)


# Inventory operations
@equipments.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html", title="Equipment Inventory")


@equipments.route("/inventory/all", methods=["GET"])
@token_required
def inventory_all(current_user):
    inventory = Inventory.query.all()
    result = equipments_schema.dump(inventory).data

    return jsonify(result)


@equipments.route("/inventory/all/available", methods=["GET"])
@token_required
def inventory_available(current_user):
    available = query_all_available()

    return equipments_schema.dump(available).data

@equipments.route("/inventory/all/lended", methods=["GET"])
@token_required
def inventory_lended(current_user):
    lended = query_all_lended()

    return equipments_schema.dump(lended).data


@equipments.route("/inventory/all/ontrip", methods=["GET"])
@token_required
def inventory_ontrip(current_user):
    ontrip = query_all_ontrip()

    return equipments_schema.dump(ontrip).data


@equipments.route("/inventory/all/broken", methods=["GET"])
@token_required
def inventory_broken(current_user):
    broken = query_all_broken()

    return equipments_schema.dump(broken).data


@equipments.route("/inventory/add", methods=["POST"])
@token_required
def inventory_add(current_user):
    name = request.json["name"]
    description = request.json["description"]
    field_eligible = request.json["field_eligible"]
    new_equip = Inventory(name=name, description=description,
        field_eligible=field_eligible, status="available")

    db.session.add(new_equip)
    db.session.commit()

    return jsonify(equipment_schema.dump(new_equip).data)


@equipments.route("/inventory/<int:id>", methods=["GET"])
@token_required
def inventory_fetch(current_user, id):
    equipment = Inventory.query.get(id).first()
    if equipment is None:
        response = {
                 'message': 'Inventory item does not exist.'
                   }
        return jsonify(response), 404

    result = equipment_schema.dump(equipment).data

    return jsonify(result)


@equipments.route("/inventory/update/<int:id>", methods=["PUT"])
@token_required
def inventory_put(current_user, id):
    equipment = Inventory.query.get(id)
    if equipment is None:
        response = {
                 'message': 'Inventory item does not exist.'
                   }
        return jsonify(response), 404

    name = request.json["name"]
    description = request.json["description"]
    field_eligible = request.json["field_eligible"]
    status = request.json["status"]

    equipment.name = name
    equipment.description = description
    equipment.field_eligible = field_eligible
    equipment.status = status

    db.session.commit()

    return jsonify(equipment_schema.dump(equipment).data) # equipment_schema.jsonify(equipment)


@equipments.route("/inventory/delete/<int:id>", methods=["DELETE"])
@token_required
def inventory_del(current_user, id):
    equipment = Inventory.query.get(id)
    if equipment is None:
        response = {
                 'message': 'Inventory item does not exist.'
                   }
        return jsonify(response), 404

    db.session.delete(equipment)
    db.session.commit()

    return jsonify(equipment_schema.dump(equipment).data)


# Lendings operations
@equipments.route("/lendings")
@login_required
def lendings():
    return render_template("lendings.html", title="Equipment Lendings")


@equipments.route("/lendings/all", methods=["GET"])
@token_required
def lendings_all(current_user):
    lendings = Lendings.query.all()

    return jsonify(lendings_schema.dump(lendings).data)


@equipments.route("/lendings/add", methods=["POST"])
@token_required
def lendings_add(current_user):
    lender = request.json["lender"]
    observations =  request.json["observations"]
    inventory_id =  request.json["inventory_id"]
    
    return_expected = datetime.strptime(request.json["lend_date"], "%Y-%m-%d")
    if request.json["lend_date"]:
        return_done = datetime.strptime(request.json["lend_date"], "%Y-%m-%d")
        new_lending = Lendings(lender=lender, lend_date=lend_date,
            return_expected=return_expected, return_done=return_done,
            observations=observations, inventory_id=inventory_id)
    else:
        new_lending = Lendings(lender=lender, lend_date=lend_date,
        return_expected=return_expected, observations=observations,
        inventory_id=inventory_id)

    # Add 'lended' status to the equipment
    update_status(new_lending.inventory_id, "lended")
    
    db.session.add(new_lending)
    db.session.commit()

    return jsonify(lending_schema.dump(new_lending).data)


@equipments.route("/lendings/<int:id>", methods=["GET"])
@token_required
def lendings_fetch(current_user, id):
    lending = Lendings.query.get(id)
    if lending is None:
        response = {
                 'message': 'This lending event does not exist.'
                   }
        return jsonify(response), 404
    
    return jsonify(lending_schema.dump(lending).data)


@equipments.route("/lendings/update/<int:id>", methods=["PUT"])
@token_required
def lendings_put(current_user, id):
    lending = Lendings.query.get(id)
    if lending is None:
        response = {
                 'message': 'This lending event does not exist.'
                   }
        return jsonify(response), 404
    
    lender = request.json["lender"]
    lend_date = request.json["lend_date"]
    return_expected = request.json["return_expected"]
    return_done = request.json["return_done"]
    observations =  request.json["observations"]
    inventory_id =  request.json["inventory_id"]

    lending.lender = lender
    lending.observations = observations
    lending.inventory_id = inventory_id
    lending.lend_date = datetime.strptime(lend_date, "%Y-%m-%d")
    lending.return_expected = datetime.strptime(return_expected, "%Y-%m-%d")
    
    # Check 'return_done' info and update equip status if present
    if return_done:
        lending.return_done = datetime.strptime(return_done, "%Y-%m-%d")
        update_status(lending.new_lending.inventory_id, "available")
    
    db.session.commit()

    return jsonify(lending_schema.dump(lending).data)


@equipments.route("/lendings/delete/<int:id>", methods=["DELETE"])
@token_required
def lendings_delete(current_user, id):
    lending = Lendings.query.get(id)
    if lending is None:
        response = {
                 'message': 'This lending event does not exist.'
                   }
        return jsonify(response), 404
    
    response = lending_schema.dump(lending).data

    # Ensure equipments status is reverted to default 'available'
    update_status(lending.inventory_id, "available")

    db.session.delete(lending)
    db.session.commit()

    return jsonify(response)


# Technical issues operations
@equipments.route("/technical")
@login_required
def technical():
    return render_template("technical.html", title="Technical Issues")


@equipments.route("/technical/all", methods=["GET"])
@token_required
def technical_all(current_user):
    issues = TechnicalIssues.query.all()

    return jsonify(issues_schema.dump(issues).data)



@equipments.route("/technical/add", methods=["POST"])
@token_required
def technical_add(current_user):
    description = request.json["description"]
    inventory_id = request.json["inventory_id"]
    
    # Parse dates
    if request.json["report_date"]:
        report_date = datetime.strptime(request.json["report_date"],
            "%Y-%m-%d")
    else:
        report_date = date.today()

    if request.json["solution_date"]:
        solution_date = datetime.strptime(request.json["solution_date"],
            "%Y-%m-%d")
    else:
        solution_date = None
    
    new_issue = TechnicalIssues(description=description,
        report_date=report_date, solution_date=solution_date,
        inventory_id=inventory_id)

    # Add 'broken' status to equipment
    update_status(new_issue.inventory_id, "broken")

    db.session.add(new_issue)
    db.session.commit()

    return jsonify(issue_schema.dump(new_issue).data)



@equipments.route("/technical/<int:id>", methods=["GET"])
@token_required
def issue_fetch(current_user, id):
    issue = TechnicalIssues.query.get(id)
    if issue is None:
        response = {
                 'message': 'This technical issue entry does not exist.'
                   }
        return jsonify(response), 404

    return jsonify(issue_schema.dump(issue).data)


@equipments.route("/technical/update/<int:id>", methods=["PUT"])
@token_required
def issue_put(current_user, id):
    issue = TechnicalIssues.query.get(id)
    if issue is None:
        response = {
                 'message': 'This technical issue entry does not exist.'
                   }
        return jsonify(response), 404
    
    description = request.json["description"]
    inventory_id = request.json["inventory_id"]
    
    # Parse dates
    if request.json["report_date"]:
        report_date = datetime.strptime(request.json["report_date"], "%Y-%m-%d")
    
    # Check 'solution_date' info and update equip status if present
    if request.json["solution_date"]:
        solution_date = datetime.strptime(request.json["solution_date"], "%Y-%m-%d")
        update_status(issue.inventory_id, "available") 

    issue.description = description
    issue.report_date = report_date
    issue.solution_date = solution_date
    issue.inventory_id = inventory_id

    db.session.commit()

    return jsonify(issue_schema.dump(issue).data)


@equipments.route("/technical/delete/<int:id>", methods=["DELETE"])
@token_required
def issue_delete(current_user, id):
    issue = TechnicalIssues.query.get(id)
    if issue is None:
        response = {
                 'message': 'This technical issue entry does not exist.'
                   }
        return jsonify(response), 404
    
    response = issue_schema.dump(issue).data

    # Ensure equipments status is reverted to default 'available'
    update_status(issue.inventory_id, "available")

    db.session.delete(issue)
    db.session.commit()

    return jsonify(response)
