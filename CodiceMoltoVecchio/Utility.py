

global allarm_mode = 0 #variabile per il controllo dell'allarme

class check_sys:

    def check():
        sensor.measure()
        temp_readed = sensor.temperature()

    def check_stop():

        if allarm_mode == 1:
            check_restore()
            allarm_control()

    def check_active():
        a

    def check_temp():


        if (temp_readed =! previus_temp):

            if temp_readed >= (temp*1.2):
                fan.start_fan()
                if temp_readed <= [(temp*1.2)*1.2]:
                    allarm_mode = 1
                    allarm_system()

            elif temp_readed <= (temp*0.8):

                if temp_readed <= [(temp*0.8)*0.8]:
                    allarm_mode = 1
                    allarm_system()







def check_light():
    lume = ldr.read()

    if lume =! previus_lume:
        if photoresistor_value < THRESHOLD_VALUE:
            led.on()
        else:
            led.off()
        previus_lume = lume
    else :
        return

def check_habitat():
    sensor.measure()
    temp_readed = sensor.temperature()
    humid_readed = sensor.humidity()
    if (temp_readed =! previus_temp or humid_readed =! previus_humid):
            if temp_readed >= (temp*1.2):
                fan.start_fan()
                if temp_readed <= [(temp*1.2)*1.2]:

                    allarme

            elif temp_readed <= (temp*0.8):

                if temp_readed <= [(temp*0.8)*0.8]:
                    led_blue1.on()
                    led_blue2.on()
                    time.sleep(1)
                    led_blue1.off()
                    led_blue2.off()

            if humid_readed >= (humid*1.2):
                fan.start_fan()
                if humid_readed >= [(humid*1.2)*1.2]:
                    led_blue1.on()
                    led_blue2.on()
                    time.sleep(1)
                    led_blue1.off()
                    led_blue2.off()
            elif humid_readed >= (humid*0.8):
                fan.start_fan()
                if humid_readed >= [(humid*0.8)*0.8]:
                    led_blue1.on()
                    led_blue2.on()
                    time.sleep(1)
                    led_blue1.off()
                    led_blue2.off()


        previus_temp = temp_readed
        previus_humid = humid_readed


class allarmed_sys:

    def allarm_control():
        allarm_mode = not allarm_mode

    def allarm_system():
        while allarm_mode == 1:
            led_blue1.on()
            led_blue2.on()
            led_red1.on()
            led_red2.on()
            time.sleep(1)
            led_blue1.off()
            led_blue2.off()
            led_red1.off()
            led_red2.off()

            check_stop()
