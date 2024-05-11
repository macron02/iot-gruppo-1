from machine import Pin, I2C, ADC, reset, PWM
import dht
import time
import ssd1306
import Allarmed_system
import my_domain



class check_habitat_sys:

    """
    Classe per il controllo della temperatura dove viene inizializzato il sensore DHT22
    e vengono implementati i metodi che eseguono tutti i controllo e le azioni necessarie al caso
    """
    def __init__(pin_dht,fan_pin, water_pin):

        sensor = dht22.DHT(Pin(pin_dht))

        fan = FanController(fan_pin)

        imp_temperature = temperature_domain()
        imp_humidity = humidity_domain()


    def set_temp_check(new_temp):

        imp_temperature = set_humid(new_temp)

        """
        metodo per modificare la temperatura impostata
        """

    def set_humid_check(new_humid):

        imp_humidity = set_humid(new_humid)
        """
        metodo per modificare l'umidità impostata
        """

     def check():
         """
         metodo per la misurazione e seguente check sui dati misurati
         """
         sensor.measure()
         try:
             humidity, temperature = sensor.read()
         except OSError as e:
             oled.print(f"Errore durante la lettura del sensore: {e.strerror}")

         if humidity is not None and temperature is not None:
             check_temp(humidity)
             check_humid(temperature)
         else:
             print("Errore durante la lettura dei dati.")

             """
             Implementare la stampa sull'oled dopo averlo portato in questa classe
             """

    def check_temp(temp_meas):
        """
        check sulla temepratura
        """
        if (temp_meas != previus_temp):
            if temp_meas >= imp_temperature:
                check_hot(temp_meas)
                """
                chiama la funzione check_hot che controlla se la temperatura è effettivamente troppo alta rispetto a quela desiderata
                """
            elif temp_meas <= imp_temperature:
                """
                chiama la funzione check_cold che controlla se la temperatura è effettivamente troppo bassa rispetto a quela desiderata
                """
                check_cold(temp_meas)
            else:
                """
                chiama la funzione check_out_temp che controlla, termina e ferma le azioni conseguenti al controllo della temperatira
                """
                check_out_temp(temp_meas)

    def check_humid(humid_meas):

        if (humid_meas != previus_humid):
            if humid_meas >= imp_humidity:
                """
                chiama la funzione check_moist che controlla se l'umidità è effettivamente troppo alta rispetto a quela desiderata
                """
                check_moist(humid_meas)
            elif humid_meas <= imp_humidity:
                """
                chiama la funzione check_dry che controlla se l'umidità è effettivamente troppo bassa rispetto a quela desiderata
                """
                check_dry(humid_meas)
            else:
                """
                chiama la funzione check_out_humid che controlla, termina e ferma le azioni conseguenti al controllo dell'umidità
                """
                check_out_humid(humid_meas)

    def check_hot(temp_meas):
        """
        verifica se la temperatura è maggiore a quella desiderata
        """
        if temp_meas > (imp_temperature*1.2):
            fan.start_fan()
            if temp_meas >= [(imp_temperature*1.2)*1.2]:
                allarm_mode = 1
                allarm_system()

    def check_cold(temp_meas):
        """
        verifica se la temperatura è inferiore a quella desiderata
        """
        if temp_meas < (imp_temperature*0.8):
            #azione da eseguire quando troppo asciutto
            if temp_meas <= [(imp_temperature*0.8)*0.8]:
                allarm_mode = 1
                allarm_system()

    def check_moist(humid_meas):
        """
        verifica se l'umidità è maggiore a quella desiderata
        """
        if humid_meas > (imp_humidity*1.2):
            fan.start_fan()
            if humid_meas >= [(imp_humidity*1.2)*1.2]:
                allarm_mode = 1
                allarm_system()

    def check_dry(humid_meas):
        """
        verifica se l'umidità è inferiore a quella desiderata
        """
        if humid_meas < (imp_humidity*0.8):
            #azione da eseguire quando troppo asciutto
            if humid_meas <= [(imp_humidity*0.8)*0.8]:
                allarm_mode = 1
                allarm_system()

    def check_out_temp(temp_meas):

        if temp_meas >= (imp_temp*0.8) and temp_meas <= (imp_temp*1.2):
            """
            implementare i controlli sulla ventola e sull'allarme per terminarli
            """


    def check_out_humid(humid_meas):

        if humid_meas >= (imp_humid*0.8) and humid_meas <= (imp_humid*1.2):
            """
            implementare i controlli sulla ventola e sull'allarme per terminarli
            """
