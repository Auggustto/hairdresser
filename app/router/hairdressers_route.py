from app import app
from flask_jwt_extended import jwt_required

from app.controllers.hairdressers_controller import HairdressersController

@app.route('/hairdressers/register', methods=["POST"])
def create_hairdressers():

    new_hairdressers = HairdressersController()
    return new_hairdressers.create_hairdressers()
    

@app.route('/hairdressers/<string:email>', methods=["GET"])
@jwt_required()
def read_hairdressers(email):

    read_hairdresser = HairdressersController()
    return read_hairdresser.read_hairdressers(email)


@app.route('/hairdressers/<string:email>', methods=["PUT"])
@jwt_required()
def update_hairdressers(email):

    update_hairdressers  = HairdressersController()
    return update_hairdressers.update_hairdressers(email)


@app.route('/hairdressers/<string:email>', methods=["DELETE"])
@jwt_required()
def delete_hairdressers(email):

    delete_hairdressers = HairdressersController()
    return delete_hairdressers.delete_hairdressers(email)


@app.route('/hairdressers/login', methods=["POST"])
def login_hairdressers():

    login_hairdresser = HairdressersController()
    return login_hairdresser.login()