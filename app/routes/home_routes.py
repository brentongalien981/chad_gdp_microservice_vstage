from flask import Blueprint
from app.controllers.home_controller import HomeController

home_bp = Blueprint("home", __name__)

home_bp.route("/", methods=["GET"])(HomeController.home)
home_bp.route("/get_my_info", methods=["GET"])(HomeController.get_my_info)
home_bp.route("/chat", methods=["POST"])(HomeController.chat)

home_bp.route("/generate_image", methods=["POST"])(HomeController.generate_image)
