class Arme:
    """Classe de base pour toutes les armes"""
    
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description
    
    def apply_bonus(self, stats):
        """Applique les bonus de l'arme aux statistiques"""
        return stats
    
    def __str__(self):
        return f"{self.nom} - {self.description}"


class Epee(Arme):
    """Arme Épée - Polyvalente entre attaque et défense"""
    
    def __init__(self):
        super().__init__("Épée", "Arme équilibrée (+2 Attaque, +1 Défense)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque et +1 Défense"""
        stats.attaque += 2
        stats.defense += 1
        return stats


class GrimoireMagique(Arme):
    """Arme Grimoire magique - Spécialisée dans la puissance magique"""
    
    def __init__(self):
        super().__init__("Grimoire magique", "Tome ancien chargé d'arcanes (+3 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +3 Attaque"""
        stats.attaque += 3
        return stats


class Lance(Arme):
    """Arme Lance - Offensive avec un peu de défense"""
    
    def __init__(self):
        super().__init__("Lance", "Arme d'allonge efficace (+2 Attaque, +1 Défense)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque et +1 Défense"""
        stats.attaque += 2
        stats.defense += 1
        return stats


class Arc(Arme):
    """Arme Arc - Spécialisée dans l'attaque à distance"""
    
    def __init__(self):
        super().__init__("Arc", "Arme de précision à distance (+2 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque"""
        stats.attaque += 2
        return stats


class MassueHache(Arme):
    """Arme Massue/Hache - Très offensive"""
    
    def __init__(self):
        super().__init__("Massue/Hache", "Arme lourde et brutale (+3 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +3 Attaque"""
        stats.attaque += 3
        return stats


class InstrumentMusique(Arme):
    """Arme Instrument de musique - Soutien et résistance"""
    
    def __init__(self):
        super().__init__("Instrument de musique", "Objet inspirant et mystique (+2 PV, +1 Défense)")
    
    def apply_bonus(self, stats):
        """Applique +2 PV et +1 Défense"""
        stats.pv_max += 2
        stats.pv += 2
        stats.defense += 1
        return stats


class Dague(Arme):
    """Arme Dague - Rapide et discrète"""
    
    def __init__(self):
        super().__init__("Dague", "Arme légère et rapide (+2 Attaque)")
    
    def apply_bonus(self, stats):
        """Applique +2 Attaque"""
        stats.attaque += 2
        return stats


class Baton(Arme):
    """Arme Bâton - Défensive et magique"""
    
    def __init__(self):
        super().__init__("Bâton", "Canalise l'énergie et protège son porteur (+1 Attaque, +2 Défense)")
    
    def apply_bonus(self, stats):
        """Applique +1 Attaque et +2 Défense"""
        stats.attaque += 1
        stats.defense += 2
        return stats


# Dictionnaire des armes disponibles
ARMES_DISPONIBLES = {
    1: Epee,
    2: GrimoireMagique,
    3: Lance,
    4: Arc,
    5: MassueHache,
    6: InstrumentMusique,
    7: Dague,
    8: Baton
}


def afficher_armes():
    """Affiche toutes les armes disponibles"""
    print("\n" + "="*60)
    print("Choisissez votre arme :")
    print("="*60)
    print("1. Épée - Arme équilibrée (+2 Attaque, +1 Défense)")
    print("2. Grimoire magique - Tome ancien chargé d'arcanes (+3 Attaque)")
    print("3. Lance - Arme d'allonge efficace (+2 Attaque, +1 Défense)")
    print("4. Arc - Arme de précision à distance (+2 Attaque)")
    print("5. Massue/Hache - Arme lourde et brutale (+3 Attaque)")
    print("6. Instrument de musique - Objet inspirant et mystique (+2 PV, +1 Défense)")
    print("7. Dague - Arme légère et rapide (+2 Attaque)")
    print("8. Bâton - Canalise l'énergie et protège son porteur (+1 Attaque, +2 Défense)")
    print("="*60)


def choisir_arme():
    """Demande au joueur de choisir son arme"""
    afficher_armes()
    
    while True:
        choix = input("Votre choix (1-8) : ")
        
        if choix in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            arme_choisie = ARMES_DISPONIBLES[int(choix)]()
            print(f"\n✅ Arme choisie : {arme_choisie.nom}")
            return arme_choisie
        else:
            print("❌ Erreur : Veuillez choisir un nombre entre 1 et 8")