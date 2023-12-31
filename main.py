import random as r



class Carte:
    """Classe représentant une carte de jeu

    ---
    ### Attributs :
    points: dict
        points d'une carte en fonction de sa valeur
    
    points_atout: dict
        points d'une carte en fonction de sa valeur en étant atout
    
    valeur: str
        valeur de la carte (ex: J = Valet)
    
    couleur: str
        couleur de la carte (ex ♦ = Carreau)
    ---
    ### Méthode
    point()
        Renvoie les points de la carte
    """
    
    points: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 2, '10': 10, '9': 0, '8': 0, '7': 0}
    points_atout: dict = {'A': 11, 'K': 4, 'Q': 3, 'J': 20, '10': 10, '9': 14, '8': 0, '7': 0}

    def __init__(self, valeur: str, couleur: str) -> None:
        """### Paramètres :
        valeur: str
            valeur de la carte (ex: J = Valet)
        
        couleur: str
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
        atout: str (optionnel)
            Couleur de l'atout en jeu
        """
        if self.couleur == atout:
            return self.points_atout[self.valeur]
        else:
            return self.points[self.valeur]
    




class Pile:
    """Classe représentant une pile de cartes

    ---
    ### Attributs :
    
    cartes : list[Carte]
        une liste d'objets Carte pour stocker les cartes qui sont dans la pile

    --- 
    ### Méthodes :
    couper()
        modifier cartes comme quand on coupe la pile
    
    distribuer() 
        ajoute des cartes à un joueur et les enlève de la pile
    
    couleurs()
        renvoie la liste des couleurs de chaque carte
    
    maitre()
        renvoie la valeur de la carte maitresse ainsi que sa position dans la pile"""

    def __init__(self) -> None:
        self.cartes: list[Carte] = []

    def __repr__(self) -> str:
        return " | ".join(map(repr, self.cartes))

    
    def couper(self) -> None:
        """Coupe la pile en deux et met le bas en haut pour mélanger"""
        milieu = len(self.cartes) // 2
        self.cartes = self.cartes[milieu:] + self.cartes[:milieu]
    
    
    def distribuer(self, nb:int, tas:list) -> None:
        """Ajoute des cartes à un joueur et les retire de la pile
        
        ---
        ### Paramètres
        nb: int
            Nombre de cartes à distribuer

        tas: list 
            Tas du joueur qui reçoit les cartes
            """
        
        tas += self.cartes[:nb]
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
        atout: str (optionnel)
            Couleur de l'atout dans le jeu
        """
        i_max = 0
        pt_max = 0
        atout_joue = False
        for i in range(len(self.cartes)):
            carte = self.cartes[i]
            pt = carte.point(atout)

            if (not atout_joue) and carte.couleur == atout:
                atout_joue = True
                i_max = i
                pt_max = pt
            elif carte.couleur == atout and pt > pt_max and atout_joue:
                i_max = i
                pt_max = pt
            elif pt > pt_max and (not atout_joue):
                i_max = i
                pt_max = pt

        return (pt_max, i_max)




class Joueur:
    """Classe représentant un joueur
    
    ---
    ### Attributs
    cartes: list[Carte]
        cartes que le joueur a en main
    
    cartes_gagnees: list[Carte]
        cartes que le joueur a gagné
    
    nom: str
        nom du joueur
    
    pos: int
        position du joueur dans le jeu
    ---
    ### Méthodes
    distribuer()
        Le joueur donne des cartes à une pile
    
    jouer()
        Le jouer pose une carte dans une pile
    
    couleurs()
        Renvoie les couleurs des cartes du joueur
    """
    
    def __init__(self, nom: str, pos: int) -> None:
        """### Paramètres
        nom: str
            nom du joueur

        pos: int
            position du joueur dans le jeu
        """
        self.nom = nom
        self.pos = pos
        self.cartes:list[Carte] = []
        self.cartes_gagnees: list[Carte] = []
    
    def __repr__(self) -> str:
        return " | ".join(map(repr, self.cartes))

    def distribuer(self, nb:int, pile:Pile) -> None:
        """Ajoute des cartes à une pile et les retire du jeu du joueur
        
        ---
        ### Paramètres
        nb: int 
            Nombre de cartes à distribuer

        pile: Pile
            Pile qui reçoit les cartes"""
        
        pile.cartes += self.cartes[:nb]
        self.cartes = self.cartes[nb:]
    
    
    def couleurs(self) -> list[str]:
        """Renvoie la liste des couleurs de chaque carte du joueur"""
        result = []
        for carte in self.cartes:
            result.append(carte.couleur)
        return result

    
    def jouer(self, i_carte: int, pile: Pile) -> None:
        """Joue une carte et la pose dans une pile
        
        ---
        ### Paramètres
        i_carte: int
            position de la carte dans le jeu du joueur (à partir de 1)

        pile: Pile 
            pile qui reçoit la carte
        """
        pile.cartes.append(self.cartes[i_carte - 1]) 
        self.cartes = self.cartes[:i_carte - 1] + self.cartes[i_carte:]


    def ramasser(self, pile: Pile) -> None:
        """Ramasse les cartes gagnées par le joueur
        
        ---
        ### Paramètres
        pile: Pile
            Pile qui va recevoir les cartes"""
        pile.cartes += self.cartes_gagnees
        self.cartes_gagnees = []




class Jeu:
    """Classe représentant une partie de belote
    
    ---
    ### Attributs
    atout: str
        Couleur de l'atout à un moment du jeu
    
    i_donneur: int
        Position du donneur dans la liste de joueurs

    i_premier_joueur: int
        Position du joueur qui pose la première carte
    
    joueur: list[Joueur]
        Liste des joueurs dans la partie
    
    pile: Pile
        Pile des cartes de la partie
    
    pli: Pile
        Pile des cartes qui sont en jeu dans un tour
    
    points: list[int]
        Points marqués par les équipes (équipe0 : j0-2 // équipe1 : j1-3)
    
    equipe_pari: int
        Indice de l'équipe qui prend le pari (équipe0 : j0-2 // équipe1 : j1-3)

    i_dix_de_der: int
        Indice du joueur qui a remporté le dernier pli (+10 points)
        
    ---
    ### Méthodes
    tour_atout()
        Lance un tour où on choisit la couleur de l'atout
    
    distribution()
        Distribue les cartes aux joueurs et propose l'atout
    
    tour()
        Lance un tour du jeu où les joueurs posent leur carte

    choix_carte()
        Le joueur choisit une carte jusqu'à ce qu'elle soit valide
    
    carte_valide()
        Teste la validité de la carte que l'on veut jouer
    
    compte_points()
        Compte les points de chaque équipe à la fin d'une manche
    
    manche()
        Lance une manche du jeu : distribution + 8 tours + comptage des points
    
    partie()
        Lance des manches jusqu'à ce que le score dépasse 1000
    """
    
    def __init__(self) -> None:
        self.atout:str = ""
        self.i_donneur = r.randint(0,3)
        self.i_premier_joueur = 0
        self.joueurs:list[Joueur] = [Joueur(nom, i) for i, nom in enumerate('J1 J2 J3 J4'.split(), 0)]

        self.pile:Pile = Pile()
        self.pile.cartes = [Carte(val, coul) for val in 'A K Q J 10 9 8 7'.split() for coul in '♥ ♦ ♣ ♠'.split()]
        r.shuffle(self.pile.cartes)

        self.pli: Pile = Pile()

        self.points: list[int] = [0, 0]
        self.equipe_pari: int = 0
        self.i_dix_de_der: int = 0

    def tour_atout(self) -> None:
        """Propose la première carte de la pile comme atout et les joueurs décident s'il la prenne ou pas"""

        carte_atout = self.pile.cartes[0]
        print(f"Atout = {carte_atout}")
        
        # premier tour
        for i in range(4):
            joueur = self.joueurs[(self.i_donneur + 1 + i)%4]
            print(f"{joueur.nom} : {joueur}")
            rep = input(f"{joueur.nom}, veux-tu l'atout ? (o/n) ")
            if rep == "o":
                self.pile.distribuer(1, joueur.cartes)
                self.atout = carte_atout.couleur
                self.equipe_pari = (self.i_donneur + 1 + i)%2
                return
        # deuxième tour 
        for i in range(4):
            joueur = self.joueurs[(self.i_donneur + 1 + i)%4]
            print(f"{joueur.nom} : {joueur}")
            rep = input(f"{joueur.nom}, quelle couleur d'atout veux-tu ? (♥/♦/♣/♠/2) ")
            if rep in '♥♦♣♠' and len(rep) > 0:
                self.atout = rep
                self.equipe_pari = (self.i_donneur + 1 + i)%2
                return
        
        # Personne n'a voulu l'atout : on ramasse et on coupe
        for j in self.joueurs:
            j.distribuer(5, self.pile)
        self.pile.couper()


    def distribution(self) -> None:
        """Lance un tour du jeu où on distribue les cartes et on choisit l'atout"""
        self.atout = ""

        while self.atout == "": # Tant qu'il n'y a pas d'atout
            self.i_donneur = (self.i_donneur + 1) % 4
            for i in range(4):
                joueur = self.joueurs[(self.i_donneur + 1 + i)%4]
                self.pile.distribuer(3, joueur.cartes)
            for i in range(4):
                joueur = self.joueurs[(self.i_donneur + 1 + i)%4]
                self.pile.distribuer(2, joueur.cartes)
            
            self.tour_atout()

        # distribue les dernières cartes
        for i in range(4):
            joueur = self.joueurs[(self.i_donneur + 1 + i)%4]
            if len(joueur.cartes) == 5:
                self.pile.distribuer(3, joueur.cartes)
            else:
                self.pile.distribuer(2, joueur.cartes)

        self.i_premier_joueur = (self.i_donneur + 1) % 4


    def tour(self) -> None:
        """Lance un tour du jeu et le joueur avec la meilleur carte remporte le pli et joue au tour suivant"""
        
        for i in range(4):
            joueur = self.joueurs[(self.i_premier_joueur + i)%4]
            
            i_carte = self.choix_carte(i, joueur)

            joueur.jouer(i_carte, self.pli)

        i_maitre = (self.pli.maitre(self.atout)[1] + self.i_premier_joueur) % 4
        self.pli.distribuer(4, self.joueurs[i_maitre].cartes_gagnees)
        self.i_premier_joueur = i_maitre


    def choix_carte(self, i_joueur: int, joueur: Joueur) -> int:
        """Renvoie l'indice de la carte choisie par le joueur (à partir de 1) bonjour

        ---
        ### Paramètres
        i_joueur: int
            position dans le joueur dans le tour
        joueur: Joueur
            joueur qui doit choisir la carte
        """
        input("\n" * 5 + f"Au tour de {joueur.nom}")

        print(f"{joueur.nom}: {joueur}")
        print(f"Carte posées : {self.pli}")

        i_carte = input(f"Quelle carte voulez-vous jouer ? (1-{len(joueur.cartes)})")

        while not self.carte_valide(i_carte, joueur, i_joueur):
            print("Carte non valide")
            i_carte = input(f"Quelle carte voulez-vous jouer (1-{len(joueur.cartes)})")

        return int(i_carte)


    def carte_valide(self, i_carte: str, joueur: Joueur, i_joueur: int) -> bool:
        """Renvoie True si la carte peut être posée et False sinon
        
        ---
        ### Paramètres 
        i_carte: str 
            Position de la carte dans le jeu du joueur

        joueur: Joueur
            Joueur qui pose la carte
        
        i_joueur: int
            Position du joueur dans le tour
        """
        try:
            i_carte = int(i_carte)
        except ValueError:
            return False
        
        if 1 > i_carte  or i_carte > len(joueur.cartes):
            return False
    
        if i_joueur == 0: # le premier peut mettre ce qu'il veut
            return True
        
        carte = joueur.cartes[i_carte - 1]
        pt_maitre, i_maitre = self.pli.maitre(self.atout)

        
        if self.atout in self.pli.couleurs(): # un atout a été posé avant 
            
            if not self.atout in joueur.couleurs(): # le joueur n'a pas d'atout
                return True 
            if carte.couleur != self.atout: # le joueur ne joue pas atout alors qu'il peut
                return False
            if carte.point(self.atout) >= pt_maitre: # le joueur monte à l'atout
                return True
            return not (True in [(carte_temp.point(self.atout) >= pt_maitre) and (carte_temp.couleur == self.atout) for carte_temp in joueur.cartes]) # le joueur ne peut pas monter à l'atout
                
        
        if carte.couleur == self.pli.cartes[0].couleur: # on joue la même couleur que l'entame
            return True
        if self.pli.cartes[0].couleur in joueur.couleurs(): # on peut jouer de la même couleur que l'entame
            return False
        if (i_maitre - i_joueur) % 2 == 0: # l'equipier est maitre (ecart entre les joueurs = 2)
            return True
        if carte.couleur == self.atout: # on joue atout
            return True
        return not self.atout in joueur.couleurs() # on ne peut pas jouer atout


    def compte_points(self) -> None:
        """Actualise les scores en comptant les points de chaque équipe selon les cartes qu'elles ont récupérées"""
        points_temp = [0, 0]
        # compte les points des cartes de chaque joueur
        for i in range(4):
            joueur = self.joueurs[i]
            for carte in joueur.cartes_gagnees:
                points_temp[i%2] += carte.point(self.atout)
        # points du dix de der
        points_temp[self.i_dix_de_der % 2] += 10

        # pari non remorté
        if points_temp[self.equipe_pari] < 82:
            points_temp[self.equipe_pari] = 0
            points_temp[(self.equipe_pari + 1) % 2] = 162
        
        # on ajoute les points au total
        self.points[0] += points_temp[0]
        self.points[1] += points_temp[1]


    def manche(self) -> None:
        """Lance une manche du jeu : distribution // 8 plis // comptage des points"""
        self.distribution()

        for _ in range(7):
            self.tour()

        # dernier tour (aucun choix)
        for i in range(4):
            joueur = self.joueurs[(self.i_premier_joueur + i) % 4]
            joueur.jouer(1, self.pli)

        i_maitre = (self.pli.maitre(self.atout)[1] + self.i_premier_joueur + 1) % 4
        self.pli.distribuer(4, self.joueurs[i_maitre].cartes_gagnees)
        self.i_dix_de_der = i_maitre

        self.compte_points()
        self.i_donneur = (self.i_donneur + 1) % 4

        # on ramasse les cartes
        for joueur in self.joueurs:
            joueur.ramasser(self.pile)
        self.pile.couper()
    

    def partie(self) -> None:
        """Lance une partie de belote : on répète des manches jusqu'a ce que le score dépasse 1000"""

        print("""
            {lig}
            {gap}
            #{txt:^48}#
            {gap}
            {lig}""".format(lig="#"*50, gap="#" + 48*" " + "#", txt="PARTIE DE BELOTE")
        )


        while max(self.points) <= 1000:
            self.manche()
            print(self.points)
            input("\n" * 10 + "MANCHE SUIVANTE")


# debug
j = Jeu()
j.partie()
