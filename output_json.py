import RPi.GPIO as GPIO
from flask import Flask, jsonify
from adc_mcp3008 import MCP3008
from temperature_humidity import TemperatureHumiditySensor
from soil_moisture_pump import SoilMoisturePump
from light_sensor_led import LightSensorLED
import RPi.GPIO as GPIO

# GPIO 초기화는 앱 시작 시 1회만 수행
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = Flask(__name__)

# 센서 핀 번호 정의
TEMP_HUMID_PIN = 5
SOIL_PUMP_IN1 = 23
SOIL_PUMP_IN2 = 24
SOIL_ANALOG_CH = 0
LIGHT_ANALOG_CH = 7
NUM_LEDS = 12

@app.route('/measure', methods=['GET'])
def measure_sensors():
    try:
        # 센서 객체 초기화
        adc = MCP3008()
        temp_humid_sensor = TemperatureHumiditySensor(pin=TEMP_HUMID_PIN)
        soil_moisture_pump = SoilMoisturePump(adc=adc, analog_channel=SOIL_ANALOG_CH,
                                              pump_in1=SOIL_PUMP_IN1, pump_in2=SOIL_PUMP_IN2)
        light_sensor_led = LightSensorLED(adc=adc, analog_channel=LIGHT_ANALOG_CH, num_leds=NUM_LEDS)

        # 센서 데이터 읽기
        temperature, humidity = temp_humid_sensor.read_data()
        soil_moisture = soil_moisture_pump.read_soil_moisture()
        light_level = light_sensor_led.read_light()

        # JSON 데이터 구성
        sensor_data = {
            'temperature': temperature,
            'humidity': humidity,
            'soil_moisture': soil_moisture,
            'light_intensity': light_level
        }

    except Exception as e:
        # 오류 발생 시 에러 메시지 반환
        sensor_data = {'error': str(e)}

    return jsonify(sensor_data)

# 앱 실행 및 GPIO 정리
if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    finally:
        GPIO.cleanup()
