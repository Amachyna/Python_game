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
        """Applique +5 PV"""
        stats.pv_max += 5
        stats.pv += 5
        return stats


class Barde(Classe):
    """Classe Barde - Spécialisée dans le soutien"""
    
    def __init__(self):
        super().__init__("Barde", "Musicien inspirant (+3 PV)")
    
    def apply_bonus(self, stats):
        """Applique +3 PV"""
        stats.pv_max += 3
        stats.pv += 3
        return stats


class Eclaireur(Classe):
    """Classe Eclaireur - Spécialisée dans l'exploration"""
    
    def __init__(self):
        super().__init__("Eclaireur", "Expert en reconnaissance (+5 PV)")
    
    def apply_bonus(self, stats):
        """Applique +5 PV"""
        stats.pv_max += 5
        stats.pv += 5
        return stats


class Mage(Classe):
    """Classe Mage - Spécialisée dans la magie"""
    
    def __init__(self):
        super().__init__("Mage", "Maître des arcanes (+2 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque magique"""
        stats.attaque += 2
        return stats


class Paladin(Classe):
    """Classe Paladin - Spécialisée dans la défense"""
    
    def __init__(self):
        super().__init__("Paladin", "Protecteur sacré (+3 Défense)")
    
    def apply_bonus(self, stats):
        """Applique +3 Défense"""
        stats.defense += 3
        return stats


class Pretre(Classe):
    """Classe Pretre - Spécialisée dans les soins divins"""
    
    def __init__(self):
        super().__init__("Pretre", "Soigneur divin (+5 PV)")
    
    def apply_bonus(self, stats):
        """Applique +5 PV"""
        stats.pv_max += 5
        stats.pv += 5
        return stats


class Viking(Classe):
    """Classe Viking - Spécialisée dans l'attaque"""
    
    def __init__(self):
        super().__init__("Viking", "Guerrier redoutable (+3 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +3 Attaque"""
        stats.attaque += 3
        return stats


class Voleur(Classe):
    """Classe Voleur - Spécialisée dans la vitesse"""
    
    def __init__(self):
        super().__init__("Voleur", "Expert en discrétion (+2 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque"""
        stats.attaque += 2
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
    8: Voleur
}


def afficher_classes():
    """Affiche toutes les classes disponibles"""
    print("\n" + "="*60)
    print("Choisissez votre classe :")
    print("="*60)
    print("1. Apothicaire - Maître des potions (+5 PV)")
    print("2. Barde - Musicien inspirant (+3 PV)")
    print("3. Eclaireur - Expert en reconnaissance (+5 PV)")
    print("4. Mage - Maître des arcanes (+2 Attaque)")
    print("5. Paladin - Protecteur sacré (+3 Défense)")
    print("6. Pretre - Soigneur divin (+5 PV)")
    print("7. Viking - Guerrier redoutable (+3 Attaque)")
    print("8. Voleur - Expert en discrétion (+2 Attaque)")
    print("="*60)


def choisir_classe():
    """Demande au joueur de choisir sa classe"""
    afficher_classes()
    
    while True:
        choix = input("Votre choix (1-8) : ")
        
        if choix in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            classe_choisie = CLASSES_DISPONIBLES[int(choix)]()
            print(f"\n✅ Classe choisie : {classe_choisie.nom}")
            return classe_choisie
        else:
            print("❌ Erreur : Veuillez choisir un nombre entre 1 et 8")