from flask import jsonify
from app.models.database.db import session
import bcrypt
import logging
from flask_jwt_extended import create_access_token

from app.models.users_models import UserManager
from app.services.email import send_email
from app.services.hash import hash


class LoginManager:

    def jwt_token_acess(self, email):

        user = UserManager()
        read_user = user.filter_user(email)
        
        token_acess = create_access_token(identity=read_user.id)

        return token_acess


    def login(self, email, password):
        try:
            user = UserManager()
            read_user = user.filter_user(email)

            if read_user:

                if read_user.email and bcrypt.checkpw(password.encode('utf-8'), read_user.password):
                    
                    token = self.jwt_token_acess(read_user.email)

                    return jsonify({"acess_token": str(token)}), 200
                
            return jsonify({"error": "Incorrect e-mail or password"}), 400
        
        except Exception as e:
            return jsonify({"error": str(e)})
        
    
    def recovery_acess(self, email, recovery_code):
        try:
            send_email(email, recovery_code)

            print('email', email, "recovery_code", recovery_code)

            return jsonify({"mensage": "E-mail send sucessfully."}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 404


    def new_password(self, email, password):
        try:
            user = UserManager()
            select_user = user.filter_user(email)

            print(password)

            if select_user:
                select_user.password = hash(password)
                session.commit()

                print("Aqui")

                return jsonify({"message": "Password updated successfully!"}), 200
            
            return jsonify({"error": f"E-mail {email} not found."}), 500
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating user: {e}")
            return str(e), 500
