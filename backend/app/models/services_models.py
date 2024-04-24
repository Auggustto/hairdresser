import logging
from flask import jsonify
from datetime import datetime

from app.models.database.db import session, Services




class ServicerManager:

    def filter_service(self, service):
        try:
            return session.query(Services).filter_by(name_service=service).first()

        
        except Exception as e:
            logging.error(f"Error filtering user: {e}")
            raise


    def create(self, name_service, description, price, duration):
        try:
            check_service = self.filter_service(name_service)

            if check_service:
                return jsonify({"error": f"E-mail {id} is already in use!"}), 400
            else:
                new_service = Services(name_service=name_service, description=description, price=price, duration=duration)
                session.add(new_service)
                session.commit()

                return {"message": "Service created successfully!"}, 201
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating user: {e}")
            return e, 500
    

    def read(self, name_service):
        try:
            check_service = self.filter_service(name_service)

            if check_service:
                return {
                    "name_service": check_service.name_service,
                    "description":check_service.description,
                    "price":check_service.price,
                    "duration":check_service.duration.strftime("%H:%M")
                    }, 200
            
            return {"error": f"Service {name_service} not found."}, 500
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating user: {e}")
            return e, 500


    def update(self, name_service, description, price, duration):
        try:
            check_service = self.filter_service(name_service)

            if check_service:
                check_service.name_service = name_service
                check_service.description = description
                check_service.price = price
                check_service.duration = duration

                session.commit()

                return {"message": "Service updated successfully!"}, 200
            
            return {"error": f"Service {name_service} not found."}, 500
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating user: {e}")
            return str(e), 500


    def delete(self, name_service):
        try:
            check_service = self.filter_service(name_service)

            if check_service:
                session.delete(check_service)
                session.commit()

                return {"message": f"User {name_service} deleted successfully!"}, 200
            
            return {"error": f"User: {name_service} not found!"}, 404
        
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting user: {e}")
            return str(e), 500