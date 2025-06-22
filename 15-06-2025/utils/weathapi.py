from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json
weather_api_key = os.getenv("WEATHER_API_KEY")
from langchain_core.tools import tool

class Weather:
    def __init__(self):
        # Placeholder for weather data
        self.weather_data = {}
        #https://api.weatherapi.com/v1/forecast.json?key=ebf398935eb44970a24101300251706&q=London&days=4&aqi=no&alerts=no
    
    def get_weather_beyond_14_days(self, dates, location):
        """
        Fetch weather data for dates beyond 14 days.
        Input: dates (list of str) - List of date strings (YYYY-MM-DD).
               location (str) - Location for which weather data is to be fetched.
        Output: List of API responses for each date.
        """
        api_key = weather_api_key  # Replace with your actual API key
        base_url = "https://api.weatherapi.com/v1/future.json"
        responses = []

        for date in dates:
            if not date or not location:
                responses.append({"error": "Both 'date' and 'location' are required"})
                continue

            try:
                response = requests.get(
                    base_url,
                    params={
                        "key": api_key,
                        "q": location,
                        "dt": date
                    }
                )
                if response.status_code == 200:
                    responses.append(self.handle_14_day_weather_data(response.json()))
                else:
                    responses.append({"error": f"API request failed with status code {response.status_code}"})
            except requests.RequestException as e:
                responses.append({"error": f"An error occurred: {str(e)}"})

        return "\n\n".join(responses)
     
    def handle_14_day_weather_data(self,weather_data:dict):
        # Extract forecast data
        forecast_days = weather_data.get("forecast", {}).get("forecastday", [])
        if not forecast_days:
            return "No weather forecast data available."
        
        # Build the summary for all dates
        summaries = []
        for day in forecast_days:
            date = day.get("date")
            day_data = day.get("day", {})
            summary = [
                f"Weather Summary for {date}:",
                f"Max Temperature: {day_data.get('maxtemp_c')}°C ({day_data.get('maxtemp_f')}°F)",
                f"Min Temperature: {day_data.get('mintemp_c')}°C ({day_data.get('mintemp_f')}°F)",
                f"Average Temperature: {day_data.get('avgtemp_c')}°C ({day_data.get('avgtemp_f')}°F)",
                f"Max Wind: {day_data.get('maxwind_kph')} kph ({day_data.get('maxwind_mph')} mph)",
                f"Total Precipitation: {day_data.get('totalprecip_mm')} mm ({day_data.get('totalprecip_in')} in)",
                f"Total Snow: {day_data.get('totalsnow_cm')} cm",
                f"Average Visibility: {day_data.get('avgvis_km')} km ({day_data.get('avgvis_miles')} miles)",
                f"Average Humidity: {day_data.get('avghumidity')}%",
                f"Will it Rain?: {'Yes' if day_data.get('daily_will_it_rain') else 'No'}",
                f"Chance of Rain: {day_data.get('daily_chance_of_rain')}%",
                f"Will it Snow?: {'Yes' if day_data.get('daily_will_it_snow') else 'No'}",
                f"Chance of Snow: {day_data.get('daily_chance_of_snow')}%"
            ]
            summaries.append("\n".join(summary))
        
        # Join all summaries into a single string
        return "\n\n".join(summaries)

    def get_weather_within_14_days(self, max_days,location):
        """
        Fetch weather data within 14 days of today.
        Input: max_days (int) - Maximum number of days (>= 14).
        Output: Response dict from the API if status code is 200, else error message.
        """
        if max_days is None or  max_days > 14:
            return "Nothing to calculate weather data for less than 14 days"

        api_key = weather_api_key  # Replace with your actual API key
        base_url = "https://api.weatherapi.com/v1/forecast.json"

        try:
            response = requests.get(
                base_url,
                params={
                    "key": api_key,
                    "q": location,
                    "days": max_days,
                    "aqi": "no",
                    "alerts": "no"
                }
            )
            if response.status_code == 200:
                return self.handle_14_day_weather_data(response.json())
            else:
                return {"error": f"API request failed with status code {response.status_code}"}
        except requests.RequestException as e:
            return {"error": f"An error occurred: {str(e)}"}


    def calculate_days_within_and_beyond_14_days(self, start_date, end_date):
        """
        Calculate days within and beyond 14 days from today.
        Returns a list of day numbers within 14 days and date strings beyond 14 days.
        """
        today = datetime.now().date()

        # Raise an error if start_date is greater than 300 days from today
        if (start_date - today).days > 300:
            raise ValueError("start_date cannot be more than 300 days from today")

        within_14_days = []
        beyond_14_days = []

        current_date = start_date
        while current_date <= end_date:
            if today <= current_date <= today + timedelta(days=14):
                day_number = (current_date - today).days + 1
                within_14_days.append(day_number)
            elif current_date > today + timedelta(days=14):
                beyond_14_days.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

        return within_14_days, beyond_14_days
     

weather = Weather()

# @tool
def get_combined_weather_summary(start_date, end_date, location):
    """
     The function take in ths start and end date of the trip with location and return the weather during that period   
    Args:
        start_date (datetime.date): Start date for the weather data.
        end_date (datetime.date): End date for the weather data.
        location (str): Location for which weather data is to be fetched.
    
    Returns:
        str: Combined weather summary for dates within and beyond 14 days.
    """
    
    print("     ")
    # Calculate days within and beyond 14 days
    #write a code that stakes start date and end date as string and convert to date time 
    # Convert start_date and end_date from string to datetime.date
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    within_14_days, beyond_14_days = weather.calculate_days_within_and_beyond_14_days(start_date, end_date)
    # Fetch weather data within 14 days
    weather_within_14_days = weather.get_weather_within_14_days(max_days=max(within_14_days) if within_14_days else None, location=location)
    
    # Fetch weather data beyond 14 days
    weather_beyond_14_days = weather.get_weather_beyond_14_days(beyond_14_days, location=location)
    
    # Combine the summaries
    combined_summary = f"Weather Within 14 Days:\n{weather_within_14_days}\n\nWeather Beyond 14 Days:\n{weather_beyond_14_days}"
    
    return combined_summary


if __name__ == "__main__":
# Example usage
    start_date = "2025-07-20"
    end_date = "2025-07-25"
    location = "Milan, Italy"

    combined_weather_summary = get_combined_weather_summary(start_date, end_date, location)
    print(combined_weather_summary)


# import json

# def summarize_weather_with_hourly(json_file_path):
#     """
#     Reads a weather JSON file and returns a text summary of the weather information for all available dates,
#     including hourly data.
    
#     Args:
#         json_file_path (str): Path to the weather JSON file.
    
#     Returns:
#         str: A text summary of the weather information for all dates, including hourly data.
#     """
#     with open(json_file_path, 'r') as file:
#         weather_data = json.load(file)
    
#     # Extract forecast data
#     forecast_days = weather_data.get("forecast", {}).get("forecastday", [])
#     if not forecast_days:
#         return "No weather forecast data available."
    
#     # Build the summary for all dates
#     summaries = []
#     for day in forecast_days:
#         date = day.get("date")
#         day_data = day.get("day", {})
#         hourly_data = day.get("hour", [])
        
#         # Daily summary
#         summary = [
#             f"Weather Summary for {date}:",
#             f"Max Temperature: {day_data.get('maxtemp_c')}°C ({day_data.get('maxtemp_f')}°F)",
#             f"Min Temperature: {day_data.get('mintemp_c')}°C ({day_data.get('mintemp_f')}°F)",
#             f"Average Temperature: {day_data.get('avgtemp_c')}°C ({day_data.get('avgtemp_f')}°F)",
#             f"Max Wind: {day_data.get('maxwind_kph')} kph ({day_data.get('maxwind_mph')} mph)",
#             f"Total Precipitation: {day_data.get('totalprecip_mm')} mm ({day_data.get('totalprecip_in')} in)",
#             f"Total Snow: {day_data.get('totalsnow_cm')} cm",
#             f"Average Visibility: {day_data.get('avgvis_km')} km ({day_data.get('avgvis_miles')} miles)",
#             f"Average Humidity: {day_data.get('avghumidity')}%",
#             f"Will it Rain?: {'Yes' if day_data.get('daily_will_it_rain') else 'No'}",
#             f"Chance of Rain: {day_data.get('daily_chance_of_rain')}%",
#             f"Will it Snow?: {'Yes' if day_data.get('daily_will_it_snow') else 'No'}",
#             f"Chance of Snow: {day_data.get('daily_chance_of_snow')}%"
#         ]
        
#         # Hourly summary
#         hourly_summary = ["Hourly Data:"]
#         for hour in hourly_data:
#             time = hour.get("time")
#             temp_c = hour.get("temp_c")
#             temp_f = hour.get("temp_f")
#             condition = hour.get("condition", {}).get("text")
#             wind_kph = hour.get("wind_kph")
#             wind_mph = hour.get("wind_mph")
#             precip_mm = hour.get("precip_mm")
#             precip_in = hour.get("precip_in")
#             humidity = hour.get("humidity")
            
#             hourly_summary.append(
#                 f"  Time: {time}, Temp: {temp_c}°C ({temp_f}°F), Condition: {condition}, "
#                 f"Wind: {wind_kph} kph ({wind_mph} mph), Precipitation: {precip_mm} mm ({precip_in} in), "
#                 f"Humidity: {humidity}%"
#             )
        
#         summaries.append("\n".join(summary))
#         summaries.append("\n".join(hourly_summary))
    
#     # Join all summaries into a single string
#     return "\n\n".join(summaries)