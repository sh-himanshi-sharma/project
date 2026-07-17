import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

def get_aqi_category(aqi_value):
    if aqi_value is None:
        return None, "Unknown"
    
    if aqi_value <= 20:
        return 1, "Good"
    elif aqi_value <= 40:
        return 2, "Fair"
    elif aqi_value <= 60:
        return 3, "Moderate"
    elif aqi_value <= 80:
        return 4, "Poor"
    elif aqi_value <= 100:
        return 5, "Very Poor"
    else:
        return 6, "Extremely Poor"

def execute(arguments: dict):
    city = arguments.get("city")
    
    if not city:
        return "Air Quality error: No city provided"
    
    try:
        # Get coordinates
        geo_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1},
            timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if "results" not in geo_data or not geo_data["results"]:
            return f"City '{city}' not found"
        
        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "Unknown")
        
        # Get air quality
        air_response = requests.get(
            AIR_QUALITY_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": ["pm10", "pm2_5", "ozone", "european_aqi"],
                "timezone": "auto"
            },
            timeout=10
        )
        air_response.raise_for_status()
        air_data = air_response.json()
        
        current = air_data.get("current", {})
        
        # Get values
        pm10 = current.get("pm10", "N/A")
        pm25 = current.get("pm2_5", "N/A")
        ozone = current.get("ozone", "N/A")
        aqi_value = current.get("european_aqi")
        
        # Convert AQI value to category
        aqi_category, aqi_description = get_aqi_category(aqi_value)
        
        return (
            f"Air Quality: {city_name}, {country}\n"
            f"PM10: {pm10} µg/m³\n"
            f"PM2.5: {pm25} µg/m³\n"
            f"Ozone: {ozone} µg/m³\n"
            f"AQI: {aqi_value} - {aqi_description}"
        )
        
    except Exception as e:
        return f"Air Quality error: {e}"

if __name__ == "__main__":
    print(execute({"city": "Delhi"}))