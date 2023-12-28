import random as r



class Carte:
    """Classe pour représenter une carte de jeu

    ---
    ### Attributs :
    - points: dict \n
            points d'une carte en fonction de sa valeur
    - points_atout: dict \n
            points d'une carte en fonction de sa valeur en étant atout
    - valeur: str \n
            valeur de la carte (ex: J = Valet)
    - couleur: str \n
            couleur de la carte (ex ♦ = Carreau)

    ---
    ### Méthode
    - point()\n
            Renvoie les points de la carte
    """
    
    points: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 2, '10': 10, '9': 0, '8': 0, '7': 0}
    points_atout: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 20, '10': 10, '9': 14, '8': 0, '7': 0}

    def __init__(self, valeur: str, couleur: str) -> None:
        """### Paramètres :
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
        ### Paramètres
        - atout: str (optionnel) \n
                Couleur de l'atout en jeu"""
        if self.couleur == atout:
            return self.points_atout[self.valeur]
        else:
            return self.points[self.valeur]
    




class Pile:
    """Une classe pour représenter une pile de cartes

    ---
    ### Attributs :
    - cartes : list[Carte] \n
            une liste d'objets Carte pour stocker les cartes qui sont dans la pile

    --- 
    ### Méthodes :
    - couper()\n
            modifier cartes comme quand on coupe la pile
    - distribuer() \n 
            ajoute des cartes à un joueur et les enlève de la pile
    - couleurs() \n
            renvoie la liste des couleurs de chaque carte
    - maitre() \n
            renvoie la valeur de la carte maitresse ainsi que sa position dans la pile
    """


    def __init__(self) -> None:
        self.cartes: list[Carte] = []
    

    def __repr__(self) -> str:
        return " | ".join(map(repr, self.cartes))

    def couper(self) -> None:
        """Coupe la pile en deux et met le bas en haut pour mélanger"""
        milieu = len(self.cartes) // 2
        self.cartes = self.cartes[milieu:] + self.cartes[:milieu]
    
    def distribuer(self, nb:int, joueur:object) -> None:
        """Ajoute des cartes à un joueur et les retire de la pile
        
        ---
        ### Paramètres
        - nb: int \n
                Nombre de cartes à distribuer
        - joueur: object \n
                Joueur qui reçoit les cartes"""
        
        joueur.cartes += self.cartes[:nb]
        self.cartes = self.cartes[nb:]
    
    def couleurs(self) -> list[str]:
        """Renvoie la liste des couleurs de chaque carte dans la pile"""
        result = [""] * len(self.cartes)
        for i in range(len(self.cartes)):
            result[i] = self.cartes[i].couleur
        return result

    def maitre(self, atout: str = '') -> tuple[int, int]:
        """Renvoie la valeur de la carte maitresse ainsi que sa position dans la pile
        
        ---
        ### Paramètres
        - atout: str (optionnel) \n
                Couleur de l'atout dans le jeu
        """
        i_max = 0
        pt_max = 0
        for i in range(len(self.cartes)):
            if self.cartes[i].point(atout) > pt_max:
                i_max = i
                pt_max = self.cartes[i].point(atout)
        return (pt_max, i_max)




class Joueur:
    """Classe représentant un joueur
    
    ---
    ### Attributs
    - cartes: list[Carte] \n
            cartes que le joueur a en main
    - nom: str \n
            nom du joueur

    ---
    ### Méthodes
    - distribuer() \n
            Le joueur donne des cartes à une pile
    """
    
    
    def __init__(self, nom: str) -> None:
        """### Paramètres
        - nom: str \n
                nom du joueur"""
        self.nom = nom
        self.cartes:list[Carte] = []
    
    def __repr__(self) -> str:
        """Affiche la main du joueur"""
        return " | ".join(map(repr, self.cartes))

    def distribuer(self, nb:int, pile:object) -> None:
        """Ajoute des cartes à une pile et les retire du jeu du joueur
        
        ---
        ### Paramètres
        - nb: int \n
                Nombre de cartes à distribuer
        - pile: object \n
                Pile qui reçoit les cartes"""
        
        pile.cartes += self.cartes[:nb]
        self.cartes = self.cartes[nb:]




class Jeu:
    """Classe représentant une partie de belote
    
    ---
    ### Attributs
    - atout: str \n
            Couleur de l'atout à un moment du jeu
    - i_donneur: int \n
            Position du donneur dans la liste de joeurs
    - joueur: list[Joueur] \n
            Liste des joueurs dans la partie
    - pile: Pile \n
            Pile des cartes de la partie
    - pli: Pile \n
            Pile des cartes qui sont en jeu dans un tour
        
    ---
    ## Méthodes
    - tour_atout() \n
            Lance un tour où on choisit la couleur de l'atout
    - distribution() \n
            Distribue les cartes aux joueurs et propose l'atout
    - tour() \n
            Lance un tour du jeu où les joueurs posent leur carte
    - carte_valide() \n
            Test la validité de la carte que l'on veut jouer
    """
    

    atout:str = ""
    i_donneur = r.randint(0,3)
    joueurs:list[Joueur] = [Joueur(nom) for nom in 'J1 J2 J3 J4'.split()]

    pile:Pile = Pile()
    pile.cartes = [Carte(val, coul) for val in 'A K Q J 10 9 8 7'.split() for coul in '♥ ♦ ♣ ♠'.split()]
    r.shuffle(pile.cartes)

    pli: Pile = Pile()


    def tour_atout(self) -> None:
        """Propose la première carte de la pile comme atout et les joueurs décident s'il la prenne ou pas"""

        carte_atout = self.pile.cartes[0]
        print(f"Atout = {carte_atout}")

        for i in range(4):
            joueur = self.joueurs[(self.i_donneur + i + 1)%4]
            print(f"{joueur.nom} : {joueur}")
            rep = input(f"{joueur.nom}, veux-tu l'atout ? (o/n) ")
            if rep == "o":
                self.pile.distribuer(1, joueur)
                self.atout = carte_atout.couleur
                return
            
        for i in range(4):
            joueur = self.joueurs[(self.i_donneur + i + 1)%4]
            print(f"{joueur.nom} : {joueur}")
            rep = input(f"{joueur.nom}, quelle couleur d'atout veux-tu ? (♥/♦/♣/♠/2) ")
            if rep in '♥♦♣♠' and len(rep) > 0:
                self.atout = rep
                return
        
        # Personne n'a voulu l'atout : on ramasse et on coupe
        for j in self.joueurs:
            j.distribuer(5, self.pile)
        self.pile.couper()


    def distribution(self) -> None:
        """Lance un tour du jeu où on distribue les cartes et on choisit l'atout"""
        self.atout = ""

        while self.atout == "": # Tant qu'il n'y a pas d'atout
            self.i_donneur += 1
            for i in range(4):
                joueur = self.joueurs[(self.i_donneur + i + 1)%4]
                self.pile.distribuer(3, joueur)
            for i in range(4):
                joueur = self.joueurs[(self.i_donneur + i + 1)%4]
                self.pile.distribuer(2, joueur)
            
            self.tour_atout()

        # distribue les dernières cartes
        for i in range(4):
            joueur = self.joueurs[(self.i_donneur + i + 1)%4]
            if len(joueur.cartes) == 5:
                self.pile.distribuer(3, joueur)
            else:
                self.pile.distribuer(2, joueur)


    def tour(self) -> None:
        """Lance un tour du jeu et le joueur avec la meilleur carte remporte le pli et joue au tour suivant"""
        print(f"{self.joueurs[(self.i_donneur + 1)%4]}")
        for i in range(4):
            joueur = self.joueurs[(self.i_donneur + 1 + i)%4]

            # premier joueur
            if i == 0:
                input(f"Au tour de {joueur.nom}")
                print(f"{joueur.nom}: {joueur}")
                i_carte = int(input(f"Quelle carte voulez-vous jouer (1-{len(joueur.cartes)})"))
                while 1 > i_carte  or i_carte > len(joueur.cartes):
                    print("Carte non valide")
                    i_carte = int(input(f"Quelle carte voulez-vous jouer (1-{len(joueur.cartes)})"))

                joueur.distribuer(1, self.pli)

            # autres joueurs
            else:
                input(f"Au tour de {joueur.nom}")
                print(f"{joueur.nom}: {joueur}")
                i_carte = int(input(f"Quelle carte voulez-vous jouer (1-{len(joueur.cartes)})"))
                while 1 > i_carte  or i_carte > len(joueur.cartes):
                    print("Carte non valide")
                    i_carte = int(input(f"Quelle carte voulez-vous jouer (1-{len(joueur.cartes)})"))
        
    def carte_valide(self, i_carte: int, joueur: Joueur) -> bool:
        """Renvoie True si la carte peut être posée et False sinon"""
        if 1 > i_carte  or i_carte > len(joueur.cartes):
            return False
        
        carte = joueur.cartes[i_carte - 1]

        if self.atout in self.pli.couleurs(): # un atout a été posé avant
            if carte.couleur == self.atout: # le joueur joue un atout
                if carte.point(self.atout) >= self.pli.maitre(self.atout)[0]: # le joueur monte à l'atout
                    return True
                # meilleur atout dans le jeu du joueur ? True ; False
            # le joueur n'a pas d'atout dans le jeu ? True ; False
        # carte jouée même couleur : True
        # carte même couleur dans le jeu : False
        # equipier maitre : True
        # carte jouée est atout : True
        # Le joueur n'a pas d'atout dans son jeu : True False
                

                
    # TODO
    # Mettre une manche : 8 plis + compter les points
    # Pli : chaque joueur à partir du donneur pose une carte (règles de pose) et à la fin le meilleur remporte le pli
    # Comptage : On compte les points par équipe avec toutes les règles (voir site) et on l'ajoute à un compteur de la partie
    # On repète les manches tant que le score max < 1001
