import csv
import os
import streamlit as st

INVENTORY_FILE = "inventory.csv"

def initialize_inventory():
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Quantity"])

def get_inventory_items():
    items = []
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            items.append(row[0])
    return items

def get_inventory_data():
    inventory_data = []
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                inventory_data.append({
                    "name": row[0],
                    "quantity": row[1]
                })
    return inventory_data

def add_item(item_name, quantity):
    with open(INVENTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, quantity])

def update_inventory(item_name, quantity, increase=True):
    rows = []
    item_found = False
    
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == item_name:
                current_quantity = int(row[1])
                new_quantity = current_quantity + quantity if increase else current_quantity - quantity
                row[1] = str(new_quantity)
                item_found = True
            rows.append(row)
    
    if item_found:
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        return True
    return False

def view_inventory():
    inventory_data = []
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header
        for row in reader:
            inventory_data.append(row)

    if inventory_data:
        st.table(inventory_data)
    else:
        st.write("No items in inventory.")
