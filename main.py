#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier principal du jeu
"""

from identiterUser import IdentiteJoueur
from breed import choisir_race
from classe import choisir_classe


def afficher_titre():
    """Affiche le titre du jeu"""
    print("\n" + "="*50)
    print("         BIENVENUE DANS LE JEU")
    print("="*50 + "\n")


def creer_personnage():
    """Crée et retourne un nouveau personnage"""
    joueur = IdentiteJoueur()
    
    # Étape 1 : Créer l'identité (prénom et nom)
    joueur.creer_identite()
    
    # Étape 2 : Choisir la race et appliquer les bonus
    print("\n")
    race_selectionnee = choisir_race()
    joueur.definir_race(race_selectionnee)
    
    # Étape 3 : Choisir la classe et appliquer les bonus
    print("\n")
    classe_selectionnee = choisir_classe()
    joueur.definir_classe(classe_selectionnee)
    
    # Afficher les statistiques finales
    print(f"\n✨ Statistiques finales : {joueur.stats}\n")
    
    return joueur


def menu_principal():
    """Affiche le menu principal du jeu"""
    print("\n" + "-"*50)
    print("MENU PRINCIPAL")
    print("-"*50)
    print("1. Commencer l'aventure")
    print("2. Voir les informations du personnage")
    print("3. Quitter le jeu")
    print("-"*50)
    
    choix = input("\nVotre choix : ")
    return choix


def main():
    """Fonction principale du jeu"""
    afficher_titre()
    
    # Création du personnage au démarrage
    personnage = creer_personnage()
    
    # Boucle principale du jeu
    en_jeu = True
    while en_jeu:
        choix = menu_principal()
        
        if choix == "1":
            print(f"\n🎮 {personnage}, votre aventure commence...")
            print("(Cette partie sera développée plus tard)")
            
        elif choix == "2":
            personnage.afficher_informations_completes()
            
        elif choix == "3":
            print(f"\n👋 Au revoir {personnage.prenom} ! À bientôt !")
            en_jeu = False
            
        else:
            print("\n❌ Choix invalide. Veuillez choisir 1, 2 ou 3.")


if __name__ == "__main__":
    main()