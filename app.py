from flask import Flask
from flask_restful import Api
from resources.application import Application, ApplicationList
import database

app = Flask(__name__)
api = Api(app)


api.add_resource(ApplicationList, '/applications')
api.add_resource(Application, '/application/<app_id>','/application')

database.initialize_db()

 

if __name__ == '__main__':
    app.run(debug=True)