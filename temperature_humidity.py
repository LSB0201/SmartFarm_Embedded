import adafruit_dht
import board
import RPi.GPIO as GPIO

class TemperatureHumiditySensor:
    def __init__(self, pin):
        self.sensor = adafruit_dht.DHT11(board.D19)
    
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
        
    def cleanup(self):
        GPIO.cleanup([self.pin])
