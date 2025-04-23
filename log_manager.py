import csv
import os  # Add this import statement
from datetime import datetime
import streamlit as st

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

def view_log():
    log_data = []
    with open(LOG_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header
        for row in reader:
            log_data.append(row)
    
    if log_data:
        st.table([header] + log_data)  # Display as a table including the header
    else:
        st.write("No log data available.")
