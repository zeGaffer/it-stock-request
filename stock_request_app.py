import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import smtplib, ssl
from email.message import EmailMessage

# ✅ ADD THIS BLOCK BELOW:
st.set_page_config(
    page_title="IT Stock Request",
    page_icon="📦",  # fallback icon
    layout="centered"
)

st.markdown("""
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/zegaffer/it-stock-request/main/icon-180.png">
""", unsafe_allow_html=True)

st.title("📦 IT Stock Request Form")

# Dropdown list of available items
items = ["Laptop - Lenovo T14", "Monitor 24-inch", "Keyboard", "Mouse", "Docking Station", "MacBook Air M4"]

item_selected = st.selectbox("Select the item you need:", items)
quantity = st.number_input("Enter quantity:", min_value=1, step=1)
requester_name = st.text_input("Your Name:")
office = st.text_input("Office Location (e.g., Tunis, Lima, Bucharest):")

if st.button("Submit Request"):
    # Save the request into an Excel file
    new_request = pd.DataFrame({
        "Requester": [requester_name],
        "Office": [office],
        "Item": [item_selected],
        "Quantity": [quantity]
    })
    
    try:
        # Append to existing Excel
        existing_data = pd.read_excel("stock_requests.xlsx")
        updated_data = pd.concat([existing_data, new_request], ignore_index=True)
        updated_data.to_excel("stock_requests.xlsx", index=False)
        st.success("✅ Request submitted and saved to Excel!")
    except:
        # Create a new Excel file if not exists
        new_request.to_excel("stock_requests.xlsx", index=False)
        st.success("✅ Request submitted and new Excel file created!")

    st.write("📄 Here is your submitted request:")
    st.table(new_request)
import streamlit as st

st.set_page_config(
    page_title="IT Stock Request",
    page_icon="📦",  # fallback icon
    layout="centered"
)
st.title("📦 IT Stock Request Form")