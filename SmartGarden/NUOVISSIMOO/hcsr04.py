from machine import Pin, time_pulse_us
import time

class HCSR04:
    """
    Driver per il sensore HC-SR04. Misura distanze da 2 cm a 400 cm.
    """
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=30000):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.echo_timeout_us = echo_timeout_us

        # Imposta il pin trigger a LOW
        self.trigger.value(0)
        time.sleep(2)  # Attendi 2 secondi per la stabilizzazione del sensore

    def _send_pulse_and_wait(self):
        """
        Invia un impulso tramite il pin trigger e misura il tempo di ritorno sul pin echo.
        """
        # Invia impulso trigger di 10µs
        self.trigger.value(0)
        time.sleep_us(5)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        # Misura la durata del segnale high sul pin echo
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            return -1

    def distance_cm(self):
        """
        Restituisce la distanza misurata in centimetri.
        """
        pulse_time = self._send_pulse_and_wait()
        if pulse_time < 0:
            return -1
        else:
            # Velocità del suono: 34300 cm/s, diviso 2 (andata e ritorno)
            distance = (pulse_time / 2) / 29.1
            return distance