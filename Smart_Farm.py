import time
import mysql.connector
import adafruit_dht
import RPi.GPIO as GPIO
import board
import neopixel
import spidev

# MariaDB 연결 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'pi',
    'password': 'raspberry',
    'database': 'smart_farm'
}

# MariaDB에 데이터 삽입하는 함수
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

# MCP3008 ADC 설정 (아날로그 센서 데이터를 읽기 위한 컨버터)
class MCP3008:
    def __init__(self, spi_channel=0):
        self.spi = spidev.SpiDev()
        self.spi.open(0, spi_channel)
        self.spi.max_speed_hz = 1350000
    
    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        return ((adc[1] & 3) << 8) + adc[2]

# 온습도 센서 클래스 (DHT11 사용)
class TemperatureHumiditySensor:
    def __init__(self, pin):
        self.sensor = adafruit_dht.DHT11(board.D5)
    
    def read_data(self):
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            if humidity is not None and temperature is not None:
                print(f"Temp: {temperature}C, Humidity: {humidity}%")
                return temperature, humidity
            else:
                print("Failed to read from sensor")
                return None, None
        except RuntimeError as error:
            print(f"Sensor read error: {error}")
            return None, None

# 토양 습도 및 펌프 클래스 (YL-69 + LM393 + L9110S)
class SoilMoisturePump:
    def __init__(self, adc, analog_channel, pump_in1, pump_in2):
        self.adc = adc
        self.analog_channel = analog_channel
        self.pump_in1 = pump_in1
        self.pump_in2 = pump_in2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_in1, GPIO.OUT)
        GPIO.setup(self.pump_in2, GPIO.OUT)
    
    def read_soil_moisture(self):
        raw_value = self.adc.read_channel(self.analog_channel)  # MCP3008에서 습도 값 읽기
        moisture = int((1023 - raw_value) * 100 / 1023)  # 백분율 변환
        print(f"Soil Moisture: {moisture}%")
        return moisture
    
    def control_pump(self, threshold, moisture):
        if moisture < threshold:
            print("Soil is dry. Pump ON")
            GPIO.output(self.pump_in1, GPIO.HIGH)
            GPIO.output(self.pump_in2, GPIO.LOW)
            time.sleep(5)
            GPIO.output(self.pump_in1, GPIO.LOW)
            GPIO.output(self.pump_in2, GPIO.LOW)
        else:
            print("Soil moisture is sufficient")

# 조도 센서 및 LED 제어 클래스 (KY-018 + WS2812B)
class LightSensorLED:
    def __init__(self, adc, analog_channel, led_pin, num_leds=12):
        self.adc = adc
        self.analog_channel = analog_channel
        self.led_pin = led_pin
        self.pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=0.5, auto_write=False)
    
    def read_light(self):
        light_level = self.adc.read_channel(self.analog_channel)  # MCP3008에서 조도 값 읽기
        print(f"Light Level: {light_level}")
        return light_level
    
    def control_led(self, threshold, light_level):
        if light_level > threshold:
            print("Low light detected. Turning LED ON")
            self.pixels.fill((255, 255, 255))  # 흰색
            self.pixels.show()
        else:
            print("Sufficient light. Turning LED OFF")
            self.pixels.fill((0, 0, 0))
            self.pixels.show()

if __name__ == "__main__":
    adc = MCP3008()  # ADC 초기화
    temp_humid_sensor = TemperatureHumiditySensor(pin=4)  # 온습도 센서 설정
    soil_moisture_pump = SoilMoisturePump(adc=adc, analog_channel=0, pump_in1=23, pump_in2=24)  # 토양 습도 및 펌프 설정
    light_sensor_led = LightSensorLED(adc=adc, analog_channel=7, led_pin=15, num_leds=12)  # 조도 센서 및 LED 설정
    
    while True:
        soil_moisture_threshold, light_intensity_threshold = get_thresholds()

        # 센서들로부터 데이터 읽기
        temperature, humidity = temp_humid_sensor.read_data()
        soil_moisture = soil_moisture_pump.read_soil_moisture()
        light_level = light_sensor_led.read_light()

        # 토양 습도 기준값으로 펌프 제어
        soil_moisture_pump.control_pump(soil_moisture_threshold, soil_moisture)
        
        # 조도 기준값으로 LED 제어
        light_sensor_led.control_led(light_intensity_threshold, light_level)

        # 모든 센서 데이터를 한 번에 DB에 삽입
        if temperature is not None and humidity is not None:
            query = """
                INSERT INTO sensor_data (temperature, humidity, soil_moisture, light_intensity, recorded_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            insert_data(query, (temperature, humidity, soil_moisture, light_level))

        # 1시간마다 실행
        time.sleep(3)
