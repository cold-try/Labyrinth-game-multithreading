# -*-coding:Utf-8 -*
from pathlib import Path
import random


ppoint=[] # ppoint = variable recevant la position des '.' (portes) de la map suite à l'appel de la fonction 'localiseporte()'
spawn=[] # Variable recevant les positions des endroits sans obstacles " " sur la map suite à l'appel de la fonction 'placement_x'

def loadmap(choice):
    "Chargement du labyrinthe choisi par le joueur sous forme de liste"

    labyrinthe=[]

    PATH_FILE = Path(__file__).parent / "facile.txt"
    PATH_FILE2 = Path(__file__).parent / "prison.txt"
    if choice == 'e' :
        with open(PATH_FILE, "r") as f_read:
            for line in f_read:
                line = line.strip()
                labyrinthe.append(list(line))
    elif choice == 'p' :
        with open(PATH_FILE2, "r") as f_read:
            for line in f_read:
                line = line.strip()
                labyrinthe.append(list(line))

    #Recuperation des positions des portes '.' sur la map, pour gerer l'affichage apres le passage de 'X'.
    localiseporte(labyrinthe)

    return labyrinthe


def affichaage(lab):
    "Affichage de la liste sans les crochets de listes et apostrophes"

    for list in lab:
        print(' '.join(list))


def playerposition(ordre,labyrinthe):
    "Recuperation de la position du joueur sur la map"

    for listx in labyrinthe :
        for index in listx :
            if ordre == 1: # la variable "ordre" est attribuee par le serveur en fonction de l'odre de connexion(d'arrivee) du joueur
                if index == 'X': # la fonction cherche la position du joueur en question puis renvoie la valeur dans la variable x
                    x = labyrinthe.index(listx), listx.index(index)
            elif ordre == 2 :
                if index == 'x':
                    x = labyrinthe.index(listx), listx.index(index)
            elif ordre == 3 :
                if index == '*':
                    x = labyrinthe.index(listx), listx.index(index)
            else :
                if index == '+':
                    x = labyrinthe.index(listx), listx.index(index)
    return x


def localiseporte(labyrinthe):
    "Recuperation des positions des '.' sur la map, pour gerer l'affichage apres le passage de 'X'."

    z = [] # les positions des portes sont ajoutees au fur et à mesure du parcours de la boucle
    for listt in labyrinthe:
        z.append(listt)
        for indexx, val in enumerate(listt):
            if val == '.':
                recup = len(z) - 1, indexx
                ppoint.append(recup)


def placement_x(ordre,labyrinthe):
    "Fait apparaître le joueur aleatoirement sur la map"

    plc_libre = []
    for listt in labyrinthe:
        plc_libre.append(listt)
        for indexx, val in enumerate(listt):
            if val == ' ': # Recuperation des endroits sans obstacles sur la map
                recup = labyrinthe.index(listt), indexx
                spawn.append(recup)
    random_x = random.choice(spawn) # Tirage d'une des positions sans obstacles à l'aide de random
    if ordre == 1 :
        labyrinthe[random_x[0]][random_x[1]] = 'X'
    elif ordre == 2 :                                # ajout du joueur sur la map en fonction de son 'personnage'( la variable "ordre" contenant le chiffre attribue par le serveur en fonction de son ordre d'arrivee )
        labyrinthe[random_x[0]][random_x[1]] = 'x'
    elif ordre == 3 :
        labyrinthe[random_x[0]][random_x[1]] = '*'
    else :
        labyrinthe[random_x[0]][random_x[1]] = '+'


def reconstructeur(data1, data2, setting, x1, x2, ply, labyrinthe):
    "Reconstruit le labyrinthe apres avoir reçu de nouvelles donnees"

    if ply == 1: # variable 'ply' : chiffre(=identite) du joueur ayant fait l'action
        player = 'X'
    elif ply == 2:
        player = 'x'
    elif ply == 3:
        player = '*'
    else:
        player = '+'

    if int(setting) == 1: # variable 'setting' transmet à la fonction le type d'action effectue sous forme de chiffres, apres le passage de la commande dans l'une des classes commandes (Module classesroboc) du joueur
        labyrinthe[int(data1)][int(data2)] = '.' # percage
    elif int(setting) == 2: # murage
        labyrinthe[int(data1)][int(data2)] = 'O'
    elif int(setting) == 3: # simple deplacement
        labyrinthe[x1][x2] = " "
        labyrinthe[int(data1)][int(data2)] = player

        for tuplepoint in ppoint:  # Boucle for pour faire reaparaître la porte '.' apres le passage du joueur.
            if (x1, x2) == tuplepoint:
                if labyrinthe[tuplepoint[0]][tuplepoint[1]] != 'O':
                    labyrinthe[x1][x2] = '.'

    elif int(setting) == 4: # victoire du joueur
        labyrinthe[x1][x2] = " "
        labyrinthe[int(data1)][int(data2)] = player
        print("")
        print("Fin de partie.")
        print("")

    elif setting == 5 : # apparition d'un nouveau joueur (avant lancement de la partie)
        labyrinthe[x1][x2] = player

    return labyrinthe
