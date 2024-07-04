from machine import Pin, ADC
import time

class MoistureSoilSensor:
    """Questa classe legge un valore da un sensore di umidità del suolo."""

    def __init__(self, ms_sensor_pin, min_value=0, max_value=4095):
        """
        Inizializza il convertitore analogico-digitale (ADC) con il pin specificato e imposta i valori minimo e massimo.
        :param ms_sensor_pin: Il pin a cui è collegato il sensore di umidità del suolo.
        :param min_value: Il valore minimo di umidità (valore ADC corrispondente a 0%).
        :param max_value: Il valore massimo di umidità (valore ADC corrispondente a 100%).
        """
        if min_value >= max_value:
            raise ValueError('Il valore minimo deve essere inferiore al valore massimo')

        self.adc = ADC(Pin(ms_sensor_pin))
        self.min_moisture = min_value
        self.max_moisture = max_value
        self.ref_value_moisture = 50  # Valore di riferimento predefinito

    def read_moisture_value(self):
        """
        Legge il valore di umidità del suolo e lo restituisce in percentuale.
        :return: Valore di umidità del suolo in percentuale.
        """
        raw_value = self.adc.read()
        if raw_value < self.min_moisture:
            raw_value = self.min_moisture
        elif raw_value > self.max_moisture:
            raw_value = self.max_moisture

        # Calcolo della percentuale di umidità
        moisture_percentage = ((raw_value - self.min_moisture) * 100) / (self.max_moisture - self.min_moisture)
        return moisture_percentage

    def get_ref_value_moisture(self):
        """
        Restituisce il valore di riferimento dell'umidità del suolo.
        :return: Valore di riferimento dell'umidità del suolo.
        """
        return self.ref_value_moisture

    def set_ref_value_moisture(self, new_moisture):
        """
        Imposta un nuovo valore di riferimento per l'umidità del suolo.
        :param new_moisture: Il nuovo valore di riferimento per l'umidità del suolo.
        """
        self.ref_value_moisture = new_moisture
