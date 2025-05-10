from flask import Flask, jsonify
from db_utils import get_latest_sensor_data  #센서대신 DB 접근

app = Flask(__name__)

@app.route('/outputData', methods=['GET'])
def measure_sensors():
    try:
        sensor_data = get_latest_sensor_data()  #DB에서 센서값 읽기
        if not sensor_data:
            return jsonify({'error': 'No sensor data found'}), 404
        return jsonify(sensor_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  #외부 접속 허용