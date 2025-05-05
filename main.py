import time
from db_utils import insert_data, get_thresholds
from adc_mcp3008 import MCP3008
from temperature_humidity import TemperatureHumiditySensor
from soil_moisture_pump import SoilMoisturePump
from light_sensor_led import LightSensorLED

if __name__ == "__main__":
    adc = MCP3008()
    temp_humid_sensor = TemperatureHumiditySensor(pin=5)
    soil_moisture_pump = SoilMoisturePump(adc=adc, analog_channel=0, pump_in1=23, pump_in2=24)
    light_sensor_led = LightSensorLED(adc=adc, analog_channel=7, num_leds=12)

    while True:
        # 기준값 가져오기
        soil_moisture_threshold, light_intensity_threshold = get_thresholds()

        # 센서 값 읽기
        temperature, humidity = temp_humid_sensor.read_data()
        soil_moisture = soil_moisture_pump.read_soil_moisture()
        light_level = light_sensor_led.read_light()

        # 펌프 및 LED 제어
        soil_moisture_pump.control_pump(soil_moisture_threshold, soil_moisture)
        light_sensor_led.control_led(light_intensity_threshold, light_level)

        # 데이터베이스에 저장
        if temperature is not None and humidity is not None:
            query = """
                INSERT INTO sensor_data (temperature, humidity, soil_moisture, light_intensity, recorded_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            insert_data(query, (temperature, humidity, soil_moisture, light_level))

        time.sleep(3600)
