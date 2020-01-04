from flask_restful import Resource
from flask import request, json, jsonify
from resources.processor import Processor, create_schedule_for_application
import database
import logging

class ApplicationList(Resource):
    def get(self):
        applications = database.select("select * from application")
        return jsonify(applications)


class Application(Resource):
    def get(self, app_id):
        application = database.select("select * from application where id={0}".format(app_id))
        return jsonify(application)
    
    def post(self):
        json_data = request.get_json(force=True)
        
        if not json_data:
            return {'message': 'No input data provided'}, 400

        name = request.json.get('name')
        check_interval = request.json.get('check_interval')
        check_data = request.json.get('check_data')
        expected_json = request.json.get('expected')
        http_notification_json = request.json.get('http_notification')
        

        command = """
        INSERT INTO application
            ("name","check_interval","check_data","expected","http_notification") 
            VALUES ('{0}',{1},'{2}','{3}', '{4}');
        """.format(name, check_interval, json.dumps(check_data), json.dumps(expected_json), json.dumps(http_notification_json))

        app_id = database.insert(command)
        job = create_schedule_for_application(app_id, check_interval)
        return {'status':'success', 'job_id': job.id}, 200
    
    def put(self, app_id):
        json_data = request.get_json(force=True)
        
        if not json_data:
            return {'message': 'No input data provided'}, 400
        
        name = request.json.get('name')
        check_interval = request.json.get('check_interval')
        check_data = request.json.get('check_data')
        expected_json = request.json.get('expected')
        http_notification_json = request.json.get('http_notification')
        

        command = """
        UPDATE "application"
            SET "name" = '{0}', 
            "check_interval"={1},
            "check_data"='{2}',
            "expected"='{3}',
            "http_notification"='{4}'
            WHERE "id" = {5} ;
        """.format(name, check_interval, json.dumps(check_data), json.dumps(expected_json), json.dumps(http_notification_json), app_id)

        database.update(command)
        return {'status':'success'}, 204

    def delete(self, app_id):
        command = "DELETE FROM application WHERE id ={0}".format(app_id)
        database.update(command)
        return {'status':'success'}, 204


