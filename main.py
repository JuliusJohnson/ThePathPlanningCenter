from inspect import Attribute
from multiprocessing.connection import Client
from queue import PriorityQueue
from urllib.request import Request
import sqlite3,requests, json
from pprint import pprint
import sendRequest, updateplanitems
from datetime import datetime

conn = sqlite3.connect('/home/julius/Documents/python/projects/thepathDB/PlanningCenter')
connectionCursor = conn.cursor()

def getNextLinkFromDB():
    for row in connectionCursor.execute("SELECT NextPlan_Link FROM PlanningCenterPlan ORDER BY PlanningCenterPlan.ID DESC LIMIT 1"):
        nextPlanLink = row[0]
        print(nextPlanLink)
        return nextPlanLink

def checkNextPlanLinkResults(result):
    for row in connectionCursor.execute("SELECT Self_Link FROM PlanningCenterPlan ORDER BY PlanningCenterPlan.ID DESC LIMIT 1"):
        if sendRequest.sendRequest(row[0])['links']['next_plan'] != None:
            updateQuery = "UPDATE PlanningCenterPlan SET NextPlan_Link = ? WHERE ID = ?"
            params = (f"https://api.planningcenteronline.com/services/v2/service_types/848341/plans/{sendRequest.sendRequest(row[0])['id']}/next_plan",sendRequest.sendRequest(row[0])['id'])
            connectionCursor.execute(updateQuery, params)
            conn.commit()
    return 
    
def writeRequestToDB(data):
    conn.execute("insert into PlanningCenterPlan values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (data['attributes']['created_at'], data['attributes']['dates'], data['attributes']['items_count'], data['attributes']['series_title'], data['attributes']['title'],data['attributes']['total_length'],data['attributes']['updated_at'],data['links']['my_schedules'],data['links']['notes'],data['links']['previous_plan'],data['links']['self'],data['links']['next_plan'],data['id'],datetime.now()))
    conn.commit()
    pprint("Update Successful")

def main():

    link = (getNextLinkFromDB())
    pprint(link)
    update = checkNextPlanLinkResults(link)
    pprint(update)
    writeRequestToDB(sendRequest.sendRequest(link))
    updateplanitems.updatePlanItems()

if __name__=="__main__":
    main()