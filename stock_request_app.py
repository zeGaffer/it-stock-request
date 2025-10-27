import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from streamlit.components.v1 import html

# ==============================
# ✅ PAGE CONFIG with iOS App Icon
# ==============================
st.set_page_config(
    page_title="IT Stock Request",
    page_icon="https://raw.githubusercontent.com/zegaffer/it-stock-request/main/icon-180.png",
    layout="centered"
)

# ==============================
# 🌗 iOS Dark/Light status bar + safe-area support
# (adds meta tags into <head> and uses prefers-color-scheme)
# ==============================
html("""
<script>
(function () {
  const head = document.head;

  // iOS standalone
  const cap = document.createElement('meta');
  cap.name = 'apple-mobile-web-app-capable';
  cap.content = 'yes';
  head.appendChild(cap);

  // Match status bar to system theme
  const bar = document.createElement('meta');
  bar.name = 'apple-mobile-web-app-status-bar-style';
  // 'black' looks best on modern iPhones (auto-contrasts with dark mode)
  bar.content = 'black';
  head.appendChild(bar);

  // Theme color for Safari toolbar (non-standalone)
  const theme = document.createElement('meta');
  theme.name = 'theme-color';
  theme.content = window.matchMedia('(prefers-color-scheme: dark)').matches ? '#0b0b0c' : '#ffffff';
  head.appendChild(theme);

  // Respect the notch/safe areas
  const viewport = document.createElement('meta');
  viewport.name = 'viewport';
  viewport.content = 'width=device-width, initial-scale=1, viewport-fit=cover';
  head.appendChild(viewport);
})();
</script>
<style>
  /* Ensure content isn't hidden under the notch/home indicator */
  .main, .block-container {
    padding-top: calc(env(safe-area-inset-top,0px) + 0.4rem) !important;
    padding-bottom: calc(env(safe-area-inset-bottom,0px) + 0.6rem) !important;
  }
</style>
""", height=0)

# ==============================
# 🔁 "Offline-friendly" input memory (persists for the session)
# ==============================
if "defaults" not in st.session_state:
    st.session_state.defaults = {
        "item": "Laptop - Lenovo T14",
        "qty": 1,
        "name": "",
        "office": ""
    }

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

item_selected = st.selectbox(
    "Select the item you need:",
    items,
    index=items.index(st.session_state.defaults["item"])
)
quantity = st.number_input(
    "Enter quantity:", min_value=1, value=int(st.session_state.defaults["qty"]), step=1
)
requester_name = st.text_input("Your Name:", value=st.session_state.defaults["name"])
office = st.text_input(
    "Office Location (e.g., Tunis, Lima, Bucharest):",
    value=st.session_state.defaults["office"]
)

# keep latest values (so if the app reloads, fields repopulate)
st.session_state.defaults.update({
    "item": item_selected,
    "qty": int(quantity),
    "name": requester_name,
    "office": office
})

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

        st.write("📄 **Here is your submitted request:**")
        st.table(new_request)
