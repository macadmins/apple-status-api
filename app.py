import json
import urllib
import requests
from chalice import Chalice
from urllib.parse import quote


app = Chalice(app_name='apple-system-status')

service_classes = {}

devjson = requests.get("https://www.apple.com/support/systemstatus/data/developer/system_status_en_US.js").text.split("(")[1].split(")")[0]
service_classes['dev'] = json.loads(devjson)['services']

prodjson = requests.get("https://www.apple.com/support/systemstatus/data/system_status_en_US.js").text
service_classes['prod'] = json.loads(prodjson)['services']

@app.route('/services')
def get_services():

    result = []

    for _, servicekeys in service_classes.items():
        for service in servicekeys:
            serviceName = service.get('serviceName')
            result.append(serviceName)

    return json.dumps(result)

@app.route('/service/{name}')
def get_service(name):

    result = {}

    for _, servicekeys in service_classes.items():
        for service in servicekeys:
            if urllib.parse.unquote(name) in service['serviceName']:
                result = service

    return json.dumps(result)

@app.route('/service/{name}/{status}')
def get_service_status(name, status):

    result = {}
    down_status_list = ['']
    up_status_list = ['resolved', 'completed']

    for _, servicekeys in service_classes.items():
        for service in servicekeys:
            if urllib.parse.unquote(name) in service['serviceName']:
                eventStatus = service['events'][0]['eventStatus']
                if 'up' in status:
                    if len(service['events']) == 0:
                        result = True
                    elif len(service['events']) > 0:
                        if any(x in eventStatus for x in up_status_list):
                            result = True
                        else:
                            result = False
                elif 'down' in status:
                    if len(service['events']) > 0:
                        if any(x in eventStatus for x in up_status_list):
                            result = False
                        else:
                            result = True
                    elif len(service['events']) == 0:
                        result = False
                else:
                    result = 'Invalid status request'

    return json.dumps(result)

@app.route('/devstatus')
def get_dev():

    result = {}

    for service in service_classes['dev']:
        serviceName = service.get('serviceName')
        if not service.get('events'):
            result[serviceName] = [{'eventStatus': 'up'}]

        else:
            result[serviceName] = service.get('events')

    return json.dumps(result)

@app.route('/prodstatus')
def get_prod():

    result = {}

    for service in service_classes['prod']:
        serviceName = service.get('serviceName')
        if not service.get('events'):
            result[serviceName] = [{'eventStatus': 'up'}]

        else:
            result[serviceName] = service.get('events')

    return json.dumps(result)
