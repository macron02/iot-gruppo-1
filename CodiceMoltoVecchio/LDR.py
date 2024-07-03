from machine import Pin
import time
import machine

class LDR:
    """Questa classe legge un valore da una resistenza dipendente dalla luce (LDR)"""
    def __init__(self, pin, min_value=0, max_value=100):
        """ Controlla che il valore minimo sia inferiore al valore massimo """
        if min_value >= max_value:
            raise ValueError('Il valore minimo è maggiore o uguale al valore massimo')
        """ Inizializza il convertitore analogico-digitale (ADC) con il pin specificato """
        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value
            
    def read(self):
        """ Legge il valore analogico dal sensore LDR """
        return self.adc.read()
    
    def value(self):
        """ Calcola e restituisce il valore di luminosità normalizzato tra min_value e max_value """
        return (self.max_value - self.min_value) * self.read() / 4095
