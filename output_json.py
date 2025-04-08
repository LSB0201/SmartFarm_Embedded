import time
import requests
from adc_mcp3008 import MCP3008
from light_sensor_led import LightSensorLED
from soil_moisture_pump import SoilMoisturePump
from temperature_humidity import TemperatureHumiditySensor

# 센서 설정
adc = MCP3008()
light_sensor = LightSensorLED(adc, analog_channel=0)
soil_sensor = SoilMoisturePump(adc, analog_channel=1, pump_in1=23, pump_in2=24)
temp_humi_sensor = TemperatureHumiditySensor(pin=6)  # DHT11(board.D6)

# 서버 설정
SERVER_URL = "http://<YOUR_FLASK_SERVER_IP>:<PORT>/sensor_data"

# 주기적으로 센서 데이터 측정 후 서버 전송
def main():
    while True:
        # 각 센서로부터 데이터 수집
        light_level = light_sensor.read_light()
        light_sensor.control_led(threshold=500, light_level=light_level)

        soil_moisture = soil_sensor.read_soil_moisture()
        soil_sensor.control_pump(threshold=40, moisture=soil_moisture)

        temperature, humidity = temp_humi_sensor.read_data()

        # JSON 데이터 생성
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

        # 대기시간 60초
        time.sleep(60)

if __name__ == "__main__":
    main()
