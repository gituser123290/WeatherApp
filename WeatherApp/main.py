import streamlit as st
import plotly.express as px
from backend import get_data
import os


st.title =("Weather forecast for  Nest days")
place=st.text_input("place: ")
days =st.slider("Forecast Days",min_value=1,max_value=5,help="Select the number og forecast days")
option = st.selectbox("Select data to view",("Tempreture","Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

is_local = os.path.exists(r"C:\Users\naura\Desktop\Streamlit\WeatherApp")

if is_local:
    images = {
        "Clear": "images/clear.jpg",
        "Clouds": "images/cloud.jpg",
        "Rain": "images/rain.jpg",
        "Snow": "images/snow.jpg"
    }
else:
    images = {
        "Clear": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/clear.jpg",
        "Clouds": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/cloud.jpg",
        "Rain": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/rain.jpg",
        "Snow": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/snow.jpg"
    }

if place:
    try:
        filtered_data = get_data(place,days)
        
        if option == "Tempreture":
            tempretures=[dict["main"]['temp']/10 for dict in filtered_data]
            
            dates=[dict["dt_txt"] for dict in filtered_data]
            
            figure=px.line(x=dates,y=tempretures,labels={"x":"Date","y":"Tempreture (C)"})
            st.plotly_chart(figure)
            
        if option == "Sky":
            # images={"Clear":"images/clear.jpg","Clouds":"images/cloud.jpg","Rain":"images/rain.jpg","Snow":"images/snow.jpg"}
            sky_conditions=[dict["weather"][0]["main"] for dict in filtered_data]
            # image_paths=[images[condition] for condition in sky_conditions]
            image_paths = [images.get(condition, "images/default.jpg") for condition in sky_conditions]
            # print(sky_conditions)
            st.image(image_paths,width=150)
            
    except KeyError:
        st.write("That place does not exist.")

