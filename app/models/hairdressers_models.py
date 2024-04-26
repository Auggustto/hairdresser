import logging
from flask import jsonify
from datetime import datetime
import json
import bcrypt
from flask_jwt_extended import create_access_token

from app.services.hash import hash
from app.models.database.db import session, Hairdressers


class HairdressersManager:

    def hash_password(self, password):
        return hash(password)



    def filter_hairdressers(self, email, type_read):
        try:
            if type_read == 0:
                return session.query(Hairdressers).filter_by(email=email).first()
            elif type_read == 1:
                return session.query(Hairdressers).filter_by(email_acess=email).first()
        
        except Exception as e:
            logging.error(f"Error filtering user: {e}")
            return str(e), 500



    def jwt_token_acess(self, email):
        token_acess = create_access_token(identity=email)

        return token_acess



    def create(self, name, email, email_acess, specialization, start_working_hours, end_of_office, password):
        try:
            check_hairdressers = self.filter_hairdressers(email, 0)

            if check_hairdressers:
                return jsonify({"error": f"E-mail {email} is already in use!"}), 400

            start_working_hours = datetime.strptime(start_working_hours, '%H:%M').time()
            end_of_office = datetime.strptime(end_of_office, '%H:%M').time()
            specialization = json.dumps([specialization])
            
            new_hairdressers = Hairdressers(
                name=name, 
                email=email,
                email_acess=email_acess,
                specialization=specialization, 
                start_working_hours=start_working_hours, 
                end_of_office=end_of_office,
                password=self.hash_password(password)
                )
            session.add(new_hairdressers)
            session.commit()

            return {"message": "Hairdressers created successfully!"}, 201
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating user: {e}")
            return e, 500



    def read(self, email):
        try:
            check_hairdressers = self.filter_hairdressers(email, 1)

            if check_hairdressers:

                start_working_hours_str = check_hairdressers.start_working_hours.strftime("%H:%M:%S")
                end_of_office_str = check_hairdressers.end_of_office.strftime("%H:%M:%S")

                return jsonify({
                    "id": check_hairdressers.id,
                    "name": check_hairdressers.name,
                    "email_acess": check_hairdressers.email_acess,
                    "specialization": check_hairdressers.specialization,
                    "start_working_hours": start_working_hours_str,
                    "end_of_office": end_of_office_str
                    }), 200
            else:
                return jsonify({"error": f"E-mail {email} not found!"}), 400
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating user: {e}")
            return e, 500



    def update(self, name, email, specialization, start_working_hours, end_of_office, password):
        try:
            check_hairdressers = self.filter_hairdressers(email, 1)
            print(check_hairdressers)

            if check_hairdressers:

                start_working_hours = datetime.strptime(start_working_hours, '%H:%M').time()
                end_of_office = datetime.strptime(end_of_office, '%H:%M').time()
                specialization = json.dumps([specialization])


                check_hairdressers.name = name
                check_hairdressers.specialization = specialization
                check_hairdressers.start_working_hours = start_working_hours
                check_hairdressers.end_of_office = end_of_office
                check_hairdressers.password = self.hash_password(password)

                session.commit()

                return {"message": "Hairdressers updated successfully!"}, 200
            
            return {"error": f"E-mail {email} not found."}, 500
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating user: {e}")
            return str(e), 500



    def delete(self, email):
        try:
            check_hairdressers = self.filter_hairdressers(email, 1)

            if check_hairdressers:
                session.delete(check_hairdressers)
                session.commit()

                return {"message": f"User {email} deleted successfully!"}, 200
            
            return {"error": f"User: {email} not found!"}, 404
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting user: {e}")
            return str(e), 500
        
    

    def login(self, email, password):
        try:
            read_user = self.filter_hairdressers(email, 1)

            if read_user:
                if read_user.email and bcrypt.checkpw(password.encode('utf-8'), read_user.password):

                    token = self.jwt_token_acess(read_user.id)

                    return jsonify({"acess_token": str(token)}), 200
                
            return jsonify({"error": "Incorrect e-mail or password"}), 400
        
        except Exception as e:
            return jsonify({"error": str(e)})
