# -*-coding:Utf-8 -*
from fonctionsroboc import *

########################################################################################################################
data1=[0]
data2=[0]
setting=[0]
playerz = ["X","x","*","+"]
########################################################################################################################

class DeplacebotS():
    "Classe permettant de modifier la position du joueur lors de l'utilisation de la commande S."


    #Les trois classes suivantes sont presque identiques si ce n'est de legeres divergences en fonction de la direction de la commande.

    def __init__(self,pos1,pos2,ordre,lab):
        self.pos1 = pos1 #pos1 et 2 = position du joueur
        self.pos2 = pos2
        self.ordre = ordre #le numero attribue au joueur lors de sa connexion sur le serveur
        self.lab=lab #le labyrinthe

    def __iadd__(self, other):
        global data1, data2, setting

        labyrinthe = self.lab

        if self.ordre == 1 : # le "personnage" differe en fonction de l'id du joueur
            ply = 'X'
        elif self.ordre == 2 :
            ply = 'x'
        elif self.ordre == 3 :
            ply = '*'
        else :
            ply = '+'

        i = 0
        while i < other :
            labyrinthe[self.pos1][self.pos2] = " "  # Efface 'X' de la case precedente (apres son passage).

            for tuplepoint in ppoint :         # Boucle for pour faire reaparaître la porte '.' apres le passage de 'X'.
                if (self.pos1,self.pos2) == tuplepoint :     # " ppoint " ->  variable ayant recupere les positions de '.' sur la map.
                    labyrinthe[tuplepoint[0]][tuplepoint[1]] = '.'

            # Incrementation position X ( 1 par tour de boucle )
            self.pos1 += 1
            i += 1

            # Reactions du programme en fonction des obstacles rencontres.
            if labyrinthe[self.pos1][self.pos2] == "O":
                print(" ")
                print("Impasse! Impossible de passer.. ")
                self.pos1 = self.pos1 - 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            if labyrinthe[self.pos1][self.pos2] in playerz : # collision
                print("")
                print("..Aie! Ne te met pas sur mon chemin.. ")
                print("")
                self.pos1 = self.pos1 - 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            for tuplepoint in ppoint : # passage du joueur sur une porte
                if (self.pos1,self.pos2) == tuplepoint :
                    labyrinthe[self.pos1][self.pos2] = ply
                    data1[0]=self.pos1
                    data2[0]=self.pos2
                    setting[0]=3

            if labyrinthe[self.pos1][self.pos2] == " ": # passage du joueur sur endroit 'vide'
                labyrinthe[self.pos1][self.pos2] = ply
                data1[0] = self.pos1
                data2[0] = self.pos2
                setting[0] = 3

            if labyrinthe[self.pos1][self.pos2] == "U": # victoire
                labyrinthe[self.pos1][self.pos2] = ply
                print(" ")
                for list in labyrinthe:
                    print(' '.join(list))
                print("")
                print("")
                print("Enfin la porte de sortie.. Victoire!")
                print("")
                data1[0] = self.pos1
                data2[0] = self.pos2
                setting[0] = 4
                break


class DeplacebotN():
    "Classe permettant de modifier la position du joueur lors de l'utilisation de la commande N."

    def __init__(self, pos1, pos2, ordre,lab):
        self.pos1 = pos1
        self.pos2 = pos2
        self.ordre = ordre
        self.lab = lab

    def __iadd__(self, other):
        global data1, data2, setting
        i = 0

        labyrinthe = self.lab

        if self.ordre == 1 :
            ply = 'X'
        elif self.ordre == 2 :
            ply = 'x'
        elif self.ordre == 3 :
            ply = '*'
        else :
            ply = '+'

        while i < other :

            labyrinthe[self.pos1][self.pos2] = " "

            for tuplepoint in ppoint :
                if (self.pos1,self.pos2) == tuplepoint :
                    labyrinthe[tuplepoint[0]][tuplepoint[1]] = '.'

            self.pos1 -= 1
            i += 1

            if labyrinthe[self.pos1][self.pos2] == "O":
                print(" ")
                print("Impasse! Impossible de passer.. ")
                self.pos1 = self.pos1 + 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            if labyrinthe[self.pos1][self.pos2] in playerz:
                print("")
                print("..Aie! Ne te met pas sur mon chemin.. ")
                print("")
                self.pos1 = self.pos1 + 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            for tuplepoint in ppoint :
                if (self.pos1,self.pos2) == tuplepoint :
                    labyrinthe[self.pos1][self.pos2] = ply
                    data1[0] = str(self.pos1)
                    data2[0] = str(self.pos2)
                    setting[0] = str(3)

            if labyrinthe[self.pos1][self.pos2] == " ":
                labyrinthe[self.pos1][self.pos2] = ply
                data1[0] = str(self.pos1)
                data2[0] = str(self.pos2)
                setting[0] = str(3)

            if labyrinthe[self.pos1][self.pos2] == "U":
                labyrinthe[self.pos1][self.pos2] = ply
                print(" ")
                for list in labyrinthe:
                    print(' '.join(list))
                print("")
                print("")
                print("Enfin la porte de sortie.. Victoire!")
                print("")
                data1[0] = self.pos1
                data2[0] = self.pos2
                setting[0] = 4
                break


class DeplacebotE():
    "Classe permettant de modifier la position du joueur lors de l'utilisation de la commande E."

    def __init__(self, pos1, pos2, ordre,lab):
        self.pos1 = pos1
        self.pos2 = pos2
        self.ordre = ordre
        self.lab=lab

    def __iadd__(self, other):
        global data1, data2, setting
        i = 0

        labyrinthe = self.lab

        if self.ordre == 1 :
            ply = 'X'
        elif self.ordre == 2 :
            ply = 'x'
        elif self.ordre == 3 :
            ply = '*'
        else :
            ply = '+'

        while i < other :

            labyrinthe[self.pos1][self.pos2] = " "

            for tuplepoint in ppoint :
                if (self.pos1,self.pos2) == tuplepoint :
                    labyrinthe[tuplepoint[0]][tuplepoint[1]] = '.'

            self.pos2 += 1
            i += 1

            if labyrinthe[self.pos1][self.pos2] == "O":
                print(" ")
                print("Impasse! Impossible de passer.. ")
                self.pos2 = self.pos2 - 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            if labyrinthe[self.pos1][self.pos2] in playerz:
                print(" ")
                print("..Aie! Ne te met pas sur mon chemin.. ")
                print("")
                self.pos2 = self.pos2 - 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            for tuplepoint in ppoint :
                if (self.pos1,self.pos2) == tuplepoint :
                    labyrinthe[self.pos1][self.pos2] = ply
                    data1[0] = str(self.pos1)
                    data2[0] = str(self.pos2)
                    setting[0] = str(3)

            if labyrinthe[self.pos1][self.pos2] == " ":
                labyrinthe[self.pos1][self.pos2] = ply
                data1[0] = str(self.pos1)
                data2[0] = str(self.pos2)
                setting[0] = str(3)

            if labyrinthe[self.pos1][self.pos2] == "U":
                labyrinthe[self.pos1][self.pos2] = ply
                print(" ")
                for list in labyrinthe:
                    print(' '.join(list))
                print("")
                print("")
                print("Enfin la porte de sortie.. Victoire!")
                print("")
                data1[0] = self.pos1
                data2[0] = self.pos2
                setting[0] = 4
                break


class DeplacebotO():
    "Classe permettant de modifier la position du joueur lors de l'utilisation de la commande O."

    def __init__(self, pos1, pos2, ordre,lab):
        self.pos1 = pos1
        self.pos2 = pos2
        self.ordre = ordre
        self.lab=lab

    def __iadd__(self, other):
        global data1, data2, setting
        i = 0

        labyrinthe = self.lab

        if self.ordre == 1 :
            ply = 'X'
        elif self.ordre == 2 :
            ply = 'x'
        elif self.ordre == 3 :
            ply = '*'
        else :
            ply = '+'

        while i < other:

            labyrinthe[self.pos1][self.pos2] = " "

            for tuplepoint in ppoint:
                if (self.pos1, self.pos2) == tuplepoint:
                    labyrinthe[tuplepoint[0]][tuplepoint[1]] = '.'

            self.pos2 -= 1
            i += 1

            if labyrinthe[self.pos1][self.pos2] == "O":
                print(" ")
                print("Impasse! Impossible de passer.. ")
                self.pos2 = self.pos2 + 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            if labyrinthe[self.pos1][self.pos2] in playerz:
                print(" ")
                print("..Aie! Ne te met pas sur mon chemin.. ")
                print("")
                self.pos2 = self.pos2 + 1
                labyrinthe[self.pos1][self.pos2] = ply
                break

            for tuplepoint in ppoint:
                if (self.pos1, self.pos2) == tuplepoint:
                    labyrinthe[self.pos1][self.pos2] = ply
                    data1[0] = str(self.pos1)
                    data2[0] = str(self.pos2)
                    setting[0] = str(3)

            if labyrinthe[self.pos1][self.pos2] == " ":
                labyrinthe[self.pos1][self.pos2] = ply
                data1[0] = str(self.pos1)
                data2[0] = str(self.pos2)
                setting[0] = str(3)

            if labyrinthe[self.pos1][self.pos2] == "U":
                labyrinthe[self.pos1][self.pos2] = ply
                print(" ")
                for list in labyrinthe:
                    print(' '.join(list))
                print("")
                print("")
                print("Enfin la porte de sortie.. Victoire!")
                print("")
                data1[0] = self.pos1
                data2[0] = self.pos2
                setting[0] = 4
                break


class DeplacebotM():
    "Classe permettant de murer une porte suivie de la lettre représentant la direction avec la commande M."

    def __init__(self,direction,x1,x2,lab):
        self.pos1 = x1
        self.pos2 = x2
        self.direction = direction # On recupere la direction choisie
        self.lab=lab

    def __iadd__(self, other):
        global data1, data2, setting
        # on recupere la position du joueur en "abscysse et en ordonnee" pour pouvoir interagir en fonction des obstacles presents sur la map"
        x1=self.pos1
        x2=self.pos2
        labyrinthe = self.lab

        # On recupere la direction choisie pour l'action
        if self.direction == "s":
            x1+=1
        elif self.direction == "n":
            x1-=1
        elif self.direction == "e":
            x2+=1
        elif self.direction == "o":
            x2-=1

        # On verifie les obstacles presents sur la direction choisie pour reagir en consequence
        for tuplepoint in ppoint:
            if (x1, x2) == tuplepoint:
                if labyrinthe[x1][x2] == "O":
                    print(" ")
                    print("Il y a déjà un mur! ")
                else:
                    labyrinthe[x1][x2] = "O"
                    data1[0] = str(x1)
                    data2[0] = str(x2)
                    setting[0] = str(2)

        if labyrinthe[x1][x2] == " ":
            print("Ce n'est pas une porte!")

        if labyrinthe[x1][x2] in playerz:
            print("Tu ne peux pas murer ton adversaire.. Ca ne se fait pas voyons!")

        if labyrinthe[x1][x2] == "U":
            print("Ce n'est pas une porte mais la sortie! Sauve-toi!")


class DeplacebotP():
    "Classe permettant de percer une porte dans un mur suivie de la lettre représentant la direction avec la commande P."

    def __init__(self,direction,x1,x2,lab):
        self.pos1 = x1
        self.pos2 = x2
        self.direction = direction # On recupere la direction choisie
        self.lab=lab

    def __iadd__(self, other):
        global data1, data2, setting
        # on recupere la position de 'X' en "abscysse et en ordonnee" pour pouvoir interagir en fonction des obstacles presents sur la map"
        x1=self.pos1
        x2=self.pos2
        labyrinthe = self.lab

        # On recupere la direction choisie pour l'action
        if self.direction == "s":
            x1+=1
        elif self.direction == "n":
            x1-=1
        elif self.direction == "e":
            x2+=1
        elif self.direction == "o":
            x2-=1

        # On verifie les obstacles presents sur la direction choisie pour reagir en consequence
        for tuplepoint in ppoint:
            if (x1, x2) == tuplepoint:
                if labyrinthe[x1][x2] == "O" :
                    labyrinthe[x1][x2] = '.'
                    data1[0] = str(x1)
                    data2[0] = str(x2)
                    setting[0] = str(1)
                else :
                    print("La porte n'est pas murée.")

        if labyrinthe[x1][x2] == "O":
            print(" ")
            print("Il n'y a pas de porte à cet emplacement.")

        if labyrinthe[x1][x2] == " ":
            print("Ce n'est pas une porte et encore moins un mur!")

        if labyrinthe[x1][x2] in playerz:
            print("Tu ne peux pas percer ton adversaire..")

        if labyrinthe[x1][x2] == "U":
            print("Ce n'est pas une porte mais la sortie! Sauve-toi!")