import time
import RPi.GPIO as GPIO

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
        raw_value = self.adc.read_channel(self.analog_channel)
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
