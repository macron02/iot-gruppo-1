import machine
import ssd1306
import time
from machine import Pin, I2C
import framebuf

class Menu:
    def __init__(self, button_display, button_reset, sda_pin=21, scl_pin=22,):
        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        oled_width = 128
        oled_height = 64
        self.oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
        self.btn_display = Pin(button_display, Pin.IN, Pin.PULL_DOWN)
        self.btn_reset = Pin(button_reset, Pin.IN, Pin.PULL_DOWN)
        self.last = 0
        self.display_mode = 1
        self.btn_reset.irq(trigger=Pin.IRQ_RISING, handler=self.button_reset_handler)
        self.btn_display.irq(trigger=Pin.IRQ_RISING, handler=self.display_mode_buttons)
            
    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    def opening(self):
        fb = framebuf.FrameBuffer(self.get_plant_img(), 128, 64, framebuf.MONO_HLSB)
        self.clear()
        self.oled.blit(fb, 8, 0)
        self.oled.show()

    def connection_idle(self, isWifi):
        self.clear()
        self.oled.text("Connecting", 0, 0)
        if isWifi:
            self.oled.text("to Wifi...", 0, 10)
        else:
            self.oled.text("to MQTT server...", 0, 10)
        self.oled.show()

    def connection_end_status(self, end_status):
        self.clear()
        self.oled.text("Connection", 0, 0)
        if end_status:
            self.oled.text("successful", 0, 10)
        else:
            self.oled.text("unsuccessful", 0, 10)
        self.oled.show()

    def connection_retrying(self):
        self.clear()
        self.oled.text("Another attempt to", 0, 0)
        self.oled.text("MQTT server connection", 0, 10)
        self.oled.text("in 5 seconds", 0, 20)
        self.oled.show()

    def button_reset_handler(self, pin):
        machine.reset()

    def display_mode_buttons(self, pin):
        current = time.ticks_ms()
        delta = time.ticks_diff(current, self.last)
        if delta < 200:
            return
        self.last = current
        if self.display_mode < 3:
            self.display_mode += 1
        else:
            self.display_mode = 1

    def display_data(self, habitat_status):
        self.clear()
        if self.display_mode == 1:
            self.oled.text('Temp: %s C' % habitat_status["temp_value"], 0, 0)
            self.oled.text('Humidity: %s %%' % habitat_status["hum_value"], 0, 10)
        elif self.display_mode == 2:
            self.oled.text('Temp: %s C' % habitat_status["temp_value"], 0, 0)
        elif self.display_mode == 3:
            self.oled.text('Humidity: %s %%' % habitat_status["hum_value"], 0, 0)
        self.oled.show()

    def display_allarmed(self, habitat_status):
        self.clear()
        if habitat_status["temp_status"] == 1 and habitat_status["hum_status"] == 1:
            self.oled.text('Ambiente ostile', 0, 0)
            self.oled.text('Temp: %s C' % habitat_status["temp_value"], 0, 10)
            self.oled.text('Humidity: %s %%' % habitat_status["hum_value"], 0, 20)
        elif habitat_status["temp_status"] == 1 and habitat_status["hum_status"] == 0:
            self.oled.text('Temperatura ostile', 0, 0)
            self.oled.text('Temp: %s C' % habitat_status["temp_value"], 0, 10)
        elif habitat_status["temp_status"] == 0 and habitat_status["hum_status"] == 1:
            self.oled.text('Umidità ostile', 0, 0)
            self.oled.text('Humidity: %s %%' % habitat_status["hum_value"], 0, 10)
        else:
            self.oled.text('Ambiente stabile', 0, 0)
            self.oled.text('Temp: %s C' % habitat_status["temp_value"], 0, 10)
            self.oled.text('Humidity: %s %%' % habitat_status["hum_value"], 0, 20)
        self.oled.show()

    def soil_mode(self, soil_mode):
        desired_humidity = {
            1: '50 %%',
            2: '30 %%',
            3: '80 %%'
        }
        if soil_mode in desired_humidity:
            self.clear()
            self.oled.text('Umidità del terreno', 0, 0)
            self.oled.text(f'desiderata: {desired_humidity[soil_mode]}', 0, 10)
            self.oled.show()

    def get_plant_img(self):
        return bytearray([
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x0f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x80, 0x0f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x01, 0x0f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0x3e, 0x0f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xe0, 0xfc, 0x4f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xe0, 0x3f, 0xff, 0xff, 0xff, 0xc3, 0xf8, 0xcf, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xe0, 0x03, 0xff, 0xff, 0xff, 0x0f, 0xf1, 0xcf, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xe0, 0x80, 0x7f, 0xff, 0xfe, 0x1f, 0xe3, 0x8f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xe0, 0x78, 0x1f, 0xff, 0xfe, 0x3f, 0xc7, 0x9f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf2, 0x3f, 0x07, 0xff, 0xfc, 0x7f, 0x8f, 0x9f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf3, 0x1f, 0xc3, 0xff, 0xf8, 0xff, 0x1f, 0x9f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf3, 0x8f, 0xf1, 0xff, 0xf9, 0xfe, 0x3f, 0x3f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf3, 0xc7, 0xf8, 0xff, 0xf1, 0xfc, 0x7f, 0x3f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf3, 0xe3, 0xfc, 0x7f, 0xf3, 0xf8, 0xfe, 0x3f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf1, 0xf1, 0xfe, 0x3f, 0xe3, 0xf1, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf9, 0xf8, 0xff, 0x3f, 0xe7, 0xe3, 0xfc, 0x7f, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf9, 0xfc, 0x7f, 0x1f, 0xe7, 0xc7, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xf8, 0xfe, 0x3f, 0x9f, 0xe7, 0x8f, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xfc, 0xff, 0x1f, 0x8f, 0xe7, 0x1f, 0xf1, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xfc, 0x7f, 0x8f, 0xcf, 0xe6, 0x3f, 0xe3, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xc7, 0xcf, 0xe4, 0x7f, 0xc7, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xfe, 0x3f, 0xe3, 0xc7, 0xe0, 0xff, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0x1f, 0xf1, 0xe7, 0xe1, 0xfc, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0x8f, 0xf8, 0xe7, 0xe1, 0xc0, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0x87, 0xfc, 0x67, 0xc0, 0x01, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xe3, 0xfe, 0x27, 0xc0, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 0xff, 0x07, 0x8f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0x3f, 0x87, 0x9f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x01, 0x87, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x80, 0x07, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x06, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf2, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf2, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 0x00, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xc1, 0xfe, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x01, 0x87, 0xff, 0x87, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0x00, 0x1f, 0xff, 0xe3, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0xe0, 0xfc, 0x3f, 0xff, 0xf1, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0x87, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0x0f, 0xff, 0xff, 0xff, 0xfc, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xff, 0x3f, 0xff, 0xff, 0xff, 0xfe, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff,
                           0xff, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xe0, 0x7f, 0xff, 0xff, 0xff, 0xff])