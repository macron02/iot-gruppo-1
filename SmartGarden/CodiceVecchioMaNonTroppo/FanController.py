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

    def check_fan(self):
        return self.relay.value()

    def start_fan(self):
        if self.check_fan() == 0:
            self.servo.set_angle(85)
            self.relay.value(1)  # Attiva il relé, quindi accende la ventola

    def stop_fan(self):
        if self.check_fan() == 1:
            self.relay.value(0)  # Disattiva il relé, quindi spegne la ventola
            time.sleep(1)
            self.servo.set_angle(15)
