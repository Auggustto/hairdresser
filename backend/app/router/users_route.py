from flask_jwt_extended import jwt_required

from app import app
from app.controllers.users.user_controller import UserController


@app.route('/users/register', methods=["POST"])
def create_user():

    user  = UserController()
    return user.create_user()


@app.route('/users/<string:email>', methods=["GET"])
@jwt_required()
def read_user(email):

    user  = UserController()
    return user.read(email)


@app.route('/users/<string:email>', methods=["PUT"])
@jwt_required()
def update_user(email):

    user  = UserController()
    return user.update(email)


@app.route('/users/<string:email>', methods=["DELETE"])
@jwt_required()
def delete_user(email):

    user = UserController()
    return user.delete(email)

