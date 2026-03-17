class Introduction:
    """Gère l'introduction du jeu"""
    
    def __init__(self, nom_jeu="Mon Jeu"):
        self.nom_jeu = nom_jeu
    
    def afficher_titre(self):
        print("=" * 50)
        print(f"      BIENVENUE DANS {self.nom_jeu.upper()}")
        print("=" * 50)
    
    def afficher_histoire(self):
        print("\nDans un monde où humains et hybrides vivent en harmonie,")
        print("un événement eut lieu et changea le destin du monde.")
        print("Le roi humain fut assassiné, et le nouveau souverain ne désirait qu'une seule chose...\n")
        print("la suprématie humaine. Sans crier gare, les hybrides se sont fait chasser et tuer au sein de la capitale.\n")
        print("Les hybrides prirent la fuite, mais beaucoup ont péri sur place !\n")
        print("Vous vous êtes réfugié et caché dans les égouts de la capitale pour fuir, mais vous allez devoir vous battre pour survivre !\n")
    
    def afficher_objectif(self):
        print("Objectif :")
        print("Fuir par les égouts de la capitale")
        print("et trouver des alliés pour vous battre, et survivre... !\n")
    
    def lancer(self):
        """Lance toute l'introduction"""
        self.afficher_titre()
        self.afficher_histoire()
        self.afficher_objectif()