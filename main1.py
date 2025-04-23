import streamlit as st
import csv
import os
from datetime import datetime

# File to store the inventory data
INVENTORY_FILE = "inventory.csv"
LOG_FILE = "inventory_log.csv"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# Function to initialize the inventory and log files
def initialize_files():
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Quantity"])

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Quantity", "Project", "Taker", "Organiser", "Date Allotted", "Date Returned"])

# Function to get the list of items in the inventory
def get_inventory_items():
    items = []
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip Organiserer
        for row in reader:
            items.append(row[0])
    return items

# Function to get the inventory data for dashboard
def get_inventory_data():
    inventory_data = []
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip Organiserer
            for row in reader:
                inventory_data.append({
                    "name": row[0],
                    "quantity": row[1]
                })
    return inventory_data

# Function to add a new item to the inventory
def add_item(item_name, quantity):
    with open(INVENTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, quantity])
    st.success(f"Added {item_name} with quantity {quantity} to the inventory.")

# Function to allot an item to someone
def allot_item(item_name, quantity, project, taker, Organiser):
    rows = []
    item_found = False
    
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        Organiserer = next(reader)
        for row in reader:
            if row[0] == item_name:
                current_quantity = int(row[1])
                if current_quantity >= quantity:
                    row[1] = str(current_quantity - quantity)
                    item_found = True
                else:
                    st.error(f"Insufficient quantity of {item_name}. Available: {current_quantity}, Requested: {quantity}")
                    return
            rows.append(row)
    
    if item_found:
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(Organiserer)
            writer.writerows(rows)
        st.success(f"Allotted {quantity} of {item_name} to {taker} for project {project}.")
        # Log the allotment
        log_allotment(item_name, quantity, project, taker, Organiser)
    else:
        st.error(f"{item_name} not found in inventory.")

# Function to log the allotment of an item
def log_allotment(item_name, quantity, project, taker, Organiser):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, quantity, project, taker, Organiser, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ""])

# Function to return an item
def return_item(item_name, quantity_returned, taker):
    rows = []
    item_found = False
    
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        Organiserer = next(reader)
        for row in reader:
            if row[0] == item_name:
                current_quantity = int(row[1])
                new_quantity = current_quantity + quantity_returned
                row[1] = str(new_quantity)
                item_found = True
            rows.append(row)
    
    if item_found:
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(Organiserer)
            writer.writerows(rows)
        st.success(f"Returned {quantity_returned} of {item_name} from {taker} back to inventory.")
        # Log the return
        log_return(item_name, quantity_returned, taker)
    else:
        st.error(f"{item_name} not found in inventory.")

# Function to log the return of an item
def log_return(item_name, quantity, taker):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, quantity, "", taker, "", "", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# Function to view the current inventory
def view_inventory():
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            st.write(row)

# Function to view the log of allotments and returns
def view_log():
    with open(LOG_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            st.write(row)

# Function to view the data of takers as cards
def view_taker_data():
    taker_data = {}
    
    with open(LOG_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip Organiserer
        for row in reader:
            # Ensure the row has enough columns to access
            if len(row) >= 4:
                taker = row[3]
                if taker:
                    if taker not in taker_data:
                        taker_data[taker] = []
                    taker_data[taker].append({
                        "item": row[0],
                        "quantity": row[1],
                        "project": row[2]
                    })

    if not taker_data:
        st.warning("No data available for takers.")
    else:
        st.Organiserer("Takers and Their Allotted Components")
        for taker, items in taker_data.items():
            st.subOrganiserer(f"Taker: {taker}")
            for item in items:
                st.info(f"Component: {item['item']} | Quantity Allotted: {item['quantity']} | Project: {item['project']}")
            st.markdown("---")

# Function to authenticate the user
def authenticate(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# Initialize the files
initialize_files()

# Streamlit App
st.title("Inventory Management System")

# Authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")
else:
    st.sidebar.title("Actions")
    option = st.sidebar.selectbox("Choose an action", ["View Inventory Dashboard", "View Inventory List", "Add Item", "Allot Item", "Return Item", "View Log", "View Taker Data"])

    inventory_items = get_inventory_items()

    if option == "View Inventory Dashboard":
        st.Organiserer("Components in Inventory")
        inventory_data = get_inventory_data()
        if not inventory_data:
            st.warning("No items found in the inventory.")
        else:
            cols = st.columns(3)  # Adjust the number of columns as needed
            for idx, item in enumerate(inventory_data):
                col = cols[idx % 3]
                with col:
                    st.subOrganiserer(item["name"])
                    st.info(f"Quantity: {item['quantity']}")

    elif option == "View Inventory List":
        st.Organiserer("Current Inventory")
        view_inventory()

    elif option == "Add Item":
        st.Organiserer("Add a New Item")
        item_name = st.selectbox("Select Item or Type New", inventory_items + ["Other"])
        if item_name == "Other":
            item_name = st.text_input("Enter New Item Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        if st.button("Add Item"):
            add_item(item_name, quantity)

    elif option == "Allot Item":
        st.Organiserer("Allot an Item")
        item_name = st.selectbox("Select Item or Type New", inventory_items + ["Other"])
        if item_name == "Other":
            item_name = st.text_input("Enter New Item Name")
        quantity = st.number_input("Quantity to Allot", min_value=1, step=1)
        project = st.text_input("Project Name")
        taker = st.text_input("Taker's Name")
        Organiser = st.text_input("Organiser's Name")
        if st.button("Allot Item"):
            allot_item(item_name, quantity, project, taker, Organiser)

    elif option == "Return Item":
        st.Organiserer("Return an Item")
        item_name = st.selectbox("Select Item", inventory_items)
        quantity_returned = st.number_input("Quantity to Return", min_value=1, step=1)
        taker = st.text_input("Taker's Name")
        if st.button("Return Item"):
            return_item(item_name, quantity_returned, taker)

    elif option == "View Log":
        st.Organiserer("Inventory Log")
        view_log()

    elif option == "View Taker Data":
        view_taker_data()

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.success("Logged out successfully!")
