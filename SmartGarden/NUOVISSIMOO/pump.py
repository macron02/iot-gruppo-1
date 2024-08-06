from machine import Pin
import time

class pump:
    def __init__(self, relay_pin):
        self.relay = Pin(relay_pin, Pin.OUT)

    def start_pump(self):
        self.relay.off()  # Attiva il relè per avviare la pompa

    def stop_pump(self):
        self.relay.on()  # Spegne il relè per avviare la pompa
