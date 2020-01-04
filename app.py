from flask import Flask
from celery import Celery
from flask_restful import Api
from resources.application import Application, ApplicationList
import database

app = Flask(__name__)
api = Api(app)

app.config.from_object('config')

api.add_resource(ApplicationList, '/applications')
api.add_resource(Application, '/application/<app_id>','/application')

database.initialize_db()


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL']
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = make_celery(app)


if __name__ == '__main__':
    app.run(debug=True)