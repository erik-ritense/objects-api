from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from objects.core.utils import check_objecttype

from .constants import Operators
from .utils import string_to_value


class JsonSchemaValidator:
    code = "invalid-json-schema"

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        self.instance = getattr(serializer, "instance", None)

    def __call__(self, attrs):
        object_type = attrs.get("object_type") or self.instance.object_type
        version = attrs.get("record", {}).get("version") or self.instance.record.version

        if attrs.get("record"):
            data = attrs["record"].get("data", {})
        else:
            data = self.instance.record.data

        if not object_type or not version or not data:
            return

        try:
            check_objecttype(object_type, version, data)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.args[0], code=self.code) from exc


class IsImmutableValidator:
    """
    Validate that the field should not be changed in update action
    """

    message = _("This field can't be changed")
    code = "immutable-field"

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.serializer_field = serializer_field
        self.instance = getattr(serializer_field.parent, "instance", None)

    def __call__(self, new_value):
        # no instance -> it's not an update
        if not self.instance:
            return

        current_value = getattr(self.instance, self.serializer_field.source)

        if new_value != current_value:
            raise serializers.ValidationError(self.message, code=self.code)


def validate_data_attrs(value: str):
    code = "invalid-data-attrs-query"
    parts = value.split(",")

    for value_part in parts:
        try:
            variable, operator, val = value_part.rsplit("__", 2)
        except ValueError as exc:
            raise serializers.ValidationError(exc.args[0], code=code) from exc

        if operator not in Operators.values:
            message = _("Comparison operator `%(operator)s` is unknown") % {
                "operator": operator
            }
            raise serializers.ValidationError(message, code=code)

        if operator not in (Operators.exact, Operators.icontains) and isinstance(
            string_to_value(val), str
        ):
            message = _(
                "Operator `%(operator)s` supports only dates and/or numeric values"
            ) % {"operator": operator}
            raise serializers.ValidationError(message, code=code)
