class Introduction:
    """Gère l'introduction du jeu"""
    
    def __init__(self, nom_jeu="Mon Jeu"):
        self.nom_jeu = nom_jeu
    
    def afficher_titre(self):
        print("=" * 50)
        print(f"      BIENVENUE DANS {self.nom_jeu.upper()}")
        print("=" * 50)
    
    def afficher_histoire(self):
        print("\nDans un monde ou humain et hybride vivent en harmonie,")
        print("un evenement eu lieux et changas le destin du monde.")
        print("le roi Humain fut assasiner, et le nouveau souverain ne desirer qu'une seul chose...\n")
        print("la suprematie humaine, sans crier gares les hybrides se sont fait chasser et tuer au seins de la capitales.\n")
        print("les hybrides prirent la fuite, mais baucoup ont peri sur place !\n")
        print("vous vous etes refugier et cacher dans les egoue de la capitale pour fuire, mais vous allez devoir vous battre pour suivivre !")
    
    def afficher_objectif(self):
        print("fuire par les egoux de la capitale")
        print("et trouver des alier pour vous battre, et survuvre... !\n")
    
    def lancer(self):
        """Lance toute l'introduction"""
        self.afficher_titre()
        self.afficher_histoire()
        self.afficher_objectif()