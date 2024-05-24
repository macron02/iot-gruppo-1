from machine import Pin, I2C, ADC, reset
import dht
import ssd1306
import SmartCheck
import time

# Impostazione dei pin

######################################################################
#pin sensori
DHT_PIN = 25
PHOTORESISTOR_PIN = 34
ULTRASOUND_PIN1 = 26
ULTRASOUND_PIN1 = 27
M0ISTURE_SOIL_SENSOR_PIN1 = 13
M0ISTURE_SOIL_SENSOR_PIN3 = 14
SCL_PN = 22
SDA_PIN = 21

######################################################################
#pin output di controllo delle parti

RELAY_WATER_PIN = 19 #OUTPUT DI CONTROLLO DELLA POMPA DELL'ACQUA
FAN_PIN = 18 #OUTPUT DI CONTROLLO PER LA VENTOLA
SERVO_PIN = 2 #OUTPUT DI CONTROLLO DEL SERVO MOTORE
RELAY_FAN_PIN = 17
"""ALTRI ED EVENTUALI OUTPUT DI CONTROLLO DEVONO ESSERE IMPLEMENTATI QUI"""

######################################################################

#pin led

LED_NIGHT_PIN = 4 #led notturno
#Led di Allarme
LED_BLUE1_PIN = 15
LED_RED1_PIN = 0
BUZZER_PIN = 16

######################################################################

# Pin dei bottoni
BUTTON_RESET_PIN = 35
BUTTON_DISPLAY_PIN = 32
"""BUTTON_THIRD_PIN = 33""" #bottone per irrigare manualmente
"""BUTTON_FOURTH_PIN = 15""" #a che serve???

######################################################################

#Inizializzazione
######################################################################

# Inizializza il display OLED
i2c = I2C(0, scl=SCL_PIN, sda=SDA_PIN)
oled = ssd1306.SSD1306_I2C(121, 64, i2c)

######################################################################
#Inizializza la Pompa

######################################################################
# Inizializza i LED
led = Pin(LED_PIN, Pin.OUT)

######################################################################
# Inizializza il fotoresistore
photoresistor = ADC(Pin(PHOTORESISTOR_PIN))
photoresistor.atten(ADC.ATTN_11DB)  # Imposta la gamma di lettura da 0 a 3.3V

######################################################################
# Inizializza i bottoni
button_reset = Pin(BUTTON_RESET_PIN, Pin.IN, Pin.PULL_UP)

button_third = Pin(BUTTON_THIRD_PIN, Pin.IN, Pin.PULL_UP)
button_fourth = Pin(BUTTON_FOURTH_PIN, Pin.IN, Pin.PULL_UP)

######################################################################

#Variabili, soglie e costanti

######################################################################
# Soglia di luminosità


######################################################################
# Variabile per tenere traccia della modalità del display

Habitat = SmartCheck.check_habitat_sys(DHT_PIN,FAN_PIN, SCL_PIN, SDA_PIN, BUTTON_DISPLAY_PIN, BUZZER_PIN, LED_BLUE1_PIN, LED_RED1_PIN)

######################################################################
######################################################################
######################################################################
######################################################################
######################################################################

"""
def check_light():
    photoresistor_value = photoresistor.read()
    if photoresistor_value < THRESHOLD_VALUE:
        led.on()
    else:
        led.off()



def check_buttons_reset():
    if not button_reset.value():
        machine.reset()
        

    # Aggiungi qui le azioni per gli altri bottoni

while True:
    check_light()
    check_temp()
    check_buttons()
    display_data()
    time.sleep(1)


class temperature_domain:
    def __init__(self):
        self.min_value = 5
        self.max_value = 35
        self.value = 18

    def set_temp(self, new_temp):
        if self.min_value <= new_temp <= self.max_value:
            self.value = new_value

        else:
            print(f"Valore {new_value} fuori dal range consentito ({self.min_value} - {self.max_value})")


class humidity_domain:
    def __init__(self):
        self.min_value = 5
        self.max_value = 95
        self.value = 40

    def set_umid(self, new_umid):
        if self.min_value <= new_umid <= self.max_value:
            self.value = new_umid
        else:
            print(f"Valore {new_value} fuori dal range consentito ({self.min_value} - {self.max_value})")

#Implementare di nuovo la classe dei domini, bisogna inizializzare le soglie nel main e poi passarle come parametri quando chiamiamo i metodi
            
"""

while True:
    
    check(20, 40)
    