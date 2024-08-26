# Codice per testare la classe
pin = 12
sensor = moisture_soil_sensor(pin)

while True:
    moisture_percentage = sensor.read_moisture_value()
    condition = sensor.soil_condition()
    print(f"Umidità del suolo: {moisture_percentage:.2f}% - Condizione del suolo: {condition}")
    time.sleep(2)
