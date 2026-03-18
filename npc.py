from dialogues.marchand import RENCONTRE, RENCONTRE_FORET
from armures import get_armures_pour_classe, choisir_armure
from weapons import get_armes_pour_classe, choisir_arme
from inventaire import PotionSoin, PotionPerfection, ArmeItem, ArmureItem


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

    def interagir(self, personnage, equipe=None):
        """Lance la rencontre : dialogue puis choix d'armure"""
        self.parler(RENCONTRE)

        nom_classe = personnage.classe.nom if personnage.classe else ""
        armures    = get_armures_pour_classe(nom_classe, nombre=3)
        armure     = choisir_armure(armures)

        ancienne = personnage.equiper_armure(armure)
        if ancienne and equipe:
            equipe.stock.ajouter(ArmureItem(ancienne))
            print(f"   {ancienne.nom} rangée dans le stock d'équipement.")
        print(f"📊 Nouvelles stats : {personnage.stats}")


class MarchandForet(NPC):
    """Marchand de la forêt — boutique payante salle 25"""

    PRIX = {
        "arme":     60,
        "armure":   50,
        "soin":     15,
        "perfection": 25,
    }

    def __init__(self):
        super().__init__("Marchand des Égouts", emoji="🧟")

    def interagir(self, personnage, equipe=None):
        """Dialogue + boutique à 4 slots, 1 achat max par slot"""
        self.parler(RENCONTRE_FORET)
        # Le joueur principal paie, l'inventaire est partagé
        inventaire = equipe.inventaire if equipe else None
        print(f"\n💰 Or de l'équipe : {personnage.gold} Gold")
        self._boutique(personnage, equipe, inventaire)

    def _boutique(self, personnage, equipe, inventaire):
        """Affiche la boutique et gère les achats (1 par slot)"""
        achetes = set()

        while True:
            print(f"\n{'='*60}")
            print(f"🏪 BOUTIQUE DU MARCHAND  —  Or : {personnage.gold} Gold")
            print(f"{'='*60}")

            slots = [
                ("arme",        self.PRIX["arme"],       "⚔️  Arme Tier 2"),
                ("armure",      self.PRIX["armure"],      "🛡️  Armure Tier 2"),
                ("soin",        self.PRIX["soin"],        "🧪 Potion de soin"),
                ("perfection",  self.PRIX["perfection"],  "⚗️  Potion de perfection"),
            ]

            for i, (slot, prix, label) in enumerate(slots, 1):
                if slot in achetes:
                    print(f"  [{i}] {label:<28} ✅ Acheté")
                elif personnage.gold < prix:
                    print(f"  [{i}] {label:<28} {prix} Gold  ❌ Pas assez d'or")
                else:
                    print(f"  [{i}] {label:<28} {prix} Gold")
            print(f"  [0] Quitter la boutique")
            print(f"{'─'*60}")

            choix = input("  Votre choix : ").strip()

            if choix == "0":
                print(f"\n🧟 Marchand : «Bonne chance à vous !»")
                break
            if not choix.isdigit() or not (1 <= int(choix) <= 4):
                print("  ❌ Choix invalide.")
                continue

            idx = int(choix) - 1
            slot, prix, label = slots[idx]

            if slot in achetes:
                print("  ❌ Vous avez déjà acheté ce slot.")
                continue
            if personnage.gold < prix:
                print(f"  ❌ Pas assez d'or. Il vous faut {prix} Gold.")
                continue

            personnage.gold -= prix
            print(f"\n✅ Achat ! Il vous reste {personnage.gold} Gold.")
            achetes.add(slot)

            if slot == "arme":
                self._acheter_equipement(personnage, equipe, inventaire, "arme")
            elif slot == "armure":
                self._acheter_equipement(personnage, equipe, inventaire, "armure")
            elif slot == "soin":
                if inventaire and inventaire.ajouter(PotionSoin()):
                    print("  🧪 Potion de soin ajoutée à l'inventaire de l'équipe.")
            elif slot == "perfection":
                if inventaire and inventaire.ajouter(PotionPerfection()):
                    print("  ⚗️  Potion de perfection ajoutée à l'inventaire de l'équipe.")

    def _acheter_equipement(self, personnage, equipe, inventaire, type_objet):
        """Choisit une arme ou armure T2 et demande sur quel membre l'équiper"""
        nom_classe = personnage.classe.nom if personnage.classe else ""
        membres = equipe.membres if equipe else [personnage]

        if type_objet == "arme":
            items = get_armes_pour_classe(nom_classe, nombre=3, tier=2)
            choix_item = choisir_arme(items)
        else:
            items = get_armures_pour_classe(nom_classe, nombre=3, tier=2)
            choix_item = choisir_armure(items)

        # Choisir le membre
        print(f"\n  Sur quel personnage équiper {choix_item.nom} ?")
        for i, m in enumerate(membres, 1):
            slot_actuel = str(m.arme) if type_objet == "arme" else str(m.armure)
            if not slot_actuel or slot_actuel == "None":
                slot_actuel = "Aucun"
            print(f"  [{i}] {m.prenom} {m.nom} — actuel : {slot_actuel}")

        while True:
            c = input(f"  Votre choix (1-{len(membres)}) : ").strip()
            if c.isdigit() and 1 <= int(c) <= len(membres):
                membre = membres[int(c) - 1]
                if type_objet == "arme":
                    ancienne = membre.equiper_arme(choix_item)
                    print(f"  ✅ {membre.prenom} équipe {choix_item.nom} !")
                    if ancienne and equipe:
                        equipe.stock.ajouter(ArmeItem(ancienne))
                        print(f"     {ancienne.nom} rangée dans le stock d'équipement.")
                else:
                    ancienne = membre.equiper_armure(choix_item)
                    print(f"  ✅ {membre.prenom} équipe {choix_item.nom} !")
                    if ancienne and equipe:
                        equipe.stock.ajouter(ArmureItem(ancienne))
                        print(f"     {ancienne.nom} rangée dans le stock d'équipement.")
                print(f"  📊 Stats : {membre.stats}")
                return
            print("  ❌ Choix invalide.")