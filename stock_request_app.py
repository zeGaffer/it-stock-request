import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ==============================
# ✅ PAGE CONFIG with iOS App Icon
# ==============================
st.set_page_config(
    page_title="IT Stock Request",
    page_icon="https://raw.githubusercontent.com/zegaffer/it-stock-request/main/icon-180.png",  # ✅ Custom icon for iOS
    layout="centered"
)

# ==============================
# 🧾 APP TITLE
# ==============================
st.title("📦 IT Stock Request Form")

# ==============================
# 🧍 USER INPUT FORM
# ==============================
items = [
    "Laptop - Lenovo T14",
    "Monitor 24-inch",
    "Keyboard",
    "Mouse",
    "Docking Station",
    "MacBook Air M4"
]

item_selected = st.selectbox("Select the item you need:", items)
quantity = st.number_input("Enter quantity:", min_value=1, value=1, step=1)
requester_name = st.text_input("Your Name:")
office = st.text_input("Office Location (e.g., Tunis, Lima, Bucharest):")

# ==============================
# 💾 PROCESS FORM SUBMISSION
# ==============================
if st.button("Submit Request"):

    if not requester_name or not office:
        st.error("⚠️ Please fill in all fields before submitting.")
    else:
        new_request = pd.DataFrame({
            "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Requester": [requester_name],
            "Office": [office],
            "Item": [item_selected],
            "Quantity": [quantity]
        })

        file_path = "stock_requests.xlsx"

        try:
            if Path(file_path).exists():
                existing_data = pd.read_excel(file_path)
                updated_data = pd.concat([existing_data, new_request], ignore_index=True)
                updated_data.to_excel(file_path, index=False)
            else:
                new_request.to_excel(file_path, index=False)

            st.success("✅ Request submitted successfully!")
        except Exception as e:
            st.error(f"❌ Error saving request: {e}")

        # Display the submitted data
        st.write("📄 **Here is your submitted request:**")
        st.table(new_request)

