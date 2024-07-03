import network
import socket
import ure
import time
import os
import json

from ConstraintDomain import ConstraintDomain
from Pump import PumpController
from FanController import FanController
from MyDHT import DHTSensor

# Configura la tua rete WiFi utilizzando variabili di ambiente
ssid = os.getenv('WIFI_SSID', 'default_SSID')
password = os.getenv('WIFI_PASSWORD', 'default_PASSWORD')

# File per conservare le informazioni sulla pianta
plant_info_file = 'plant_info.json'

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        time.sleep(1)

    print('Connection successful')
    print(wlan.ifconfig())
    return wlan

def create_server_socket():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)
    return s

def load_plant_info():
    if os.path.exists(plant_info_file):
        with open(plant_info_file, 'r') as file:
            return json.load(file)
    return {}

def save_plant_info(plant_info):
    with open(plant_info_file, 'w') as file:
        json.dump(plant_info, file)

def handle_request(request, temp_constraint, hum_constraint, pump_ctrl, fan_ctrl):
    if b'infosystem' in request:
        temperature = temp_constraint.def_value  # Replace with actual sensor reading
        humidity = hum_constraint.def_value      # Replace with actual sensor reading
        plant_info = load_plant_info()
        plant_name = plant_info.get('name', 'N/A')
        return f"Informazioni sull'ambiente:\n- Temperatura: {temperature}°C\n- Umidità: {humidity}%\n- Pianta: {plant_name}"

    elif b'newtemperature' in request:
        match = ure.search(r'/newtemperature (\d+)', request)
        if match:
            new_temp = int(match.group(1))
            temp_constraint.set_value(new_temp)
            return f"Nuova temperatura impostata: {new_temp}"
        else:
            return "Formato non valido. Utilizzare /newtemperature [valore]"

    elif b'newhumidity' in request:
        match = ure.search(r'/newhumidity (\d+)', request)
        if match:
            new_humidity = int(match.group(1))
            hum_constraint.set_value(new_humidity)
            return f"Nuova umidità impostata: {new_humidity}"
        else:
            return "Formato non valido. Utilizzare /newhumidity [valore]"

    elif b'newplant' in request:
        match = ure.search(r'/newplant (\w+)', request)
        if match:
            plant_name = match.group(1)
            plant_info = load_plant_info()
            plant_info['name'] = plant_name
            save_plant_info(plant_info)
            return f"Nuova pianta impostata: {plant_name}"
        else:
            return "Formato non valido. Utilizzare /newplant [nome_pianta]"

    elif b'startpump' in request:
        pump_ctrl.start_pump()
        return "Pompa avviata"

    elif b'startfan' in request:
        fan_ctrl.start_fan()
        return "Ventola avviata"

    elif b'stoppump' in request:
        pump_ctrl.stop_pump()
        return "Pompa fermata"

    elif b'stopfan' in request:
        fan_ctrl.stop_fan()
        return "Ventola fermata"

    return "Comando non valido"

def automatic_control(temp_constraint, hum_constraint, pump_ctrl, fan_ctrl, dht_sensor):
    temperature, humidity = dht_sensor.read()

    if temperature > temp_constraint.max_value:
        fan_ctrl.start_fan()
    elif temperature < temp_constraint.min_value:
        fan_ctrl.stop_fan()

    if humidity < hum_constraint.min_value:
        pump_ctrl.start_pump()
    elif humidity > hum_constraint.max_value:
        pump_ctrl.stop_pump()

def main():
    wlan = connect_to_wifi(ssid, password)

    temp_constraint = ConstraintDomain(def_value=25, max_value=40, min_value=10)
    hum_constraint = ConstraintDomain(def_value=60, max_value=90, min_value=30)
    pump_ctrl = PumpController(relay_pin=5)
    fan_ctrl = FanController(relay_pin=4, servo_pin=14)
    dht_sensor = DHTSensor(pin=2)  # Sostituisci con il pin corretto

    server_socket = create_server_socket()

    while True:
        automatic_control(temp_constraint, hum_constraint, pump_ctrl, fan_ctrl, dht_sensor)

        try:
            client_socket, addr = server_socket.accept()
            print('Client connected from', addr)
            request = client_socket.recv(1024)
            print('Request = %s' % request)
            response = handle_request(request, temp_constraint, hum_constraint, pump_ctrl, fan_ctrl)
            client_socket.send('HTTP/1.1 200 OK\n')
            client_socket.send('Content-Type: text/html\n')
            client_socket.send('Connection: close\n\n')
            client_socket.sendall(response)
            client_socket.close()
        except OSError as e:
            client_socket.close()
            print('Connection closed')

if _name_ == '_main_':
    main()