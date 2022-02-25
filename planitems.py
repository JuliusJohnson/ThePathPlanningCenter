import json
from urllib.request import Request
import requests
import sqlite3
from pprint import pprint
from config import credentials

conn = sqlite3.connect('/home/julius/Documents/python/projects/thepath/PlanningCenter')
connectionCursor = conn.cursor()

def getSelfLinkFromDB():
    for row in connectionCursor.execute("SELECT Self_Link FROM PlanningCenterPlan ORDER BY UpdatedDate DESC LIMIT 1"):
        nextPlanLink = row[0]
        return str(nextPlanLink) + "/items"

print(getSelfLinkFromDB())