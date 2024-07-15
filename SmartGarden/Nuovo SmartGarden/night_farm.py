from machine import Pin, ADC
import ldr
import time


class night_farm:
    def __init__(self, night_led_pin, ldr_pin, low_light_level=200):
        self.night_led = Pin(night_led_pin, Pin.OUT)
        self.ldr = ldr.ldr(ldr_pin)
        self.low_light_level = low_light_level

    def check_night(self):
        if self.ldr.read_light_value() < self.low_light_level:
            self.night_led.on()
        else:
            self.night_led.off()
