class my_error:
    global error_value = 0
    def error_message(error_value):
        oled.setTextSize(1)  # Imposta la dimensione del testo a 1
        if error_value == 1: #errore temperatura sbagliata
            oled.text('Error_code: %s' % error_value, 0, 0)
            oled.text('Valore inserito', 0, 10)
            oled.text('non valido (5-35)', 0, 20)
        elif error_value == 2: # errore umidità sbagliata
            oled.text('Error_code: %s' % error_value, 0, 0)
            oled.text('Valore inserito', 0, 10)
            oled.text('non valido (0-100)', 0, 20)
        elif error_value == 3:
            oled.text('Error_code: %s' % error_value, 0, 0)
            oled.text('Valore inserito', 0, 10)
            oled.text('non valido (5-35)', 0, 20)
        elif error_value == 4:
            oled.text('Error_code: %s' % error_value, 0, 0)
            oled.text('Valore inserito', 0, 10)
            oled.text('non valido (5-35)', 0, 20)
        elif error_value == 5:
            oled.text('Error_code: %s' % error_value, 0, 0)
            oled.text('Valore inserito', 0, 10)
            oled.text('non valido (5-35)', 0, 20)
        else :
            oled.text('Error_code: %s' % error_value, 0, 0)
            oled.text('Valore inserito', 0, 10)
            oled.text('non valido (5-35)', 0, 20)