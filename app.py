import streamlit as st
import datetime

st.title("☕ Café Order Form")
st.markdown("Select a drink and enter your contact info.")

# --- Form inputs ---
drink = st.radio("Choose a drink:", [
    "Iced Lavender Chai",
    "Jashan (tangy, mango, papaya)",
    "Humsafar (blackberry, lychee, pomegranate)"
])

name = st.text_input("Your Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email")

# --- Submit button ---
if st.button("Submit Order"):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    st.success("Order submitted successfully!")
    
    st.write("### Order Details")
    st.write(f"**Name:** {name}")
    st.write(f"**Drink:** {drink}")
    st.write(f"**Phone:** {phone}")
    st.write(f"**Email:** {email}")
    st.write(f"**Time:** {time}")

