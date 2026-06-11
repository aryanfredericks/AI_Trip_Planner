import os
from typing import List,Dict,Any,Optional
from dotenv import load_dotenv
from utils.weather_info import WeatherInformation
from langchain.tools import tool

class WeatherInfoTool():
    def __init__(self):
        self.api_key = None
        self.weather_info = None
        self.tools = None
    
    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(location: str) -> str:
            """Get current weather for a given location."""
            weather_data = self.weather_service.get_current_weather(location)
            if weather_data:
                temp = weather_data.get('main', {}).get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {location}: {temp}°C, {desc}"
            return f"Could not fetch weather for {location}"
        
        @tool
        def get_weather_forecast(location: str) -> str:
            """Get weather forecast for a given location."""
            forecast_data = self.weather_service.get_forecast_weather(location)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp} degree celcius , {desc}")
                return f"Weather forecast for {location}:\n" + "\n".join(forecast_summary)
            return f"Could not fetch forecast for {location}"
        
        
        return [get_current_weather, get_weather_forecast]
    
    def get_tools(self)->List:
        """Get all the tools for fetching weather of a location.

        Returns:
            List: all the tools.
        """
        return self.tools
    
    def __call__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.weather_info = WeatherInformation(api_key=self.api_key)
        self.tools = self._setup_tools()