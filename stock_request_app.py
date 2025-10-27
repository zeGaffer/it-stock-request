import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from streamlit.components.v1 import html

# ==============================
# ✅ PAGE CONFIG (Required for iOS + App Icon)
# ==============================
st.set_page_config(
    page_title="IT Stock Request",
    page_icon="📦",
    layout="centered"
)

# Inject Apple iOS PWA metadata and custom icon
html("""
<script>
(function() {
  const head = document.head;

  // Enable Add to Home Screen
  const meta1 = document.createElement('meta');
  meta1.name = 'apple-mobile-web-app-capable';
  meta1.content = 'yes';
  head.appendChild(meta1);

  const meta2 = document.createElement('meta');
  meta2.name = 'apple-mobile-web-app-status-bar-style';
  meta2.content = 'black-translucent';
  head.appendChild(meta2);

  // Set custom icon (with cache buster)
  const link = document.createElement('link');
  link.rel = 'apple-touch-icon';
  link.sizes = '180x180';
  link.href = 'https://raw.githubusercontent.com/zegaffer/it-stock-request/main/icon-180.png?v=2';
  head.appendChild(link);
})();
</script>
""", height=0)

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
