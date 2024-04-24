from flask import json, request, jsonify, render_template
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

from app import app
from app.controllers.login.login_controller import LoginController


@app.route('/', methods=["POST"])
def login():
    login = LoginController()
    return login.login()


@app.route('/login/recovery', methods=["POST"])
def recovery():
    recovery = LoginController()
    return recovery.recovery_acess()


@app.route('/login/token-validation', methods=["POST"])
def acess_token_validation():
    validation = LoginController()
    return validation.acess_token_validation()


@app.route('/login/new-password', methods=["POST"])
def new_passwords():
    password = LoginController()
    return password.new_password()