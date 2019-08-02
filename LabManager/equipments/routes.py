# import marshmallow
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from LabManager import db
from LabManager.dbModels import Inventory, Lendings, TechnicalIssues
from LabManager.maSchemas import equipment_schema, equipments_schema


equipments = Blueprint("equips", __name__)


@equipments.route("/inventory")
@login_required
def inventory():
    return render_template("inventory.html", title="Equipment Inventory")


@equipments.route("/inventory/all", methods=["GET"])
def inventory_all():
    inventory = Inventory.query.all()
    result = equipments_schema.dump(inventory).data

    return jsonify(result)


@equipments.route("/inventory/<int:id>", methods=["GET"])
def inventory_fetch(id):
    equipment = Inventory.query.get(id).first()
    if equipment is None:
        response = {
                 'message': 'Inventory item does not exist'
                   }
        return jsonify(response), 404

    result = equipment_schema.dump(equipment).data

    return jsonify(result)


@equipments.route("/inventory/add", methods=["POST"])
def inventory_add():
    # new_data = request.json
    # load = equipment_schema.load(new_data)
    name = request.json["name"]
    description = request.json["description"]
    new_equip = Inventory(name=name, description=description)
    db.session.add(new_equip)
    db.session.commit()

    # equipment_schema = new_equip.__marshmallow__()

    return jsonify(equipment_schema.dump(new_equip).data)


@equipments.route("/inventory/update/<int:id>", methods=["PUT"])
def inventory_put(id):
    equipment = Inventory.query.get(id)
    if equipment is None:
        response = {
                 'message': 'Inventory item does not exist'
                   }
        return jsonify(response), 404

    name = request.json["name"]
    description = request.json["description"]
    equipment.name = name
    equipment.description = description
    db.session.commit()

    return jsonify(equipment_schema.dump(equipment).data) # equipment_schema.jsonify(equipment)


@equipments.route("/inventory/delete/<int:id>", methods=["DELETE"])
def inventory_del(id):
    equipment = Inventory.query.get(id)
    if equipment is None:
        response = {
                 'message': 'Inventory item does not exist'
                   }
        return jsonify(response), 404

    db.session.delete(equipment)
    db.session.commit()

    return jsonify(equipment_schema.dump(equipment).data)


@equipments.route("/lendings")
@login_required
def lendings():
    return render_template("lendings.html", title="Equipment Lendings")


@equipments.route("/technical")
@login_required
def technical():
    return render_template("technical.html", title="Technical Issues")
