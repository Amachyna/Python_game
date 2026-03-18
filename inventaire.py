class Objet:
    """Classe de base pour tous les objets utilisables"""

    def __init__(self, nom, description, emoji):
        self.nom = nom
        self.description = description
        self.emoji = emoji

    def utiliser(self, personnage, combat=None):
        """À surcharger dans chaque sous-classe. Retourne True si l'objet est consommé."""
        raise NotImplementedError

    def afficher(self):
        print(f"  {self.emoji} {self.nom} — {self.description}")

    def __str__(self):
        return f"{self.emoji} {self.nom}"


class PotionSoin(Objet):
    """Restaure 50% des PV max du joueur"""

    def __init__(self):
        super().__init__(
            nom="Potion de soin",
            description="Restaure 50% de vos PV maximum.",
            emoji="🧪"
        )

    def utiliser(self, personnage, combat=None):
        soin = max(1, personnage.stats.pv_max // 2)
        avant = personnage.stats.pv
        personnage.stats.pv = min(personnage.stats.pv_max, personnage.stats.pv + soin)
        reel = personnage.stats.pv - avant
        print(f"\n🧪 Vous buvez la Potion de soin et récupérez {reel} PV !")
        print(f"❤️  PV : {personnage.stats.pv}/{personnage.stats.pv_max}")
        return True  # Consommée


class PotionPerfection(Objet):
    """Permet de frapper 2 fois par tour pendant 3 tours"""

    DUREE = 3

    def __init__(self):
        super().__init__(
            nom="Potion de perfection",
            description=f"Vous frappez 2 fois par tour pendant {self.DUREE} tours.",
            emoji="⚗️"
        )

    def utiliser(self, personnage, combat=None):
        if combat is None:
            print("⚠️  Cette potion ne peut être utilisée qu'en combat !")
            return False  # Non consommée
        combat.activer_perfection(self.DUREE)
        print(f"\n⚗️  Potion de perfection ! Vous frapperez 2 fois par tour pendant {self.DUREE} tours !")
        return True  # Consommée


# ─── Classe Inventaire ───────────────────────────────────────────────────────

class Inventaire:
    """Gère l'inventaire du joueur"""

    CAPACITE_MAX = 10

    def __init__(self):
        self.objets = []

    def ajouter(self, objet):
        """Ajoute un objet si l'inventaire n'est pas plein"""
        if len(self.objets) >= self.CAPACITE_MAX:
            print(f"⚠️  Inventaire plein ! Impossible d'ajouter {objet.nom}.")
            return False
        self.objets.append(objet)
        return True

    def retirer(self, index):
        """Retire et retourne l'objet à l'index donné"""
        if 0 <= index < len(self.objets):
            return self.objets.pop(index)
        return None

    def est_vide(self):
        return len(self.objets) == 0

    def afficher(self):
        print(f"\n{'='*50}")
        print(f"🎒 INVENTAIRE ({len(self.objets)}/{self.CAPACITE_MAX})")
        print(f"{'='*50}")
        if self.est_vide():
            print("  Inventaire vide.")
        else:
            for i, objet in enumerate(self.objets, 1):
                print(f"  [{i}]", end=" ")
                objet.afficher()
        print(f"{'='*50}")

    def choisir_et_utiliser(self, personnage, combat=None):
        """
        Affiche l'inventaire et demande au joueur quel objet utiliser.
        Retourne True si un objet a été utilisé (tour consommé), False sinon.
        """
        self.afficher()

        if self.est_vide():
            input("  [ Appuyez sur Entrée pour continuer... ]")
            return False

        print(f"  [0] Retour")
        while True:
            choix = input(f"  Utiliser quel objet ? (0-{len(self.objets)}) : ").strip()
            if choix == "0":
                return False
            if choix.isdigit() and 1 <= int(choix) <= len(self.objets):
                index = int(choix) - 1
                objet = self.objets[index]
                consomme = objet.utiliser(personnage, combat=combat)
                if consomme:
                    self.retirer(index)
                return True  # Tour consommé même si l'objet n'est pas utilisé
            else:
                print(f"  ❌ Choix invalide.")

    def __len__(self):
        return len(self.objets)

    def __str__(self):
        if self.est_vide():
            return "Inventaire vide"
        return ", ".join(str(o) for o in self.objets)