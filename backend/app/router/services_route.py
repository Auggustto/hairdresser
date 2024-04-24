from flask import json, request, jsonify, render_template 
from app import app
from flask_jwt_extended import jwt_required

from app.controllers.services_controller import ServicesController

@app.route('/services/register', methods=["POST"])
@jwt_required()
def create_services():
    login = ServicesController()
    return login.create_service()


@app.route('/services/<string:service>', methods=["GET"])
def read_service(name_service):
    service  = ServicesController()
    return service.read(name_service)


@app.route('/services/<string:service>', methods=["PUT"])
@jwt_required()
def update_service(name_service):
    service = ServicesController()
    return service.update(name_service)


@app.route('/services/<string:name_service>', methods=["DELETE"])
@jwt_required()
def delete_service(name_service):

    service = ServicesController()
    return service.delete(name_service)
