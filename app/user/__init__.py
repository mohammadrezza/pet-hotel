from flask import Blueprint

BASE_ROUTE = "/users"


def create_bp():
    from .controller import login
    from .controller import invite
    from .controller import register
    from .controller import create_staff
    from .controller import get_user
    from .controller import update_status

    bp = Blueprint("user", __name__)
    bp.add_url_rule(f'{BASE_ROUTE}/login', view_func=login, methods=["POST"])
    bp.add_url_rule(f'{BASE_ROUTE}/invite', view_func=invite, methods=["POST"])
    bp.add_url_rule(f'{BASE_ROUTE}/register', view_func=register, methods=["POST"])
    bp.add_url_rule(f'{BASE_ROUTE}/staff', view_func=create_staff, methods=["POST"])
    bp.add_url_rule(f'{BASE_ROUTE}', view_func=get_user, methods=["GET"])
    bp.add_url_rule(f'{BASE_ROUTE}/<string:customer_id>/status', view_func=update_status, methods=["PATCH"])
    return bp
