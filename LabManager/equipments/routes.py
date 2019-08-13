from datetime import datetime, date
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from LabManager import db
from LabManager.dbModels import Inventory, Lendings, TechnicalIssues
from LabManager.maSchemas import equipment_schema, equipments_schema, lending_schema, lendings_schema, issue_schema, issues_schema
from LabManager.auth.utils import token_required


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


@equipments.route("/inventory/add", methods=["POST"])
@token_required
def inventory_add(current_user):
    # new_data = request.json
    # load = equipment_schema.load(new_data)
    name = request.json["name"]
    description = request.json["description"]
    new_equip = Inventory(name=name, description=description)
    db.session.add(new_equip)
    db.session.commit()

    # equipment_schema = new_equip.__marshmallow__()

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

    equipment.name = name
    equipment.description = description

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

    lend_date = datetime.strptime(request.json["lend_date"], "%Y-%m-%d")
    return_expected = datetime.strptime(request.json["lend_date"], "%Y-%m-%d")
    if request.json["lend_date"]:
        return_done = datetime.strptime(request.json["lend_date"], "%Y-%m-%d")
        new_lending = Lendings(lender=lender, lend_date=lend_date, return_expected=return_expected, return_done=return_done, observations=observations, inventory_id=inventory_id)
    else:
        new_lending = Lendings(lender=lender, lend_date=lend_date, return_expected=return_expected, observations=observations, inventory_id=inventory_id)

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
    if return_done:
        lending.return_done = datetime.strptime(return_done, "%Y-%m-%d")
    
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
        report_date = datetime.strptime(request.json["report_date"], "%Y-%m-%d")
    else:
        report_date = date.today()
    if request.json["solution_date"]:
        solution_date = datetime.strptime(request.json["solution_date"], "%Y-%m-%d")
    else:
        solution_date = None
    
    new_issue = TechnicalIssues(description=description, report_date=report_date, solution_date=solution_date, inventory_id=inventory_id)
    db.session.add(new_issue)
    db.session.commit()

    return jsonify(issue_schema.dump(new_issue).data)


@equipments.route("/technical/<int:id>", methods=["GET"])
@token_required
def issue_fetch(current_user, id):
    issue = TechnicalIssues.query.get(id)
    if issue is None:
        response = {
                 'message': 'This technical issue does not exist.'
                   }
        return jsonify(response), 404

    return jsonify(issue_schema.dump(issue).data)


@equipments.route("/technical/update/<int:id>", methods=["PUT"])
@token_required
def issue_put(current_user, id):
    issue = TechnicalIssues.query.get(id)
    if issue is None:
        response = {
                 'message': 'This technical issue does not exist.'
                   }
        return jsonify(response), 404
    
    description = request.json["description"]
    inventory_id = request.json["inventory_id"]
    
    # Parse dates
    if request.json["report_date"]:
        report_date = datetime.strptime(request.json["report_date"], "%Y-%m-%d")
    if request.json["solution_date"]:
        solution_date = datetime.strptime(request.json["solution_date"], "%Y-%m-%d")

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
                 'message': 'This technical issue does not exist.'
                   }
        return jsonify(response), 404
    
    response = issue_schema.dump(issue).data
    db.session.delete(issue)
    db.session.commit()

    return jsonify(response)
