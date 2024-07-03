from machine import Pin
import time
import machine


class HCSR04:
    """
    Definizione del driver per il sensore HC-SR04
    Range sensore -> 2cm : 400cm
    """

    def __init__(self, trigger_pin, echo_pin, echot_timeout_us = 30_000):
        """
        trigger_pin: output pin per inviare inpulsi
        echo_pin: input pin che misura la distanza
        echo_timeout_us: attesa di ascolto in microsecondi pin echo
        """

        self.echo_timeout_us = echot_timeout_us

        # Inizializzazione del pin trigger (output)
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.trigger.value(0)

        # Inizializzazione del pin echo (input)
        self.echo = Pin(echo_pin, Pin.IN)


    def send_and_wait(self):
        """
        Invia un impulso da parte del pin trigger
        e rimane in ascolto sul pin echo.
        """

        self.trigger.value(0)
        time.sleep_us(5)
        self.trigger.value(1)

        time.sleep_us(10)
        self.trigger.value(0)

        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            raise ex

    def distance_mm(self):
        """
        Acquisizione della distanza in millimetri (valore intero)
        """

        pulse_time = self.send_and_wait()

        mm = pulse_time*100//582
        return mm
