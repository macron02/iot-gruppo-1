import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient
import constraint_domain
import Allarmed_system, ControlSoilSys, Menu, NightFarm

# Definizione dei vincoli dei valori ambientali da rilevare
# Per la temperatura, range 5°C - 35°C, valore riferimento 18°C
temp_constraint = constraint_domain.constraint_domain(18, 5, 35)
# Per l'umidità dell'aria, range 10% - 90%, valore riferimento 40%
humid_constraint = constraint_domain.constraint_domain(40, 10, 90)

# MQTT Server Parameters
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

DHT_PIN = 25 #
LDR_PIN = 34 #
ECHO_PIN = 26
TRIG_PIN = 27
M0ISTURE_SOIL_SENSOR_PIN = 13 #
SCL_PIN = 22 #
SDA_PIN = 21 #
WATER_PIN = 19 #OUTPUT DI CONTROLLO DELLA POMPA DELL'ACQUA #
FAN_PIN = 18 #OUTPUT DI CONTROLLO PER LA VENTOLA #
SERVO_PIN = 2 #OUTPUT DI CONTROLLO DEL SERVO MOTORE

LED_NIGHT_PIN = 4 #led notturno #
#Led di Allarme
LED_BLUE1_PIN = 5 #
LED_RED1_PIN = 0 #
BUZZER_PIN = 16 #
BUTTON_RESET_PIN = 35 #
BUTTON_DISPLAY_PIN = 32 #
BUTTON_PUMP = 33 #bottone per irrigare manualmente #
BUTTON_SOIL = 15 #CAMBIO MODALITà TERRENO #

WATER_LEVEL_MIN = 2 """DA AGGIUNGERE""""

habitat_param = MyDHT.MyDHT(DHT_PIN, FAN_PIN, SERVO_PIN)
night_led = NightFarm.NightFarm(LED_NIGHT_PIN, LDR_PIN)
control_soil_sys = ControlSoilSys.ControlSoilSys(M0ISTURE_SOIL_SENSOR_PIN,
                                                WATER_PIN,BUTTON_PUMP,BUTTON_SOIL,M0ISTURE_SOIL_SENSOR_PIN,
                                                ECHO_PIN,TRIG_PIN, WATER_LEVEL_MIN)
allarme = Allarmed_system.Allarmed_system(BUZZER_PIN, LED_RED1_PIN, LED_BLUE1_PIN)
menu = Menu.Menu(SDA_PIN, SCL_PIN, BUTTON_DISPLAY_PIN, BUTTON_RESET_PIN)

def connect_to_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected to WiFi!")

def connect_to_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=MQTT_KEEPALIVE)
    while True:
        try:
            client.connect()
            print("Connected to MQTT server!")
            return client
        except OSError as e:
            print("Failed to connect to MQTT server, retrying in 5 seconds...")
            time.sleep(5)

# Connect to WiFi
connect_to_wifi()

# Connect to MQTT
client = connect_to_mqtt()

# Funzione di callback per la gestione dei messaggi MQTT ricevuti
def sub_cb(topic, msg):
    # Decode the incoming message and topic from bytes to string
    msg_str = msg.decode('utf-8')
    topic_str = topic.decode('utf-8')

    # Print the decoded topic and message for debugging
    print(f"Received message: '{msg_str}' on topic: '{topic_str}'")

    # Temperature constraint setting
    if topic_str == MQTT_TOPIC_SET_TEMP:
        temp_constraint.set_ref_value(float(msg_str))
        print("New default target temperature:", temp_constraint.get_value())

    # Humidity constraint setting
    elif topic_str == MQTT_TOPIC_SET_HUMID:
        humid_constraint.set_ref_value(float(msg_str))
        print("New default target humidity:", humid_constraint.get_value())

    else:
        print(f"Invalid topic: '{topic_str}'")


# Set the callback
client.set_callback(sub_cb)
client.subscribe(MQTT_TOPIC_SET_TEMP)
client.subscribe(MQTT_TOPIC_SET_HUMID)

# Publish default target values to MQTT
client.publish(MQTT_TOPIC_SHOW_TEMP, ujson.dumps(temp_constraint.get_value()))
client.publish(MQTT_TOPIC_SHOW_HUMID, ujson.dumps(humid_constraint.get_value()))
print("Default target temperature: {}°C".format(temp_constraint.get_value()))
print("Default target humidity: {}%".format(humid_constraint.get_value()))

menu.opening()
time.sleep(5)
menu.clear()
habitat_param.measure()
moist_sens = control_soil_sys.get_moist_sens()

prev_temp = habitat_param.temperature()
prev_humid = habitat_param.humidity()
prev_moisture = moist_sens.read_moisture_value()
prev_soil_mode = control_soil_sys.get_soil_mode()
menu.soil_mode(prev_soil_mode)

print("Measuring weather conditions... ", end="")

while True:
    night_led.night_light()
    control_soil_sys.watering_plant()
    habitat_param.checkGarden(temp_constraint.get_ref_value(), humid_constraint.get_ref_value())
    habitat_status = habitat_param.get_habitat_status()
    if( habitat_status["temp_status"] == 1 || habitat_status["humid_status"] == 1)
        menu.display_allarmed(habitat_status)
    else:
        menu.display_data(habitat_status)

    if prev_soil_mode != curr_soil_mode:
        menu.soil_mode(curr_soil_mode)
        prev_soil_mode = curr_soil_mode

    habitat_param.measure()
    curr_temp = habitat_param.temperature()  # Measured value from DHT22
    curr_humid = habitat_param.humidity()
    curr_moist = moist_sens.read_moisture_value()
    curr_soil_mode = control_soil_sys.get_soil_mode()

    message_temp = ujson.dumps(curr_temp)
    message_humid = ujson.dumps(curr_humid)
    message_moist = ujson.dumps(curr_moist)




    # Publish temperature if it's changed
    if curr_temp != prev_temp:
        print("Updated temperature!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_SHOW_TEMP, message_temp))
        client.publish(MQTT_TOPIC_SHOW_TEMP, message_temp)
        prev_temp = curr_temp

    # Publish humidity if it's changed
    if curr_humid != prev_humid:
        print("Updated humidity!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_SHOW_HUMID, message_humid))
        client.publish(MQTT_TOPIC_SHOW_HUMID, message_humid)
        prev_humid = curr_humid

    # Publish moisture if it's changed
    if curr_moist != prev_moisture:
            print("Updated moisture!")
            print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_SHOW_MOIST, message_moist))
            client.publish(MQTT_TOPIC_SHOW_MOIST, message_moist)
            prev_moisture = curr_moist


    # Check for messages from Node-RED
    try:
        client.check_msg()
    except OSError as e:
        print("Error checking messages: ", e)
        client = connect_to_mqtt()

    time.sleep(1)



"""aggiungere bottone per la pompa e pin"""
