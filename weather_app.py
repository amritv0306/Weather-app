import streamlit as st
import requests

def get_weather_data(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Page configuration
st.set_page_config(page_title="Weather App", page_icon="🌤️")

# App UI with custom styling
st.markdown("""
    <style>
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">☁️ Weather Finder</h1>', unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input('Enter city name:', placeholder="e.g., London, Tokyo, New York")
with col2:
    api_key = st.text_input('API Key:', type='password', placeholder="Your API key")

# Search button
if st.button('Get Weather', type="primary"):
    if api_key and city:
        with st.spinner('Fetching weather data...'):
            data = get_weather_data(api_key, city)
            
        if data:
            # Display weather information in an attractive card
            st.markdown(f"<div class='weather-card'>", unsafe_allow_html=True)
            
            # City name and country with weather icon
            weather_icon = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"Weather in {data['name']}, {data['sys']['country']}")
                st.caption(f"As of {st.session_state.get('current_time', 'now')}")
            with col2:
                st.image(icon_url, width=80)
            
            # Main weather metrics
            st.markdown(f"### {data['weather'][0]['description'].capitalize()}")
            
            # Temperature section
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Temperature", f"{data['main']['temp']} °C")
                st.metric("Feels Like", f"{data['main']['feels_like']} °C")
            with col2:
                st.metric("Min Temp", f"{data['main']['temp_min']} °C")
                st.metric("Max Temp", f"{data['main']['temp_max']} °C")
            
            # Additional weather details
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Humidity", f"{data['main']['humidity']}%")
            with col2:
                st.metric("Pressure", f"{data['main']['pressure']} hPa")
            with col3:
                st.metric("Visibility", f"{data.get('visibility', 'N/A')} m")
            
            # Wind information
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Wind Speed", f"{data['wind']['speed']} m/s")
            with col2:
                st.metric("Wind Direction", f"{data['wind']['deg']}°")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            st.error('❌ Error fetching weather data. Please check the city name and API key.')
    else:
        st.warning('⚠️ Please enter both API key and city name.')

# Footer
st.markdown("---")
st.caption("Data provided by OpenWeatherMap API")
