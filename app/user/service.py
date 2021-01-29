from typing import Union
from app import mongo, mailer
from app.utilities import gen_id, datetime_now
from .model import UserRole, Customer, Staff, Manager


class UserService:
    @staticmethod
    def __load_user(db_res):
        if db_res["role"] == UserRole.CUSTOMER.value:
            return Customer.from_db(db_res)
        elif db_res["role"] == UserRole.STAFF.value:
            return Staff.from_db(db_res)
        elif db_res["role"] == UserRole.MANAGER.value:
            return Manager.from_db(db_res)

    @staticmethod
    def find_by_id(identifier: str):
        return mongo.db.users.find_one({"_id": identifier})

    @staticmethod
    def find_by_email(email: str, user_role: UserRole = None):
        filters = dict()
        filters["email"] = email
        if user_role is not None:
            filters["role"] = user_role.value
        return mongo.db.users.find_one(filters)

    @staticmethod
    def get_by_id(identifier: str):
        res = UserService.find_by_id(identifier)
        if res is not None:
            return UserService.__load_user(res)

    @staticmethod
    def get_by_email(email: str):
        res = UserService.find_by_email(email)
        if res is not None:
            return UserService.__load_user(res)

    @staticmethod
    def insert(user: Union[Customer, Staff, Manager]):
        dumped_obj = user.dump()
        mongo.db.users.insert_one(dumped_obj)

    @staticmethod
    def update(user: Union[Customer, Staff, Manager]):
        user.updated_at = datetime_now()
        dumped_obj = user.dump()
        del dumped_obj["_id"]
        mongo.db.users.update_one({"_id": user.identifier}, {"$set": dumped_obj})

    @staticmethod
    def invite(name, email: str):
        subject = 'Signup to Pet Hotel Now !'
        text = 'http://localhost:5000/users/register'
        to = [{'name': name, 'email': email}]
        return mailer.send_mail(subject, text, to)


class CustomerService:
    @staticmethod
    def create(fullname, email, password):
        customer = Customer(
            identifier=gen_id(),
            fullname=fullname,
            email=email,
            password=password,
            role=UserRole.CUSTOMER,
            created_at=datetime_now(),
            updated_at=datetime_now(),
            is_active=True,
            failed_login_attempts=0,
            last_failed_login_at=''
        )
        customer.hash_password(password)
        return customer


class StaffService:
    @staticmethod
    def create(fullname, email, password):
        staff = Staff(
            identifier=gen_id(),
            fullname=fullname,
            email=email,
            password=password,
            role=UserRole.STAFF,
            created_at=datetime_now(),
            updated_at=datetime_now(),
        )
        staff.hash_password(password)
        return staff


class ManagerService:
    pass
