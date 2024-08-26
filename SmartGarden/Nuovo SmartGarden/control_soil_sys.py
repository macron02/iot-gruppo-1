from machine import Pin
import pump, moisture_soil_sensor, hcsr04
import time

class control_soil_sys:
    def __init__(self, relay_pin, button_pump_pin, moisture_soil_sensor_pin, hcsr04_pin_echo, hcsr04_pin_trigger, water_level_min):
        self.pump = pump.pump(relay_pin)  # DA COMMENTARE
        self.min_water = water_level_min # livello minimo di acqua richiesto per irrigare
        self.btn_pump = Pin(button_pump_pin, Pin.IN, Pin.PULL_DOWN)
        self.btn_pump.irq(trigger=Pin.IRQ_RISING, handler=self.click_pump)
        self.us_sensor = hcsr04.hcsr04(hcsr04_pin_echo,hcsr04_pin_trigger)
        self.moist_sens = moisture_soil_sensor.moisture_soil_sensor(moisture_soil_sensor_pin)

    def click_pump(self, pin):
        """
        Controlla lo stato del suolo e se non è Water permette di irrigare col bottone.
        """
        self.pump.start_pump()
        while self.btn_pump.value() == 1:
            time.sleep(0.2)  # Aspetta una frazione irrisoria di tempo per assestare il funzionamento del while e della pompa
        self.pump.stop_pump()  # Ferma la pompa quando il bottone viene rilasciato

    def watering_plant(self):
        """
        Controlla lo stato del suolo e se è Dry avvia la pompa dell'acqua.
        """
        if self.us_sensor.distance_mm() > self.min_water:
            soil_state = self.moist_sens.soil_condition()
            if soil_state == "Dry":
                self.pump.start_pump()
                time.sleep(3)
            self.pump.stop_pump()

    def get_moist_sens(self):
        return self.moist_sens.soil_condition()

     water_level = 100 - int((distance_mm / self.min_water) * 100)
        return water_level
