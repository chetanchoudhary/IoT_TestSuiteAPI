from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid certificate."
    }

    def _deserialize(self, value, attr, data) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")

        return value


class CertificateSchema(Schema):
    certificate = FileStorageField(required=True)
