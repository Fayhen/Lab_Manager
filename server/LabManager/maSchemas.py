# from marshmallow import fields
# from marshmallow_sqlalchemy import ModelSchema
from LabManager import ma
# from LabManager.dbModels import PersonType, Gender, Person, User, FrequencyEvent, Inventory, Lendings, TechnicalIssues, Notices, FieldEvent, helper_field_person, helper_field_equips
import LabManager.dbModels as models


# class SmartNested(fields.Nested):
#     def serialize(self, attr, obj, accessor=None):
#         if attr not in obj.__dict__:
#             return {"id": int(getattr(obj, attr + "_id"))}
#         return super(SmartNested, self).serialize(attr, obj, accessor)


# Marshmallow schema definitions
class TypeSchema(ma.ModelSchema):
    class Meta:
        model = models.PersonType


class GenderSchema(ma.ModelSchema):
    class Meta:
        model = models.Gender


class PersonSchema(ma.ModelSchema):
    # person_type = SmartNested(TypeSchema)
    # gender = SmartNested(GenreSchema)
    class Meta:
        model = models.Person
        fields = ("first_name", "last_name", "middle_name", "phone",
            "birthday", "occupation", "institution", "type_id", "gender_id",
            "frequency", "field_events")
    
    type_id = ma.Nested(TypeSchema)
    gender_id = ma.Nested(GenderSchema)


class UserSchema(ma.ModelSchema):
    # person = SmartNested(PersonSchema)
    class Meta:
        model = models.User
        fields = ("username", "email")


class ProfileSchema(ma.ModelSchema):
    class Meta:
        model = models.User
        fields = ("username", "email", "notices", "person_id")
    
    person_id = ma.Nested(PersonSchema)


class FrequencySchema(ma.ModelSchema):
    # person = SmartNested(PersonSchema)
    class Meta:
        model = models.FrequencyEvent


class InventorySchema(ma.ModelSchema):
    class Meta:
        model = models.Inventory


class LendingSchema(ma.ModelSchema):
    # equipment = SmartNested(InventorySchema)
    class Meta:
        model = models.Lendings


class IssueSchema(ma.ModelSchema):
    # equipment = SmartNested(InventorySchema)
    class Meta:
        model = models.TechnicalIssues


class NoticeSchema(ma.ModelSchema):
    # user = SmartNested(UserSchema)
    class Meta:
        model = models.Notices


class FieldSchema(ma.ModelSchema):
    class Meta:
        model = models.FieldEvent


class FieldPerson(ma.TableSchema):
    class Meta:
        table = models.helper_field_person


class FieldEquips(ma.TableSchema):
    class Meta:
        table = models.helper_field_equips

# Marshmallow schema inits
type_schema = TypeSchema(strict=True)
types_schema = TypeSchema(many=True, strict=True)
gender_schema = GenderSchema(strict=True)
genders_schema = GenderSchema(many=True, strict=True)
person_schema = PersonSchema(strict=True)
people_schema = PersonSchema(many=True, strict=True)
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)
frequency_schema = FrequencySchema(strict=True)
frequencies_schema = FrequencySchema(many=True, strict=True)
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
profile_schema = ProfileSchema(strict=True)

# fields_person_schema = FieldPerson(many=True, strict=True)
# fields_equips_schema = FieldEquips(many=True, strict=True)
