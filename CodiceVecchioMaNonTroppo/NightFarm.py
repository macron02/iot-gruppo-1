from machine import Pin, ADC
import LDR
import time


class NightFarm:
    def __init__(self, night_led_pin, ldr_pin):
        self.night_led = Pin(night_led_pin, Pin.OUT)
        self.ldr = LDR.LDR(ldr_pin)

    def controlLed(self):
        if self.ldr.checkLight() < 40:
            self.night_led.on()
        else:
            self.night_led.off()
