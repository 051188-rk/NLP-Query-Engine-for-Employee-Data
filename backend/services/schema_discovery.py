from sqlalchemy import create_engine, inspect
import json

class SchemaDiscovery:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self._last = None

    def analyze_database(self):
        if not self.connection_string:
            raise ValueError("No connection string provided.")
        engine = create_engine(self.connection_string)
        inspector = inspect(engine)
        schema = {}
        for table_name in inspector.get_table_names():
            cols = inspector.get_columns(table_name)
            fks = inspector.get_foreign_keys(table_name)
            schema[table_name] = {
                'columns': [{ 'name': c['name'], 'type': str(c['type']) } for c in cols],
                'foreign_keys': fks
            }
        self._last = schema
        return schema

    def get_last_schema(self):
        if self._last is None:
            return self.analyze_database()
        return self._last
