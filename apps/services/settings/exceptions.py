from .constants import Messages

class InputError(Exception):
    def __init__(self, message):
        self.message = message


class ParameterTypeError(InputError):
    def __init__(self, param):
        super().__init__(
            Messages.REQUARED_PARAMETER_MISSING.format(param)
        )


class ParameterValueError(InputError):
    def __init__(self, param):
        super().__init__(
            Messages.INVALID_VALUE_PARAMETER.format(param)
        )
