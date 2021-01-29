from flask import request
from flask_api import status
from flask_jwt_extended import get_current_user
from app.middlewares import api_exception_handler, roles_required
from app.utilities import send_ok, calc_skip
from app.errors import ErrValidation, ErrForbidden, ErrRoomIsFull, ErrPetNotFound
from app.user.service import UserService
from .service import PetService
from .model import PetType
from .schema import create_pet_request_schema, create_pet_response_schema
from .schema import edit_pet_request_schema, edit_pet_response_schema
from .schema import get_pets_request_schema, get_pets_response_schema
from .schema import move_pet_request_schema
from .schema import check_in_request_schema


@api_exception_handler
@roles_required(['CUSTOMER', 'STAFF', 'MANAGER'])
def creat_pet():
    data = request.json
    errors = create_pet_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    curr_user = get_current_user()
    name = data["name"]
    pet_type = PetType(data["type"])
    if curr_user.is_customer:
        pet = PetService.create(name, pet_type, curr_user.identity)
    else:
        pet = PetService.create(name, pet_type)
    PetService.insert(pet)
    return send_ok(status_code=status.HTTP_201_CREATED, msg=create_pet_response_schema.dump({"data": pet}))


@api_exception_handler
@roles_required(['CUSTOMER', 'STAFF', 'MANAGER'])
def edit_pet():
    data = request.json
    errors = edit_pet_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    curr_user = get_current_user()
    pet_id = data["pet_id"]
    pet = PetService.get_by_id(pet_id)
    if pet is None:
        raise ErrPetNotFound()
    if curr_user.is_customer and pet.owner_id != curr_user.identity:
        raise ErrForbidden()
    if curr_user.is_customer and pet.room_id is None:
        raise ErrForbidden("cannot update pet that is checked in")
    pet.name = data["name"]
    pet.type = PetType(data["type"])
    if curr_user.is_manager or curr_user.is_staff:
        pet.owner_id = data.get("owner", pet.owner_id)
    PetService.update(pet)
    return send_ok(edit_pet_response_schema.dump({"data": pet}))


@api_exception_handler
@roles_required(['CUSTOMER', 'STAFF', 'MANAGER'])
def get_pets():
    data = dict(request.args)
    errors = get_pets_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    curr_user = get_current_user()
    q = data["q"]
    page = int(data["page"])
    size = int(data["size"])
    skip = calc_skip(page, size)
    if curr_user.is_customer:
        pets = PetService.get_customer_pets(curr_user.identity, q, skip, size)
    else:
        pets = PetService.get_all(q, skip, size)
    for i, pet in enumerate(pets):
        owner = UserService.get_by_id(pet.owner_id)
        pet.owner = owner
    return send_ok(get_pets_response_schema.dump({"data": pets}))


@api_exception_handler
@roles_required(['STAFF', 'MANAGER'])
def check_in(pet_id):
    data = request.json
    errors = check_in_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    room_id = int(data["room_id"])
    if not PetService.is_room_available(room_id):
        raise ErrRoomIsFull()
    pet = PetService.get_by_id(pet_id)
    pet.room_id = room_id
    PetService.update(pet)
    return send_ok()


@api_exception_handler
@roles_required(['STAFF', 'MANAGER'])
def check_out(pet_id):
    pet = PetService.get_by_id(pet_id)
    if pet is None:
        raise ErrPetNotFound()
    pet.free_room()
    PetService.update(pet)
    return send_ok()


@api_exception_handler
@roles_required(['MANAGER'])
def move_pet(pet_id):
    data = request.json
    errors = move_pet_request_schema.validate(data)
    if errors:
        raise ErrValidation(errors)
    new_room_id = int(data["new_room_id"])
    pet = PetService.get_by_id(pet_id)
    if pet is None:
        raise ErrPetNotFound()
    if PetService.get_by_room_id(new_room_id) is not None:
        raise ErrRoomIsFull()
    pet.room_id = new_room_id
    PetService.update(pet)
    return send_ok()


@api_exception_handler
@roles_required(['CUSTOMER', 'MANAGER'])
def delete_pet(pet_id):
    curr_user = get_current_user()
    pet = PetService.get_by_id(pet_id)
    if pet is None:
        raise ErrPetNotFound()
    if curr_user.is_customer and pet.is_checked_in():
        raise ErrForbidden("You can not delete a pet that is checked-in")
    PetService.delete_by_id(pet_id)
    return send_ok()
