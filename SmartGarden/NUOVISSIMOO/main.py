import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient
import constraint_domain
import control_soil_sys, menu_system, habitat, plant, night_farm

# Oggetto pianta
my_plant = plant.plant()

# Definizione dei vincoli dei valori ambientali da rilevare
# Per la temperatura, range 5°C - 35°C, valore riferimento 18°C
temp_constraint = constraint_domain.constraint_domain(my_plant.get_plant_temp(), 35, 5)
# Per l'umidità dell'aria, range 10% - 90%, valore riferimento 40%
humid_constraint = constraint_domain.constraint_domain(my_plant.get_plant_hum(), 90, 10)

# Parametri del server MQTT
MQTT_CLIENT_ID = "TDM's smart garden"
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# TOPIC
MQTT_TOPIC_SET_TEMP = "g1/set_temperature"
MQTT_TOPIC_SET_HUMID = "g1/set_humidity"
MQTT_TOPIC_SHOW_TEMP = "g1/show_temperature"
MQTT_TOPIC_SHOW_HUMID = "g1/show_humidity"
MQTT_TOPIC_SHOW_MOIST = "g1/show_moisture"

# Lista dei Pin
DHT_PIN = 25
LDR_PIN = 34
ECHO_PIN = 26
TRIG_PIN = 27
M0ISTURE_SOIL_SENSOR_PIN = 12
SCL_PIN = 22
SDA_PIN = 21
WATER_PIN = 19
FAN_PIN = 18
SERVO_PIN = 2
LED_NIGHT_PIN = 4
LED_BLUE1_PIN = 5
LED_RED1_PIN = 15
BUZZER_PIN = 16
BUTTON_RESET_PIN = 35
BUTTON_DISPLAY_PIN = 32
BUTTON_PUMP = 33
WATER_LEVEL_MIN = 20

print("target 1")

menu = menu_system.menu_system(BUTTON_DISPLAY_PIN, BUTTON_RESET_PIN, SDA_PIN, SCL_PIN, BUZZER_PIN, LED_RED1_PIN, LED_BLUE1_PIN)

print("target 1.1")

def connect_to_wifi():
    print("Connecting to WiFi", end="")
    menu.connection_idle(True)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Tuttappost', 'Calamarata')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected to WiFi!")
    menu.connection_end_status(True)

def connect_to_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=MQTT_KEEPALIVE)
    while True:
        try:
            client.connect()
            print("Connected to MQTT server!")
            menu.connection_end_status(True)
            return client
        except OSError as e:
            print("Failed to connect to MQTT server, retrying in 5 seconds...")
            menu.connection_end_status(False)
            time.sleep(2)
            menu.connection_retrying()
            time.sleep(5)

# Connessione WiFi
connect_to_wifi()
menu.connection_idle(False)

# Connessione al server MQTT
client = connect_to_mqtt()

# Funzione di callback per la gestione dei messaggi MQTT ricevuti
def sub_cb(topic, msg):
    msg_str = msg.decode('utf-8')
    topic_str = topic.decode('utf-8')
    print(f"Received message: '{msg_str}' on topic: '{topic_str}'")

    if topic_str == MQTT_TOPIC_SET_TEMP:
        temp_constraint.set_ref_value(float(msg_str))
        print("New default target temperature:", temp_constraint.get_value())
    elif topic_str == MQTT_TOPIC_SET_HUMID:
        humid_constraint.set_ref_value(float(msg_str))
        print("New default target humidity:", humid_constraint.get_value())
    else:
        print(f"Invalid topic: '{topic_str}'")
print("target 2")

#Configurazione della callback e iscrizione ai topic MQTT
client.set_callback(sub_cb)
client.subscribe(MQTT_TOPIC_SET_TEMP)
client.subscribe(MQTT_TOPIC_SET_HUMID)

# Pubblicazione dei valori di riferimento iniziali
client.publish(MQTT_TOPIC_SHOW_TEMP, ujson.dumps(temp_constraint.get_ref_value()))
client.publish(MQTT_TOPIC_SHOW_HUMID, ujson.dumps(humid_constraint.get_ref_value()))
print("Default target temperature: {}°C".format(temp_constraint.get_ref_value()))
print("Default target humidity: {}%".format(humid_constraint.get_ref_value()))

menu.opening()
time.sleep(5)
menu.clear()

habitat_param = habitat.habitat(DHT_PIN, FAN_PIN, SERVO_PIN)

night_led = night_farm.night_farm(LED_NIGHT_PIN, LDR_PIN)
print("target 1.2")

control_soil_sys = control_soil_sys.control_soil_sys(WATER_PIN, BUTTON_PUMP, M0ISTURE_SOIL_SENSOR_PIN, ECHO_PIN, TRIG_PIN, WATER_LEVEL_MIN)

print("target 1.3")

print("target 1.4")

# Misura delle condizioni iniziali
habitat_param.check_habitat_status(temp_constraint.get_ref_value(), humid_constraint.get_ref_value())
moist_sens = control_soil_sys.get_moist_sens()
prev_temp = habitat_param.get_habitat_temperature()
prev_humid = habitat_param.get_habitat_humidity()
prev_moisture = control_soil_sys.get_moist_sens()

print("Measuring weather conditions... ", end="")

print("target 3")

while True:
    # Controllo delle luci notturne
    night_led.check_night()

    # Controllo dell'irrigazione
    control_soil_sys.watering_plant()

    # Misura delle condizioni attuali e aggiornamento dello stato dell'habitat
    habitat_param.check_habitat_status(temp_constraint.get_ref_value(), humid_constraint.get_ref_value())
    habitat_status = habitat_param.get_habitat_status()

    # Visualizzazione dello stato dell'habitat
    if habitat_status["temp_status"] == 1 or habitat_status["hum_status"] == 1:
        menu.display_allarmed(habitat_status)
    else:
        menu.display_data(habitat_status)
    print("target 4")
    # Pubblicazione delle misure su MQTT
    curr_temp = habitat_param.get_habitat_temperature()
    curr_humid = habitat_param.get_habitat_humidity()
    curr_moist = moist_sens.read_moisture_value()

    message_temp = ujson.dumps(curr_temp)
    message_humid = ujson.dumps(curr_humid)
    message_moist = ujson.dumps(curr_moist)

    # Pubblica la temperatura se è cambiata
    if curr_temp != prev_temp:
        print("Updated temperature!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_SHOW_TEMP, message_temp))
        client.publish(MQTT_TOPIC_SHOW_TEMP, message_temp)
        prev_temp = curr_temp

    # Pubblica l'umidità se è cambiata
    if curr_humid != prev_humid:
        print("Updated humidity!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_SHOW_HUMID, message_humid))
        client.publish(MQTT_TOPIC_SHOW_HUMID, message_humid)
        prev_humid = curr_humid

    # Pubblica l'umidità del terreno se è cambiata
    if curr_moist != prev_moisture:
        print("Updated moisture!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_SHOW_MOIST, message_moist))
        client.publish(MQTT_TOPIC_SHOW_MOIST, message_moist)
        prev_moisture = curr_moist

    # Controlla i messaggi MQTT in arrivo
    try:
        client.check_msg()
    except OSError as e:
        print("Error checking messages: ", e)
        client = connect_to_mqtt()

    time.sleep(1)
