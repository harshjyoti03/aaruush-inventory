import streamlit as st
from inventory import initialize_inventory, get_inventory_items, get_inventory_data, add_item, update_inventory, view_inventory
from log_manager import initialize_log, log_allotment, log_return, view_log
from taker_view import view_taker_data
from auth import login

# Initialize files
initialize_inventory()
initialize_log()

# Streamlit App
st.title("Inventory Management System")

# Authentication
if login():  # Show the login form only if the user is not authenticated
    # Once logged in, display the main dashboard and hide the login form
    st.sidebar.title("Actions")
    option = st.sidebar.selectbox("Choose an action", ["View Inventory Dashboard", "View Inventory List", "Add Item", "Allot Item", "Return Item", "View Log", "View Taker Data"])

    inventory_items = get_inventory_items()

    if option == "View Inventory Dashboard":
        st.header("Components in Inventory")
        inventory_data = get_inventory_data()
        if not inventory_data:
            st.warning("No items found in the inventory.")
        else:
            cols = st.columns(3)  # Adjust the number of columns as needed
            for idx, item in enumerate(inventory_data):
                col = cols[idx % 3]
                with col:
                    st.subheader(item["name"])
                    st.info(f"Quantity: {item['quantity']}")

    elif option == "View Inventory List":
        st.header("Current Inventory")
        view_inventory()  # Correctly display the inventory list

    elif option == "Add Item":
        st.header("Add a New Item")
        item_name = st.selectbox("Select Item or Type New", inventory_items + ["Other"])
        if item_name == "Other":
            item_name = st.text_input("Enter New Item Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        if st.button("Add Item"):
            add_item(item_name, quantity)
            st.success(f"Added {item_name} with quantity {quantity} to the inventory.")

    elif option == "Allot Item":
        st.header("Allot an Item")
        item_name = st.selectbox("Select Item or Type New", inventory_items + ["Other"])
        if item_name == "Other":
            item_name = st.text_input("Enter New Item Name")
        quantity = st.number_input("Quantity to Allot", min_value=1, step=1)
        project = st.text_input("Project Name")
        taker = st.text_input("Taker's Name")
        head = st.text_input("Head's Name")
        if st.button("Allot Item"):
            if update_inventory(item_name, quantity, increase=False):
                log_allotment(item_name, quantity, project, taker, head)
                st.success(f"Allotted {quantity} of {item_name} to {taker} for project {project}.")
            else:
                st.error(f"Failed to allot {quantity} of {item_name}. Item may not exist or insufficient quantity.")

    elif option == "Return Item":
        st.header("Return an Item")
        item_name = st.selectbox("Select Item", inventory_items)
        quantity_returned = st.number_input("Quantity to Return", min_value=1, step=1)
        taker = st.text_input("Taker's Name")
        if st.button("Return Item"):
            if update_inventory(item_name, quantity_returned, increase=True):
                log_return(item_name, quantity_returned, taker)
                st.success(f"Returned {quantity_returned} of {item_name} from {taker} back to inventory.")
            else:
                st.error(f"Failed to return {quantity_returned} of {item_name}. Item may not exist.")

    elif option == "View Log":
        st.header("Inventory Log")
        view_log()  # Correctly display the log

    elif option == "View Taker Data":
        st.header("Takers and Their Allotted Components")
        view_taker_data()  # Correctly display the taker data

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.success("Logged out successfully!")
