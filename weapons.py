import random


class Arme:
    """Classe de base pour toutes les armes"""

    def __init__(self, nom, type_arme, bonus_attaque, bonus_defense, description, classes_compatibles, emoji,
                 bonus_attaque_magique=0, bonus_defense_magique=0, est_magique=False):
        self.nom = nom
        self.type_arme = type_arme
        self.bonus_attaque = bonus_attaque
        self.bonus_defense = bonus_defense
        self.bonus_attaque_magique = bonus_attaque_magique
        self.bonus_defense_magique = bonus_defense_magique
        self.est_magique = est_magique  # Si True, l'attaque scale sur ATK MAG et est bloquée par DEF MAG
        self.description = description
        self.classes_compatibles = classes_compatibles
        self.emoji = emoji

    def afficher(self):
        """Affiche les informations de l'arme"""
        type_label = "✨ MAGIQUE" if self.est_magique else "⚔️  PHYSIQUE"
        print(f"\n  {self.emoji} {self.nom} [{self.type_arme}] — {type_label}")
        print(f"     {self.description}")
        parties = []
        if self.bonus_attaque > 0:
            parties.append(f"+{self.bonus_attaque} ATK")
        if self.bonus_defense > 0:
            parties.append(f"+{self.bonus_defense} DEF")
        if self.bonus_attaque_magique > 0:
            parties.append(f"+{self.bonus_attaque_magique} ATK MAG")
        if self.bonus_defense_magique > 0:
            parties.append(f"+{self.bonus_defense_magique} DEF MAG")
        print(f"     📈 {'  |  '.join(parties) if parties else 'Aucun bonus'}")

    def __str__(self):
        parties = []
        if self.bonus_attaque > 0:
            parties.append(f"+{self.bonus_attaque} ATK")
        if self.bonus_defense > 0:
            parties.append(f"+{self.bonus_defense} DEF")
        if self.bonus_attaque_magique > 0:
            parties.append(f"+{self.bonus_attaque_magique} ATK MAG")
        if self.bonus_defense_magique > 0:
            parties.append(f"+{self.bonus_defense_magique} DEF MAG")
        tag = " [MAG]" if self.est_magique else ""
        return f"{self.emoji} {self.nom}{tag} ({', '.join(parties)})"


# ─── Les 8 armes ────────────────────────────────────────────────────────────

class Epee(Arme):
    def __init__(self):
        super().__init__(
            nom="Épée longue",
            type_arme="Épée",
            bonus_attaque=4,
            bonus_defense=1,
            description="Une lame équilibrée, fiable au corps à corps.",
            classes_compatibles=["Viking", "Paladin", "Eclaireur"],
            emoji="⚔️"
        )


class Grimoire(Arme):
    def __init__(self):
        super().__init__(
            nom="Grimoire des Arcanes",
            type_arme="Grimoire magique",
            bonus_attaque=0,
            bonus_defense=0,
            bonus_attaque_magique=6,
            bonus_defense_magique=1,
            est_magique=True,
            description="Un livre ancien qui amplifie la puissance magique.",
            classes_compatibles=["Mage", "Apothicaire", "Pretre"],
            emoji="📖"
        )


class Lance(Arme):
    def __init__(self):
        super().__init__(
            nom="Lance de guerre",
            type_arme="Lance",
            bonus_attaque=4,
            bonus_defense=2,
            description="Une lance robuste, idéale pour tenir les ennemis à distance.",
            classes_compatibles=["Viking", "Paladin", "Eclaireur"],
            emoji="🗡️"
        )


class Arc(Arme):
    def __init__(self):
        super().__init__(
            nom="Arc composite",
            type_arme="Arc",
            bonus_attaque=5,
            bonus_defense=0,
            description="Un arc puissant taillé pour la précision.",
            classes_compatibles=["Eclaireur", "Voleur", "Barde"],
            emoji="🏹"
        )


class Massue(Arme):
    def __init__(self):
        super().__init__(
            nom="Hache brutale",
            type_arme="Massue/Hache",
            bonus_attaque=6,
            bonus_defense=0,
            description="Une arme lourde qui fracasse tout sur son passage.",
            classes_compatibles=["Viking", "Paladin"],
            emoji="🪓"
        )


class Instrument(Arme):
    def __init__(self):
        super().__init__(
            nom="Luth enchanté",
            type_arme="Instrument de musique",
            bonus_attaque=0,
            bonus_defense=2,
            bonus_attaque_magique=4,
            bonus_defense_magique=1,
            est_magique=True,
            description="Les notes jouées envoûtent et désarçonnent les ennemis.",
            classes_compatibles=["Barde", "Apothicaire"],
            emoji="🎸"
        )


class Dague(Arme):
    def __init__(self):
        super().__init__(
            nom="Dague empoisonnée",
            type_arme="Dague",
            bonus_attaque=4,
            bonus_defense=1,
            description="Légère et rapide, son poison affaiblit les ennemis.",
            classes_compatibles=["Voleur", "Eclaireur", "Barde"],
            emoji="🔪"
        )


class Baton(Arme):
    def __init__(self):
        super().__init__(
            nom="Bâton des esprits",
            type_arme="Bâton",
            bonus_attaque=0,
            bonus_defense=2,
            bonus_attaque_magique=5,
            bonus_defense_magique=2,
            est_magique=True,
            description="Un bâton ancien qui canalise les énergies protectrices.",
            classes_compatibles=["Mage", "Pretre", "Apothicaire", "Barde"],
            emoji="🪄"
        )


# ─── Registre complet des armes ─────────────────────────────────────────────

TOUTES_LES_ARMES = [
    Epee,
    Grimoire,
    Lance,
    Arc,
    Massue,
    Instrument,
    Dague,
    Baton,
]


def get_armes_pour_classe(nom_classe, nombre=3):
    """
    Retourne `nombre` armes aléatoires adaptées à la classe du joueur.
    Priorité aux armes compatibles, complétées par des armes neutres si besoin.
    """
    compatibles = [cls() for cls in TOUTES_LES_ARMES
                   if nom_classe in cls().classes_compatibles]
    incompatibles = [cls() for cls in TOUTES_LES_ARMES
                     if nom_classe not in cls().classes_compatibles]

    random.shuffle(compatibles)
    random.shuffle(incompatibles)

    selection = compatibles[:nombre]

    # Compléter si moins de 3 armes compatibles
    if len(selection) < nombre:
        selection += incompatibles[:nombre - len(selection)]

    return selection[:nombre]


def choisir_arme(armes):
    """
    Affiche les 3 armes proposées et demande au joueur d'en choisir une.
    Retourne l'arme choisie.
    """
    print(f"\n{'='*60}")
    print("🎁  VOUS TROUVEZ UN COFFRE D'ARMES !")
    print(f"{'='*60}")
    print("Trois armes s'offrent à vous. Choisissez-en une :\n")

    for i, arme in enumerate(armes, 1):
        print(f"  [{i}]", end="")
        arme.afficher()

    print(f"\n{'─'*60}")

    while True:
        choix = input("Votre choix (1/2/3) : ").strip()
        if choix in ["1", "2", "3"] and int(choix) <= len(armes):
            arme_choisie = armes[int(choix) - 1]
            print(f"\n✅ Vous équipez : {arme_choisie}")
            return arme_choisie
        else:
            print("❌ Choix invalide. Entrez 1, 2 ou 3.")