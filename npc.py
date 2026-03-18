from dialogues.marchand import RENCONTRE
from armures import get_armures_pour_classe, choisir_armure


class NPC:
    """Classe de base pour tous les PNJ"""

    def __init__(self, nom, emoji="🧑"):
        self.nom = nom
        self.emoji = emoji

    def parler(self, texte):
        """Affiche un dialogue formaté"""
        print(f"\n{'─'*60}")
        print(f"{self.emoji}  {self.nom} :")
        print()
        for ligne in texte.split("\n"):
            print(f"   {ligne}")
        print(f"{'─'*60}")

    def interagir(self, personnage):
        """À surcharger dans chaque sous-classe"""
        raise NotImplementedError


class Marchand(NPC):
    """Marchand des égouts — offre 3 armures gratuites au joueur"""

    def __init__(self):
        super().__init__("Marchand des Égouts", emoji="🧟")

    def interagir(self, personnage):
        """Lance la rencontre : dialogue puis choix d'armure"""
        self.parler(RENCONTRE)

        nom_classe = personnage.classe.nom if personnage.classe else ""
        armures    = get_armures_pour_classe(nom_classe, nombre=3)
        armure     = choisir_armure(armures)

        personnage.equiper_armure(armure)
        print(f"📊 Nouvelles stats : {personnage.stats}")