from machine import Pin, ADC
import time

class ldr:
    """Questa classe legge un valore da una resistenza dipendente dalla luce (LDR)"""
    def __init__(self, pin, min_value=0, max_value=100):
        """ Controlla che il valore minimo sia inferiore al valore massimo """
        if min_value >= max_value:
            raise ValueError('Il valore minimo è maggiore o uguale al valore massimo')
        """ Inizializza il convertitore analogico-digitale (ADC) con il pin specificato """
        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value

    def read_light_value(self):
        """Legge il valore di umidità del suolo e lo stampa in percentuale"""
        return ((self.max_value - self.adc.read()) * 100 / (self.max_value - self.min_value))
