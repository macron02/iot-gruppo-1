from machine import Pin, ADC
import time

class moisture_soil_sensor:
    """Questa classe legge un valore da un sensore di umidità del suolo."""

    def __init__(self, ms_sensor_pin, min_value=260, max_value=520):
        """
        Inizializza il convertitore analogico-digitale (ADC) con il pin specificato e imposta i valori minimo e massimo.
        ms_sensor_pin: Il pin a cui è collegato il sensore di umidità del suolo.
        min_value: Il valore minimo di umidità (valore ADC corrispondente a terreno completamente bagnato).
        max_value: Il valore massimo di umidità (valore ADC corrispondente a terreno completamente secco).
        Dal datasheet del sensore (Capacitive Moisture Soil Sensor) sappiamo che il range per determinare
        l'umidità del suolo si divide in 3 stati dry, wet, water.
        I loro relativi valori sono:
            Dry in range [520, 430] cioé tra 0-34.62%
            Wet in range [430, 350] cioé tra 34.62-65.38%
            Full_Wet in range [350, 260] cioé tra 65.38-100%
        """
        if min_value >= max_value:
            raise ValueError('Il valore minimo deve essere inferiore al valore massimo')
        self.adc = ADC(Pin(ms_sensor_pin))
        self.adc.atten(ADC.ATTN_11DB)  # Imposta l'attenuazione a 11dB
        self.adc.width(ADC.WIDTH_10BIT)  # Imposta la larghezza a 10 bit
        self.min_moisture = min_value
        self.max_moisture = max_value

    def read(self):
        """
        Lettura del sensore
        """
        raw_value = self.adc.read()
        # Scala il valore grezzo per mappare l'intervallo 0-1023 al range 260-520
        scaled_value = int((raw_value / 1023.0) * (self.max_moisture - self.min_moisture) + self.min_moisture)
        return scaled_value

    def read_moisture_value(self):
        """
        Legge il valore di umidità del suolo e lo restituisce in percentuale.
        """
        raw_value = self.read()
        print(f"Valore scalato letto dal sensore: {raw_value}")  # Aggiungi questa linea per la diagnostica

        if raw_value < self.min_moisture:
            raw_value = self.min_moisture
        elif raw_value > self.max_moisture:
            raw_value = self.max_moisture

        """
        Calcolo della percentuale di umidità invertita per trovare il
        massimo grado di umidità del suolo al 100% (full_wet) e il minimo allo 0% (dry)
        """
        moisture_percentage = 100 - ((raw_value - self.min_moisture) * 100) / (self.max_moisture - self.min_moisture)
        return moisture_percentage

    def soil_condition(self):
        """
        Determina lo stato del suolo (dry, wet, water) e se è necessario irrigare.
        """
        moisture_percentage = self.read_moisture_value()
        if moisture_percentage < 34.62:
            return "Dry" # È necessario irrigare.
        elif 34.62 <= moisture_percentage <= 65.38:
            return "Wet" # Il terreno è umido
        else:
            return "Water" # Il terreno è bagnato.
        
# Codice per testare la classe
pin = 12
sensor = moisture_soil_sensor(pin)

while True:
    moisture_percentage = sensor.read_moisture_value()
    condition = sensor.soil_condition()
    print(f"Umidità del suolo: {moisture_percentage:.2f}% - Condizione del suolo: {condition}")
    time.sleep(2)