from machine import Pin, I2C, ADC, PWM
import dht
import time
import fan_controller

class Habitat:

    def __init__(self, dht_pin, fan_pin, servo_pin):
        self.sensor = dht.DHT22(Pin(dht_pin))
        self.fan = fan_controller.fan_controller(fan_pin, servo_pin)
        self.previous_humid = None
        self.previous_temp = None
        self.habitat_status = {"exception": 0, "temp_value": 0, "temp_status": 0, "hum_value": 0, "hum_status": 0}
        self.habitat_range_values = [1.44, 1.2, 0.8, 0.64]

    def get_habitat_status(self):
        return self.habitat_status

    def check_habitat_status(self, ref_temperature, ref_humidity):
        """
        Metodo per la misurazione e seguente check sui dati misurati
        """
        try:
            self.sensor.measure()
            temperature = self.sensor.temperature()
            humidity = self.sensor.humidity()
        except OSError as e:
            self.habitat_status["exception"] = 1
            return self.habitat_status

        if humidity is not None and temperature is not None:
            self.habitat_status.update({"temp_value": temperature, "hum_value": humidity})
            if temperature != self.previous_temp:
                self.check_temp(temperature, ref_temperature)
                self.previous_temp = temperature
            if humidity != self.previous_humid:
                self.check_humid(humidity, ref_humidity)
                self.previous_humid = humidity
        else:
            print("Errore durante la lettura dei dati.")
        return self.habitat_status

    def check_temp(self, temp_meas, ref_temperature):
        if temp_meas > ref_temperature:
            if temp_meas > (ref_temperature * self.habitat_range_values[1]):
                """
                Verifica se la temperatura è maggiore di quella desiderata
                """
                self.fan.start_fan()
                if temp_meas >= (ref_temperature * self.habitat_range_values[0]):
                    # Verifica se la temperatura è troppo maggiore di quella desiderata
                    self.habitat_status["temp_status"] = 1
        elif temp_meas < (ref_temperature * self.habitat_range_values[2]):
            """
            Verifica se la temperatura è minore di quella desiderata
            """
            if temp_meas <= (ref_temperature * self.habitat_range_values[3]):
                """
                Verifica se la temperatura è troppo minore di quella desiderata
                """
                self.habitat_status["temp_status"] = 1

    def check_humid(self, humid_meas, ref_humidity):
        if humid_meas > ref_humidity:
            if humid_meas > (ref_humidity * self.habitat_range_values[1]):
                """
                Verifica se l'umidità è maggiore di quella desiderata
                """
                if humid_meas >= (ref_humidity * self.habitat_range_values[0]):
                    """
                    Verifica se l'umidità è eccessivamente più alta di quella desiderata
                    """
                    self.fan.start_fan()
                    self.habitat_status["hum_status"] = 1
        elif humid_meas < (ref_humidity * self.habitat_range_values[2]):
            """
            Verifica se l'umidità è inferiore a quella desiderata
            """
            if humid_meas <= (ref_humidity * self.habitat_range_values[3]):
                """
                Verifica se l'umidità è eccessivamente più bassa di quella desiderata
                """
                self.habitat_status["hum_status"] = 1

    def get_habitat_temperature(self):
        return self.sensor.temperature()

    def get_habitat_humidity(self):
        return self.sensor.humidity()
