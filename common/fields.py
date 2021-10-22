from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

__all__ = [
    'VirtualBooleanField',
]

class VirtualBooleanField(serializers.Field):
    default_error_messages = {
        'invalid': _('Must be a valid boolean.')
    }
    default_empty_html = False
    initial = False
    TRUE_VALUES = {
        't', 'T',
        'y', 'Y', 'yes', 'Yes', 'YES',
        'true', 'True', 'TRUE',
        'on', 'On', 'ON',
        '1', 1,
        True
    }
    FALSE_VALUES = {
        'f', 'F',
        'n', 'N', 'no', 'No', 'NO',
        'false', 'False', 'FALSE',
        'off', 'Off', 'OFF',
        '0', 0, 0.0,
        False
    }
    NULL_VALUES = {'null', 'Null', 'NULL', '', None}

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs['source'] = '*'
        kwargs['read_only'] = False
        kwargs['required'] = False
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        # The method name defaults to `get_{field_name}`.
        if self.method_name is None:
            self.method_name = 'get_{field_name}'.format(field_name=field_name)

        super().bind(field_name, parent)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)


    def to_internal_value(self, data):
        try:
            if data in self.TRUE_VALUES:
                return { self.field_name: True }
            elif data in self.FALSE_VALUES:
                return { self.field_name: False }
            elif data in self.NULL_VALUES and self.allow_null:
                return { self.field_name: None }
        except TypeError:  # Input is an unhashable type
            pass
        self.fail('invalid', input=data)