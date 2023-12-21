import random as r

class Carte:
    valeurs = {'A': 11, 'K': 4, 'Q': 3, 'J': 2, '10': 10, '9': 0, '8': 0, '7': 0}
    valeurs_atout = {'A': 11, 'K': 4, 'Q': 3, 'J': 20, '10': 10, '9': 14, '8': 0, '7': 0}

    def __init__(self, valeur, couleur) -> None:
        self.valeur = valeur
        self.couleur = couleur
    
    def __repr__(self) -> str:
        return f'{self.valeur} {self.couleur}'
    
    def get_val(self, atout) -> int:
        if self.couleur == atout:
            return self.valeurs_atout[self.valeur]
        else:
            return self.valeurs[self.valeur]
    


class Pile:

    cartes = [Carte(val, coul) for val in 'A K Q J 10 9 8 7'.split() for coul in '♥ ♦ ♣ ♠'.split()]
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
    cartes = []
    def __init__(self, nom, num) -> None:
        self.nom = nom
        self.num = num
    
    def __repr__(self) -> str:
        return " | ".join(map(repr, self.cartes))


class Jeu:
    pass


p = Pile()

print(p)
j1 = Joueur("Ivan", 1)

p.distribuer(4, j1)
print(j1)
print(p)
