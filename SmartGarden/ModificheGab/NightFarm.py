from machine import Pin, ADC
import LDR
import time


class NightFarm:
    def __init__(self, night_led_pin, ldr_pin, low_light_level=40):
        self.night_led = Pin(night_led_pin, Pin.OUT)
        self.ldr = LDR.LDR(ldr_pin)
        self.low_light_level = low_light_level

    def night_light(self):
        if self.ldr.read_light_value() < self.low_light_level:
            self.night_led.on()
        else:
            self.night_led.off()

    def set_low_light_level(self, new_value):
        self.low_light_level = new_value

    def get_low_light_level(self):
        return low_light_level
