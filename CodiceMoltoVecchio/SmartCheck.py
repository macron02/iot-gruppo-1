from machine import Pin, I2C, ADC, reset, PWM
import dht
import time
import ssd1306
import AllarmeHabitat from Allarmed_system
import my_domain



class check_habitat_sys:

    """
    Classe per il controllo della temperatura dove viene inizializzato il sensore DHT22
    e vengono implementati i metodi che eseguono tutti i controllo e le azioni necessarie al caso
    """
    def __init__(self, pin_dht,fan_pin, pin_scl_oled, pin_sda_oled, button_display_pin, pin_buzzer, red_led_pin_, blue_led_pin_):

        sensor = dht.DHT22(Pin(pin_dht))

        fan = FanController(fan_pin)

        previus_humid = imp_humidity
        previus_temp = imp_temperature

        i2c = I2C(0, scl=Pin(pin_scl_oled), sda=Pin(pin_sda_oled))
        oled = ssd1306.SSD1306_I2C(121, 64, i2c)

        """ Configura il pin del pulsante come input """
        button_display = Pin(button_display_pin, Pin.IN, Pin.PULL_UP)
        """ Imposta un'interrupt sul fronte di discesa, chiamando la funzione switch """
        button_display.irq(trigger=Pin.IRQ_FALLING, handler=check_buttons)
        """ inizializzazione variabile per il controllo della modalità di stampa"""
        display_mode = 1

        allarme = AllarmeHabitat(pin_buzzer, pin_led1, pin_led2, pin_dht, pin_scl_oled, pin_sda_oled)

    def check_buttons(button_display):
        global display_mode
        if not button_display.value():
            if display_mode < 3:
                display_mode = (display_mode + 1)
            else display_mode = 1


    def display_data(temperature, humidity):
        global display_mode
        oled.fill(0)
        if display_mode == 1:
            oled.setTextSize(1)  # Imposta la dimensione del testo a 1
            oled.text('Temp: %s C' % temperature, 0, 0)
            oled.text('Humidity: %s %%' % humidity, 0, 10)
        elif display_mode == 2:
            oled.setTextSize(2)  # Imposta la dimensione del testo a 2
            oled.text('Temp: %s C' % temperature, 0, 0)
        elif display_mode == 3:
            oled.setTextSize(2)  # Imposta la dimensione del testo a 2
            oled.text('Humidity: %s %%' % humidity, 0, 0)
        oled.show()

     def check(imp_temperature, imp_humidity):
         """
         metodo per la misurazione e seguente check sui dati misurati
         """
         sensor.measure()
         try:
             humidity, temperature = sensor.read()
         except OSError as e:
             oled.print(f"Errore durante la lettura del sensore: {e.strerror}")

         if humidity is not None and temperature is not None:
             display_data(temperature, humidity)
             if (temp_meas != previus_temp):
                 check_temp(temperature,imp_temperature)
                 previus_temp = temperature
             if (humid_meas != previus_humid):
                  check_humid(humidity,imp_humidity)
                  previus_humid = humidity
             #controlla sia corretto
         else:
             print("Errore durante la lettura dei dati.")

             """
             Implementare la stampa sull'oled dopo averlo portato in questa classe
             """

    def check_temp(temp_meas,imp_temperature,previus_temp):

        if temp_meas > imp_temperature:
            """
            chiama la funzione check_hot che controlla se la temperatura è effettivamente troppo alta rispetto a quela desiderata
            """
            check_hot(temp_meas,imp_temperature)
            return NULL
        else temp_meas < imp_temperature:
            """
            chiama la funzione check_cold che controlla se la temperatura è effettivamente troppo bassa rispetto a quela desiderata
            """
            check_cold(temp_meas,imp_temperature)
            return NULL

    def check_humid(humid_meas,imp_humidity):
        if humid_meas > imp_humidity:
            """
            chiama la funzione check_moist che controlla se l'umidità è effettivamente troppo alta rispetto a quela desiderata
            """
            check_moist(humid_meas)
            return NULL
        elif humid_meas < imp_humidity:
            """
            chiama la funzione check_dry che controlla se l'umidità è effettivamente troppo bassa rispetto a quela desiderata
            """
            check_dry(humid_meas)
            return NULL


    def check_hot(temp_meas, imp_temperature):
        """
        verifica se la temperatura è maggiore a quella desiderata
        """
        if temp_meas > (imp_temperature*1.2):
            fan.start_fan_base()
            if temp_meas >= [(imp_temperature*1.2)*1.2]:
                fan.start_fan_max()
                allarme.attiva_allarme(imp_temperature, imp_humidity)

    def check_cold(temp_meas,imp_temperature):
        """
        verifica se la temperatura è inferiore a quella desiderata
        """
        if temp_meas < (imp_temperature*0.8):
            #azione da eseguire quando troppo asciutto
            if temp_meas <= [(imp_temperature*0.8)*0.8]:
                allarme.attiva_allarme(imp_temperature, imp_humidity)

    def check_moist(humid_meas,imp_humidity):
        """
        verifica se l'umidità è maggiore a quella desiderata
        """
        if humid_meas > (imp_humidity*1.2):
            fan.start_fan()
            if humid_meas >= ((imp_humidity*1.2)*1.2):
                allarm_mode = 1
                allarme.attiva_allarme(imp_temperature, imp_humidity)

    def check_dry(humid_meas,imp_humidity):
        """
        verifica se l'umidità è inferiore a quella desiderata
        """
        if humid_meas < (imp_humidity*0.8):
            #azione da eseguire quando troppo asciutto
            if humid_meas <= [(imp_humidity*0.8)*0.8]:
                allarme.attiva_allarme(imp_temperature, imp_humidity)

class ControllWater:
    def __init__(self, red_led_pin, trigger_pin, echo_pin):
        self.red_led = Pin(red_led_pin, Pin.OUT)
        self.us_sensor = HCSR04(trigger_pin, echo_pin)

    def waterCheck():

        misura = us_sensor.distance_mm()

        if misura < min_water:
            red_led.on()
        else:
            red_led.off()
