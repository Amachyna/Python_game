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


# ─── Objets équipement ───────────────────────────────────────────────────────

class ArmeItem(Objet):
    """Wrapper permettant de stocker une arme dans l'inventaire pour l'équiper plus tard"""

    def __init__(self, arme):
        super().__init__(
            nom=arme.nom,
            description=arme.description,
            emoji=arme.emoji
        )
        self.arme = arme

    def utiliser(self, personnage, combat=None):
        """Équipe l'arme sur un membre de l'équipe choisi par le joueur"""
        equipe = _get_equipe(personnage, combat)
        if equipe is None:
            # Hors combat : équiper directement sur le personnage
            ancienne = personnage.equiper_arme(self.arme)
            print(f"\n{self.emoji} {personnage.prenom} équipe {self.arme.nom} !")
            if ancienne:
                print(f"   {ancienne} est remise dans l'inventaire.")
            return True, ancienne
        # En équipe : choisir le membre
        return _choisir_membre_et_equiper(equipe, self.arme, "arme")

    def afficher(self):
        self.arme.afficher()

    def __str__(self):
        return str(self.arme)


class ArmureItem(Objet):
    """Wrapper permettant de stocker une armure dans l'inventaire"""

    def __init__(self, armure):
        super().__init__(
            nom=armure.nom,
            description=armure.description,
            emoji=armure.emoji
        )
        self.armure = armure

    def utiliser(self, personnage, combat=None):
        """Équipe l'armure sur un membre de l'équipe choisi par le joueur"""
        equipe = _get_equipe(personnage, combat)
        if equipe is None:
            ancienne = personnage.equiper_armure(self.armure)
            print(f"\n{self.emoji} {personnage.prenom} équipe {self.armure.nom} !")
            if ancienne:
                print(f"   {ancienne} est remise dans l'inventaire.")
            return True, ancienne
        return _choisir_membre_et_equiper(equipe, self.armure, "armure")

    def afficher(self):
        self.armure.afficher()

    def __str__(self):
        return str(self.armure)


def _get_equipe(personnage, combat):
    """Récupère l'équipe depuis le combat ou retourne None"""
    if combat and hasattr(combat, 'equipe'):
        return combat.equipe
    return None


def _choisir_membre_et_equiper(equipe, objet, type_objet):
    """
    Affiche les membres de l'équipe et demande lequel équiper.
    Retourne (True, ancienne_piece) ou (False, None) si annulé.
    """
    vivants = equipe.membres_vivants()
    print(f"\n👥 Choisissez le membre à équiper :")
    for i, m in enumerate(vivants, 1):
        equipe_actuel = str(m.arme) if type_objet == "arme" else str(m.armure)
        slot = f"Arme actuelle : {equipe_actuel}" if type_objet == "arme" else f"Armure actuelle : {equipe_actuel}"
        print(f"  [{i}] {m.prenom} {m.nom} — {slot}")
    print(f"  [0] Annuler")

    while True:
        choix = input(f"  Votre choix (0-{len(vivants)}) : ").strip()
        if choix == "0":
            return False, None
        if choix.isdigit() and 1 <= int(choix) <= len(vivants):
            membre = vivants[int(choix) - 1]
            if type_objet == "arme":
                ancienne = membre.equiper_arme(objet)
                print(f"\n⚔️  {membre.prenom} équipe {objet.nom} !")
            else:
                ancienne = membre.equiper_armure(objet)
                print(f"\n🛡️  {membre.prenom} équipe {objet.nom} !")
            if ancienne:
                print(f"   {ancienne} sera remise dans l'inventaire.")
            return True, ancienne
        print("  ❌ Choix invalide.")


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

    def choisir_et_utiliser(self, personnage, combat=None, equipe=None):
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

                # Arme ou armure : équipement sur un membre de l'équipe
                if isinstance(objet, (ArmeItem, ArmureItem)):
                    if equipe is None:
                        print("  ⚠️  Ouvrez le stock depuis le menu principal pour gérer les armes et armures.")
                        return False
                    self.retirer(index)
                    stock = equipe.stock if hasattr(equipe, 'stock') else self
                    _equiper_sur_membre(objet, equipe, stock)
                    return False  # N'est pas une action de combat

                # Potion ou autre objet consommable
                consomme = objet.utiliser(personnage, combat=combat)
                if consomme:
                    self.retirer(index)
                return consomme
            else:
                print(f"  ❌ Choix invalide.")

    def __len__(self):
        return len(self.objets)

    def __str__(self):
        if self.est_vide():
            return "Inventaire vide"
        return ", ".join(str(o) for o in self.objets)


# ─── Objets équipement (armes/armures depuis l'inventaire) ───────────────────

class ArmeItem(Objet):
    """Wrapper pour utiliser une arme depuis l'inventaire"""

    def __init__(self, arme):
        tier_label = f" T{arme.tier}" if arme.tier > 1 else ""
        super().__init__(
            nom=f"{arme.nom}{tier_label}",
            description=f"Arme — {arme}",
            emoji=arme.emoji
        )
        self.arme = arme

    def utiliser(self, personnage, combat=None):
        """Propose au joueur de choisir quel membre équiper (nécessite equipe)"""
        # On ne peut pas équiper depuis le combat sans référence à l'équipe
        # On renvoie False pour ne pas consommer le tour — à appeler hors combat
        print(f"\n⚠️  Utilisez l'équipement hors combat pour gérer les armes.")
        return False

    def equiper_sur(self, membre, inventaire_equipe):
        """Équipe l'arme sur le membre. L'ancienne arme retourne dans l'inventaire."""
        ancienne = membre.equiper_arme(self.arme)
        print(f"\n✅ {membre.prenom} équipe : {self.arme}")
        if ancienne is not None:
            item_ancien = ArmeItem(ancienne)
            if inventaire_equipe.ajouter(item_ancien):
                print(f"   {ancienne.nom} a été rangée dans l'inventaire de l'équipe.")
        print(f"   Stats : {membre.stats}")


class ArmureItem(Objet):
    """Wrapper pour utiliser une armure depuis l'inventaire"""

    def __init__(self, armure):
        tier_label = f" T{armure.tier}" if armure.tier > 1 else ""
        super().__init__(
            nom=f"{armure.nom}{tier_label}",
            description=f"Armure — {armure}",
            emoji=armure.emoji
        )
        self.armure = armure

    def utiliser(self, personnage, combat=None):
        print(f"\n⚠️  Utilisez l'équipement hors combat pour gérer les armures.")
        return False

    def equiper_sur(self, membre, inventaire_equipe):
        """Équipe l'armure sur le membre. L'ancienne armure retourne dans l'inventaire."""
        ancienne = membre.equiper_armure(self.armure)
        print(f"\n✅ {membre.prenom} équipe : {self.armure}")
        if ancienne is not None:
            item_ancien = ArmureItem(ancienne)
            if inventaire_equipe.ajouter(item_ancien):
                print(f"   {ancienne.nom} a été rangée dans l'inventaire de l'équipe.")
        print(f"   Stats : {membre.stats}")


def _equiper_sur_membre(item, equipe, retour_container):
    """Demande quel membre équiper et applique l'arme ou l'armure.
    retour_container : StockEquipement ou Inventaire où remettre l'ancienne pièce."""
    membres = equipe.membres
    print(f"\n  Sur quel personnage équiper {item.nom} ?")
    for i, m in enumerate(membres, 1):
        if isinstance(item, ArmeItem):
            slot = str(m.arme) if m.arme else "Aucune arme"
        else:
            slot = str(m.armure) if m.armure else "Aucune armure"
        print(f"  [{i}] {m.prenom} {m.nom}  (slot actuel : {slot})")
    print("  [0] Annuler")

    while True:
        choix = input(f"  Votre choix (0-{len(membres)}) : ").strip()
        if choix == "0":
            retour_container.ajouter(item)
            print("  Annulé — objet remis dans le stock.")
            return
        if choix.isdigit() and 1 <= int(choix) <= len(membres):
            membre = membres[int(choix) - 1]
            # Équiper et récupérer l'ancienne pièce
            if isinstance(item, ArmeItem):
                ancienne = membre.equiper_arme(item.arme)
                print(f"\n✅ {membre.prenom} équipe : {item.arme}")
                if ancienne:
                    retour_container.ajouter(ArmeItem(ancienne))
                    print(f"   {ancienne.nom} rangée dans le stock.")
            else:
                ancienne = membre.equiper_armure(item.armure)
                print(f"\n✅ {membre.prenom} équipe : {item.armure}")
                if ancienne:
                    retour_container.ajouter(ArmureItem(ancienne))
                    print(f"   {ancienne.nom} rangée dans le stock.")
            print(f"   Stats : {membre.stats}")
            return
        print("  ❌ Choix invalide.")


# ─── Stock d'équipement (armes/armures non équipées) ─────────────────────────

class StockEquipement:
    """Stocke les armes et armures non équipées de l'équipe"""

    def __init__(self):
        self.items = []  # Liste d'ArmeItem et ArmureItem

    def ajouter(self, item):
        if not isinstance(item, (ArmeItem, ArmureItem)):
            print(f"⚠️  {item} n'est pas un équipement.")
            return False
        self.items.append(item)
        return True

    def est_vide(self):
        return len(self.items) == 0

    def afficher(self):
        print(f"\n{'='*50}")
        print(f"🗃️  STOCK D'ÉQUIPEMENT ({len(self.items)} objet(s))")
        print(f"{'='*50}")
        if self.est_vide():
            print("  Aucun équipement en stock.")
        else:
            for i, item in enumerate(self.items, 1):
                type_label = "⚔️  Arme" if isinstance(item, ArmeItem) else "🛡️  Armure"
                print(f"  [{i}] {type_label} — ", end="")
                if isinstance(item, ArmeItem):
                    item.arme.afficher()
                else:
                    item.armure.afficher()
        print(f"{'='*50}")

    def gerer(self, equipe):
        """Menu interactif pour équiper un item du stock sur un membre"""
        self.afficher()
        if self.est_vide():
            input("  [ Appuyez sur Entrée pour continuer... ]")
            return

        print("  [0] Retour")
        while True:
            choix = input(f"  Équiper quel item ? (0-{len(self.items)}) : ").strip()
            if choix == "0":
                return
            if choix.isdigit() and 1 <= int(choix) <= len(self.items):
                item = self.items.pop(int(choix) - 1)
                _equiper_sur_membre(item, equipe, self)
                return
            print("  ❌ Choix invalide.")

    def __len__(self):
        return len(self.items)

    def __str__(self):
        if self.est_vide():
            return "Stock vide"
        return ", ".join(item.nom for item in self.items)