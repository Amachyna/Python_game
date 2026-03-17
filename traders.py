class Marchand:
    def __init__(self):
        self.nom = "Marchand"
        self.inventaire = {
            # Potions
            "Potion de soin":       {"prix": 10,  "type": "potion",  "effet": {"hp": 20}},
            "Grande potion de soin":{"prix": 25,  "type": "potion",  "effet": {"hp": 50}},
            "Potion de force":      {"prix": 20,  "type": "potion",  "effet": {"attack": 5}},

            # Armes
            "Épée en bois":         {"prix": 15,  "type": "arme",    "effet": {"attack": 3}},
            "Épée en fer":          {"prix": 40,  "type": "arme",    "effet": {"attack": 7}},
            "Épée en acier":        {"prix": 80,  "type": "arme",    "effet": {"attack": 12}},
            "Dague":                {"prix": 20,  "type": "arme",    "effet": {"attack": 4}},
            "Arc":                  {"prix": 35,  "type": "arme",    "effet": {"attack": 6}},

            # Armures
            "Armure en cuir":       {"prix": 30,  "type": "armure",  "effet": {"defense": 3}},
            "Armure en fer":        {"prix": 60,  "type": "armure",  "effet": {"defense": 6}},
            "Armure en acier":      {"prix": 100, "type": "armure",  "effet": {"defense": 10}},
            "Bouclier en bois":     {"prix": 20,  "type": "armure",  "effet": {"defense": 2}},
            "Bouclier en fer":      {"prix": 45,  "type": "armure",  "effet": {"defense": 5}},
        }

    def afficher_inventaire(self):
        print(f"\n🏪 Bienvenue chez le {self.nom} !")
        print("=" * 50)

        categories = {"potion": "🧪 Potions", "arme": "⚔️  Armes", "armure": "🛡️  Armures"}

        for cat_key, cat_nom in categories.items():
            print(f"\n{cat_nom}")
            print("-" * 30)
            for nom, data in self.inventaire.items():
                if data["type"] == cat_key:
                    effet = list(data["effet"].items())
                    effet_str = ", ".join(f"+{v} {k}" for k, v in effet)
                    print(f"  {nom:<25} {data['prix']:>3} 💰  ({effet_str})")

        print("=" * 50)

    def acheter(self, joueur, nom_objet):
        """Le joueur achète un objet au marchand"""
        if nom_objet not in self.inventaire:
            print(f"❌ '{nom_objet}' n'existe pas dans l'inventaire.")
            return False

        objet = self.inventaire[nom_objet]

        if joueur.gold < objet["prix"]:
            print(f"❌ Pas assez d'or ! (Tu as {joueur.gold}💰, il faut {objet['prix']}💰)")
            return False

        joueur.gold -= objet["prix"]
        joueur.inventaire.append({"nom": nom_objet, **objet})
        print(f"✅ Tu as acheté '{nom_objet}' pour {objet['prix']}💰 !")
        print(f"   💰 Or restant : {joueur.gold}")
        return True

    def vendre(self, joueur, nom_objet):
        """Le joueur vend un objet au marchand (moitié prix)"""
        objet_joueur = next((o for o in joueur.inventaire if o["nom"] == nom_objet), None)

        if not objet_joueur:
            print(f"❌ Tu ne possèdes pas '{nom_objet}'.")
            return False

        prix_vente = objet_joueur["prix"] // 2
        joueur.inventaire.remove(objet_joueur)
        joueur.gold += prix_vente
        print(f"✅ Tu as vendu '{nom_objet}' pour {prix_vente}💰 !")
        print(f"   💰 Or total : {joueur.gold}")
        return True