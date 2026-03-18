import random
from identiterUser import IdentiteJoueur, Statistiques
from inventaire import Inventaire, PotionSoin, StockEquipement
from breed import Feline, Human, Panda, Reptilian, Spirit, RACES_DISPONIBLES
from classe import (Apothicaire, Barde, Eclaireur, Mage, Paladin,
                    Pretre, Viking, Voleur, Admin, CLASSES_DISPONIBLES)

# Classes accessibles aux compagnons (Admin exclue)
CLASSES_COMPAGNON = {k: v for k, v in CLASSES_DISPONIBLES.items() if v is not Admin}

# ─── Banques de prénoms et noms aléatoires ───────────────────────────────────

PRENOMS = [
    "Aelys", "Bran", "Ciara", "Dorn", "Elowen", "Fynn", "Gara",
    "Haleth", "Isola", "Joren", "Kael", "Lira", "Morn", "Nessa",
    "Oryn", "Priya", "Quillan", "Reva", "Soren", "Tilda", "Ulric",
    "Vael", "Wren", "Xana", "Yola", "Zeph"
]

NOMS = [
    "Ashveil", "Brondar", "Coldmere", "Duskfall", "Emberholt",
    "Frostwick", "Gravenmore", "Holloway", "Ironkeep", "Jadewing",
    "Kettlemoor", "Lantern", "Mistholm", "Nightvale", "Oakhurst",
    "Pinewatch", "Quickthorn", "Ravenscar", "Stormgate", "Thistlewood",
    "Underhill", "Veilstone", "Whitecrest", "Yarrowfield", "Zephyrmoor"
]


def _prenom_aleatoire(exclu=""):
    candidats = [p for p in PRENOMS if p.lower() != exclu.lower()]
    return random.choice(candidats)


def _nom_aleatoire(exclu=""):
    candidats = [n for n in NOMS if n.lower() != exclu.lower()]
    return random.choice(candidats)


# ─── Création du compagnon ────────────────────────────────────────────────────

def creer_compagnon(joueur_principal):
    """
    Crée un compagnon avec race/classe/nom aléatoires différents du joueur,
    stats niveau 1 de base puis montée au niveau actuel du joueur avec
    tous les points de compétence appliqués automatiquement + 1 point libre.
    """
    compagnon = IdentiteJoueur()

    # Prénom et nom différents du joueur
    prenom = _prenom_aleatoire(exclu=str(joueur_principal.prenom))
    nom    = _nom_aleatoire(exclu=str(joueur_principal.nom))
    compagnon.prenom._prenom = prenom
    compagnon.nom._nom       = nom

    # Race aléatoire
    race_cls = random.choice(list(RACES_DISPONIBLES.values()))
    compagnon.definir_race(race_cls())

    # Classe aléatoire
    classe_cls = random.choice(list(CLASSES_COMPAGNON.values()))
    compagnon.definir_classe(classe_cls())

    # Monter au niveau du joueur avec tous les points auto + 1 libre par niveau
    niveau_cible = joueur_principal.niveau
    if niveau_cible > 1:
        _montee_niveau_auto(compagnon, niveau_cible)

    print(f"\n{'='*60}")
    print(f"🤝 {prenom} {nom} rejoint votre équipe !")
    print(f"   Race : {compagnon.race.nom}  |  Classe : {compagnon.classe.nom}")
    print(f"   Niveau : {compagnon.niveau}")
    print(f"   {compagnon.stats}")
    print(f"{'='*60}")

    return compagnon


def _montee_niveau_auto(compagnon, niveau_cible):
    """Monte le compagnon jusqu'au niveau cible en appliquant les bonus auto."""
    STATS_AUTO = ["attaque", "defense", "attaque_magique", "defense_magique", "vitesse"]

    while compagnon.niveau < niveau_cible:
        compagnon.niveau += 1
        compagnon.xp_prochain_niveau = int(compagnon.xp_prochain_niveau * 1.5)

        # +1 à toutes les stats
        compagnon.stats.pv_max += 1
        compagnon.stats.pv     += 1
        for stat in STATS_AUTO:
            setattr(compagnon.stats, stat, getattr(compagnon.stats, stat) + 1)

        # 1 point auto sur une stat aléatoire (rattrapage)
        stat_auto = random.choice(STATS_AUTO)
        setattr(compagnon.stats, stat_auto, getattr(compagnon.stats, stat_auto) + 1)

    # 1 point libre supplémentaire à placer par le joueur
    print(f"\n🎯 {compagnon.prenom} a rejoint au niveau {compagnon.niveau}.")
    print("   Vous pouvez lui attribuer 1 point de compétence :")
    compagnon._attribuer_point_competence()


# ─── Classe Equipe ────────────────────────────────────────────────────────────

class Equipe:
    """Gère l'équipe du joueur (personnage principal + compagnons)"""

    def __init__(self, joueur_principal):
        self.membres = [joueur_principal]   # Le joueur principal est toujours en index 0
        self.inventaire = Inventaire()       # Inventaire partagé (potions)
        self.inventaire.ajouter(PotionSoin())  # Potion de départ
        self.stock = StockEquipement()         # Armes/armures non équipées

    @property
    def joueur(self):
        return self.membres[0]

    def ajouter_membre(self, compagnon):
        self.membres.append(compagnon)
        print(f"✅ {compagnon.prenom} a rejoint l'équipe !")

    def membres_vivants(self):
        return [m for m in self.membres if m.stats.pv > 0]

    def est_en_vie(self):
        return any(m.stats.pv > 0 for m in self.membres)

    def afficher(self):
        print(f"\n{'='*60}")
        print(f"👥 ÉQUIPE ({len(self.membres_vivants())}/{len(self.membres)} en vie)")
        print(f"{'='*60}")
        for i, m in enumerate(self.membres):
            statut = "✅" if m.stats.pv > 0 else "💀"
            role   = " (Principal)" if i == 0 else " (Compagnon)"
            print(f"  {statut} {m.prenom} {m.nom}{role}")
            print(f"     Niv.{m.niveau} | {m.stats}")
        print(f"  🎒 Inventaire : {self.inventaire}")
        print(f"  🗃️  Stock équipement : {self.stock}")
        print(f"{'='*60}")

    def gagner_xp_equipe(self, xp, gold):
        """Distribue l'XP et le gold à tous les membres vivants"""
        for m in self.membres_vivants():
            m.gagner_xp(xp, gold)