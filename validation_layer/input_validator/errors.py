class ValidationError(Exception):
    pass

class MissingFieldError(ValidationError):
    pass

class TypeMismatchError(ValidationError):
    pass

class EmptyValueError(ValidationError):
    pass