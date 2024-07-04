from machine import Pin, ADC
import time

class MoistureSoilSensor:
    """Questa classe legge un valore da un sensore di umidità del suolo"""

    def __init__(self, ms_sensor_pin, min_value=0, max_value=4095):
        """Inizializza il convertitore analogico-digitale (ADC) con il pin specificato e imposta i valori minimo e massimo"""
        if min_value >= max_value:
            raise ValueError('Il valore minimo deve essere inferiore al valore massimo')
        self.adc = ADC(Pin(ms_sensor_pin))
        self.adc.atten(ADC.ATTN_11DB)       # attenuatore
        self.adc.width(ADC.WIDTH_12BIT)     # larghezza di banda
        self.min_moisture = min_value
        self.max_moisture = max_value

    def read_moisture_value(self):
        """Legge il valore di umidità del suolo e lo stampa in percentuale"""
        return ((self.max_moisture - self.adc.read()) * 100 / (self.max_moisture - self.min_moisture))
