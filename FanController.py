from machine import Pin
import time
import machine

class FanController:
    """
    Definizione della classe per il controllo della ventola
    """
    def __init__(self,relay_pin):
        """relay_pyn: pin per il controllo del relé che comanda l'accensione della ventola"""
        self.relay = Pin(relay_pin, Pin.OUT)

    def start_fan(self):
        self.relay.value(1)  # Attiva il relé, quindi accende la ventola
    

    def stop_fan(self):
        self.relay.value(0)  # Disattiva il relé, quindi spegne la ventola