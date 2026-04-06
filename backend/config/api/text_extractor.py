from mongoengine import Document, EmbeddedDocument, fields

class TestCase(EmbeddedDocument):
    test_id = fields.StringField(required=True)
    type = fields.StringField()
    priority = fields.StringField()
    test_case = fields.StringField()
    expected_result = fields.StringField()


class User(Document):
    username = fields.StringField(required=True, unique=True)
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True)

class TestCaseRun(Document):
    requirement = fields.DictField()
    test_cases = fields.EmbeddedDocumentListField(TestCase)
