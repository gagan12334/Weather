import requests
import streamlit as st
from transformers import pipeline
import config

pipe = pipeline("translation", model="t5-base")

@st.cache_data
def translate(text):
    return pipe(text)[0]["translation_text"]

api_key = config.API_KEY

# Farenheit to celcius
def conversion(temp):
    sum =  (temp-32)*(5/9)
    return round(sum,2)

st.title("WEATHER APP")

st.header("Enter city: ")
user_input = st.text_input("Enter city: ").lower().capitalize()


weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")



if len(user_input)>= 1:
    weathers = weather_data.json()["weather"][0]['main']
    temp = weather_data.json()['main']['temp']
    tempC = conversion(temp)
    feelsLike = weather_data.json()['main']['feels_like']
    windSpeed = weather_data.json()['wind']['speed']

    input1 = st.selectbox('Celcius or Farenheit🌤️', ['Celcius', 'Farenheit'])
    input2 = st.selectbox('Language:',['English','German'])
    if input2 == 'English':
        if input1 == 'Farenheit':
            st.text(f"temp: {temp}°F")
            st.text(f"weather feels like: {feelsLike}°F")
        else:
            st.text(f"temp: {tempC}°C")
            st.text(f"weather feels like: {conversion(feelsLike)}°C")
    else:
        if input1 == 'Farenheit':
            st.text(translate(f"temp: {temp}°F"))
            st.text(translate(f"weather feels like: {feelsLike}°F"))
        else:
            st.text(translate(f"temp: {tempC}°C"))
            st.text(translate(f"weather feels like: {conversion(feelsLike)}°C"))

    if input2 == 'German':
        if temp >= 90:
            st.text(translate(f"The weather: {weathers} and it is too hot"))
        elif temp < 90 and temp>= 72:
            st.text(translate(f"The weather: {weathers} and it is warm"))
        elif temp <72 and temp>=52:
            st.text(translate(f"The weather: {weathers} and it is perfect"))
        else:
            st.text(translate(f"The weather: {weathers} and it is cold"))
        st.text(translate(f"The wind speed is {windSpeed}mph"))
    else:
        if temp >= 90:
            st.text(f"The weather: {weathers} and it is too hot")
        elif temp < 90 and temp>= 72:
            st.text(f"The weather: {weathers} and it is warm")
        elif temp <72 and temp>=52:
            st.text(f"The weather: {weathers} and it is perfect")
        else:
            st.text(f"The weather: {weathers} and it is cold")
        st.text(f"The wind speed is {windSpeed}mph")