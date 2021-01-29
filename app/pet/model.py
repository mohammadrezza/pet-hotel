from enum import Enum


class PetType(Enum):
    CAT = "CAT"
    DOG = "DOG"

    def __str__(self):
        return self.value


class Pet:
    def __init__(self, identifier, name, pet_type, owner_id, room_id, created_at, updated_at):
        self.identifier = identifier
        self.name = name
        self.type = pet_type
        self.owner_id = owner_id
        self.room_id = room_id
        self.created_at = created_at
        self.updated_at = updated_at

    def free_room(self):
        self.room_id = -1

    def is_checked_in(self):
        return False if self.room_id is -1 else True

    def dump(self):
        return {
            "_id": self.identifier,
            "name": self.name,
            "type": self.type.value if type(self.type) is PetType else self.type,
            "owner_id": self.owner_id,
            "room_id": int(self.room_id),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_db(cls, json_obj):
        return cls(
            identifier=json_obj["_id"],
            name=json_obj["name"],
            pet_type=PetType(json_obj["type"]),
            owner_id=json_obj["owner_id"],
            room_id=json_obj["room_id"],
            created_at=json_obj["created_at"],
            updated_at=json_obj["updated_at"],
        )
