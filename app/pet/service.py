from app.utilities import gen_id, datetime_now
from app import mongo
from .model import Pet, PetType


class PetService:

    @staticmethod
    def create(name: str, pet_type: PetType, owner_id: str = '', room_id: int = -1) -> Pet:
        return Pet(
            identifier=gen_id(),
            name=name,
            pet_type=pet_type,
            owner_id=owner_id,
            room_id=room_id,
            created_at=datetime_now(),
            updated_at=datetime_now()
        )

    @staticmethod
    def insert(pet: Pet):
        mongo.db.pets.insert_one(pet.dump())

    @staticmethod
    def update(pet: Pet):
        pet.updated_at = datetime_now()
        dumped_obj = pet.dump()
        del dumped_obj["_id"]
        mongo.db.pets.update_one({"_id": pet.identifier}, {"$set": dumped_obj})

    @staticmethod
    def delete_by_id(pet_id: str):
        mongo.db.pets.delete_one({"_id": pet_id})

    @staticmethod
    def get_by_id(pet_id: str):
        res = mongo.db.pets.find_one({"_id": pet_id})
        if res is not None:
            return Pet.from_db(res)

    @staticmethod
    def get_by_room_id(room_id: int):
        res = mongo.db.pets.find_one({"room_id": room_id})
        if res is not None:
            return Pet.from_db(res)

    @staticmethod
    def get_customer_pets(customer_id, q: str, skip: int, size: int):
        filters = dict()
        filters["owner_id"] = customer_id
        if q != "":
            filters["name"] = {"$regex": f'.*{q}.*'}
        res = list(mongo.db.pets.find(filters).skip(skip).limit(size))
        return [Pet.from_db(doc) for doc in res]

    @staticmethod
    def get_all(q: str, skip: int, limit: int):
        filters = {}
        if q != "":
            filters["name"] = {"$regex": f'.*{q}.*'}
        res = list(mongo.db.pets.find(filters).skip(skip).limit(limit))
        return [Pet.from_db(doc) for doc in res]

    @staticmethod
    def is_room_available(room_id: int) -> bool:
        res = mongo.db.pets.find_one({"room_id": room_id})
        return True if res is None else False
