from flask import request, render_template 
from app import app
from flask_jwt_extended import jwt_required

from app.controllers.schedulling_controller import SchedulingController


@app.route('/scheduling/register', methods=["POST"])
@jwt_required()
def create_scheduling():
    scheduling  = SchedulingController()
    return scheduling.create_scheduling()


@app.route('/scheduling/<int:schedulin_id>', methods=["GET"])
@jwt_required()
def read_schedulin(schedulin_id):
    scheduli_id  = SchedulingController()
    return scheduli_id.read(schedulin_id)


@app.route('/scheduling/<int:schedulin_id>', methods=["PUT"])
@jwt_required()
def update_schedulin(schedulin_id):
    schedulin  = SchedulingController()
    return schedulin.update(schedulin_id)


@app.route('/scheduling/<int:check_scheduling>', methods=["DELETE"])
@jwt_required()
def delete_scheduling(check_scheduling):

    scheduling = SchedulingController()
    return scheduling.delete(check_scheduling)

