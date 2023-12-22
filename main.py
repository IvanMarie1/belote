import random as r



class Carte:
    """Classe pour représenter une carte de jeu

    ---
    ## Attributs :
    - points: dict \n
        points d'une carte en fonction de sa valeur
    - points_atout: dict \n
        points d'une carte en fonction de sa valeur en étant atout
    - valeur: str \n
        valeur de la carte (ex: J = Valet)
    - couleur: str \n
        couleur de la carte (ex ♦ = Carreau)

    ---
    ## Méthode
    - point(atout="")\n
        Renvoie les points de la carte
    """
    
    points: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 2, '10': 10, '9': 0, '8': 0, '7': 0}
    points_atout: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 20, '10': 10, '9': 14, '8': 0, '7': 0}

    def __init__(self, valeur: str, couleur: str) -> None:
        """## Paramètres :
        - valeur: str \n
            valeur de la carte (ex: J = Valet)
        - couleur: str \n
            couleur de la carte (ex ♦ = Carreau)
        """
        self.valeur: str = valeur
        self.couleur: str = couleur
    
    def __repr__(self) -> str:
        return f'{self.valeur} {self.couleur}'
    

    def point(self, atout:str ="") -> int:
        """Renvoie les points de la carte en prenant en compte si c'est un atout
        
        ---
        ## Paramètres
        - atout:str \n
            Couleur de l'atout en jeu"""
        if self.couleur == atout:
            return self.points_atout[self.valeur]
        else:
            return self.points[self.valeur]
    




class Pile:
    """Une classe pour représenter une pile

    ---
    ### Attributs :
    - cartes : list \n
        une liste d'objets Carte pour stocker les cartes qui sont dans la pile

    --- 
    ### Méthodes :
    - couper()\n
        modifier cartes comme quand on coupe la pile
    - distribuer() \n 
        ajoute des cartes à un joueur et les enlève de la pile
    """

    cartes:list[Carte] = [Carte(val, coul) for val in 'A K Q J 10 9 8 7'.split() for coul in '♥ ♦ ♣ ♠'.split()]
    r.shuffle(cartes)

    def __repr__(self) -> str:
        return " | ".join(map(repr, self.cartes))

    def couper(self) -> None:
        """Coupe la pile en deux et met le bas en haut pour mélanger"""
        milieu = len(self.cartes) // 2
        self.cartes = self.cartes[milieu:] + self.cartes[:milieu]
    
    def distribuer(self, nb:int, joueur:object) -> None:
        """Ajoute des cartes à un joueur et les retire de la pile
        
        ---
        ## Paramètres
        - nb: int \n
            Nombre de cartes à distribuer
        - joueur: object \n
            Joueur qui reçoit les cartes"""
        
        joueur.cartes += self.cartes[:nb]
        self.cartes = self.cartes[nb:]




class Joueur:
    """Classe représentant un joueur
    
    ---
    ## Attributs
    - cartes: list[Carte] \n
        cartes que le joueur a en main
    - nom: str\n
        nom du joueur"""
    
    cartes:list[Carte] = []
    def __init__(self, nom: str) -> None:
        """## Paramètres
        - nom: str \n
            nom du joueur"""
        self.nom = nom
    
    def __repr__(self) -> str:
        """Affiche la main du joueur"""
        return " | ".join(map(repr, self.cartes))




class Jeu:
    """Classe représentant une partie de belote
    
    ---
    ## Attributs
    - atout: str \n
        Couleur de l'atout à un moment du jeu
    - joueur: list[Joueur] \n
        Liste des joueurs dans la partie
    - pile: Pile \n
        Pile des cartes de la partie
        
    ---
    ## Méthodes
    - choisir_atout() \n
        Lance un tour où on choisit la couleur de l'atout"""

    atout:str = ""
    joueurs:list[Joueur] = [Joueur(nom) for nom in 'J1 J2 J3 J4'.split()]
    pile:Pile = Pile()

    def choisir_atout(self) -> None:
        """Lance un tour du jeu où on choisit l'atout"""

        carte_atout = self.pile.cartes[0]
        print(f"Atout = {carte_atout}")

        # TODO mettre ça dans une fonction et répéter tant qu'il n'y a pas d'atout
        for _ in range(2): # TODO changer le deuxième tour : le joueur peut décider de la couleur de l'atout
            for j in self.joueurs:
                rep = input(f"{j.nom} : veux-tu l'atout ? (o/n) ")
                if rep == "o":
                    self.pile.distribuer(1, j)
                    self.atout = carte_atout.couleur
                    return
                
        self.pile.couper() # personne ne veut l'atout
