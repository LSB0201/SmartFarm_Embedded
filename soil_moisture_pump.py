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
        # threshold는 read_soil_moisture()와 같은 % 단위(0~100)
        if moisture < threshold:
            print("Soil is dry. Pump ON")
            try:
                GPIO.output(self.pump_in1, GPIO.HIGH)
                GPIO.output(self.pump_in2, GPIO.LOW)
                time.sleep(5)
            finally:
                self.pump_off()  # 중단/예외 시에도 반드시 펌프 정지
        else:
            print("Soil moisture is sufficient")

    def pump_off(self):
        GPIO.output(self.pump_in1, GPIO.LOW)
        GPIO.output(self.pump_in2, GPIO.LOW)
