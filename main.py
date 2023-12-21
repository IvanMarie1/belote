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
        self.cartes = self.cartes[16:] + self.cartes[:16]

p = Pile()

print(p)
p.couper()
print(p)
