import unittest
from tests.base import BaseTestCase
from app import mongo


class TestPets(BaseTestCase):

    def tearDown(self):
        mongo.db.users.delete_many({})

    def test_create_pet(self):
        token = self.get_customer_token()
        response = self.create_pet(token, "micky", "DOG")
        self.assert201(response)

    def test_edit_pet(self):
        token = self.get_customer_token()
        response = self.create_pet(token, "micky", "DOG")
        self.assert201(response)

        pet_id = response.json["data"]["identifier"]
        pet_name = "lily"
        pet_type = "CAT"
        response = self.edit_pet(token, pet_id, pet_name, pet_type)
        self.assert200(response)

    def test_pet_check_in_forbidden(self):
        token = self.get_customer_token()
        response = self.create_pet(token, "micky", "DOG")
        self.assert201(response)

        pet_id = response.json["data"]["identifier"]
        response = self.pet_check_in(token, pet_id, 10)
        self.assert403(response)

    def test_pet_check_in_successful(self):
        token = self.get_customer_token()
        response = self.create_pet(token, "micky", "DOG")
        self.assert201(response)
        pet_id = response.json["data"]["identifier"]

        token = self.get_staff_token()
        response = self.pet_check_in(token, pet_id, 10)
        self.assert200(response)

    def test_pet_check_in_full_room(self):
        token = self.get_staff_token()
        room_id = 10

        # create and check in first pet
        response = self.create_pet(token, "micky", "DOG")
        self.assert201(response)
        pet_id = response.json["data"]["identifier"]
        response = self.pet_check_in(token, pet_id, room_id)
        self.assert200(response)

        # create second pet
        response = self.create_pet(token, "billy", "DOG")
        self.assert201(response)
        pet_id = response.json["data"]["identifier"]

        # check in second pet into first pet room
        response = self.pet_check_in(token, pet_id, room_id)
        self.assertStatus(response, 409)

    def test_pet_check_out(self):
        token = self.get_staff_token()

        response = self.create_pet(token, "micky", "DOG")
        self.assert201(response)
        pet_id = response.json["data"]["identifier"]

        response = self.pet_check_in(token, pet_id, 20)
        self.assert200(response)

        response = self.pet_check_out(token, pet_id)
        self.assert200(response)

    def test_get_pets_by_customer(self):
        token = self.get_customer_token()
        # check empty list
        response = self.get_pets(token, "", 1, 10)
        self.assert200(response)
        self.assertIs(len(response.json["data"]), 0)

        # create some pets
        for pet in [{"name": "billy", "type": "DOG"}, {"name": "brayan", "type": "CAT"}]:
            response = self.create_pet(token, pet["name"], pet["type"])
            self.assert201(response)

        response = self.get_pets(token, "br", 1, 10)
        self.assert200(response)
        self.assertIs(len(response.json["data"]), 1)

    def test_get_pets_by_staff(self):
        token = self.get_staff_token()
        # create some pets
        for pet in [{"name": "billy", "type": "DOG"}, {"name": "brayan", "type": "CAT"}]:
            response = self.create_pet(token, pet["name"], pet["type"])
            self.assert201(response)

        response = self.get_pets(token, "b", 1, 10)
        self.assert200(response)
        self.assertIs(len(response.json["data"]), 2)

    def test_delete_pet_checked_in_by_customer(self):
        customer_token = self.get_customer_token()
        staff_token = self.get_staff_token()

        response = self.create_pet(customer_token, "micky", "DOG")
        self.assert201(response)
        pet_id = response.json["data"]["identifier"]

        response = self.pet_check_in(staff_token, pet_id, 15)
        self.assert200(response)

        response = self.delete_pet(customer_token, pet_id)
        self.assert_403(response)

    def test_delete_pet_by_manager(self):
        token = self.get_manager_token()
        response = self.create_pet(token, "micky", "DOG")
        self.assert201(response)
        pet_id = response.json["data"]["identifier"]
        response = self.delete_pet(token, pet_id)
        self.assert200(response)


if __name__ == "__main__":
    unittest.main()
