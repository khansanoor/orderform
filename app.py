import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

# --- CONFIG: Get secrets from Streamlit's secrets.toml ---
TWILIO_SID = st.secrets["TWILIO_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = st.secrets["TWILIO_PHONE"]

EMAIL_USER = st.secrets["EMAIL_USER"]
EMAIL_PASS = st.secrets["EMAIL_PASS"]

# --- UI: Order Form ---
st.title("☕ Drinks Menu")
st.markdown("Select your drink and enter your contact info.")

drink = st.radio("Choose a drink:", [
    "Iced Lavender Chai",
    "Jashan (tangy, mango, papaya)",
    "Humsafar (blackberry, lychee, pomegranate)"
])

name = st.text_input("Your Name")
phone = st.text_input("Phone Number (for SMS)")
email = st.text_input("Email (for backup)", placeholder="Optional")

if st.button("Submit Order"):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    order_msg = f"Hi {name}, your order for {drink} was received at {time}!"

# Store in session
    if 'orders' not in st.session_state:
        st.session_state.orders = []

    st.session_state.orders.append({
        "name": name,
        "drink": drink,
        "phone": phone,
        "email": email,
        "time": time,
        "status": "Pending"
    })

    # --- Send SMS ---
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=order_msg,
            from_=TWILIO_PHONE,
            to=phone
        )
        st.success("SMS sent ✅")
    except Exception as e:
        st.error(f"SMS failed: {e}")

    # --- Send Email ---
    if email:
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = email
            msg['Subject'] = "Your Drink Order Confirmation"
            msg.attach(MIMEText(order_msg, 'plain'))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            server.quit()

            st.success("Email sent ✅")
        except Exception as e:
            st.error(f"Email failed: {e}")

# --- Admin Panel ---
st.markdown("---")
st.subheader("📋 Admin Panel")

if 'orders' in st.session_state and st.session_state.orders:
    for i, order in enumerate(st.session_state.orders):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{order['name']}** - {order['drink']} @ {order['time']} — *{order['status']}*")
        with col2:
            if order['status'] != "Done" and st.button("Mark as Done", key=f"done_{i}"):
                st.session_state.orders[i]['status'] = "Done"
                # Notify customer
                ready_msg = f"Hi {order['name']}, your {order['drink']} is ready for pickup!"
                try:
                    if order['phone']:
                        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                        client.messages.create(
                            body=ready_msg,
                            from_=TWILIO_PHONE,
                            to=order['phone']
                        )
                    if order['email']:
                        msg = MIMEMultipart()
                        msg['From'] = EMAIL_USER
                        msg['To'] = order['email']
                        msg['Subject'] = "Your Drink is Ready"
                        msg.attach(MIMEText(ready_msg, 'plain'))

                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(EMAIL_USER, EMAIL_PASS)
                        server.send_message(msg)
                        server.quit()
                except Exception as e:
                    st.error(f"Ready notification failed: {e}")
else:
    st.write("No orders yet.")
