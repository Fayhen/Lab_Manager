import os
from LabManager import db


class PersonType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String)
    person = db.relationship('Person', backref='person_type', lazy="joined")


class Gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender_name = db.Column(db.String)
    person = db.relationship('Person', backref='person_gender', lazy="joined")


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    phone = db.Column(db.String)
    birthday = db.Column(db.String)
    occupation = db.Column(db.Text)
    institution = db.Column(db.String)
    is_visitor = db.Column(db.Boolean)
    imagefile = db.Column(db.String, nullable=False,
        default='default.jpg')
    imagefile_path = db.Column(db.String, nullable=False,
        default=os.path.join("static/profile_pics", "default.jpg"))
    type_id = db.Column(db.Integer, db.ForeignKey(PersonType.id))
    gender_id = db.Column(db.Integer, db.ForeignKey(Gender.id))
    account = db.relationship('User', backref='own_info', lazy="joined")
    frequency = db.relationship('FrequencyEvent',
        backref='person_frequency', lazy="joined")
    field_events = db.relationship("FieldEvent",
        secondary=lambda: helper_field_person, back_populates="personnel")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created = db.Column(db.String, nullable=False)
    last_modified = db.Column(db.String, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))
    notices = db.relationship('Notices', backref='author', lazy="joined")


class FrequencyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    entry_time = db.Column(db.String, nullable=False)
    exit_time = db.Column(db.String, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id))


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    buy_date = db.Column(db.String, nullable=True)
    imagefile = db.Column(db.String(20),
        default='default.jpg')
    imagefile_path = db.Column(db.String,
        default=os.path.join("static/equip_pics", "default.jpg"))
    field_eligible = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String, nullable=False, default="available")
    lendings = db.relationship('Lendings', backref='equipment', lazy="joined")
    issues = db.relationship('TechnicalIssues', backref='equipment', lazy="joined")
    field_events = db.relationship("FieldEvent", 
        secondary=lambda: helper_field_equips, back_populates="equipments")


class Lendings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lender = db.Column(db.String, nullable=False)
    lend_date = db.Column(db.String, nullable=False)
    return_expected = db.Column(db.String, nullable=False)
    return_done = db.Column(db.String, nullable=True)
    observations = db.Column(db.Text)
    inventory_id = db.Column(db.Integer, db.ForeignKey(Inventory.id))


class TechnicalIssues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    report_date = db.Column(db.String, nullable=False)
    solution_date = db.Column(db.String, nullable=True)
    inventory_id = db.Column(db.Integer,db.ForeignKey(Inventory.id))


class Notices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=True)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))


class FieldEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    date_start = db.Column(db.String)
    date_end_expected = db.Column(db.String)
    date_end_done = db.Column(db.String)
    observations = db.Column(db.Text)
    personnel = db.relationship("Person",
        secondary=lambda: helper_field_person, back_populates="field_events")
    equipments = db.relationship("Inventory",
        secondary=lambda: helper_field_equips, back_populates="field_events")


helper_field_person = db.Table("helper_field_person",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("Person", db.Integer, db.ForeignKey(Person.id)),
    db.Column("FieldEvent", db.Integer, db.ForeignKey(FieldEvent.id))
)

helper_field_equips = db.Table("helper_field_equips",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("Inventory", db.Integer, db.ForeignKey(Inventory.id)),
    db.Column("FieldEvent", db.Integer, db.ForeignKey(FieldEvent.id))
)
