import neopixel
import board

class LightSensorLED:
    def __init__(self, adc, analog_channel, num_leds=12):
        self.adc = adc
        self.analog_channel = analog_channel
        self.num_leds = num_leds
        self.pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=0.5, auto_write=False)
    
    def read_light(self):
        light_level = self.adc.read_channel(self.analog_channel)
        print(f"Light Level: {light_level}")
        return light_level
    
    def control_led(self, threshold, light_level):
        if light_level > threshold:
            print("Low light detected. Turning LED ON")
            self.pixels.fill((255, 0, 255))
            self.pixels.show()
        else:
            print("Sufficient light. Turning LED OFF")
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
            
    def cleanup(self):
        GPIO.cleanup([self.led_pin])
