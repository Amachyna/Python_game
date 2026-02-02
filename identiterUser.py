class Statistiques:
    """Classe pour gérer les statistiques du personnage"""
    
    def __init__(self, pv=20, attaque=3, defense=5):
        self._pv = pv
        self._pv_max = pv
        self._attaque = attaque
        self._defense = defense
    
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
    
    def afficher_stats(self):
        """Affiche les statistiques du personnage"""
        print(f"\n📊 === STATISTIQUES ===")
        print(f"❤️  Points de Vie : {self._pv}/{self._pv_max}")
        print(f"⚔️  Attaque        : {self._attaque}")
        print(f"🛡️  Défense       : {self._defense}")
    
    def __str__(self):
        return f"PV: {self._pv}/{self._pv_max} | ATK: {self._attaque} | DEF: {self._defense}"


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
    
    def creer_identite(self):
        """Demande au joueur de créer son identité complète"""
        print("\n=== Création de votre personnage ===\n")
        self.prenom.demander_prenom()
        self.nom.demander_nom()
        print(f"\nBienvenue, {self.prenom} {self.nom} !")
        print(f"Statistiques initiales : {self.stats}")
    
    def obtenir_nom_complet(self):
        """Retourne le nom complet du joueur"""
        return f"{self.prenom} {self.nom}"
    
    def afficher_informations_completes(self):
        """Affiche toutes les informations du personnage"""
        print(f"\n{'='*50}")
        print(f"👤 INFORMATIONS DU PERSONNAGE")
        print(f"{'='*50}")
        print(f"Nom complet : {self.obtenir_nom_complet()}")
        self.stats.afficher_stats()
        print(f"{'='*50}")
    
    def __str__(self):
        return self.obtenir_nom_complet()

# Ce module sera importé par main.py pour la création du personnage