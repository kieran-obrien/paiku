import os
import time
import requests
import random
from dotenv import load_dotenv

load_dotenv()

def get_location_and_weather():
  ip_permission = os.environ.get("USE_IP_LOCATION")
  if ip_permission.lower() == "true":
    ip = requests.get('https://api.ipify.org?format=json').json()['ip']
    geo_loc = requests.get(f"http://ip-api.com/json/{ip}").json()
    open_weather_api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    weather_res = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather",
    params={"lat": geo_loc['lon'], "lon": geo_loc['lat'], "appid": open_weather_api_key, "units": "metric"}
    ).json()
    weather = "\n" + format_value({"description": weather_res["weather"][0]["description"],
               "temp": weather_res["main"]["temp"],
               "humidity": weather_res["main"]["humidity"],
               "windspeed": weather_res["wind"]["speed"]})
    return {
    "weather": weather,
    "city": geo_loc["city"],
    "country": geo_loc["country"]
    }  
  return

def format_value(value):
    if isinstance(value, dict):
        return "\n".join(f"  {k}: {v}" for k, v in value.items())
    return str(value)

def build_prompt(user_params):
    prompt = "Write a reflective haiku inspired by the following data:\n\n"
    for key, val in user_params.items():
        if add_to_prompt(os.environ.get("RANDOMISER")):
            formatted = format_value(val)
            prompt += f"{key}:\n{formatted}\n\n"
    prompt += "Only ever return a 3 line haiku."
    print(prompt)
    return prompt

def add_to_prompt(probability):
    """Return True with the given probability (0.0 - 1.0), with fallback to 0.25"""
    default_failsafe = 0.25
    try:
        probability = float(probability)
        if not (0 <= probability <= 1):
            print(f"Probability not within safe parameters, defaulting to {default_failsafe}")
            probability = default_failsafe
    except (ValueError, TypeError):
        print(f"Probability not within safe parameters, defaulting to {default_failsafe}")
        probability = default_failsafe

    return random.random() < probability
 
def generate_haiku():   
  location_and_weather = get_location_and_weather()
  current_time = time.strftime("%H:%M")
  month = time.strftime("%B")

  prompt = build_prompt(dict(location_and_weather=location_and_weather, current_time=current_time, month=month))

  groq_api_key = os.environ.get("GROQ_API_KEY")
  groq_url = "https://api.groq.com/openai/v1/chat/completions"
  groq_headers = {
      "Authorization": f"Bearer {groq_api_key}",
      "Content-Type": "application/json"
  }
  groq_data = {
    "model": "llama-3.3-70b-versatile",
    "temperature": 1.4,
    "messages": [
      {
        "role": "user",
        "content": prompt
      }
    ]
  }

  res = requests.post(groq_url, json=groq_data, headers=groq_headers)
  if res.status_code == 200:
    haiku = res.json()['choices'][0]['message']['content']
    print(haiku)
    return haiku
  else:
    print("Error: Something went wrong during Paiku generation!", res.status_code, res.text)

if __name__ == "__main__":
    generate_haiku()