import random


class Armure:
    """Classe de base pour toutes les armures"""

    def __init__(self, nom, type_armure, bonus_defense, bonus_defense_magique,
                 bonus_vitesse, description, classes_compatibles, emoji):
        self.nom = nom
        self.type_armure = type_armure
        self.bonus_defense = bonus_defense
        self.bonus_defense_magique = bonus_defense_magique
        self.bonus_vitesse = bonus_vitesse
        self.description = description
        self.classes_compatibles = classes_compatibles
        self.emoji = emoji

    def afficher(self):
        """Affiche les informations de l'armure"""
        print(f"\n  {self.emoji} {self.nom} [{self.type_armure}]")
        print(f"     {self.description}")
        parties = []
        if self.bonus_defense > 0:
            parties.append(f"+{self.bonus_defense} DEF")
        if self.bonus_defense_magique > 0:
            parties.append(f"+{self.bonus_defense_magique} DEF MAG")
        if self.bonus_vitesse > 0:
            parties.append(f"+{self.bonus_vitesse} VIT")
        elif self.bonus_vitesse < 0:
            parties.append(f"{self.bonus_vitesse} VIT")
        print(f"     📈 {'  |  '.join(parties) if parties else 'Aucun bonus'}")

    def __str__(self):
        parties = []
        if self.bonus_defense > 0:
            parties.append(f"+{self.bonus_defense} DEF")
        if self.bonus_defense_magique > 0:
            parties.append(f"+{self.bonus_defense_magique} DEF MAG")
        if self.bonus_vitesse != 0:
            signe = "+" if self.bonus_vitesse > 0 else ""
            parties.append(f"{signe}{self.bonus_vitesse} VIT")
        return f"{self.emoji} {self.nom} ({', '.join(parties)})"


# ─── Les 8 armures ──────────────────────────────────────────────────────────

class CuirassePlates(Armure):
    """Tank physique pur — lourde mais très protectrice"""
    def __init__(self):
        super().__init__(
            nom="Cuirasse de plaques",
            type_armure="Armure lourde",
            bonus_defense=6,
            bonus_defense_magique=0,
            bonus_vitesse=-2,
            description="Une armure massive qui absorbe les coups les plus violents.",
            classes_compatibles=["Viking", "Paladin"],
            emoji="🛡️"
        )


class RobeArcane(Armure):
    """Protection magique pure — légère mais résistante aux sorts"""
    def __init__(self):
        super().__init__(
            nom="Robe arcanique",
            type_armure="Robe magique",
            bonus_defense=0,
            bonus_defense_magique=6,
            bonus_vitesse=1,
            description="Tissée de fils enchantés, elle dissipe les énergies magiques.",
            classes_compatibles=["Mage", "Pretre", "Apothicaire"],
            emoji="🔮"
        )


class CuirBarde(Armure):
    """Équilibre défense physique et vitesse"""
    def __init__(self):
        super().__init__(
            nom="Cuir souple du barde",
            type_armure="Armure légère",
            bonus_defense=2,
            bonus_defense_magique=2,
            bonus_vitesse=2,
            description="Un cuir travaillé qui ne gêne pas les mouvements.",
            classes_compatibles=["Barde", "Voleur", "Eclaireur"],
            emoji="🎭"
        )


class CotteMailles(Armure):
    """Défense physique solide sans trop pénaliser la vitesse"""
    def __init__(self):
        super().__init__(
            nom="Cotte de mailles",
            type_armure="Armure intermédiaire",
            bonus_defense=4,
            bonus_defense_magique=1,
            bonus_vitesse=-1,
            description="Des anneaux de métal entrelacés, robuste et polyvalente.",
            classes_compatibles=["Viking", "Paladin", "Eclaireur"],
            emoji="⛓️"
        )


class ManteauEsprits(Armure):
    """Défense magique + bonus de vitesse pour les classes Spirit"""
    def __init__(self):
        super().__init__(
            nom="Manteau des esprits",
            type_armure="Manteau enchanté",
            bonus_defense=1,
            bonus_defense_magique=5,
            bonus_vitesse=2,
            description="Un manteau imprégné d'énergie spectrale qui repousse les sorts.",
            classes_compatibles=["Mage", "Pretre", "Barde"],
            emoji="🌫️"
        )


class ArmeureEclaireur(Armure):
    """Légère, bonus de vitesse important"""
    def __init__(self):
        super().__init__(
            nom="Tenue de l'éclaireur",
            type_armure="Tenue légère",
            bonus_defense=2,
            bonus_defense_magique=0,
            bonus_vitesse=4,
            description="Conçue pour courir et esquiver plutôt qu'encaisser.",
            classes_compatibles=["Eclaireur", "Voleur"],
            emoji="🏃"
        )


class BouclierRunique(Armure):
    """Équilibre défenses physique et magique"""
    def __init__(self):
        super().__init__(
            nom="Bouclier runique",
            type_armure="Bouclier",
            bonus_defense=3,
            bonus_defense_magique=3,
            bonus_vitesse=0,
            description="Gravé de runes anciennes, il résiste aux attaques de toute nature.",
            classes_compatibles=["Paladin", "Viking", "Pretre"],
            emoji="🔰"
        )


class VoileVoleur(Armure):
    """Maximise la vitesse, défense symbolique"""
    def __init__(self):
        super().__init__(
            nom="Voile du voleur",
            type_armure="Tenue furtive",
            bonus_defense=1,
            bonus_defense_magique=1,
            bonus_vitesse=5,
            description="Aussi léger qu'une ombre, impossible à frapper.",
            classes_compatibles=["Voleur", "Barde", "Eclaireur"],
            emoji="🕶️"
        )


# ─── Registre complet ───────────────────────────────────────────────────────

TOUTES_LES_ARMURES = [
    CuirassePlates,
    RobeArcane,
    CuirBarde,
    CotteMailles,
    ManteauEsprits,
    ArmeureEclaireur,
    BouclierRunique,
    VoileVoleur,
]


def get_armures_pour_classe(nom_classe, nombre=3):
    """Retourne `nombre` armures adaptées à la classe du joueur."""
    compatibles   = [cls() for cls in TOUTES_LES_ARMURES
                     if nom_classe in cls().classes_compatibles]
    incompatibles = [cls() for cls in TOUTES_LES_ARMURES
                     if nom_classe not in cls().classes_compatibles]

    random.shuffle(compatibles)
    random.shuffle(incompatibles)

    selection = compatibles[:nombre]
    if len(selection) < nombre:
        selection += incompatibles[:nombre - len(selection)]

    return selection[:nombre]


def choisir_armure(armures):
    """Affiche les armures proposées et retourne celle choisie par le joueur."""
    print(f"\n{'='*60}")
    print("🛡️  CHOISISSEZ UNE ARMURE")
    print(f"{'='*60}\n")

    for i, armure in enumerate(armures, 1):
        print(f"  [{i}]", end="")
        armure.afficher()

    print(f"\n{'─'*60}")

    while True:
        choix = input("Votre choix (1/2/3) : ").strip()
        if choix in ["1", "2", "3"] and int(choix) <= len(armures):
            armure_choisie = armures[int(choix) - 1]
            print(f"\n✅ Vous équipez : {armure_choisie}")
            return armure_choisie
        else:
            print("❌ Choix invalide. Entrez 1, 2 ou 3.")