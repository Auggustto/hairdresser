import logging
from flask import jsonify

from app.models.database.db import session, User
from app.services.hash import hash



class UserManager:

    def hash_password(self, password):
        return hash(password)

    def filter_user(self, email):
        try:
            return session.query(User).filter_by(email=email).first()
        
        except Exception as e:
            logging.error(f"Error filtering user: {e}")
            raise


    def create(self, name, lastname, telephone, birthdata, email, password):
        try:
            check_user = self.filter_user(email)

            if check_user:
                return jsonify({"error": f"E-mail {email} is already in use!"}), 400
            
            new_user = User(name=name, lastname=lastname, telephone=telephone, birthdata=birthdata, email=email, password=password)
            session.add(new_user)
            session.commit()

            return jsonify({"message": "User created successfully!"}), 201
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating user: {e}")
            return e, 500
    

    def read(self, email):
        try:
            check_user = self.filter_user(email)
            
            if check_user:
                return {
                    "name": check_user.name,
                    "lastname":check_user.lastname,
                    "telephone": check_user.telephone,
                    "birthdata":check_user.birthdata.strftime("%d/%m/%Y"),
                    "email":check_user.email
                    }, 200
            
            return {"error": f"E-mail {email} not found."}, 500
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating user: {e}")
            return e, 500


    def update(self, user_email, name, lastname, telephone, birthdata, email, password):
        try:
            check_user = self.filter_user(user_email)

            if check_user:
                check_user.name = name
                check_user.lastname = lastname
                check_user.telephone = telephone
                check_user.birthdata = birthdata
                check_user.email = email
                check_user.password = password

                session.commit()

                return {"message": "User updated successfully!"}, 200
            
            return {"error": f"E-mail {email} not found."}, 500
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating user: {e}")
            return str(e), 500


    def delete(self, email):
        try:
            check_user = self.filter_user(email)

            if check_user:
                session.delete(check_user)
                session.commit()

                return {"message": f"User {email} deleted successfully!"}, 200
            
            return {"error": f"User: {email} not found!"}, 404
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting user: {e}")
            return str(e), 500