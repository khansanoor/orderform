import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

st.title("☕ Café Order Form")
st.markdown("Select your drink and enter your contact info.")
