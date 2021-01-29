from flask import Blueprint

BASE_ROUTE = "/pets"


def create_bp():
    from .controller import creat_pet
    from .controller import edit_pet
    from .controller import get_pets
    from .controller import delete_pet
    from .controller import check_in
    from .controller import check_out
    from .controller import move_pet

    bp = Blueprint("pet", __name__)
    bp.add_url_rule(f'{BASE_ROUTE}', view_func=creat_pet, methods=["POST"])
    bp.add_url_rule(f'{BASE_ROUTE}', view_func=edit_pet, methods=["PUT"])
    bp.add_url_rule(f'{BASE_ROUTE}/<string:pet_id>/check-in', view_func=check_in, methods=["POST"])
    bp.add_url_rule(f'{BASE_ROUTE}/<string:pet_id>/check-out', view_func=check_out, methods=["POST"])
    bp.add_url_rule(f'{BASE_ROUTE}/<string:pet_id>/move', view_func=move_pet, methods=["post"])
    bp.add_url_rule(f'{BASE_ROUTE}', view_func=get_pets, methods=["GET"])
    bp.add_url_rule(f'{BASE_ROUTE}/<string:pet_id>', view_func=delete_pet, methods=["DELETE"])
    return bp
