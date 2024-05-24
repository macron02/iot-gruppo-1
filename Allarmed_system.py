from machine import Pin, PWM, I2C
import time
import HCSR04
import dht
import ssd1306

class AllarmeHabitat:
    def __init__(self, pin_buzzer, red_led_pin_, blue_led_pin_, pin_dht, pin_scl_oled, pin_sda_oled):
        self.buzzer = Pin(pin_buzzer, Pin.OUT)
        self.pwm_buzzer = PWM(self.buzzer_pin)
        self.sensor = dht.DHT22(Pin(pin_dht))
        self.leds = [Pin(red_led_pin_, Pin.OUT), Pin(blue_led_pin_, Pin.OUT)]
        self.i2c = I2C(0, scl=Pin(pin_scl_oled), sda=Pin(pin_sda_oled))
        self.oled = ssd1306.SSD1306_I2C(121, 64, self.i2c)
        self.allarm_mode = 0

    def attiva_allarme(self, imp_temperature, imp_humidity):
        self.allarm_mode = 1
        while self.allarm_mode == 1:
            """tono alto"""
            self.pwm_buzzer.freq(900)
            self.leds[0].on()
            self.leds[1].off()
            time.sleep(0.2)  # Durata del tono alto
            """tono basso"""
            self.pwm_buzzer.freq(450)
            self.leds[0].off()
            self.leds[1].on()
            time.sleep(0.2) # Durata del tono basso
            self.spin_off(imp_temperature, imp_humidity)

    def spin_off(self, imp_temperature, imp_humidity):
        self.sensor.measure()
        try:
            humidity, temperature = self.sensor.read()
        except OSError as e:
            self.oled.print(f"Errore durante la lettura del sensore: {e.strerror}")
            if (temperature > (imp_temperature*1.2) or  temperature < (imp_temperature*0.8)) and (humidity > (imp_temperature*1.2) or  humidity < (imp_temperature*0.8)):
                oled.setTextSize(1)  # Imposta la dimensione del testo a 1
                oled.text('Ambiente ostile', 0, 0)
                oled.text('Temp: %s C' % temperature, 0, 10)
                oled.text('Humidity: %s %%' % humidity, 0, 20)
            elif (temperature > (imp_temperature*1.2) or  temperature < (imp_temperature*0.8)):
                oled.setTextSize(1)  # Imposta la dimensione del testo a 2
                oled.text('Temperatura ostile', 0, 0)
                oled.text('Temp: %s C' % temperature, 0, 0)
            elif (humidity > (imp_temperature*1.2) or  humidity< (imp_temperature*0.8)):
                oled.setTextSize(1)  # Imposta la dimensione del testo a 2
                oled.text('Umidità ostile', 0, 0)
                oled.text('Humidity: %s %%' % humidity, 0, 10)
            else :
                oled.setTextSize(1)  # Imposta la dimensione del testo a 2
                oled.text('Ambiente ostile', 0, 0)
                oled.text('Humidity: %s %%' % humidity, 0, 10)
            oled.show()
        if (temperature < (imp_temperature*1.2) and  temperature > (imp_temperature*0.8)) and (humidity < (imp_temperature*1.2) and  humidity > (imp_temperature*0.8)):
                 set_allarm_mode = 0

#manca la parte dove si legge la distanza e in base a quella si accende il led
