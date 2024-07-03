from machine import Pin
import time

class PumpCheck:
    def __init__(self, relay_pin):
        self.relay = Pin(relay_pin, Pin.OUT)

    def start_pump(self):
        self.relay.on()  # Attiva il relè per avviare la pompa

    def stop_pump(self):
        self.relay.off()  # Spegne il relè per avviare la pompa
