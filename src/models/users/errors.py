
'''
UserNotExistsError and IncorrectPasswordError are sub-classes of UserError.
In Python, when you catch the parent class, all subclasses are also caught.
'''
class UserError(Exception):
    def __init__(self, message):
        self.message = message

class UserNotExistsError(UserError):  # This method inherit from UserError
    pass


class IncorrectPasswordError(UserError):
    pass

class UserAlreadyRegisteredError(UserError):
    pass

class InvalidEmailError(UserError):
    pass