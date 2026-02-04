class Breed:
    def __init__(self, name_breed, bonus_type):
        self.name_breed = name_breed
        self.bonus_type = bonus_type

    def description(self):
        return f"Breed: {self.name_breed} | Bonus: {self.bonus_type}"

    def apply_bonus(self, stats):
        # Méthode générique (sera redéfinie)
        return stats
