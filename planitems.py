from asyncore import write
import json
from urllib.request import Request
import requests
import sqlite3
import sendRequest
from pprint import pprint
from config import credentials
from datetime import date

conn = sqlite3.connect('/home/julius/Documents/python/projects/thepath/PlanningCenter')
connectionCursor = conn.cursor()

def getSelfLinkFromDB():
    for row in connectionCursor.execute("SELECT Self_Link FROM PlanningCenterPlan ORDER BY UpdatedDate DESC LIMIT 1"):
        nextPlanLink = row[0]
        return str(nextPlanLink) + "/items"

def writeRequestToDB(data):
    conn.execute("insert into PlanningCenterItems values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (data['attributes']['created_at'], data['attributes']['custom_arrangement_sequence'], data['attributes']['custom_arrangement_sequence_full'], data['attributes']['custom_arrangement_sequence_short'], data['attributes']['description'],data['attributes']['html_details'],data['attributes']['item_type'],data['attributes']['key_name'],data['attributes']['length'], data['attributes']['sequence'], data['attributes']['service_position'], data['attributes']['title'], data['attributes']['updated_at'], data['links']['self'], date.today(), data['relationships']['plan']['data']['id']))
    conn.commit()
    pprint("Update Successful")

x = getSelfLinkFromDB()
y = (sendRequest.sendRequest(x)[0])
writeRequestToDB(y)