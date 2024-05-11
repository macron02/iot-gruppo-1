from machine import Pin, I2C, ADC, reset, PWM
import dht
import time
import ssd1306

class allarmed_sys:
    
        def __init__(pin_buzzer, pin_led1, pin_led2, pin_led3, pin_led4):