from pathlib import Path

from agents.openapi_utils import serializer_from_json_schema


def test_serializer_from_json_schema():
    schema_path = Path('agents/schema/GoalList.json')
    serializer_cls = serializer_from_json_schema(schema_path)
    fields = serializer_cls.get_fields()
    assert 'goals' in fields
