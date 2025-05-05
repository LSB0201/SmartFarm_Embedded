from picamera2 import Picamera2
from datetime import datetime, timedelta
import time
import os
import mysql.connector

SAVE_DIR = "/home/piserver/SmartFarm_Embedded/captured_images"
DB_CONFIG = {
	"host": "localhost",
	"user": "piserver",
	"password": "1234",
	"database": "smart_farm"
}

if not os.path.exists(SAVE_DIR):
	os.makedirs(SAVE_DIR)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
time.sleep(2)

def wait_until_next_capture(target_hour):
	now = datetime.now()
	next_time = now.replace(hour=target_hour, minute=0, second=0, microsecond=0)

	if now >= next_time:
		next_time += timedelta(days=1)

	wait_time = (next_time - now).total_seconds()

	time.sleep(wait_time)
	return next_time

while True:
	next_capture = wait_until_next_capture(6)
	now = datetime.now()
	filename = now.strftime("%Y-%m-%d_%H-%M-%S.jpg")
	filepath = os.path.join(SAVE_DIR, filename)

	try:
		picam2.capture_file(filepath)

		conn = mysql.connector.connect(**DB_CONFIG)
		cursor = conn.cursor()
		query = "INSERT INTO captured_images (file_path, captured_at) VALUES (%s, %s)"
		cursor.execute(query, (filepath, now))
		conn.commit()
		cursor.close()
		conn.close()

		print(f"{now} DB Correct")

	except Exception as e:
		print(f"Error: {e}")

	next_capture = wait_until_next_capture(18)
	now = datetime.now()
	filename = now.strftime("%Y-%m-%d_%H-%M-%S.jpg")
	filepath = os.path.join(SAVE_DIR, filename)

	try:
		picam2.capture_file(filepath)

		conn = mysql.connector.connect(**DB_CONFIG)
		cursor = conn.cursor()
		query = "INSERT INTO captured_images (file_path, captured_at) VALUES (%s, %s)"
		cursor.execute(query, (filepath, now))
		conn.commit()
		cursor.close()
		conn.close()

		print(f"{now} DB Correct")

	except Exception as e:
		print(f"Error: {e}")
