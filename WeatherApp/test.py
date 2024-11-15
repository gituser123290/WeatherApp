# import os
# import streamlit as st
# import plotly.express as px
# from backend import get_data

# # Title of the app
# st.title("Weather forecast for Next days")

# # Input fields for place and forecast days
# place = st.text_input("Place: ")
# days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecast days")
# option = st.selectbox("Select data to view", ("Temperature", "Sky"))

# # Display the option selected
# st.subheader(f"{option} for the next {days} days in {place}")

# # Check if the app is running locally by verifying if the 'images' folder exists
# is_local = os.path.exists("images")

# # Define image paths (local or remote based on environment)
# if is_local:
#     images = {
#         "Clear": "images/clear.jpg",
#         "Clouds": "images/cloud.jpg",
#         "Rain": "images/rain.jpg",
#         "Snow": "images/snow.jpg"
#     }
# else:
#     images = {
#         "Clear": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/clear.jpg",
#         "Clouds": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/cloud.jpg",
#         "Rain": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/rain.jpg",
#         "Snow": "https://github.com/gituser123290/WeatherApp/tree/main/WeatherApp/images/snow.jpg"
#     }

# # Main logic for fetching and displaying data
# if place:
#     try:
#         filtered_data = get_data(place, days)  # Fetch weather data using backend API
        
#         if option == "Temperature":
#             # Extract temperatures and dates
#             temperatures = [dict["main"]['temp'] / 10 for dict in filtered_data]  # Convert from Kelvin to Celsius
#             dates = [dict["dt_txt"] for dict in filtered_data]
            
#             # Create a plot using Plotly
#             figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
#             st.plotly_chart(figure)
        
#         if option == "Sky":
#             # Extract sky conditions (e.g., Clear, Clouds, etc.)
#             sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            
            
#             image_paths = [images.get(condition, "images/default.jpg") for condition in sky_conditions]
            
#             st.image(image_paths, width=150)
    
#     except KeyError:
#         st.write("That place does not exist.")
