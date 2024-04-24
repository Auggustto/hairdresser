import logging
from flask import jsonify, request
from datetime import datetime

from app.models.services_models import ServicerManager


class ServicesController:

    def get_metadata(self):
        name_service = request.json.get("name_service")
        description = request.json.get("description")
        price = request.json.get("price")
        duration = request.json.get("duration")

        return name_service, description, price, duration
            
    
    def create_service(self):
        name_service, description, price, duration = self.get_metadata()

        if not all([name_service, description, price, duration]):
            return jsonify({"error": "All fields are required"}), 400
        else:
            try:
                duration_obj = datetime.strptime(duration, '%H:%M').time()

                new_service = ServicerManager()
                return new_service.create(name_service, description, price, duration_obj)
            
            except Exception as e:
                return {"error": str(e)}, 500
                

    def read(self, name_service):
        # print(name_service)
        
        if not all(name_service):
            return jsonify({"error": "Field name_service are required"}), 400
        try:
            service = ServicerManager()
            return service.read(name_service)
        
        except Exception as e:
            return jsonify({"error": str(e)})
        
    
    def update(self, name_service):
        try:
            _, description, price, duration = self.get_metadata()

            if not all([name_service, description, price, duration]):
                return jsonify({"error": "All fields are required"}), 400
            else:
                duration_obj = datetime.strptime(duration, '%H:%M').time()

                service = ServicerManager()
                return service.update(name_service, description, price, duration_obj)
        
        except Exception as e:
            return jsonify({"error": str(e)})
        
    
    def delete(self, name_service):
        try:
            services = ServicerManager()
            return services.delete(name_service)
            
        except Exception as e:
            return jsonify({"error": str(e)})
