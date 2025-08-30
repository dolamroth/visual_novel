from django.db.models import JSONField


class PostgresqlJsonField(JSONField):
    def from_db_value(self, value, expression, connection):
        return value
