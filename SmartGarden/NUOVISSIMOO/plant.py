class plant:
    def __init__(self, nome="informazione non disponibile", specie="informazione non disponibile",
        temp=20,hum=40):
        self.nome = nome
        self.specie = specie
        self.temp = temp
        self.hum = hum

    def get_plant_name(self):
        return self.nome

    def get_plant_species(self):
        return self.specie

    def get_plant_temp(self):
        return self.temp

    def get_plant_hum(self):
        return self.hum

    def set_plant_name(self, new_nome):
        self.nome = new_nome

    def set_plant_species(self, new_specie):
        self.specie = new_specie

    def set_default_plant(self):
        """Resetta le informazioni della pianta ai valori di default."""
        self.nome = "informazione non disponibile"
        self.specie = "informazione non disponibile"
        self.hum=40
        self.temp=20
