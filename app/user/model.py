from enum import Enum
from app import bcrypt


class UserRole(Enum):
    CUSTOMER = "CUSTOMER"
    STAFF = "STAFF"
    MANAGER = "MANAGER"


class User:
    def __init__(self, identifier, fullname, email, password, role, created_at, updated_at):
        self.identifier = identifier
        self.fullname = fullname
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at

    def dump(self):
        return {
            "_id": self.identifier,
            "fullname": self.fullname,
            "email": self.email,
            "password": self.password,
            "role": self.role.value if type(self.role) is UserRole else self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_db(cls, json_obj):
        return cls(
            identifier=json_obj['_id'],
            fullname=json_obj['fullname'],
            email=json_obj['email'],
            password=json_obj['password'],
            role=UserRole(json_obj['role']),
            created_at=json_obj['created_at'],
            updated_at=json_obj['updated_at'],
        )

    def hash_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password):
        return True if bcrypt.check_password_hash(self.password, plain_text_password) else False


class Customer(User):
    def __init__(self, identifier, fullname, email, password, role, created_at, updated_at, is_active,
                 failed_login_attempts, last_failed_login_at):
        super(Customer, self).__init__(identifier, fullname, email, password, role, created_at, updated_at)
        self.is_active = is_active
        self.failed_login_attempts = failed_login_attempts
        self.last_failed_login_at = last_failed_login_at

    def dump(self):
        return {
            **super().dump(),
            "is_active": self.is_active,
            "failed_login_attempts": self.failed_login_attempts,
            "last_failed_login_at": self.last_failed_login_at
        }

    @classmethod
    def from_db(cls, json_obj):
        return cls(
            identifier=json_obj['_id'],
            fullname=json_obj['fullname'],
            email=json_obj['email'],
            password=json_obj['password'],
            role=UserRole(json_obj["role"]),
            created_at=json_obj['created_at'],
            updated_at=json_obj['updated_at'],
            is_active=json_obj['is_active'],
            failed_login_attempts=json_obj['failed_login_attempts'],
            last_failed_login_at=json_obj['last_failed_login_at']
        )


class Staff(User):
    def __init__(self, identifier, fullname, email, password, role, created_at, updated_at):
        super(Staff, self).__init__(identifier, fullname, email, password, role, created_at, updated_at)


class Manager(User):
    def __init__(self, identifier, fullname, email, password, role, created_at, updated_at):
        super(Manager, self).__init__(identifier, fullname, email, password, role, created_at, updated_at)
