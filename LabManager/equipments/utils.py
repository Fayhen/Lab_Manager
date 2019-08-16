from flask import make_response
from LabManager import app, db
from LabManager.dbModels import Inventory


def update_status(id, new_status):
    """
    Updates an inventory entry with the passed status.
    """
    equipment = Inventory.query.get(id)
    if equipment is None:
        return make_response("An error has occured while updating item status. Item was not found.",
            500)
    else:
        equipment.status = new_status
        db.session.commit()
        return True


def query_all_available():
    """
    Will return all from the 'inventory' table
    with 'available' status.
    """
    available = Inventory.query.filter_by(status="available").all()
    
    return available


def query_all_lended():
    """
    Will return all from the 'inventory' table
    with 'lended' status.
    """
    lended = Inventory.query.filter_by(status="lended").all()

    return lended


def query_all_ontrip():
    """
    Will return all from the 'inventory' table
    with 'on_trip' status.
    """
    on_trip = Inventory.query.filter_by(status="on_trip").all()

    return on_trip


def query_all_broken():
    """
    Will return all from the 'inventory' table
    with 'broken' status.
    """
    broken = Inventory.query.filter_by(status='broken').all()

    return broken


def query_all_field_eligible():
    """
    Will return all from the 'inventory' table
    that with 'True' on 'field_eligible'.
    """
    field_eligible = Inventory.query.filter_by(field_eligible=True).all()

    return field_eligible


def query_all_field_available():
    """
    Will return all from the 'inventory' table
    with both 'field_eligible=True' and 'status="avaialble"'.
    """
    field_available = Inventory.query.filter_by(field_available=True,
        status="available").all()
    
    return field_available
