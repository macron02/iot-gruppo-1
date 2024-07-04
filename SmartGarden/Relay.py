from machine import Pin

class Relay:
    def __init__(self, relay_pin):
        self.relay = Pin(relay_pin, Pin.OUT)

    def start_relay(self):
        self.relay.off()  # Attiva il relè

    def stop_relay(self):
        self.relay.on()  # Spegne il relè
