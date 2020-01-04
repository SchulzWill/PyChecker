from flask_restful import Resource
from flask import request, json, jsonify

class HealthCheck(Resource):
   
    def get(self):
        return {'status':'ok'},200