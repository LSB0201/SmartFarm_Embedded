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
