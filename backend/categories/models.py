from uuid import uuid4
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, UUIDField


class Category(Document):
    uuid = UUIDField(default=uuid4, unique=True)
    name = StringField(max_length=120, unique=True, required=True)
    created_at = DateTimeField(default=datetime.now)

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'name': self.name}
