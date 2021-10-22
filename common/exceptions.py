from rest_framework.exceptions import APIException
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.utils.translation import ugettext_lazy as _
from common import status


class AppsProtectedError(APIException):
    status_code = status.HTTP_550_PROTECTED_ERROR
    default_detail = _('Cannot delete some instances of model.')
    default_code = 'protected_error'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        super(AppsProtectedError, self).__init__(detail=detail, code=code)


class FieldValidationError(ValidationError):

    def __init__(self, field=None, detail=None, code=None):
        if field is not None:
            super(FieldValidationError, self).__init__({field: [ErrorDetail(detail ,code=code)]})
        if field is None:
            super(FieldValidationError, self).__init__(detail=detail, code=code)
