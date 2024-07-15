from machine import Pin, PWM
import time

class FanController:
    """
    Definizione della classe per il controllo della ventola
    """
    def __init__(self, relay_pin, servo_pin):
        """relay_pyn: pin per il controllo del relé che comanda l'accensione della ventola"""
        self.relay = Pin(relay_pin, Pin.OUT)
        self.servo = PWM(Pin(servo_pin), freq=50)

    def set_angle(self, angle):
        min_angle = 26
        max_angle = 206
        self.servo.duty(int(min_angle + (angle/180)*(max_angle - min_angle)))

    def clear_fan(self):
        self.set_angle(0)
        self.relay.on()

    def start_fan(self):
        self.clear_fan()
        self.set_angle(90)
        time.sleep(1)
        self.relay.off()

    def stop_fan(self):
        self.relay.on()
        time.sleep(1)
        self.set_angle(0)
