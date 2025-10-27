import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import smtplib, ssl
from email.message import EmailMessage

# ==============================
# ✅ PAGE CONFIG with iOS App Icon
# ==============================
st.set_page_config(
    page_title="IT Stock Request",
    page_icon="https://raw.githubusercontent.com/zegaffer/it-stock-request/main/icon-180.png",
    layout="centered"
)

# ==============================
# ✉️ Email helper
# ==============================
def send_email(subject: str, body: str) -> tuple[bool, str]:
    try:
        cfg = st.secrets["email"]
        msg = EmailMessage()
        msg["From"] = cfg["sender"]
        msg["To"] = cfg["to"]
        if cfg.get("cc"):
            msg["Cc"] = cfg["cc"]
        msg["Subject"] = subject
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP(cfg["smtp_server"], int(cfg.get("smtp_port", 587))) as server:
            server.starttls(context=context)
            server.login(cfg["sender"], cfg["password"])
            server.send_message(msg)

        return True, "Email sent."
    except Exception as e:
        return False, f"Email error: {e}"

# ==============================
# 🧾 Title
# ==============================
st.title("📦 IT Stock Request Form")

# ==============================
# 🧍 Form
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
# 💾 Submit
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

            # -------- Email notification --------
            subject = f"[IT Stock] {requester_name} requested {quantity} × {item_selected}"
            body = (
                "New IT Stock Request\n\n"
                f"Requester : {requester_name}\n"
                f"Office    : {office}\n"
                f"Item      : {item_selected}\n"
                f"Quantity  : {quantity}\n"
                f"Timestamp : {new_request.iloc[0]['Timestamp']}\n"
            )
            ok, msg = send_email(subject, body)
            if ok:
                st.info("📧 Notification email sent.")
            else:
                st.warning(f"📧 {msg}")

        except Exception as e:
            st.error(f"❌ Error saving request: {e}")

        st.write("📄 **Here is your submitted request:**")
        st.table(new_request)