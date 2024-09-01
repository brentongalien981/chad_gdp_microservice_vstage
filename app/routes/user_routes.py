from flask import Blueprint
from app.controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)

user_bp.route('/', methods=['GET'])(UserController.get_all_users)
user_bp.route('/', methods=['POST'])(UserController.create_user)
