from flask import jsonify, request
from datetime import datetime
import random

from app.models.hairdressers.hairdressers_models import HairdressersManager
from app.services.email_hairdressers import send_email



class HairdressersController:

    def get_metadata(self):
        name = request.json.get("name")
        email = request.json.get("email")
        email_acess = request.json.get("email_acess")
        specialization = request.json.get("specialization")
        start_working_hours = request.json.get("start_working_hours")
        end_of_office = request.json.get("end_of_office")
        password = request.json.get("password")

        return name, email, email_acess, specialization, start_working_hours, end_of_office, password


    def create_hairdressers(self):
        name, email, _, specialization, start_working_hours, end_of_office, _ = self.get_metadata()

        if not all([name, specialization, start_working_hours, end_of_office]):
            return jsonify({"error": "All fields are required"}), 400
        else:
            try:
                code = str(random.randint(100, 600))
                sep_name = name.split(" ")

                email_acess = sep_name[0].lower() + "hairdressers" + code + "@domain.com"
                password = f"{sep_name[0]}@{random.randint(1000000, 60000000)}"

                print("-"*90)
                print(specialization)

                new_hairdressers = HairdressersManager()
                hairdressers = new_hairdressers.create(name, email, email_acess, specialization, start_working_hours, end_of_office, password)

                if hairdressers[1] == 201:
                    send_email(email, email_acess, password)

                    return hairdressers
                return hairdressers
            
            except Exception as e:
                return {"error": str(e)}, 500
    

    def read_hairdressers(self, email):

        if not all(email):
            return jsonify({"error": "email_acess are required"}), 400
        else:
            try:
                hairdressers = HairdressersManager()
                return hairdressers.read(email)
            except Exception as e:
                return {"error": str(e)}, 500
    
    def update_hairdressers(self, email):

        name, _, _, specialization, start_working_hours, end_of_office, password= self.get_metadata()

        if not all([name, specialization, start_working_hours, end_of_office, password]):
            return jsonify({"error": "email_acess are required"}), 400
        else:
            try:
                hairdressers = HairdressersManager()
                return hairdressers.update(name, email, specialization, start_working_hours, end_of_office, password)
            except Exception as e:
                return {"error": str(e)}, 500


    def  delete_hairdressers(self, email):
        if not all(email):
            return jsonify({"error": "email_acess are required"}), 400
        else:
            try:
                hairdressers = HairdressersManager()
                return hairdressers.delete(email)
            except Exception as e:
                return {"error": str(e)}, 500
            


    def login(self):

        email = request.json.get("email")
        password = request.json.get("password")

        if not all([email, password]):
            return jsonify({"error": "All fields are required"}), 400
        
        try:
            user = HairdressersManager()
            return user.login(email, password)
        
        except Exception as e:
            return jsonify({"error": str(e)})
