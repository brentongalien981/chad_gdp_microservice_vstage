from flask import jsonify, request
from app.models.user_model import User
from app import db
from typing import Tuple

class UserController:

    @staticmethod
    def get_all_users() -> Tuple[dict, int]:
        users = User.query.all()
        return jsonify([user.__dict__ for user in users]), 200

    @staticmethod
    def create_user() -> Tuple[dict, int]:
        data = request.get_json()
        new_user = User(name=data.get('name'), email=data.get('email'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.__dict__), 201
