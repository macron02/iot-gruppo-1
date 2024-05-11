from machine import Pin, I2C, ADC, reset
import dht
import ssd1306
import time

# Impostazione dei pin

######################################################################
#pin sensori
DHT_PIN = 25
PHOTORESISTOR_PIN = 34
ULTRASOUND_PIN = 26

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
LED_RED2_PIN = 16
LED_BLUE2_PIN = 5

######################################################################

# Pin dei bottoni
BUTTON_RESET_PIN = 35
BUTTON_DISPLAY_PIN = 32
"""BUTTON_THIRD_PIN = 33""" #bottone per irrigare manualmente
"""BUTTON_FOURTH_PIN = 15""" #a che serve???

######################################################################

#Inizializzazione

######################################################################

# Inizializza il sensore DHT
d = dht.DHT22(Pin(DHT_PIN))

######################################################################

# Inizializza il sensore a ultrasuoni

######################################################################

# Inizializza il display OLED
i2c = I2C(0, scl=Pin(21), sda=Pin(22))
oled = ssd1306.SSD1306_I2C(121, 64, i2c)

def display_data():
    d.measure()
    temp = d.temperature()
    humidity = d.humidity()
    oled.fill(0)
    if display_mode == 0:
        oled.setTextSize(1)  # Imposta la dimensione del testo a 1
        oled.text('Temp: %s C' % temp, 0, 0)
        oled.text('Humidity: %s %%' % humidity, 0, 10)
    elif display_mode == 1:
        oled.setTextSize(2)  # Imposta la dimensione del testo a 2
        oled.text('Temp: %s C' % temp, 0, 0)
    elif display_mode == 2:
        oled.setTextSize(2)  # Imposta la dimensione del testo a 2
        oled.text('Humidity: %s %%' % humidity, 0, 0)
    oled.show()

    """
    implementare un passaggio con la classe smartcheck per stampare la temperatura a schermo con le sue modalità
    insomma, spostare la definizione delle modalità nella classe smartcheck e inizializzare lì l'oled
    """

######################################################################
#Inizializza la Pompa
water = Pin(WATER_PIN, Pin.OUT)
fan =   # Imposta i pin corretti per la tua configurazione

######################################################################
# Inizializza i LED
led = Pin(LED_PIN, Pin.OUT)

led_blue1 = Pin(LED_BLUE1_PIN, Pin.OUT)
led_red1 = Pin(LED_RED1_PIN, Pin.OUT)
led_red2 = Pin(LED_RED2_PIN, Pin.OUT)
led_blue2 = Pin(LED_BLUE2_PIN, Pin.OUT)

######################################################################
# Inizializza il fotoresistore
photoresistor = ADC(Pin(PHOTORESISTOR_PIN))
photoresistor.atten(ADC.ATTN_11DB)  # Imposta la gamma di lettura da 0 a 3.3V

######################################################################
# Inizializza i bottoni
button_reset = Pin(BUTTON_RESET_PIN, Pin.IN, Pin.PULL_UP)
button_display = Pin(BUTTON_DISPLAY_PIN, Pin.IN, Pin.PULL_UP)
button_third = Pin(BUTTON_THIRD_PIN, Pin.IN, Pin.PULL_UP)
button_fourth = Pin(BUTTON_FOURTH_PIN, Pin.IN, Pin.PULL_UP)

######################################################################

#Variabili, soglie e costanti

######################################################################
# Soglia di luminosità
THRESHOLD_VALUE = 500 "sicuro??"

######################################################################
# Variabile per tenere traccia della modalità del display
display_mode = 0

######################################################################
######################################################################
######################################################################
######################################################################
######################################################################


def check_light():
    photoresistor_value = photoresistor.read()
    if photoresistor_value < THRESHOLD_VALUE:
        led.on()
    else:
        led.off()


"""errori a display"""
"""controllo livello dell'acqua"""

def check_buttons_reset():
    if not button_reset.value():
        reset()
        """DA IMPLEMENTARE IL RESET"""

def check_buttons():
    """RIVEDERE!!!"""
    global display_mode
    if not button_display.value():
        display_mode = (display_mode + 1) % 3
    # Aggiungi qui le azioni per gli altri bottoni

while True:
    check_light()
    check_temp()
    check_buttons()
    display_data()
    time.sleep(1)
