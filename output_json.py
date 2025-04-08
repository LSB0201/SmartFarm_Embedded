import time
import threading
import requests
from flask import Flask, request, jsonify

from adc_mcp3008 import MCP3008
from light_sensor_led import LightSensorLED
from soil_moisture_pump import SoilMoisturePump
from temperature_humidity import TemperatureHumiditySensor

# Flask 서버 설정
app = Flask(__name__)

@app.route('/sensor_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received JSON data:", data)
    return jsonify({"status": "success"}), 200

# 센서 측정 및 서버로 데이터 전송
def sensor_loop():
    adc = MCP3008()
    light_sensor = LightSensorLED(adc, analog_channel=7)
    soil_sensor = SoilMoisturePump(adc, analog_channel=0, pump_in1=23, pump_in2=24)
    temp_humi_sensor = TemperatureHumiditySensor(pin=6)

    SERVER_URL = "http://127.0.0.1:5000/sensor_data"  # 내부 루프백 주소

    while True:
        light_level = light_sensor.read_light()
        light_sensor.control_led(threshold=500, light_level=light_level)

        soil_moisture = soil_sensor.read_soil_moisture()
        soil_sensor.control_pump(threshold=40, moisture=soil_moisture)

        temperature, humidity = temp_humi_sensor.read_data()

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "light_level": light_level,
            "soil_moisture": soil_moisture
        }

        print("Sending data to server:", data)

        try:
            response = requests.post(SERVER_URL, json=data)
            print(f"Server response: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send data: {e}")

        time.sleep(60)

if __name__ == '__main__':
    # 센서 측정 루프는 백그라운드 스레드에서 실행
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()

    # Flask 서버 실행
    app.run(host='0.0.0.0', port=5000)
