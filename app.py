from flask import Flask
from datetime import datetime
from flask_restful import Api
from resources.application import Application, ApplicationList
from resources.processor import Processor
from resources.healthcheck import HealthCheck
import database
import logging

app = Flask(__name__)

database.initialize_db()

api = Api(app)
api.add_resource(ApplicationList, '/applications')
api.add_resource(Application, '/application/<app_id>','/application')
api.add_resource(Processor, '/processor', '/processor/<job_id>')
api.add_resource(HealthCheck, '/check')

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Application started")

if __name__ == '__main__':
    app.run()