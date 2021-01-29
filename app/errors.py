from flask_api import status


class Err(Exception):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg


class ErrValidation(Err):
    def __init__(self, msg):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.msg = msg


class ErrUserNotFound(Err):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.msg = "User not found!"


class ErrUserIsBlocked(Err):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.msg = "Your account is locked due to too many failed login attempts, contact manager to unblock"


class ErrInvalidLogin(Err):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.msg = "Incorrect Email/Password"


class ErrForbidden(Err):
    def __init__(self, msg=None):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.msg = msg


class ErrRoomIsFull(Err):
    def __init__(self):
        self.status_code = status.HTTP_409_CONFLICT
        self.msg = "Requested room is reserved, please try another room"


class ErrPetNotFound(Err):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.msg = "Pet not found!"


class ErrEmailAlreadyExist(Err):
    def __init__(self):
        self.status_code = status.HTTP_409_CONFLICT
        self.msg = "User with this email address already exist"


class ErrServiceUnavailable(Err):
    def __init__(self):
        self.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        self.msg = "Please try again in few minutes"


class ErrUnauthorized(Err):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.msg = None
