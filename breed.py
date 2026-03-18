class Race:
    """Classe de base pour toutes les races"""
    
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description
    
    def apply_bonus(self, stats):
        """Applique les bonus de la race aux statistiques"""
        return stats
    
    def __str__(self):
        return f"{self.nom} - {self.description}"


class Feline(Race):
    """Race Feline - Bonus de chances critiques"""
    
    def __init__(self):
        super().__init__("Feline", "Agilité féline (+2 ATK, +3 VIT)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque, +3 Vitesse"""
        stats.attaque += 2
        stats.vitesse += 3
        return stats


class Human(Race):
    """Race Human - Bonus d'arme"""
    
    def __init__(self):
        super().__init__("Human", "Maîtrise des armes (+1 ATK, +1 ATK MAG, +1 VIT)")
    
    def apply_bonus(self, stats):
        """Applique +1 Attaque, +1 Attaque magique, +1 Vitesse"""
        stats.attaque += 1
        stats.attaque_magique += 1
        stats.vitesse += 1
        return stats


class Panda(Race):
    """Race Panda - Bonus de défense"""
    
    def __init__(self):
        super().__init__("Panda", "Endurance naturelle (+2 DEF, +2 DEF MAG)")
    
    def apply_bonus(self, stats):
        """Applique +2 Défense, +2 Défense magique, -1 Vitesse"""
        stats.defense += 2
        stats.defense_magique += 2
        stats.vitesse -= 1
        return stats


class Reptilian(Race):
    """Race Reptilian - Bonus de force"""
    
    def __init__(self):
        super().__init__("Reptilian", "Force brute (+2 ATK)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque, -1 Vitesse"""
        stats.attaque += 2
        stats.vitesse -= 1
        return stats


class Spirit(Race):
    """Race Spirit - Pouvoir élémentaire"""
    
    def __init__(self):
        super().__init__("Spirit", "Puissance élémentaire (+3 PV, +3 ATK MAG, +2 VIT)")
    
    def apply_bonus(self, stats):
        """Applique +3 PV, +3 Attaque magique, +2 Défense magique, +2 Vitesse"""
        stats.pv_max += 3
        stats.pv += 3
        stats.attaque_magique += 3
        stats.defense_magique += 2
        stats.vitesse += 2
        return stats


# Dictionnaire des races disponibles
RACES_DISPONIBLES = {
    1: Feline,
    2: Human,
    3: Panda,
    4: Reptilian,
    5: Spirit
}


def afficher_races():
    """Affiche toutes les races disponibles"""
    print("\n" + "="*60)
    print("Choisissez votre race :")
    print("="*60)
    print("1. Feline    - Agilité féline        (+2 ATK, +3 VIT)")
    print("2. Human     - Maîtrise des armes    (+1 ATK, +1 ATK MAG, +1 VIT)")
    print("3. Panda     - Endurance naturelle   (+2 DEF, +2 DEF MAG)")
    print("4. Reptilian - Force brute           (+2 ATK)")
    print("5. Spirit    - Puissance élémentaire (+3 PV, +3 ATK MAG, +2 VIT)")
    print("="*60)


def choisir_race():
    """Demande au joueur de choisir sa race"""
    afficher_races()
    
    while True:
        choix = input("Votre choix (1-5) : ")
        
        if choix in ["1", "2", "3", "4", "5"]:
            race_choisie = RACES_DISPONIBLES[int(choix)]()
            print(f"\n✅ Race choisie : {race_choisie.nom}")
            return race_choisie
        else:
            print("❌ Erreur : Veuillez choisir un nombre entre 1 et 5")