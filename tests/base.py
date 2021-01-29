from flask_testing import TestCase
from app import create_app, mongo


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app("test")
        mongo.db.pets.drop()
        mongo.db.users.drop()
        return app

    """
    helper methods
    """

    def assert201(self, response):
        self.assertStatus(response, 201)

    def __create_auth_header(self, token):
        return {"Authorization": f'Bearer {token}'}

    def register(self, fullname, email, password):
        return self.client.post("/users/register",
                                json={
                                    "fullname": fullname,
                                    "email": email,
                                    "password": password
                                })

    def login(self, email, password):
        return self.client.post("/users/login",
                                json={
                                    "email": email,
                                    "password": password
                                })

    def invite(self, token, email):
        return self.client.post("/users/invite",
                                headers=self.__create_auth_header(token),
                                json={
                                    "email": email
                                })

    def update_status(self, token, user_id, active):
        return self.client.patch(f"/users/{user_id}/status",
                                 headers=self.__create_auth_header(token),
                                 json={
                                     "active": active
                                 })

    def create_staff(self, token, fullname, email, password):
        return self.client.post(f"/users/staff",
                                headers=self.__create_auth_header(token),
                                json={
                                    "fullname": fullname,
                                    "email": email,
                                    "password": password
                                })

    def get_user(self, token):
        return self.client.get("/users", headers=self.__create_auth_header(token))

    def create_pet(self, token, name, pet_type):
        return self.client.post("/pets",
                                headers=self.__create_auth_header(token),
                                json={
                                    "name": name,
                                    "type": pet_type
                                })

    def edit_pet(self, token, pet_id, name, pet_type, owner_id=None):
        json = {
            "pet_id": pet_id,
            "name": name,
            "type": pet_type,
        }
        if owner_id is not None:
            json["owner_id"] = owner_id
        return self.client.put("/pets", headers=self.__create_auth_header(token), json=json)

    def pet_check_in(self, token, pet_id, room_id):
        return self.client.post(f"/pets/{pet_id}/check-in",
                                headers=self.__create_auth_header(token),
                                json={
                                    "room_id": room_id,
                                })

    def pet_check_out(self, token, pet_id):
        return self.client.post(f"/pets/{pet_id}/check-out",
                                headers=self.__create_auth_header(token))

    def change_pet_room(self, token, pet_id, new_room_id):
        return self.client.post(f"/pets/{pet_id}/move",
                                headers=self.__create_auth_header(token),
                                json={
                                    "new_room_id": new_room_id
                                })

    def get_pets(self, token, q, page, size):
        return self.client.get(f"/pets?q={q}&page={page}&size={size}",
                               headers=self.__create_auth_header(token))

    def delete_pet(self, token, pet_id):
        return self.client.delete(f"/pets/{pet_id}",
                                  headers=self.__create_auth_header(token))

    def get_customer_token(self):
        email = 'customer@test.com'
        password = '1234567890'
        self.register('customer-user', email, password)
        response = self.login(email, password)
        return response.json["data"]["token"]

    def get_staff_token(self):
        email = 'staff@test.com'
        password = '0987654321'
        token = self.get_manager_token()
        self.create_staff(token, 'staff-user', email, password)
        response = self.login(email, password)
        return response.json["data"]["token"]

    def get_manager_token(self):
        email = 'mrmirhajian1996@gmail.com'
        password = '1qaz!QAZ'
        mongo.db.users.insert_one({
            "_id": "f8f1a5f478414dfdabbca7807384aec1",
            "fullname": "mohammadreza mirhajian",
            "email": email,
            "password": b'$2b$12$LVwtDHJGKDKBeEE2Ikph.eNAarP8QqcQtF7.L4qcfY9ofP0B2Zvka',  # 1qaz!QAZ
            "role": "MANAGER",
            "created_at": "2020-12-21 22:31:04",
            "updated_at": "2020-12-21 22:31:04"
        })
        response = self.login(email, password)
        return response.json["data"]["token"]
