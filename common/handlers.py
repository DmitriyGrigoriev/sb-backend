from jsondiff import diff
from django.http import JsonResponse
from rest_framework import status
from django.core import serializers
from django.utils.translation import ugettext as _

from common.models import TemplateModel

def conflict(request, target=None):
    _hidden_fields = TemplateModel._meta.get_fields()

    try:
        saved = target.__class__._default_manager.get(pk=target.pk)
    except target.__class__.DoesNotExists:
        saved = None

    def serialize_record(fields=None):
        array_result = serializers.serialize('json', [fields,], ensure_ascii=False)
        json_string = array_result[1:-1]
        # Replace field value in a json string such as "Blocked": True to the "Blocked": 1
        # because that format needs for diff utility
        return json_string\
            .replace(": true,", ": 1,")\
            .replace(": true", ": 1")\
            .replace(": false,", ": 0,")\
            .replace(": false", ": 0")

    # Don't show errors for the service fields
    def _is_hidden(field_name=None):
        max_fields = len(_hidden_fields)
        for i in range(max_fields):
            if (field_name == _hidden_fields[i].name):
                return True
        return False

    target_json = serialize_record(fields=target)
    saved_json = serialize_record(fields=saved)
    # See documentation: https://github.com/xlwings/jsondiff
    ddiff = diff(target_json, saved_json, load=True)
    # Iterate only fields dict
    if ('fields' in ddiff):
        fields = ddiff['fields'].copy()
        for field, _value in fields.items():
            # todo: It possible the best solution add value to the message text
            # At moment leave only warning text
            if _is_hidden(field_name=field):
                del ddiff['fields'][field]
            else:
                ddiff['fields'][field] = [_('Значение поля было изменено другим пользователем')]
        ctx = ddiff['fields']
    else:
        ctx = None

    return JsonResponse(
        data=ctx,
        status=status.HTTP_409_CONFLICT
    )
