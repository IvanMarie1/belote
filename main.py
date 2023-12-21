import random as r

class Carte:
    """Carte: \n
    Objet qui pourra être distribué aux joueurs ou rester dans la pile"""
    
    valeurs: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 2, '10': 10, '9': 0, '8': 0, '7': 0}
    valeurs_atout: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 20, '10': 10, '9': 14, '8': 0, '7': 0}

    def __init__(self, valeur: str, couleur: str) -> None:
        self.valeur: str = valeur
        self.couleur: str = couleur
    
    def __repr__(self) -> str:
        return f'{self.valeur} {self.couleur}'
    

    def get_val(self, atout:str="") -> int:
        """Renvoie la valeur de la carte en prenant en compte si c'est un atout"""

        if self.couleur == atout:
            return self.valeurs_atout[self.valeur]
        else:
            return self.valeurs[self.valeur]
    



class Pile:
    """Pile :\n
    Liste de cartes pour mélanger, distribuer etc"""

    cartes: list = [Carte(val, coul) for val in 'A K Q J 10 9 8 7'.split() for coul in '♥ ♦ ♣ ♠'.split()]
    r.shuffle(cartes)

    def __repr__(self) -> str:
        return " | ".join(map(repr, self.cartes))

    def couper(self) -> None:
        milieu = len(self.cartes) // 2
        self.cartes = self.cartes[milieu:] + self.cartes[:milieu]
    
    def distribuer(self, nb:int, joueur:object) -> None:
        joueur.cartes += self.cartes[:nb]
        self.cartes = self.cartes[nb:]




class Joueur:
    """Joueur: \n
    Le joueur peut stocker des cartes"""
    cartes:list[object] = []
    def __init__(self, nom: str) -> None:
        self.nom = nom
    
    def __repr__(self) -> str:
        return " | ".join(map(repr, self.cartes))




class Jeu:
    """Jeu: \n
    Crée une partie de belote et pourra lancer des manches etc."""

    atout:str = ""
    joueurs:list[object] = [Joueur(nom) for nom in 'J1 J2 J3 J4'.split()]
    pile:object = Pile()

    def choisir_atout(self) -> None:
        """Lance un tour du jeu où on choisit l'atout"""

        carte_atout = self.pile.cartes[0]
        print(f"Atout = {carte_atout}")

        # mettre ça dans une fonction (privée) et répéter tant qu'il n'y a pas d'atout
        for _ in range(2):
            for j in self.joueurs:
                rep = input(f"{j.nom} : veux-tu l'atout ? (o/n) ")
                if rep == "o":
                    self.pile.distribuer(1, j)
                    self.atout = carte_atout.couleur
                    return
                
        self.pile.couper() # personne ne veut l'atout


j = Jeu()
j.choisir_atout()
print(j.atout)
