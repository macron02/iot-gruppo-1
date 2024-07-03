import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython100"
MQTT_BROKER    = "test.mosquitto.org"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = ["1","2","3","4"]
#MQTT_LED = b'wokwi-setLed'

sensor = dht.DHT22(Pin(15)) 
#led = Pin(32, Pin.OUT)
#led.off()

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Lidia', 'helloworld')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

def subCallback(topic, msg):
  if topic == MQTT_LED:
    if msg == b'1':
      led.on()
    elif msg == b'0':
      led.off()

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
#client.set_callback(subCallback)
client.connect()
#client.subscribe(MQTT_LED)

print("Connected!")

prev_weather = ""
while True:
  client.check_msg()
  print("Measuring weather conditions... ", end="")
  sensor.measure()
  """Questa funzione è parte del modulo ujson (MicroJSON) in Python,
  che è un'implementazione di JSON.
  La funzione dumps() prende un oggetto Python (in questo caso, un dizionario)
  e lo converte in una stringa JSON."""
  message = ujson.dumps({
    "temp": sensor.temperature(),
    "humidity": sensor.humidity(),
  })
  if message != prev_weather:
    print("Updated!")
    print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
    client.publish(MQTT_TOPIC, message)
    prev_weather = message
  else:
    print("No change")
  time.sleep(1)