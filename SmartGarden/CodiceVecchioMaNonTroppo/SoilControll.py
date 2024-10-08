from machine import Pin
import time
import Pump
import MoistureSoilSensor
import HCSR04

class ControlSoilSys:
    def __init__(self, relay_pin, button_pump_pin, button_soil_pin, moistur_soil_sensor_pin, hcsr04_pin_echo, hcsr04_pin_trigger, water_level):
        self.pump = Pump.Pump(relay_pin)  # DA COMMENTARE
        self.min_water = water_level # livello minimo di acqua richiesto per irrigare
        self.btn_pump = Pin(button_pump_pin, Pin.IN, Pin.PULL_DOWN)
        self.btn_pump.irq(trigger=Pin.IRQ_RISING, handler=self.click_pump)
        self.ms_sensor = MoistureSoilSensor.MoistureSoilSensor(moistur_soil_sensor_pin)
        self.soil_mode = 1 #modalità default del suolo
        self.soil_moisture = 50
        self.us_sensor = HCSR04.HCSR04(hcsr04_pin_echo,hcsr04_pin_trigger)
        self.btn_soil_mode = Pin(button_soil_pin, Pin.IN, Pin.PULL_DOWN)
        self.btn_soil_mode.irq(trigger=Pin.IRQ_RISING, handler=self.soil_mode_buttons)
        self.last = time.ticks_ms()
        self.delta = 0

    def click_pump(self, pin):
        self.pump.start_pump()
        while self.btn_pump.value() == 1:
            time.sleep(0.2) # Aspetta una frazione irrisoria di tempo per assestare il funzionamento del while e della pompa
        self.pump.stop_pump()  # Ferma la pompa quando il bottone viene rilasciato

    def soil_mode_buttons(self, pin):
        current = time.ticks_ms()
        delta = time.ticks_diff(current, self.last)
        if delta < 200:
            return
        self.last = current
        if self.soil_mode < 3:
            self.soil_mode += 1
        else:
            self.soil_mode = 1

    def select_soil_mode(self):
        if self.soil_mode == 1:
            self.soil_moisture = 50
        elif self.soil_mode == 2:
            self.soil_moisture = 30
        elif self.soil_mode == 3:
            self.soil_moisture = 80

    def water(self):
        if self.us_sensor.distance_mm() > self.min_water:
            if self.ms_sensor.checkSoil() < self.soil_moisture:
                self.pump.start_pump()
                time.sleep(3)
            self.pump.stop_pump()
