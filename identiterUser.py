class Statistiques:
    """Classe pour gérer les statistiques du personnage"""
    
    def __init__(self, pv=20, attaque=3, defense=5, attaque_magique=2, defense_magique=3, vitesse=5):
        self._pv = pv
        self._pv_max = pv
        self._attaque = attaque
        self._defense = defense
        self._attaque_magique = attaque_magique
        self._defense_magique = defense_magique
        self._vitesse = vitesse
    
    @property
    def pv(self):
        """Getter pour les points de vie"""
        return self._pv
    
    @pv.setter
    def pv(self, valeur):
        """Setter pour les points de vie"""
        if valeur < 0:
            self._pv = 0
        elif valeur > self._pv_max:
            self._pv = self._pv_max
        else:
            self._pv = valeur
    
    @property
    def pv_max(self):
        """Getter pour les PV maximum"""
        return self._pv_max
    
    @pv_max.setter
    def pv_max(self, valeur):
        """Setter pour les PV maximum"""
        if valeur >= 0:
            self._pv_max = valeur
    
    @property
    def attaque(self):
        """Getter pour l'attaque"""
        return self._attaque
    
    @attaque.setter
    def attaque(self, valeur):
        """Setter pour l'attaque"""
        if valeur >= 0:
            self._attaque = valeur
    
    @property
    def defense(self):
        """Getter pour la défense"""
        return self._defense
    
    @defense.setter
    def defense(self, valeur):
        """Setter pour la défense"""
        if valeur >= 0:
            self._defense = valeur

    @property
    def attaque_magique(self):
        return self._attaque_magique

    @attaque_magique.setter
    def attaque_magique(self, valeur):
        if valeur >= 0:
            self._attaque_magique = valeur

    @property
    def defense_magique(self):
        return self._defense_magique

    @defense_magique.setter
    def defense_magique(self, valeur):
        if valeur >= 0:
            self._defense_magique = valeur

    @property
    def vitesse(self):
        return self._vitesse

    @vitesse.setter
    def vitesse(self, valeur):
        if valeur >= 0:
            self._vitesse = valeur

    def afficher_stats(self):
        """Affiche les statistiques du personnage"""
        print(f"\n📊 === STATISTIQUES ===")
        print(f"❤️  Points de Vie    : {self._pv}/{self._pv_max}")
        print(f"⚔️  Attaque          : {self._attaque}")
        print(f"🛡️  Défense          : {self._defense}")
        print(f"✨ Attaque magique  : {self._attaque_magique}")
        print(f"🔮 Défense magique  : {self._defense_magique}")
        print(f"💨 Vitesse          : {self._vitesse}")
    
    def __str__(self):
        return (f"PV: {self._pv}/{self._pv_max} | ATK: {self._attaque} | DEF: {self._defense} | "
                f"ATK MAG: {self._attaque_magique} | DEF MAG: {self._defense_magique} | VIT: {self._vitesse}")


class Nom:
    """Classe pour gérer le nom de famille du joueur"""
    
    def __init__(self, nom=""):
        self._nom = nom
    
    @property
    def nom(self):
        """Getter pour le nom"""
        return self._nom
    
    @nom.setter
    def nom(self, valeur):
        """Setter pour le nom avec validation"""
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le nom doit être une chaîne non vide")
        
        valeur_nettoyee = valeur.strip()
        
        # Vérifier la longueur maximale
        if len(valeur_nettoyee) > 16:
            raise ValueError("Le nom ne peut pas dépasser 16 caractères")
        
        # Vérifier qu'il n'y a pas de chiffres
        if any(char.isdigit() for char in valeur_nettoyee):
            raise ValueError("Le nom ne peut pas contenir de chiffres")
        
        # Vérifier qu'il n'y a pas de caractères spéciaux (sauf espaces, tirets et apostrophes)
        caracteres_autorises = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàâäæçéèêëïîôùûüÿœÀÂÄÆÇÉÈÊËÏÎÔÙÛÜŸŒ -'")
        if not all(char in caracteres_autorises for char in valeur_nettoyee):
            raise ValueError("Le nom ne peut contenir que des lettres, espaces, tirets et apostrophes")
        
        self._nom = valeur_nettoyee
    
    def demander_nom(self):
        """Demande le nom au joueur"""
        while True:
            nom_saisi = input("Entrez votre nom de famille (max 16 caractères, lettres uniquement) : ")
            try:
                self.nom = nom_saisi
                break
            except ValueError as e:
                print(f"❌ Erreur : {e}")
        return self._nom
        return self._nom
    
    def __str__(self):
        return self._nom


class Prenom:
    """Classe pour gérer le prénom du joueur"""
    
    def __init__(self, prenom=""):
        self._prenom = prenom
    
    @property
    def prenom(self):
        """Getter pour le prénom"""
        return self._prenom
    
    @prenom.setter
    def prenom(self, valeur):
        """Setter pour le prénom avec validation"""
        if not isinstance(valeur, str) or not valeur.strip():
            raise ValueError("Le prénom doit être une chaîne non vide")
        
        valeur_nettoyee = valeur.strip()
        
        # Vérifier la longueur maximale
        if len(valeur_nettoyee) > 16:
            raise ValueError("Le prénom ne peut pas dépasser 16 caractères")
        
        # Vérifier qu'il n'y a pas de chiffres
        if any(char.isdigit() for char in valeur_nettoyee):
            raise ValueError("Le prénom ne peut pas contenir de chiffres")
        
        # Vérifier qu'il n'y a pas de caractères spéciaux (sauf espaces, tirets et apostrophes)
        caracteres_autorises = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàâäæçéèêëïîôùûüÿœÀÂÄÆÇÉÈÊËÏÎÔÙÛÜŸŒ -'")
        if not all(char in caracteres_autorises for char in valeur_nettoyee):
            raise ValueError("Le prénom ne peut contenir que des lettres, espaces, tirets et apostrophes")
        
        self._prenom = valeur_nettoyee
    
    def demander_prenom(self):
        """Demande le prénom au joueur"""
        while True:
            prenom_saisi = input("Entrez votre prénom (max 16 caractères, lettres uniquement) : ")
            try:
                self.prenom = prenom_saisi
                break
            except ValueError as e:
                print(f"❌ Erreur : {e}")
        return self._prenom
    
    def __str__(self):
        return self._prenom


class IdentiteJoueur:
    """Classe pour gérer l'identité complète du joueur"""
    
    def __init__(self):
        self.nom = Nom()
        self.prenom = Prenom()
        self.stats = Statistiques()  # Ajout des statistiques initiales
        self.race = None   # Race du personnage
        self.classe = None  # Classe du personnage
        self.arme = None    # Arme équipée
        self.armure = None  # Armure équipée
        self.niveau = 1
        self.xp = 0
        self.xp_prochain_niveau = 50  # XP nécessaire pour le niveau 2
        self.gold = 0
    
    def definir_race(self, race):
        """Définit la race du personnage et applique les bonus"""
        self.race = race
        self.race.apply_bonus(self.stats)
    
    def definir_classe(self, classe):
        """Définit la classe du personnage et applique les bonus"""
        self.classe = classe
        self.classe.apply_bonus(self.stats)
    
    def equiper_arme(self, arme):
        """Équipe une nouvelle arme en retirant les bonus de la précédente"""
        if self.arme is not None:
            self.stats.attaque         -= self.arme.bonus_attaque
            self.stats.defense         -= self.arme.bonus_defense
            self.stats.attaque_magique -= self.arme.bonus_attaque_magique
            self.stats.defense_magique -= self.arme.bonus_defense_magique

        self.arme = arme
        if arme is not None:
            self.stats.attaque         += arme.bonus_attaque
            self.stats.defense         += arme.bonus_defense
            self.stats.attaque_magique += arme.bonus_attaque_magique
            self.stats.defense_magique += arme.bonus_defense_magique

    def equiper_armure(self, armure):
        """Équipe une nouvelle armure en retirant les bonus de la précédente"""
        if self.armure is not None:
            self.stats.defense         -= self.armure.bonus_defense
            self.stats.defense_magique -= self.armure.bonus_defense_magique
            self.stats.vitesse         -= self.armure.bonus_vitesse

        self.armure = armure
        if armure is not None:
            self.stats.defense         += armure.bonus_defense
            self.stats.defense_magique += armure.bonus_defense_magique
            self.stats.vitesse         += armure.bonus_vitesse

    def gagner_xp(self, xp_gagne, gold_gagne=0):
        """Gagne de l'XP et de l'or, gère la montée de niveau"""
        self.xp += xp_gagne
        self.gold += gold_gagne
        print(f"\n✨ +{xp_gagne} XP  |  💰 +{gold_gagne} Gold")
        print(f"   XP : {self.xp}/{self.xp_prochain_niveau}  |  Gold total : {self.gold}")

        # Boucle au cas où plusieurs niveaux sont gagnés d'un coup
        while self.xp >= self.xp_prochain_niveau:
            self.xp -= self.xp_prochain_niveau
            self._monter_niveau()

    def _monter_niveau(self):
        """Gère la montée de niveau"""
        self.niveau += 1
        # XP requis augmente de 50% à chaque niveau
        self.xp_prochain_niveau = int(self.xp_prochain_niveau * 1.5)

        print(f"\n{'🌟'*30}")
        print(f"🌟 NIVEAU {self.niveau} ATTEINT !")
        print(f"{'🌟'*30}")
        print("Toutes vos statistiques augmentent de 1 !")

        # +1 à toutes les stats
        self.stats.pv_max      += 1
        self.stats.pv          += 1
        self.stats.attaque     += 1
        self.stats.defense     += 1
        self.stats.attaque_magique  += 1
        self.stats.defense_magique  += 1
        self.stats.vitesse     += 1

        print(f"📊 Stats actuelles : {self.stats}")

        # Point de compétence à placer
        self._attribuer_point_competence()

    def _attribuer_point_competence(self):
        """Permet au joueur de placer son point de compétence"""
        stats_choices = {
            "1": ("pv_max",          "❤️  PV Max"),
            "2": ("attaque",         "⚔️  Attaque"),
            "3": ("defense",         "🛡️  Défense"),
            "4": ("attaque_magique", "✨ Attaque Magique"),
            "5": ("defense_magique", "🔮 Défense Magique"),
            "6": ("vitesse",         "💨 Vitesse"),
        }
        print(f"\n🎯 Vous avez 1 point de compétence à placer !")
        print("   Choisissez la statistique à améliorer :")
        for key, (_, label) in stats_choices.items():
            valeur = getattr(self.stats, _.replace("pv_max", "pv_max"), 0)
            print(f"   {key}. {label} (actuel : {getattr(self.stats, _)})")
        print()

        while True:
            choix = input("   Votre choix (1-6) : ").strip()
            if choix in stats_choices:
                attr, label = stats_choices[choix]
                if attr == "pv_max":
                    self.stats.pv_max += 1
                    self.stats.pv     += 1
                else:
                    setattr(self.stats, attr, getattr(self.stats, attr) + 1)
                print(f"\n✅ {label} améliorée !")
                print(f"📊 Stats finales : {self.stats}")
                break
            else:
                print("   ❌ Choix invalide. Entrez un nombre entre 1 et 6.")

    def afficher_equipement(self):
        """Affiche l'équipement actuel du joueur"""
        print(f"\n{'='*50}")
        print(f"🎒 ÉQUIPEMENT")
        print(f"{'='*50}")
        if self.arme:
            print(f"  Arme :")
            self.arme.afficher()
        else:
            print(f"  Arme    : Aucune arme équipée.")
        if self.armure:
            print(f"\n  Armure :")
            self.armure.afficher()
        else:
            print(f"  Armure  : Aucune armure équipée.")
        print(f"{'='*50}")

    def creer_identite(self):
        """Demande au joueur de créer son identité complète"""
        print("\n=== Création de votre personnage ===\n")
        self.prenom.demander_prenom()
        self.nom.demander_nom()
        print(f"\nBienvenue, {self.prenom} {self.nom} !")
        print(f"Statistiques de base : {self.stats}")
    
    def obtenir_nom_complet(self):
        """Retourne le nom complet du joueur"""
        return f"{self.prenom} {self.nom}"
    
    def afficher_informations_completes(self):
        """Affiche toutes les informations du personnage"""
        print(f"\n{'='*50}")
        print(f"👤 INFORMATIONS DU PERSONNAGE")
        print(f"{'='*50}")
        print(f"Nom complet : {self.obtenir_nom_complet()}")
        print(f"Niveau      : {self.niveau}  |  XP : {self.xp}/{self.xp_prochain_niveau}  |  💰 Gold : {self.gold}")
        if self.race:
            print(f"Race        : {self.race.nom}")
        if self.classe:
            print(f"Classe      : {self.classe.nom}")
        if self.arme:
            print(f"Arme        : {self.arme}")
        if self.armure:
            print(f"Armure      : {self.armure}")
        self.stats.afficher_stats()
        print(f"{'='*50}")
    
    def __str__(self):
        return self.obtenir_nom_complet()

# Ce module sera importé par main.py pour la création du personnage