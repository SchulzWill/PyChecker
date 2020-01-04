from flask_restful import Resource
from flask import request, json, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import database
import datetime
import logging
import requests

scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/London'})
scheduler.add_jobstore('sqlalchemy', url="sqlite:///{0}".format(database.DATABASE))
scheduler.start()

def create_schedule_for_application(app_id, check_interval):
    try:
        job = scheduler.add_job(ping_application, 'interval', seconds=check_interval, args=[app_id], name="ping_application_id_{0}".format(app_id))
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    return job

def ping_application(app_id):
    application = database.select("select * from application where id={0}".format(app_id))[0]
    if application['check_data'] is not None:
        check_data = eval(application['check_data'])
        try:
            headers = check_data['headers'] if check_data.get('headers') is not None else ''
            if check_data['method'] == 'GET' or check_data['method'] == 'get':
                
                result = requests.request(check_data['method'], url=check_data['endpoint'], headers=headers)
            else:
                body = str(check_data['body']) if check_data['body'] is not None else ''
                result = requests.request(check_data['method'], url=check_data['endpoint'], headers=headers, data = body)
            
            compare_result(application['name'], application['expected'], result)
        except Exception as e:
            error_description = "Failed to contact application {0}".format(application['name'])
            logging.error("{0}, will notify mantainer".format(error_description))

            notify_mantainer(application['name'], error_description, application['http_notification'])
    return

def compare_result(app_name, expectation, call_result):
    error_count = 0
    right_count = 0

    if expectation is not None:
        expected_result = eval(expectation)
        
        if expected_result.get('code') is not None:
            if call_result.status_code != int(expected_result['code']):
                logging.info("{0} - Obtained result code is {1} and expected was {2}".format(app_name, call_result.status_code, expected_result.get('code')))
                error_count+=1
            else:
                right_count+=1
        
        if expected_result.get('headers') is not None and str(expected_result['headers']) != '':
            expected_headers = set(expected_result.get('headers'))
            received_headers = set(call_result.headers)
            if bool(set(expected_result.get('headers')) & set(call_result.headers)) is not True:
                logging.info("{0} - Obtained headers are {1} and expected was {2}".format(app_name, received_headers, expected_headers))
                error_count+=1
            else:
                right_count+=1
        else:
            right_count+=1

        if expected_result.get('body') is not None and str(expected_result['body']) != '':
            expected_body = set(expected_result.get('body'))
            received_body = set(call_result.get_json())
            if bool(set(expected_result.get('headers')) & set(call_result.headers)) is not True:
                logging.info("{0} - Obtained body is {1} and expected was {2}".format(app_name, received_body, expected_body))
                error_count+=1
            else:
                right_count+=1
        else:
            right_count+=1

        if error_count > right_count:
            error_description = "Failed to compare result of check application {0}".format(app_name)
            logging.error("{0}, will notify mantainer".format(error_description))
        
        return

def notify_mantainer(app_name, error_description, channel):
    http_notification = eval(channel)
    try:
        body = http_notification['body']
        body['description'] = error_description
        body['service'] = app_name
        result = requests.request(http_notification['method'], url=http_notification['endpoint'], headers=http_notification['headers'], data = body)
        if result.status_code != 200:
            logging.error("Failed to notify mantainer on {0}, received response {1} {2}".format(http_notification['endpoint'], result.status_code, result.text))
    except Exception as e:
        logging.error("Failed to notify mantainer on {0}".format(http_notification['endpoint']), exc_info=True)
    return

class Processor(Resource):
    def get(self):
        jobs = scheduler.get_jobs()
        job_state = []
        
        for job in jobs:
            job_state.append([job.id, job.name, job.next_run_time])

        return jsonify(job_state)
    
    def delete(self, job_id):
        scheduler.remove_job(job_id)
        return {'status':'success'}