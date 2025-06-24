import requests
import os

API_KEY = "f40317b78fd1a0ba7f1419d24fbab29b"  # Replace with your actual key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"
API_KEY = os.getenv("OPENWEATHER_API_KEY", "f40317b78fd1a0ba7f1419d24fbab29b")

def fetch_weather_data(city, unit="metric"):
    try:
        params = {"q": city, "appid": API_KEY, "units": unit}
        res = requests.get(BASE_URL, params=params)
        res.raise_for_status()
        data = res.json()

        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "desc": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"]
        }
    except:
        return None

def fetch_5_day_forecast(city, unit="metric"):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        forecast = []
        seen_dates = set()

        for item in data["list"]:
            dt_txt = item["dt_txt"]
            date = dt_txt.split(" ")[0]
            if date not in seen_dates and len(forecast) < 5:
                seen_dates.add(date)
                forecast.append({
                    "date": date,
                    "temp": item["main"]["temp"],
                    "desc": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"]
                })

        return forecast
    except Exception as e:
        print("Forecast error:", e)
        return []


def fetch_hourly_forecast(city, unit="metric"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={unit}"
    try:
        res = requests.get(url)
        data = res.json()

        if "list" not in data:
            return None

        hourly_forecast = []
        for entry in data["list"][:12]:  # next 12 entries = ~36 hours (3-hour interval)
            hour_data = {
                "time": entry["dt_txt"].split(" ")[1][:5],  # Extract HH:MM
                "temp": int(entry["main"]["temp"]),
                "desc": entry["weather"][0]["description"].capitalize(),
                "icon": entry["weather"][0]["icon"]
            }
            hourly_forecast.append(hour_data)

        return hourly_forecast

    except Exception as e:
        print("Hourly forecast error:", e)
        return None
    
def get_icon(icon_id):
    folder = "icons"
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, f"{icon_id}.png")
    if not os.path.exists(path):
        url = ICON_URL.format(icon_id)
        res = requests.get(url)
        with open(path, "wb") as f:
            f.write(res.content)
    return path

def fetch_weather_by_zip(zip_code, units="metric", country="IN"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country}&appid={API_KEY}&units={units}"
        response = requests.get(url)
        response.raise_for_status()
        raw = response.json()
        return {
            "city": raw["name"],
            "temp": round(raw["main"]["temp"]),
            "feels_like": round(raw["main"]["feels_like"]),
            "humidity": raw["main"]["humidity"],
            "wind": raw["wind"]["speed"],
            "desc": raw["weather"][0]["description"].title(),
            "icon": raw["weather"][0]["icon"],
            "sunrise": raw["sys"]["sunrise"],
            "sunset": raw["sys"]["sunset"],
            "wind_deg": raw["wind"].get("deg", 0)
        }
    except Exception as e:
        print("ZIP fetch error:", e)
        return None