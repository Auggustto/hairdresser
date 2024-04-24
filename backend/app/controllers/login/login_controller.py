from flask import jsonify, request, session
import random
import datetime
import uuid

from app.models.login.login_models import LoginManager
from app.services.email import send_email


class LoginController:

    def login(self):

        email = request.json.get("email")
        password = request.json.get("password")

        if not all([email, password]):
            return jsonify({"error": "All fields are required"}), 401
        
        try:
            user = LoginManager()
            return user.login(email, password)
        
        except Exception as e:
            return jsonify({"error": str(e)})
        
    
    def recovery_acess(self):

        email = request.json.get("email")

        if not all(email):
            return jsonify({"error": "E-mail are required"}), 400
        try:
            recovery_code = str(random.randint(1000000, 60000000))
            recovery_code_expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)

            # Store data in the session
            session['recovery_code'] = recovery_code
            session['user_email'] = email
            session['recovery_code_expiration'] = recovery_code_expiration
            session['session_id'] = str(uuid.uuid4())

            session.modified = True

            return send_email(email, recovery_code)
        
        except Exception as e:
            return jsonify({"error": str(e)})
        
    
    def acess_token_validation(self):

        token = request.json.get("token")

        if not all(token):
            return jsonify({"error": "Token are required"}), 400

        if session.get("recovery_code") == str(token):
            return jsonify({"message": "Token Ok"}), 200
        return jsonify({"error": "Token expired!"}), 500
    
    
    def new_password(self):

        email = request.json.get("email")
        password = request.json.get("password")

        
        if not all(password):
            return jsonify({"error": "Password are required"}), 400
        
        try:
            if session.get("user_email") == email:
                # return {"teste": "teste", "email": email, "password": password}
                new_password = LoginManager()
                return new_password.new_password(email, password)
            
        except Exception as e:
            return jsonify({"error": str(e)})
