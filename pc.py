from inspect import Attribute
from multiprocessing.connection import Client
import json
from urllib.request import Request
import requests
import sqlite3
from pprint import pprint
from config import credentials

conn = sqlite3.connect('/home/julius/Documents/python/projects/thepath/PlanningCenter')
connectionCursor = conn.cursor()
# grant_type = 'client_credentials'
# url = "https://api.planningcenteronline.com/services/v2"

def getNextLinkFromDB():
    
    for row in connectionCursor.execute("SELECT NextPlan_Link FROM PlanningCenterPlan ORDER BY UpdatedDate DESC LIMIT 1"):
        nextPlanLink = row[0]

def checkNextPlanLinkResults(result):
    if result == None:
        pprint('No new PlanningCenter Plans. Please try again later.')
    else:
        return result

def sendRequest(pcRequest):
    response = requests.get(pcRequest, auth=(credentials.username, credentials.secret))
    data = response.json()['data']
    pprint(response.json()['data'])

def writeRequestToDB(data):
    c.execute("insert into PlanningCenterPlan values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",
    (data['attributes']['created_at'], data['attributes']['dates'], data['attributes']['items_count'], data['attributes']['series_title'], data['attributes']['title'],data['attributes']['total_length'],data['attributes']['updated_at'],data['links']['my_schedules'],data['links']['notes'],data['links']['previous_plan'],data['links']['self'],data['links']['next_plan'],data['id']))
    conn.commit()
    