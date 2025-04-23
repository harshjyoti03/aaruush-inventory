import csv
import os
from datetime import datetime

LOG_FILE = "inventory_log.csv"

def initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Quantity", "Project", "Taker", "Head", "Date Allotted", "Date Returned"])

def log_allotment(item_name, quantity, project, taker, head):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, quantity, project, taker, head, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ""])

def log_return(item_name, quantity, taker):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, quantity, "", taker, "", "", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
