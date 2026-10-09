from flask import Flask, jsonify
from db_utils import get_latest_sensor_data  #센서를 직접 잡지 않고 main.py가 저장한 DB값 사용

app = Flask(__name__)

@app.route('/measure', methods=['GET'])
def measure_sensors():
    try:
        latest = get_latest_sensor_data()  #DB에서 최신 센서값 읽기
        if not latest:
            return jsonify({'error': 'No sensor data found'}), 404

        # AI 입력용 데이터만 JSON으로 반환
        sensor_data = {
            'temperature': latest['temperature'],
            'humidity': latest['humidity'],
        }
        return jsonify(sensor_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)  #debug=True는 외부 노출 시 원격 코드 실행 위험
