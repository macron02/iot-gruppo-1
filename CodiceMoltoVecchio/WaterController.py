from machine import Pin
import time
import machine

class WaterController:
    def __init__(self, relay_pin):
        self.relay = Pin(relay_pin, Pin.OUT)
"""
    def daily_water(self):
        self.relay.value(1)  # Attiva il relè per avviare la pompa
        time.sleep(3)
        self.relay.value(0)  # Spegne il relè per disattivare la pompa
"""
    def start_pump(self):
        self.relay.value(1)  # Attiva il relè per avviare la pompa

    def stop_pump(self):
        self.relay.value(0)  # Spegne la pompa

"""
manca l'implementazione del sensore di umidità del suolo, dei metodi
per verificarlo che tengano conto e che funzionino in ogni momento,
quindi, vanno implmentati all'interno dei check e dell'allarme
"""
