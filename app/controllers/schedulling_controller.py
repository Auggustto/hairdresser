import logging
from flask import jsonify, request
from datetime import datetime

from app.models.scheduling_models import SchedulingManager


class SchedulingController:

    def get_metadata(self):
        user_email = request.json.get("user_email")
        hairdressers_email = request.json.get("hairdressers_email")
        name_service = request.json.get("name_service")
        date_service = request.json.get("date_service")
        hour = request.json.get("hour")

        return user_email, hairdressers_email, name_service, date_service, hour
            
    
    def create_scheduling(self):
        user_email, hairdressers_email, name_service, date_service, hour = self.get_metadata()

        if not all([user_email, hairdressers_email, name_service, date_service, hour]):
            return jsonify({"error": "All fields are required"}), 400
        else:
            try:
                date_obj = datetime.strptime(date_service, '%d/%m/%Y')
                hour_obj = datetime.strptime(hour, '%H:%M').time()

                new_schedulin = SchedulingManager()
                return new_schedulin.create(user_email, hairdressers_email, name_service, date_obj, hour_obj)
            
            except Exception as e:
                logging.error(f"Error crate scheduling: {e}")
                return jsonify({"error": str(e)}), 500
                

    def read_scheduling(self, schedulin_id):
        if not all([schedulin_id]):
            return jsonify({"error": "Field schedulin_id id are required"}), 400
        try:
            service = SchedulingManager()
            return service.read(schedulin_id)
        
        except Exception as e:
            logging.error(f"Error read: {e}")
            return jsonify({"error": str(e)}), 500
        
    
    def update_scheduling(self, scheduling_id):
        try:
            user_email, hairdressers_email, name_service, date_service, hour = self.get_metadata()

            if not all([user_email, hairdressers_email, name_service, date_service, hour]):
                return jsonify({"error": "All fields are required"}), 400
            else:
                hour_obj = datetime.strptime(hour, '%H:%M').time()
                date_obj = datetime.strptime(date_service, '%d/%m/%Y')

                service = SchedulingManager()
                return service.update(scheduling_id, user_email, hairdressers_email, name_service, date_obj, hour_obj)
        
        except Exception as e:
            logging.error(f"Error update scheduling: {e}")
            return jsonify({"error": str(e)}), 500
        

    def delete_scheduling(self, check_scheduling):
        try:
            scheduling = SchedulingManager()
            return scheduling.delete(check_scheduling)
            
        except Exception as e:
            logging.error(f"Error delete scheduling: {e}")
            return jsonify({"error": str(e)}), 500
