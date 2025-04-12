import requests
import random
import time
from datetime import datetime

# Flask server URL
server_url = "http://10.15.63.81:5000/submit&quot;"  # Replace with your Flask server's IP
 # Replace with your Flask server's IP

def generate_sensor_data():
    """Generates random sensor data."""
    humidity = random.uniform(20, 90)
    temperature = random.uniform(10, 40)
    soil_moisture = random.uniform(0, 100)
    return humidity, temperature, soil_moisture

def send_sensor_data(humidity, temperature, soil_moisture):
    """Sends sensor data to the Flask server."""
    data = {
        "humidity": humidity,
        "temperature": temperature,
        "soil_moisture": soil_moisture,
    }

    try:
        response = requests.post(server_url, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Data sent successfully. Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

def simulate_esp32():
    """Simulates the ESP32 sending sensor data."""
    while True:
        humidity, temperature, soil_moisture = generate_sensor_data()
        send_sensor_data(humidity, temperature, soil_moisture)
        time.sleep(5)  # Simulate sending data every 5 seconds

if __name__ == "__main__":
    simulate_esp32()