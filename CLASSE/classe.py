class classe:
    def init(self, name_classe, bonus_classe):
        self.name_classe = name_classe
        self.bonus_classe = bonus_classe

    def description(self):
        return f"Breed: {self.name_classe} | Bonus: {self.bonus_classe}"

    def apply_bonus(self, stats):
        # Méthode générique (sera redéfinie)
        return stats