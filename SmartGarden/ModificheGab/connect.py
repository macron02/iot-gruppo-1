import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient
import constraint_domain


temp_constraint = constraint_domain.constraint_domain(18, 5, 35)
humid_constraint = constraint_domain.constraint_domain(40, 10, 90)

# MQTT Server Parameters
MQTT_CLIENT_ID = "TDM's smart garden"
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_TOPIC_TEMP = "g1/temperature"
MQTT_TOPIC_HUMID = "g1/humidity"
MQTT_TOPIC_SET_TEMP = "g1/set_temperature"
MQTT_TOPIC_SET_HUMID = "g1/set_humidity"
MQTT_TOPIC_DEF_TEMP = "g1/deftemperature"
MQTT_TOPIC_DEF_HUMID = "g1/defhumidity"

DHT_PIN = 25
PHOTORESISTOR_PIN = 34
ULTRASOUND_PIN1 = 26
ULTRASOUND_PIN2 = 27
M0ISTURE_SOIL_SENSOR_PIN = 13
SCL_PIN = 22
SDA_PIN = 21
WATER_PIN = 19 #OUTPUT DI CONTROLLO DELLA POMPA DELL'ACQUA
FAN_PIN = 18 #OUTPUT DI CONTROLLO PER LA VENTOLA
SERVO_PIN = 2 #OUTPUT DI CONTROLLO DEL SERVO MOTORE

LED_NIGHT_PIN = 4 #led notturno
#Led di Allarme
LED_BLUE1_PIN = 15
LED_RED1_PIN = 0
BUZZER_PIN = 16
BUTTON_RESET_PIN = 35
BUTTON_DISPLAY_PIN = 32
BUTTON_PUMP = 33 #bottone per irrigare manualmente
BUTTON_SOIL = 15 #CAMBIO MODALITà TERRENO
LDR_PIN = #DA AGGIUNGERE!!!!

WATER_LEVEL = O """DA AGGIUNGERE""""

sensore_ambiente = MyDHT.MyDHT(DHT_PIN, FAN_PIN, SERVO_PIN)
night_led = NightFarm.NightFarm(LED_NIGHT_PIN, LDR_PIN)
sensore_terreno = ControlSoilSys.ControlSoilSys(M0ISTURE_SOIL_SENSOR_PIN,
                                                WATER_PIN,BUTTON_PUMP,BUTTON_SOIL,M0ISTURE_SOIL_SENSOR_PIN,
                                                ULTRASOUND_PIN1,ULTRASOUND_PIN2, WATER_LEVEL)
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

"""
# Funzione di callback per la gestione dei messaggi MQTT ricevuti
def subCallback(topic, msg):
    # Decode the incoming message and topic from bytes to string
    msg_str = msg.decode('utf-8')
    topic_str = topic.decode('utf-8')

    # Print the decoded topic and message for debugging
    print(f"Received message: '{msg_str}' on topic: '{topic_str}'")

    # Servo control
    if topic_str== MQTT_TOPIC[1]:
        if msg_str == 'true':
            alarm.food_refill()
            servo.rotate(0,100)
        elif msg_str == 'false':
            servo.rotate(0,100,-1)
        else:
            print(f"Invalid message for servo control: '{msg_str}'")

    # Water pump control
    elif topic_str == MQTT_TOPIC[2]:
        if msg_str == 'true':
            alarm.water_trig_flow()
            water_pump.activate_pump(True) # attivo
        elif msg_str == 'false':
            water_pump.activate_pump(False) # disattivo
        else:
            print(f"Invalid message for water pump control: '{msg_str}'")

"""

# Callback function to handle incoming messages
def sub_cb(topic, msg):
    global temp_constraint, humid_constraint
    if topic == MQTT_TOPIC_SET_TEMP.encode():
        temp_constraint.set_value(float(msg))
        print("New default target temperature:", temp_constraint.get_value())
    elif topic == MQTT_TOPIC_SET_HUMID.encode():
        humid_constraint.set_value(float(msg))
        print("New default target humidity:", humid_constraint.get_value())

# Set the callback
client.set_callback(sub_cb)
client.subscribe(MQTT_TOPIC_SET_TEMP)
client.subscribe(MQTT_TOPIC_SET_HUMID)

# Publish default target values to MQTT
client.publish(MQTT_TOPIC_DEF_TEMP, ujson.dumps(temp_constraint.get_value()))
client.publish(MQTT_TOPIC_DEF_HUMID, ujson.dumps(humid_constraint.get_value()))
print("Default target temperature: {}°C".format(temp_constraint.get_value()))
print("Default target humidity: {}%".format(humid_constraint.get_value()))

prev_temp = None
prev_humid = None

print("Measuring weather conditions... ", end="")

while True:
    sensor.measure()
    measured_temp = sensor.temperature()  # Measured value from DHT22
    humid = sensor.humidity()
    message_temp = ujson.dumps(measured_temp)
    message_humid = ujson.dumps(humid)

    # Publish temperature if it's changed
    if measured_temp != prev_temp:
        print("Updated temperature!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_TEMP, message_temp))
        client.publish(MQTT_TOPIC_TEMP, message_temp)
        prev_temp = measured_temp

    # Publish humidity if it's changed
    if humid != prev_humid:
        print("Updated humidity!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC_HUMID, message_humid))
        client.publish(MQTT_TOPIC_HUMID, message_humid)
        prev_humid = humid

    # Check for messages from Node-RED
    try:
        client.check_msg()
    except OSError as e:
        print("Error checking messages: ", e)
        client = connect_to_mqtt()

    time.sleep(1)



"""aggiungere bottone per la pompa e pin"""
