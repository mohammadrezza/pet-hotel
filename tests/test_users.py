import unittest
from tests.base import BaseTestCase
from app import mongo


class TestUsers(BaseTestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self):
        mongo.db.users.delete_many({})

    def test_user_register_successful(self):
        response = self.register('john doe', 'johndoe@gmail.com', '1234567890')
        self.assert201(response)

    def test_user_login_invalid_password(self):
        email = 'janedoe@gmail.com'
        response = self.register('john doe', email, '1234567890')
        self.assert201(response)
        response = self.login(email, 'invalid_password')
        self.assert_401(response)

    def test_user_login_email_not_exist(self):
        email = 'janedoe@gmail.com'
        password = '1234567890'
        response = self.register('john doe', email, password)
        self.assert201(response)
        response = self.login('emaildoesnotexist@gmail.com', password)
        self.assert_404(response)

    def test_get_customer_info(self):
        token = self.get_customer_token()
        response = self.get_user(token)
        self.assert200(response)

    def test_create_new_staff_successful(self):
        token = self.get_manager_token()
        email = 'janedoe@gmail.com'
        response = self.create_staff(token, 'jane doe', email, '1234567890')
        self.assert201(response)

    def test_create_new_staff_forbidden(self):
        token = self.get_staff_token()
        email = 'janedoe@gmail.com'
        response = self.create_staff(token, 'jane doe', email, '1234567890')
        self.assert_403(response)

    def test_create_new_staff_unauthorized(self):
        email = 'janedoe@gmail.com'
        response = self.create_staff(None, 'jane doe', email, '1234567890')
        self.assert_401(response)

    def test_user_login_block_after_failed_attempts(self):
        email = 'janedoe@gmail.com'
        password = '123456790'
        response = self.register('jane doe', email, password)
        self.assert201(response)
        for i in range(3):
            response = self.login(email, 'invalid_password')
            self.assert_401(response)
        response = self.login(email, password)
        self.assert_403(response)

    def test_update_status_successful(self):
        email = 'janedoe@gmail.com'
        password = '123456790'
        response = self.register('jane doe', email, password)
        user_id = response.json["data"]["identifier"]
        self.assert201(response)
        for i in range(3):
            response = self.login(email, 'invalid_password')
            self.assert_401(response)
        response = self.login(email, 'invalid_password')
        self.assert_403(response)

        token = self.get_manager_token()
        response = self.update_status(token, user_id, True)
        self.assert200(response)

        response = self.login(email, password)
        self.assert200(response)


if __name__ == "__main__":
    unittest.main()
