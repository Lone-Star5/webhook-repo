from flask import Blueprint, json, request,render_template
import datetime
from app.extensions import mongo
from bson.json_util import dumps
import os


#Route to display data from database to the UI
display = Blueprint('display',__name__,url_prefix='/')
@display.route('/display', methods=["GET","POST"])
def dis():
    if(request.method=="POST"): 
        newData = mongo.db.webhooks.find({})  # data is fetched from database
        newData = dumps(list(newData))
        return newData,200
    return render_template('index.html')

#Route to add webhook data to MongoDB database
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
@webhook.route('/receiver', methods=["POST"])
def receiver():

    # Convert data to json format
    data = json.dumps(request.json)
    data = json.loads(data)
    # print(json.dumps(request.json, indent = 1))
    # Initial Object that will be populated with data and added to MongoDB database
    webhookData = {'request_id': None, 'action': None, 'author': None, 'to_branch': None, 'from_branch': None, 'timestamp': None}
    
    # This means it's either a Pull request or a merge request as action attribute is not present in Push request
    if('action' in data):
        author = data['sender']['login']
        request_id = data['pull_request']['id']
        to_branch = data['pull_request']['base']['ref']
        from_branch = data['pull_request']['head']['ref']
        timestamp = data['pull_request']['updated_at']
        timestamp = datetime.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")

        webhookData['author'] = author  
        webhookData['from_branch'] = from_branch    
        webhookData['to_branch'] = to_branch
        webhookData['timestamp'] = timestamp
        webhookData['request_id'] = request_id
        if(data['pull_request']['merged']==True):
            webhookData['action']="MERGE"
        else:
            webhookData['action'] = "PULL_REQUEST"
    else: # It is a Push request as action attribute is not present
        author = data['commits'][0]['author']['name']
        request_id = data['commits'][0]['id']
        to_branch = data['ref']
        to_branch = to_branch.split('/')
        to_branch = to_branch[2]
        timestamp = data['commits'][0]['timestamp']
        timestamp = datetime.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S+05:30")
        timestamp = timestamp - datetime.timedelta(hours=5,minutes=30) #Conversion of timestamp to UTC
        tmp = list(mongo.db.webhooks.find({'request_id':request_id}))
        if(len(tmp)>0):
            return "already exist"
        webhookData['author'] = author
        webhookData['to_branch'] = to_branch
        webhookData['timestamp'] = timestamp
        webhookData['action'] = "PUSH"
        webhookData['request_id'] = request_id
    
    #Data is added to Mongo DB successfully and we return a 200 OK status code
    mongo.db.webhooks.insert(webhookData)
    return {}, 200
