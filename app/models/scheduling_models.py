import logging
from flask import jsonify

from app.models.database.db import Scheduling, session
from app.models.users_models import UserManager
from app.models.hairdressers_models import HairdressersManager
from app.models.services_models import ServicerManager


class SchedulingManager:

    def filter_user_hairdressers(self, user_email, hairdressers_email, name_service):
        try:
            user = UserManager()
            users = user.filter_user(user_email)

            hairdresser = HairdressersManager()
            hairdressers = hairdresser.filter_hairdressers(hairdressers_email, 1)

            service = ServicerManager()
            services = service.filter_service(name_service)

            return users, hairdressers, services
        
        except Exception as e:
            logging.error(f"Error filter user and hairdressers: {e}")
            return jsonify({"error": str(e)}), 500
        


    def filter_scheduling(self, scheduling_id):
        try:
            return session.query(Scheduling).filter_by(id=scheduling_id).first()
        
        except Exception as e:
            logging.error(f"Error filtering user: {e}")
            return jsonify({"error": str(e)}), 500 


    def create(self, user_email, hairdressers_email, name_service, date_service, hour_obj):
        try:
            users, hairdressers, services = self.filter_user_hairdressers(user_email, hairdressers_email, name_service)

            new_scheduling = Scheduling(
                client_id=users.id,
                hairdresser_id=hairdressers.id,
                service_id=services.id,
                date=date_service,
                time=hour_obj
            )
            session.add(new_scheduling)
            session.commit()

            return jsonify({"message": "Service created successfuly."}), 201

        except Exception as e:
            logging.error(f"Error filtering user: {e}")
            return jsonify({"error": str(e)}), 500
    
    def read(self, schedulin_id):
        try:
            check_scheduling = self.filter_scheduling(schedulin_id)

            if check_scheduling:
                return {
                    "client": check_scheduling.client_id,
                    "hairdresser": check_scheduling.hairdresser_id,
                    "service":check_scheduling.service_id,
                    "date": check_scheduling.date,
                    "time":check_scheduling.time.strftime("%H:%M")
                    }, 200
            
            return jsonify({"error": f"Service {schedulin_id} not found."}), 500
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating user: {e}")
            return jsonify({"error": str(e)}), 500


    def update(self, scheduling_id, user_email, hairdressers_email, name_service, date_service, hour_obj):
        try:
            check_scheduling = self.filter_scheduling(scheduling_id)
            users, hairdressers, services = self.filter_user_hairdressers(user_email, hairdressers_email, name_service)

            if check_scheduling:
                check_scheduling.client_id = users.id
                check_scheduling.hairdresser_id = hairdressers.id
                check_scheduling.service_id = services.id
                check_scheduling.date = date_service
                check_scheduling.time = hour_obj

                session.commit()

                return jsonify({"message": "Service updated successfully!"}), 200
            
            return jsonify({"error": f"Service {name_service} not found."}), 500
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating user: {e}")
            return jsonify({"error": str(e)}), 500


    def delete(self, scheduling_id):
        try:
            check_scheduling = self.filter_scheduling(scheduling_id)

            if check_scheduling:
                session.delete(check_scheduling)
                session.commit()

                return jsonify({"message": f"Service {scheduling_id} deleted successfully!"}), 200
            
            return jsonify({"error": f"Service: {scheduling_id} not found!"}), 404
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting user: {e}")
            return jsonify({"error": str(e)}), 500

