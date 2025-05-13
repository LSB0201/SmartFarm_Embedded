from flask import Flask, jsonify
from adc_mcp3008 import MCP3008
from temperature_humidity import TemperatureHumiditySensor

app = Flask(__name__)

@app.route('/measure', methods=['GET'])
def measure_sensors():
    # 센서 초기화
    adc = MCP3008()
    temp_humid_sensor = TemperatureHumiditySensor(pin=5)

    # 센서 값 읽기
    temperature, humidity = temp_humid_sensor.read_data()

    # 센서 데이터를 JSON 형식으로 준비
    sensor_data = {
        'temperature': temperature,
        'humidity': humidity,
    }

    # JSON 형식으로 데이터 반환
    return jsonify(sensor_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)