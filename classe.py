class Classe:
    """Classe de base pour toutes les classes de personnage"""
    
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description
    
    def apply_bonus(self, stats):
        """Applique les bonus de la classe aux statistiques"""
        return stats
    
    def __str__(self):
        return f"{self.nom} - {self.description}"


class Apothicaire(Classe):
    """Classe Apothicaire - Spécialisée dans les soins"""
    
    def __init__(self):
        super().__init__("Apothicaire", "Maître des potions (+5 PV)")
    
    def apply_bonus(self, stats):
        """Applique +5 PV, +2 ATK MAG, +2 DEF MAG"""
        stats.pv_max += 5
        stats.pv += 5
        stats.attaque_magique += 2
        stats.defense_magique += 2
        return stats


class Barde(Classe):
    """Classe Barde - Spécialisée dans le soutien"""
    
    def __init__(self):
        super().__init__("Barde", "Musicien inspirant (+3 PV)")
    
    def apply_bonus(self, stats):
        """Applique +3 PV, +1 ATK MAG, +2 VIT"""
        stats.pv_max += 3
        stats.pv += 3
        stats.attaque_magique += 1
        stats.vitesse += 2
        return stats


class Eclaireur(Classe):
    """Classe Eclaireur - Spécialisée dans l'exploration"""
    
    def __init__(self):
        super().__init__("Eclaireur", "Expert en reconnaissance (+5 PV)")
    
    def apply_bonus(self, stats):
        """Applique +5 PV, +4 VIT"""
        stats.pv_max += 5
        stats.pv += 5
        stats.vitesse += 4
        return stats


class Mage(Classe):
    """Classe Mage - Spécialisée dans la magie"""
    
    def __init__(self):
        super().__init__("Mage", "Maître des arcanes (+2 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +4 ATK MAG, +3 DEF MAG, -1 VIT"""
        stats.attaque_magique += 4
        stats.defense_magique += 3
        stats.vitesse -= 1
        return stats


class Paladin(Classe):
    """Classe Paladin - Spécialisée dans la défense"""
    
    def __init__(self):
        super().__init__("Paladin", "Protecteur sacré (+3 Défense)")
    
    def apply_bonus(self, stats):
        """Applique +3 DEF, +2 DEF MAG, -1 VIT"""
        stats.defense += 3
        stats.defense_magique += 2
        stats.vitesse -= 1
        return stats


class Pretre(Classe):
    """Classe Pretre - Spécialisée dans les soins divins"""
    
    def __init__(self):
        super().__init__("Pretre", "Soigneur divin (+5 PV)")
    
    def apply_bonus(self, stats):
        """Applique +5 PV, +2 ATK MAG, +2 DEF MAG"""
        stats.pv_max += 5
        stats.pv += 5
        stats.attaque_magique += 2
        stats.defense_magique += 2
        return stats


class Viking(Classe):
    """Classe Viking - Spécialisée dans l'attaque"""
    
    def __init__(self):
        super().__init__("Viking", "Guerrier redoutable (+3 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +3 ATK, +3 VIT"""
        stats.attaque += 3
        stats.vitesse += 3
        return stats


class Voleur(Classe):
    """Classe Voleur - Spécialisée dans la vitesse"""
    
    def __init__(self):
        super().__init__("Voleur", "Expert en discrétion (+2 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +2 ATK, +5 VIT"""
        stats.attaque += 2
        stats.vitesse += 5
        return stats


class Admin(Classe):
    """Classe Admin — Stats maximales"""

    def __init__(self):
        super().__init__("Admin", "Mode administrateur (+100 partout)")

    def apply_bonus(self, stats):
        stats.pv_max          += 100
        stats.pv              += 100
        stats.attaque         += 100
        stats.defense         += 100
        stats.attaque_magique += 100
        stats.defense_magique += 100
        stats.vitesse         += 100
        return stats


# Dictionnaire des classes disponibles
CLASSES_DISPONIBLES = {
    1: Apothicaire,
    2: Barde,
    3: Eclaireur,
    4: Mage,
    5: Paladin,
    6: Pretre,
    7: Viking,
    8: Voleur,
    9: Admin
}


def afficher_classes():
    """Affiche toutes les classes disponibles"""
    print("\n" + "="*60)
    print("Choisissez votre classe :")
    print("="*60)
    print("1. Apothicaire - Maître des potions   (+5 PV, +2 ATK MAG, +2 DEF MAG)")
    print("2. Barde       - Musicien inspirant  (+3 PV, +1 ATK MAG, +2 VIT)")
    print("3. Eclaireur   - Expert en reco.      (+5 PV, +4 VIT)")
    print("4. Mage        - Maître des arcanes   (+4 ATK MAG, +3 DEF MAG)")
    print("5. Paladin     - Protecteur sacré     (+3 DEF, +2 DEF MAG)")
    print("6. Pretre      - Soigneur divin       (+5 PV, +2 ATK MAG, +2 DEF MAG)")
    print("7. Viking      - Guerrier redoutable  (+3 ATK, +3 VIT)")
    print("8. Voleur      - Expert en discrétion (+2 ATK, +5 VIT)")
    print("9. Admin       - Mode administrateur   (+100 partout)")
    print("="*60)


def choisir_classe():
    """Demande au joueur de choisir sa classe"""
    afficher_classes()
    
    while True:
        choix = input("Votre choix (1-8) : ")
        
        if choix in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            classe_choisie = CLASSES_DISPONIBLES[int(choix)]()
            print(f"\n✅ Classe choisie : {classe_choisie.nom}")
            return classe_choisie
        else:
            print("❌ Erreur : Veuillez choisir un nombre entre 1 et 9")