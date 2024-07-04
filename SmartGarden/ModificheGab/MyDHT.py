from machine import Pin, I2C, ADC, PWM
import dht
import time
import FanController

class MyDHT:

    def __init__(self, dht_pin, fan_pin, servo_pin):
        self.sensor = dht.DHT22(Pin(dht_pin))
        self.fan = FanController.FanController(fan_pin,servo_pin)
        self.previous_humid = None
        self.previous_temp = None
        self.habitat_status = {"temp_value": 0, "temp_status": 0, "hum_value": 0, "hum_status": 0}
        self.habitat_exception = 0
        self.habitat_range_values = [1.44, 1.2, 0.8, 0.64]

    def get_habitat_exception(self):
        return self.habitat_exception

    def get_habitat_status(self):
        return self.habitat_status

    def checkGarden(self, ref_temperature, ref_humidity):
        """
        Metodo per la misurazione e seguente check sui dati misurati
        """
        try:
            self.sensor.measure()
            temperature = self.sensor.temperature()
            humidity = self.sensor.humidity()
        except OSError as e:
            self.habitat_exception = 1
            return self.habitat_status

        if humidity is not None and temperature is not None:
            self.habitat_status.update({"temp_value": temperature, "hum_value": humidity})
            if temperature != self.previus_temp:
                self.check_temp(temperature, ref_temperature)
                self.previus_temp = temperature
            if humidity != self.previus_humid:
                self.check_humid(humidity, ref_humidity)
                self.previus_humid = humidity
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

                    #Verifica se la temperatura è troppo maggiore di quella desiderata
                    self.fan.start_fan()
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
                Verifica se l'umidità è maggiore a quella desiderata
                """
                self.fan.start_fan()
                if humid_meas >= (ref_humidity * self.habitat_range_values[0]):
                    """
                    Verifica se l'umidità è troppo maggiore a quella desiderata
                    """
                    self.habitat_status["hum_status"] = 1

        elif humid_meas < (ref_humidity*self.habitat_range_values[2]):
            """
            Verifica se l'umidità è inferiore a quella desiderata
            """
            if humid_meas <= (ref_humidity * self.habitat_range_values[3]):
                """
                Verifica se l'umidità è troppo inferiore a quella desiderata
                """
                self.habitat_status["hum_status"] = 1
