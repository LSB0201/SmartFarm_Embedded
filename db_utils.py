import mysql.connector

# MariaDB 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'piserver',
    'password': '1234',
    'database': 'smart_farm'
}

# 데이터 삽입 함수
def insert_data(query, values):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")

# 기준값 가져오는 함수
def get_thresholds():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT soil_moisture_threshold, light_intensity_threshold FROM standard_data WHERE id = 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result if result else (500, 300)  # 기본값 설정
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")
        return (500, 300)
    
def get_latest_sensor_data():  #최신 센서값 조회 함수 추가
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT temperature, humidity, soil_moisture, light_intensity
            FROM sensor_data
            ORDER BY recorded_at DESC
            LIMIT 1
        """)  #최신 1개 레코드만 가져옴
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result if result else {}
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")
        return {}