import streamlit as st
import pandas as pd
import pickle


with open("gradboost_model.sav", "rb") as f:
    model = pickle.load(f)

st.title("🚗 Car Price Prediction App")
st.write("Enter the details of the car to predict its **selling price**.")


name = st.text_input("Car Name (e.g., Maruti Swift Dzire)")
year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, step=1)
km_driven = st.number_input("Kilometers Driven", min_value=0, step=100)
fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual", "Trustmark Dealer"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.selectbox("Owner", ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "Test Drive Car"])

def encode_inputs(name, fuel, seller_type, transmission, owner):
   
    fuel_map = {"Petrol": 3, "Diesel": 1, "CNG": 0, "LPG": 2, "Electric": 4}
    seller_map = {"Dealer": 0, "Individual": 1, "Trustmark Dealer": 2}
    transmission_map = {"Manual": 1, "Automatic": 0}
    owner_map = {
        "First Owner": 1,
        "Second Owner": 3,
        "Third Owner": 4,
        "Fourth & Above Owner": 0,
        "Test Drive Car": 2
    }
    name_encoded = hash(name) % 1000
    return [name_encoded, year, km_driven,
            fuel_map[fuel], seller_map[seller_type],
            transmission_map[transmission], owner_map[owner]]


if st.button("Predict Selling Price"):
    input_data = encode_inputs(name, fuel, seller_type, transmission, owner)
    input_df = pd.DataFrame([input_data], columns=["name", "year", "km_driven", "fuel", "seller_type", "transmission", "owner"])
    prediction = model.predict(input_df)[0]
    st.success(f"Estimated Selling Price: ₹ {prediction:,.2f}")
