import json
from pathlib import Path
from typing import Dict, List, Type

from rest_framework import serializers
from drf_spectacular.utils import inline_serializer


def _field_from_spec(spec: Dict, required: bool) -> serializers.Field:
    """Return a DRF field based on a JSON schema spec."""
    typ = spec.get("type")
    if typ == "string":
        return serializers.CharField(required=required)
    if typ == "number":
        return serializers.FloatField(required=required)
    if typ == "integer":
        return serializers.IntegerField(required=required)
    if typ == "boolean":
        return serializers.BooleanField(required=required)
    if typ == "array":
        return serializers.ListField(child=serializers.JSONField(), required=required)
    if typ == "object" or "properties" in spec:
        return serializers.DictField(required=required)
    return serializers.JSONField(required=required)


def serializer_from_json_schema(path: Path) -> Type[serializers.Serializer]:
    """Create an inline serializer from a JSON schema file."""
    with open(path) as f:
        schema = json.load(f)

    required = set(schema.get("required", []))
    fields = {
        name: _field_from_spec(spec, name in required)
        for name, spec in schema.get("properties", {}).items()
    }

    return inline_serializer(name=schema.get("$id", path.stem), fields=fields)


def message_serializer_for_schema(schema_file: str) -> Type[serializers.Serializer]:
    """Return Message serializer subclass with payload typed by schema."""
    from app.serializers import MessageSerializer

    path = Path(__file__).parent / "schema" / schema_file
    payload_serializer = serializer_from_json_schema(path)

    return type(
        f"{path.stem}MessageSerializer",
        (MessageSerializer,),
        {"payload": payload_serializer}
    )


def get_all_message_serializers() -> List[Type[serializers.Serializer]]:
    schema_dir = Path(__file__).parent / "schema"
    return [message_serializer_for_schema(p.name) for p in schema_dir.glob("*.json")]
