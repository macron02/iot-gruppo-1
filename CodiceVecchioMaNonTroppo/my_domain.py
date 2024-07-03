class constraint_domain:
    def _init_(self, def_value, max_value, min_value):
        self.max_value = max_value
        self.min_value = min_value
        self.value = def_value

    def set_value(self, new_value):
        if new_value >= self.min_value and new_value <= self.max_value:
            self.value = new_value
        else:
            print(f"Valore {new_value} fuori dal range consentito ({self.min_value} - {self.max_value})")
