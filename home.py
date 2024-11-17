import streamlit as st
from model import helper
from model import use_model

@st.cache_data
def circuits():
    return helper.circut_names()

st.set_page_config(
    page_title="F1 Group Project",
    page_icon="🏎️",
)

st.title("🏎️ F1 Tyre Strategy Predictor")

st.header("Predict Optimal Starting Tyre Compound")

st.subheader("Input Race Conditions")

# Conditions
circuit = st.selectbox('Circuit', circuits())
air_temperature = st.slider('Air Temperature (°C)', 10, 50, 25)
humidity = st.slider('Humidity (%)', 0, 100, 50)
pressure = st.slider('Pressure (hPa)', 900, 1100, 1013)
wind_speed = st.slider('Wind Speed (km/h)', 0, 50, 10)
wind_direction = st.slider('Wind Direction (degrees)', 0, 360, 180)
track_temperature = st.slider('Track Temperature (°C)', 10, 60, 30)


# Input Data
input = {
        "air_temperature": air_temperature,
        "circuit_short_name": circuit,
        "humidity": humidity,
        "pressure": pressure,
        "track_temperature": track_temperature,
        "wind_direction": wind_direction,
        "wind_speed": wind_speed
    }
# Process
prediction = use_model.run_model(input)[0]

# Make Prediction

st.subheader("Recommended Starting Tyre Compound")
st.write(f"Based on the input conditions, the model recommends using the {prediction.capitalize()} tyre.")

# Display tyre image
st.image(f"images/{prediction.lower()}.png", width=200)

# Additional stats?