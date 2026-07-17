import requests

API_KEY = "rc_live_ebdfacb5ec8e42fd9b4d11c9e8e368dc"

def execute(arguments: dict):
    country = arguments.get("country")
    
    if not country:
        return "Country info error: No country provided"
    
    try:
        # Try exact match first
        response = requests.get(
            f'https://api.restcountries.com/countries/v5?q={country}&fullText=true',
            headers={'Authorization': f'Bearer {API_KEY}'},
            timeout=10
        )
        
        # If exact match fails, try partial
        if response.status_code == 404 or not response.json().get("data", {}).get("objects"):
            response = requests.get(
                f'https://api.restcountries.com/countries/v5?q={country}',
                headers={'Authorization': f'Bearer {API_KEY}'},
                timeout=10
            )
        
        response.raise_for_status()
        data = response.json()
        
        if not data or "data" not in data or not data["data"].get("objects"):
            return f"Country '{country}' not found"
        
        objects = data["data"]["objects"]
        
        # Find exact match
        exact_match = None
        for obj in objects:
            common_name = obj.get("names", {}).get("common", "").lower()
            if common_name == country.lower():
                exact_match = obj
                break
        
        c = exact_match if exact_match else objects[0]
        
        # Get country name
        name = c.get("names", {}).get("common", "N/A")
        official_name = c.get("names", {}).get("official", "N/A")
        
        # Get capital
        capitals = c.get("capitals", [])
        if capitals and isinstance(capitals[0], dict):
            capital = capitals[0].get("name", "N/A")
        elif capitals:
            capital = capitals[0] if capitals else "N/A"
        else:
            capital = "N/A"
        
        # Get currencies - remove special characters
        currencies = c.get("currencies", [])
        if currencies:
            currency = currencies[0]
            currency_name = currency.get("name", "N/A")
            currency_symbol = currency.get("symbol", "")
            # Remove special characters from symbol
            currency_symbol = currency_symbol.replace('₹', 'Rs.').replace('$', 'USD').replace('€', 'EUR')
            currency_info = f"{currency_name} ({currency_symbol})" if currency_symbol else currency_name
        else:
            currency_info = "N/A"
        
        # Get population
        population = c.get("population", "N/A")
        if population != "N/A":
            population = f"{population:,}"
        
        # Get timezones
        timezones = c.get("timezones", [])
        timezone_list = ", ".join(timezones) if timezones else "N/A"
        
        # Get coordinates
        coords = c.get("coordinates", {})
        lat = coords.get("lat", "N/A")
        lng = coords.get("lng", "N/A")
        coordinates = f"{lat}, {lng}" if lat != "N/A" and lng != "N/A" else "N/A"
        
        return (
            f"Country: {name}\n"
            f"Official Name: {official_name}\n"
            f"Capital: {capital}\n"
            f"Currency: {currency_info}\n"
            f"Population: {population}\n"
            f"Timezones: {timezone_list}\n"
            f"Coordinates: {coordinates}"
        )
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return "Country info error: Invalid API key"
        if e.response.status_code == 404:
            return f"Country '{country}' not found"
        return f"Country info error: HTTP {e.response.status_code}"
    except Exception as e:
        return f"Country info error: {e}"

if __name__ == "__main__":
    print(execute({"country": "India"}))