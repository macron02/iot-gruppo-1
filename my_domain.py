"""file dedito ai domini per migliorare l'efficienza dei parametri"""            
class temperature_domein:
    def __init__(self, name):
        self.name = name
        self.min_value = 5
        self.max_value = 35
        self.value = 18
    
    def set_temp(self, new_temp):
        if self.min_value <= new_temp <= self.max_value:
            self.value = new_value
        else:
            print(f"Valore {new_value} fuori dal range consentito ({self.min_value} - {self.max_value})")
        
            
class umidity_domein:
    def __init__(self, name):
        self.name = name
        self.min_value = 5
        self.max_value = 95
        self.value = 40
    
    def set_umid(self, new_umid):
        if self.min_value <= new_umid <= self.max_value:
            self.value = new_umid
        else:
            print(f"Valore {new_value} fuori dal range consentito ({self.min_value} - {self.max_value})")
            
