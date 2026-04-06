from mongoengine import Document, EmbeddedDocument, fields
from datetime import datetime

class TestCase(EmbeddedDocument):
    test_id = fields.StringField(required=True)
    type = fields.StringField()
    priority = fields.StringField()
    test_case = fields.StringField()
    expected_result = fields.StringField()
    # Optional: add more fields if needed, like test_category, steps, etc.
    # test_category = fields.StringField()
    # steps = fields.ListField(fields.StringField())

class User(Document):
    username = fields.StringField(required=True, unique=True)
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True)

class TestCaseRun(Document):
    user = fields.ReferenceField(User, required=True)          # Link to the user who generated this run
    requirement = fields.DictField()                            # Store the requirement analysis
    test_cases = fields.EmbeddedDocumentListField(TestCase)    # List of generated test cases
    created_at = fields.DateTimeField(default=datetime.now)    # Timestamp of generation