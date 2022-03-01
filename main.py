from inspect import Attribute
from multiprocessing.connection import Client
from queue import PriorityQueue
from urllib.request import Request
import sqlite3,requests, json
from pprint import pprint
import sendRequest, updateplanitems

conn = sqlite3.connect('/home/julius/Documents/python/projects/thepath/PlanningCenter')
connectionCursor = conn.cursor()

def getNextLinkFromDB():
    for row in connectionCursor.execute("SELECT NextPlan_Link FROM PlanningCenterPlan ORDER BY UpdatedDate DESC LIMIT 1"):
        nextPlanLink = row[0]
        return nextPlanLink

def checkNextPlanLinkResults(result):
    if result == None:
        for row in connectionCursor.execute("SELECT Self_Link FROM PlanningCenterPlan ORDER BY UpdatedDate DESC LIMIT 1"):
            if sendRequest.sendRequest(row[0])['links']['next_plan'] == None:
                return "None"
            else:
                return(f"https://api.planningcenteronline.com/services/v2/service_types/848341/plans/{sendRequest.sendRequest(row[0])['id']}/next_plan")

def writeRequestToDB(data):
    conn.execute("insert into PlanningCenterPlan values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",
    (data['attributes']['created_at'], data['attributes']['dates'], data['attributes']['items_count'], data['attributes']['series_title'], data['attributes']['title'],data['attributes']['total_length'],data['attributes']['updated_at'],data['links']['my_schedules'],data['links']['notes'],data['links']['previous_plan'],data['links']['self'],data['links']['next_plan'],data['id']))
    conn.commit()
    pprint("Update Successful")

def main():
    link = (getNextLinkFromDB())
    update = checkNextPlanLinkResults(link)
    if update != "None":
        writeRequestToDB(sendRequest.sendRequest(update))
        updateplanitems.updatePlanItems()

if __name__=="__main__":
    main()