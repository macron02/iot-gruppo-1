class constraint_domain:
    def __init__(self, def_value, max_value, min_value):
        self.max_value = max_value
        self.min_value = min_value
        self.value = def_value
        if min_value > max_value:
            raise OSError

    def set_value(self, new_value):
        if new_value >= self.min_value and new_value <= self.max_value:
            self.value = new_value
            return 0
        else:
            print(f"Valore {new_value} fuori dal range consentito ({self.min_value} - {self.max_value})")
            return 1

    def get_value(self):
        return self.value
