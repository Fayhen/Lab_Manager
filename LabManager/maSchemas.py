from marshmallow import fields
# from marshmallow_sqlalchemy import ModelSchema
from LabManager import ma
from LabManager.dbModels import PersonType, Gender, Person, User, FrequencyEvent, Inventory, Lendings, TechnicalIssues, Notices, FieldEvent


class SmartNested(fields.Nested):
    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return {"id": int(getattr(obj, attr + "_id"))}
        return super(SmartNested, self).serialize(attr, obj, accessor)


# Marshmellow schema definitions
class TypeSchema(ma.ModelSchema):
    class Meta:
        model = PersonType
        # id = fields.Integer
        # type_name = fields.String


class GenreSchema(ma.ModelSchema):
    class Meta:
        model = Gender
        # id = fields.Integer
        # genre_name = fields.String


class PersonSchema(ma.ModelSchema):
    # person_type = SmartNested(TypeSchema)
    # gender = SmartNested(GenreSchema)

    class Meta:
        model = Person
        # id = fields.Integer
        # first_name = fields.String
        # last_name = fields.String
        # middle_name = fields.String
        # formatted_name = fields.Method("format_name", dump_only=True)
        # phone = fields.String
        # birthday = fields.Date
        # occupation = fields.String
        # institution = fields.String
        # imagefile = fields.String
        # imagefile_path = fields.String
        # person_type = fields.Nested(TypeSchema)
        # genre = fields.Nested(GenreSchema)

    # def formatted_name(self, Person):
    #     if Person.middle_name:
    #         return f"{Person.first_name} {Person.middle_name} {Person.last_name}"
    #     else:
    #         return f"{Person.first_name} {Person.last_name}"


class UserSchema(ma.ModelSchema):
    # person = SmartNested(PersonSchema)

    class Meta:
        model = User
    #     fields = ('id', 'username', 'email', 'notices',
    #         person_id = fields.Nested(PersonSchema),
    #         notices = fields.Pluck('self', 'id', 'title', 'date', many=True))
        # id = fields.Integer
        # username = fields.String
        # email = fields.Email
        # person = fields.Nested(PersonSchema)


class FrequencySchema(ma.ModelSchema):
    # person = SmartNested(PersonSchema)

    class Meta:
        model = FrequencyEvent
    #     fields = ('id', 'date', 'entry_time', 'exit_time',
    #         person_id = fields.Nested(PersonSchema, only=['id, first_name', 'last_name']))
        # id = fields.Integer
        # date = fields.Date
        # entry_time = fields.Time
        # exit_time = fields.Time
        # person = fields.Nested(PersonSchema)


class InventorySchema(ma.ModelSchema):
    class Meta:
        model = Inventory
        # fields = ('id', 'name', 'description', 'imagefile', 'imagefile_path',
        #     lendings = fields.Pluck('self', 'id', 'lender', 'lend_date', many=True),
        #     issues = fields.Pluck('self', 'id', 'report_date', many=True),
        #     field_events = fields.Pluck('self', 'id', 'laction', 'date_start', many=True))
        # id = fields.Integer
        # name = fields.String
        # description = fields.String
        # imagefile = fields.String
        # imagefile_path = fields.String


class LendingSchema(ma.ModelSchema):
    # equipment = SmartNested(InventorySchema)

    class Meta:
        model = Lendings
    #     fields = ('id', 'lender', 'lend_date', 'return_expected', 'return_done', 'observations',
    #         inventory_id = fields.Nested(InventorySchema))
        # id = fields.Integer
        # lender = fields.String
        # lend_date = fields.Date
        # return_expected = fields.Date
        # return_done = fields.Date
        # equipment = fields.Nested(InventorySchema)


class IssueSchema(ma.ModelSchema):
    # equipment = SmartNested(InventorySchema)

    class Meta:
        model = TechnicalIssues
    #     fields = ('id', 'description', 'report_date', 'solution_date',
    #         inventory_id = fields.Nested(InventorySchema))
        # id = fields.Integer
        # description = fields.String
        # report_date = fields.Date
        # solution_date = fields.Date
        # equipment = fields.Nested(InventorySchema)


class NoticeSchema(ma.ModelSchema):
    # user = SmartNested(UserSchema)
    class Meta:
        model = Notices
    #     fields = ('id', 'title', 'date', 'content', 'archived',
    #         user_id = fields.Nested(UserSchema, only=['id, username', 'email']))
        # id = fields.Integer
        # title = fields.String
        # date = fields.DateTime
        # content = fields.String
        # archived = fields.Boolean
        # equipment = fields.Nested(InventorySchema)


class FieldSchema(ma.ModelSchema):
    # personnel = SmartNested(PersonSchema)
    # equipments = SmartNested(InventorySchema)

    class Meta:
        model = FieldEvent
    #     fields = ('id', 'location', 'date_start', 'date_end_expected', 'date_end_done', 'observations',
    #         personnel = fields.Pluck('self', 'id', many=True),
    #         equipments = fields.Pluck('self', 'id', many=True))
        # id = fields.Integer
        # location = fields.String
        # date_start = fields.Date
        # date_end_expected = fields.Date
        # date_end_done = fields.Date
        # observations = fields.String
        # personnel = fields.Nested(PersonSchema)
        # equipments = fields.Nested(InventorySchema)


# Marshmallow schema inits
type_schema = TypeSchema(strict=True)
genre_schema = GenreSchema(strict=True)
person_schema = PersonSchema(strict=True)
persons_schema = PersonSchema(many=True, strict=True)
user_schema = UserSchema(strict=True)
frequency_schema = FrequencySchema(strict=True)
equipment_schema = InventorySchema(strict=True)
equipments_schema = InventorySchema(many=True, strict=True)
lending_schema = LendingSchema(strict=True)
lendings_schema = LendingSchema(many=True, strict=True)
issue_schema = IssueSchema(strict=True)
issues_schema = IssueSchema(many=True, strict=True)
notice_schema = NoticeSchema(strict=True)
notices_schema = NoticeSchema(many=True, strict=True)
field_schema = FieldSchema(strict=True)
fields_schema = FieldSchema(many=True, strict=True)
