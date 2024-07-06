from machine import Pin
import Pump, MoistureSoilSensor, HCSR04
import time

class ControlSoilSys:
    def __init__(self, relay_pin, button_pump_pin, moisture_soil_sensor_pin, hcsr04_pin_echo, hcsr04_pin_trigger, water_level_min):
        self.pump = Pump.Pump(relay_pin)  # DA COMMENTARE
        self.min_water = water_level_min # livello minimo di acqua richiesto per irrigare
        self.btn_pump = Pin(button_pump_pin, Pin.IN, Pin.PULL_DOWN)
        self.btn_pump.irq(trigger=Pin.IRQ_RISING, handler=self.click_pump)
        self.moist_sens = MoistureSoilSensor.MoistureSoilSensor(moisture_soil_sensor_pin)
        self.soil_mode = 1 #modalità default del suolo
        self.us_sensor = HCSR04.HCSR04(hcsr04_pin_echo,hcsr04_pin_trigger)

    def click_pump(self, pin):
        self.pump.start_pump()
        while self.btn_pump.value() == 1:
            time.sleep(0.2) # Aspetta una frazione irrisoria di tempo per assestare il funzionamento del while e della pompa
        self.pump.stop_pump()  # Ferma la pompa quando il bottone viene rilasciato

    def watering_plant(self):
        if self.us_sensor.distance_mm() > self.min_water:
            if self.moist_sens.read_moisture_value() < self.moist_sens.get_ref_value_moisture():
                self.pump.start_pump()
                time.sleep(3)
            self.pump.stop_pump()

    def get_moist_sens(self):
        return self.moist_sens
