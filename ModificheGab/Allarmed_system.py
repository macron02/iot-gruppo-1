from machine import Pin, PWM
import time

class AllarmeHabitat:
    def __init__(self, pin_buzzer, red_led_pin_0, blue_led_pin_0,red_led_pin_1, blue_led_pin_1):
        self.pwm_buzzer = PWM(Pin(pin_buzzer, Pin.OUT))
        self.leds = [Pin(red_led_pin_0, Pin.OUT),
                     Pin(blue_led_pin_0, Pin.OUT),
                     Pin(red_led_pin_1, Pin.OUT),
                     Pin(blue_led_pin_1, Pin.OUT)]

    def attiva_allarme(self):
        for i in range (0,12):
            """tono alto"""
            self.pwm_buzzer.freq(900)
            self.leds[0].on()
            self.leds[1].off()
            time.sleep(0.2)  # Durata del tono alto
            """tono basso"""
            self.pwm_buzzer.freq(450)
            self.leds[0].off()
            self.leds[1].on()
            time.sleep(0.2) # Durata del tono basso
            
