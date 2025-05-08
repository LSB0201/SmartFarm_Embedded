from flask import Flask, jsonify
from adc_mcp3008 import MCP3008
from temperature_humidity import TemperatureHumiditySensor
from soil_moisture_pump import SoilMoisturePump
from light_sensor_led import LightSensorLED

app = Flask(__name__)

@app.route('/measure', methods=['GET'])
def measure_sensors():
    # 센서 초기화
    adc = MCP3008()
    temp_humid_sensor = TemperatureHumiditySensor(pin=5)
    soil_moisture_pump = SoilMoisturePump(adc=adc, analog_channel=0, pump_in1=23, pump_in2=24)
    light_sensor_led = LightSensorLED(adc=adc, analog_channel=7, num_leds=12)

    # 센서 값 읽기
    temperature, humidity = temp_humid_sensor.read_data()
    soil_moisture = soil_moisture_pump.read_soil_moisture()
    light_level = light_sensor_led.read_light()

    # 센서 데이터를 JSON 형식으로 준비
    sensor_data = {
        'temperature': temperature,
        'humidity': humidity,
        'soil_moisture': soil_moisture,
        'light_intensity': light_level
    }

    # JSON 형식으로 데이터 반환
    return jsonify(sensor_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)