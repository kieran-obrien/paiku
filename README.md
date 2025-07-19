<img src="https://github.com/kieran-obrien/pitest/blob/main/public/readme-splash.png?raw=true"/>

# 🌸 Pyku – Raspberry Pi Haiku Generator

Pyku is a contemplative haiku generator that runs on a Raspberry Pi. It fetches real-time weather and geolocation data, crafts a reflective prompt, and uses an open-source large language model (LLM) to generate beautiful, minimalist haiku.

Whether displayed on an e-ink screen or logged to your terminal, Paiku brings a quiet moment of poetry to your day.

## ✨ Features
- Uses IP-based geolocation and OpenWeather data
- Generates traditional 3-line haikus via the LLaMA model hosted by Groq
- Customizable prompt logic with probability-based field inclusion

## 🔧 Requirements
- Python 3.8+
- Raspberry Pi (or any Linux device)

.env file with:
```
GROQ_API_KEY=<your_api_key>
OPEN_WEATHER_API_KEY=<your_api_key>
LLM_TEMP=<num from 0-2>
RANDOMISER=<num from 0-1>
USE_IP_LOCATION=<boolean true/false>
```

## 🚀 Usage

#### Clone the repo
```
git clone https://github.com/kieran-obrien/paiku.git
cd paiku
```
#### Start a virtual environment and install dependencies
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
#### Run the script
```
python3 main.py
```

## 📷 Preview
Example output:

Clouds drift through the day  
A still breeze whispers gently  
Edinburgh sighs

## 🖼 E-Ink Display Support
To minimize ghosting and preserve hardware, a recommended refresh interval is once every 30–60 minutes.

## 📜 License
MIT License. Poetry belongs to everyone.
