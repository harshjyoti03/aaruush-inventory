import csv
import streamlit as st

LOG_FILE = "inventory_log.csv"

def view_taker_data():
    taker_data = {}
    
    # Open the log file and read the data
    with open(LOG_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        
        # Iterate through each row in the log file
        for row in reader:
            if len(row) >= 4:  # Ensure the row has at least 4 columns (Item, Quantity, Project, Taker)
                taker = row[3]
                if taker:
                    if taker not in taker_data:
                        taker_data[taker] = []
                    taker_data[taker].append({
                        "item": row[0],
                        "quantity": row[1],
                        "project": row[2]
                    })

    # Display the data using Streamlit
    if not taker_data:
        st.warning("No data available for takers.")
    else:
        for taker, items in taker_data.items():
            st.subheader(f"Taker: {taker}")
            for item in items:
                st.info(f"Component: {item['item']} | Quantity Allotted: {item['quantity']} | Project: {item['project']}")
            st.markdown("---")
