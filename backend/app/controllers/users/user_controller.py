from flask import jsonify, request
from datetime import datetime

from app.models.user.users_models import UserManager
from app.services.hash import hash
from app.services.telephone import format_telephone


class UserController:

    def get_metadata(self):
        name = request.json.get("name")
        lastname = request.json.get("lastname")
        telephone = request.json.get("telephone")
        birthdata = request.json.get("birthdata")
        email = request.json.get("email")
        password = request.json.get("password")

        return name, lastname, telephone, birthdata, email, password
            
    
    def create_user(self):
        name, lastname, telephone, birthdata, email, password = self.get_metadata()

        if not all([name, lastname, telephone, birthdata, email, password]):
            return jsonify({"error": "All fields are required"}), 400
        else:
            try:
                birthdata_obj = datetime.strptime(birthdata, '%d/%m/%Y')
                date = birthdata_obj.date()

                new_user = UserManager()
                return new_user.create(name, lastname, format_telephone(telephone), date, email, hash(password))
            
            except Exception as e:
                return {"error": str(e)}, 500
                

    def read(self, email):

        if not all(email):
            return jsonify({"error": "Field email are required"}), 400
        try:
            user = UserManager()
            return user.read(email)
        
        except Exception as e:
            return jsonify({"error": str(e)})
        
    
    def update(self, user_email):
        try:
            name, lastname, telephone, birthdata, email, password = self.get_metadata()

            if not all([name, lastname, telephone, birthdata, email, password]):
                return jsonify({"error": "All fields are required"}), 400
            else:
                birthdata_obj = datetime.strptime(birthdata, '%d/%m/%Y')

                user = UserManager()
                return user.update(user_email, name, lastname, telephone, birthdata_obj, email, hash(password))
        
        except Exception as e:
            return jsonify({"error": str(e)})
        
    
    def delete(self, email):
        try:
            print(email)
            user = UserManager()
            return user.delete(email)
            
        except Exception as e:
            return jsonify({"error": str(e)})