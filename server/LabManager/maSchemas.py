from marshmallow import Schema, fields
from LabManager import ma

class TypeSchema(Schema):
    id = fields.Int()
    type_name = fields.Str()
    person = fields.List(fields.Nested(lambda: PersonSchema, only=("id",
        "first_name", "last_name")))

class GenderSchema(Schema):
    id = fields.Int()
    gender_name = fields.Str()
    person = fields.List(fields.Nested(lambda: PersonSchema, only=("id",
        "first_name", "last_name")))

class PersonSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    middle_name = fields.Str()
    phone = fields.Str()
    birthday = fields.Str()
    occupation = fields.Str()
    institution = fields.Str()
    is_visitor = fields.Bool()
    person_type = fields.Nested(TypeSchema, only=("id", "type_name",))
    # person_type = fields.Pluck(TypeSchema, "type_name",)
    person_gender = fields.Nested(GenderSchema, only=("id", "gender_name",))
    # person_gender = fields.Pluck(GenderSchema, "gender_name")
    account = fields.List(fields.Nested(lambda: UserSchema))

class UserSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    created = fields.Str()
    last_modified = fields.Str()

class ProfileSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    # person_id = fields.Int()
    own_info = fields.Nested(PersonSchema, only=("first_name", "last_name",
        "middle_name", "phone", "birthday", "occupation", "institution",
        "person_gender")) #This works. own_info is the backref used on the parent Model on the relationship

class FrequencySchema(Schema):
    id = fields.Int()
    date = fields.Str()
    entry_time = fields.Str()
    exit_time = fields.Str()
    # person_id = fields.Int()
    person_frequency = fields.Nested(PersonSchema, only=("first_name",
        "last_name", "middle_name"))

class InventorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    buy_date = fields.Str()
    field_eligible = fields.Bool()
    status = fields.Str()
    lendings = fields.List(fields.Nested(lambda: LendingSchema, only=("id",)))
    issues = fields.List(fields.Nested(lambda: IssueSchema, only=("id", "description")))
    field_events = fields.List(fields.Nested(lambda: FieldSchema, only=("id", "location")))

class LendingSchema(Schema):
    id = fields.Int()
    lender = fields.Str()
    lend_date = fields.Str()
    return_expected = fields.Str()
    return_done = fields.Str()
    observations = fields.Str()
    equipment = fields.Nested(InventorySchema, only=("id", "name"))

class IssueSchema(Schema):
    id = fields.Int()
    description = fields.Str()
    report_date = fields.Str()
    solution_date = fields.Str()
    equipment = fields.Nested(InventorySchema, only=("id", "name"))

class NoticeSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    date = fields.Str()
    content = fields.Str()
    archived = fields.Bool()
    user_id = fields.Int()

class FieldSchema(Schema):
    id = fields.Int()
    location = fields.Str()
    date_start = fields.Str()
    date_end_expected = fields.Str()
    date_end_done = fields.Str()
    observations = fields.Str()
    personnel = fields.List(fields.Int())
    equipments = fields.List(fields.Int())

# Marchmallow schemas initialization
type_schema = TypeSchema()
types_schema = TypeSchema(many=True)
gender_schema = GenderSchema()
genders_schema = GenderSchema(many=True)
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
profile_schema = ProfileSchema()
frequency_schema = FrequencySchema()
frequencies_schema = FrequencySchema(many=True)
equipment_schema = InventorySchema()
equipments_schema = InventorySchema(many=True)
lending_schema = LendingSchema()
lendings_schema = LendingSchema(many=True)
issue_schema = IssueSchema()
issues_schema = IssueSchema(many=True)
notice_schema = NoticeSchema()
notices_schema = NoticeSchema(many=True)
field_schema = FieldSchema()
fields_schema = FieldSchema(many=True)
