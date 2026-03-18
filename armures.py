import random


class Armure:
    """Classe de base pour toutes les armures"""

    def __init__(self, nom, type_armure, bonus_defense, bonus_defense_magique,
                 bonus_vitesse, description, classes_compatibles, emoji, tier=1):
        self.nom = nom
        self.type_armure = type_armure
        self.bonus_defense = bonus_defense
        self.bonus_defense_magique = bonus_defense_magique
        self.bonus_vitesse = bonus_vitesse
        self.description = description
        self.classes_compatibles = classes_compatibles
        self.emoji = emoji
        self.tier = tier

    def afficher(self):
        """Affiche les informations de l'armure"""
        tier_label = f" ★ Tier {self.tier}" if self.tier > 1 else ""
        print(f"\n  {self.emoji} {self.nom} [{self.type_armure}]{tier_label}")
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
        tier = f" T{self.tier}" if self.tier > 1 else ""
        return f"{self.emoji} {self.nom}{tier} ({', '.join(parties)})"


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

ARMURES_T1 = [CuirassePlates, RobeArcane, CuirBarde, CotteMailles,
              ManteauEsprits, ArmeureEclaireur, BouclierRunique, VoileVoleur]
TOUTES_LES_ARMURES = ARMURES_T1  # Compatibilité


def get_armures_pour_classe(nom_classe, nombre=3, tier=1):
    """Retourne `nombre` armures du tier donné adaptées à la classe du joueur."""
    pool = ARMURES_T1 if tier == 1 else ARMURES_T2
    compatibles   = [cls() for cls in pool if nom_classe in cls().classes_compatibles]
    incompatibles = [cls() for cls in pool if nom_classe not in cls().classes_compatibles]
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


# ─── Armures Tier 2 — Forêt ──────────────────────────────────────────────────

class PlaquesForet(Armure):
    def __init__(self):
        super().__init__("Plaques de la Forêt", "Armure lourde",
            12, 0, -1,
            "Des plaques d'écorce d'ent renforcées de métal.",
            ["Viking", "Paladin"], "🛡️", tier=2)

class RobeNaturelle(Armure):
    def __init__(self):
        super().__init__("Robe de la Nature", "Robe magique",
            0, 13, 2,
            "Tissée avec les fils de la magie sylvestre.",
            ["Mage", "Pretre", "Apothicaire"], "🔮", tier=2)

class CuirRodeur(Armure):
    def __init__(self):
        super().__init__("Cuir du Rôdeur", "Armure légère",
            5, 4, 4,
            "Un cuir tanné par les esprits de la forêt, léger et résistant.",
            ["Barde", "Voleur", "Eclaireur"], "🎭", tier=2)

class CotteMithril(Armure):
    def __init__(self):
        super().__init__("Cotte de Mithril", "Armure intermédiaire",
            9, 3, -1,
            "Des anneaux de mithril, résistants mais étonnamment légers.",
            ["Viking", "Paladin", "Eclaireur"], "⛓️", tier=2)

class ManteauArchimage(Armure):
    def __init__(self):
        super().__init__("Manteau de l'Archimage", "Manteau enchanté",
            2, 11, 3,
            "Un manteau tissé de sorts anciens, dissipant la magie ennemie.",
            ["Mage", "Pretre", "Barde"], "🌫️", tier=2)

class TenueOmbre(Armure):
    def __init__(self):
        super().__init__("Tenue de l'Ombre", "Tenue légère",
            4, 0, 7,
            "Une tenue forgée dans l'obscurité, presque impossible à toucher.",
            ["Eclaireur", "Voleur"], "🏃", tier=2)

class BouclierDruidique(Armure):
    def __init__(self):
        super().__init__("Bouclier Druidique", "Bouclier",
            7, 7, 0,
            "Gravé de runes druidiques, protège contre toute forme d'attaque.",
            ["Paladin", "Viking", "Pretre"], "🔰", tier=2)

class VoileSpectre(Armure):
    def __init__(self):
        super().__init__("Voile du Spectre", "Tenue furtive",
            2, 2, 9,
            "Une tenue quasi immatérielle, vous rendant aussi rapide qu'un fantôme.",
            ["Voleur", "Barde", "Eclaireur"], "🕶️", tier=2)


ARMURES_T2 = [PlaquesForet, RobeNaturelle, CuirRodeur, CotteMithril,
              ManteauArchimage, TenueOmbre, BouclierDruidique, VoileSpectre]