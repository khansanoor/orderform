import streamlit as st
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(credentials)

# Open the sheet
sheet = client.open("heart_drink_orders").sheet1

# Streamlit UI
st.title("☕ Café Order Form")

drink = st.radio("Choose a drink:", ["Iced Lavender Chai", "Jashan", "Humsafar"])
name = st.text_input("Name")
phone = st.text_input("Phone")
email = st.text_input("Email")

# --- Submit button ---
if st.button("Submit Order"):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    row = [name, drink, phone, email, time]
    sheet.append_row(row)
    st.success("Order submitted and saved to Google Sheet ✅")

