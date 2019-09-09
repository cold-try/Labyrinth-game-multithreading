import unittest
import random
from fonctionsroboc import *

labyrinthe = loadmap('e')

class Test_Fonctions(unittest.TestCase):
    "Test case utilisé pour tester les fonctions du module 'fonctionsroboc'"


    def test_loadmap(self):
        "Test le fonctionnement de la fonction 'loadmap' : Verifie qu'elle transforme bien les donnees du bloc note en listes, si la longueur du .txt correspond bien à celle du labyrinthe retourne par la fonction"

        PATH_FILE = Path(__file__).parent / "facile.txt"

        longueur_txt=0

        with open(PATH_FILE, "r") as f_read:
            with open(PATH_FILE, "r") as f_read:
                for line in f_read:
                    longueur_txt+=1

        longueur_load = len(loadmap('e'))

        self.assertIs(longueur_txt,longueur_load)

        a, b = type(loadmap('e')), list
        self.assertIs(a,b)


    def test_localiseporte(self):
        "Test le fonctionnement de la fonction 'localiseporte' : Verifie que les donnees retournees correspondent bien à des portes. (.) "

        localiseporte(labyrinthe)
        # Les donnees sont capturees dans la variable 'ppoint' dans le module fonctionsboc ( le module contenant la fonction )

        for position in ppoint :
            self.assertIs(labyrinthe[position[0]][position[1]], '.') # on passe en index de 'labyrinthe' le resultat de chaque tuple contenue dans notre variable 'ppoint' en on verifie qu'il correspond bien à '.'


    def test_placement_x(self):
        "Test le fonctionnement de la fonction 'placement_x' : disposition des robots sur les endroits vides de la map (sans obstacles) de façon aleaatoire "

        robots = ["X","x","*","+"]
        place_libre = []
        positions_robots = []

        for listt in labyrinthe:
            for index, valeur in enumerate(listt):
                if valeur == ' ':
                    place_libre.append(index)  # on recupere les positions des zones libres ' ' sur la map

        placement_x(1, labyrinthe)
        placement_x(2, labyrinthe)
        placement_x(3, labyrinthe)
        placement_x(4, labyrinthe)

        resultat = 0

        for liste in labyrinthe :
            for sous_liste in liste :
                if sous_liste in robots :
                    resultat += 1  # On commence par verifier que les differents robots ont bien ete disposes sur la map
        self.assertIs(resultat, 4)

        for liste in labyrinthe :
            for sous_liste in liste :
                if sous_liste in robots :
                    positions_robots.append(resultat) # on recupere les positions des robots sur la map

        resultat_2 = True

        for position in positions_robots :
            if position not in place_libre :
                resultat_2 = False

        self.assertTrue(resultat_2) # On verifie que les robots ont bien ete aleatoirement places sur des zones initialement 'libre'

        placement_x(1, labyrinthe)
        placement_x(2, labyrinthe)
        placement_x(3, labyrinthe)
        placement_x(4, labyrinthe) # On replace de façon aleatoire les robots

        positions_robots_2 = []

        for liste in labyrinthe :
            for sous_liste in liste :
                if sous_liste in robots :
                    positions_robots_2.append(resultat) # on recupere les nouvelles positions des robots

        self.assertNotEqual(positions_robots, positions_robots_2) # enfin, on verifie que les nouvelles positions des robots ne correpondent pas aux anciennes, prouvant par celà que le tirage est bien aleatoire.



    def test_playerposition(self):
        "Test le fonctionnement de la fcnction 'playerposition' : Verifie que la position recuperee par la fonction correspond bien à la position du robot"

        placement_x(1, labyrinthe) # On place le robot n°1 ( = 'X' ) avec notre fonction placement_x

        for list in labyrinthe :
            for indexx in list :
                if indexx == "X" :
                    position_X = labyrinthe.index(list), list.index(indexx) # on recupere sa position 'manuellement'

        position_X_2 = playerposition(1, labyrinthe) # on recupere sa position à l'aide de notre fonction

        self.assertEqual(position_X,position_X_2) # on compare nos deux resultats.


    def test_reconstructeur(self):
        "Test le fonctionnement de la fonction 'reconstruction' "

        # On commence par verifier le setting 2 => qui mure la porte (actualise la map avec la porte muree)
        localiseporte(labyrinthe) # On envoie les positions des portes dans notre variable 'ppoint' contenue dans le module fonctionsroboc.
        porte1 = ppoint[0] # on recupere la premiere position de porte de la liste pour effectuer notre test.

        if labyrinthe[porte1[0]][porte1[1]] == '.' :
            success = True
        else :
            success = False

        reconstructeur(porte1[0],porte1[1],2,0,0,1,labyrinthe) # appel de la fonction avec en parametre les donnees de la tuple 'porte1' + le num du setting + la position du joueur
        # (qui là, n'a pas d'importance(=0,0)) le caractere du robot (1 = 'X') + le labyrinthe .

        if labyrinthe[porte1[0]][porte1[1]] == 'O' :
            success_0 = True
        else :
            success_0 = False

        self.assertEqual(success,success_0) # On verifie que les deux resultats soient True, et donc que la porte ai bien ete changee en mur.

        # On verifie maintenant le setting 1 => qui perce la porte muree .
        reconstructeur(porte1[0], porte1[1], 1, 0, 0, 1, labyrinthe) # on change le troisieme parametre pour mettre le setting à 1 (= percage)

        if labyrinthe[porte1[0]][porte1[1]] == '.':
            success_1 = True
        else:
            success_1 = False

        self.assertEqual(success_0, success_1) # On compare cette fois avec le resultat precedent, si le changement a bien ete effectue

        # On verifie maintenant le setting 3 => correspondant au simple deplacement du joueur

        placement_x(2, labyrinthe) # On fait apparaître notre robot 2 (= 'x') sur le labyrinthe
        position_robot = playerposition(2, labyrinthe) # puis on recupere sa position

        if labyrinthe[position_robot[0]][position_robot[1]] == 'x' :
            success_2 = True
        else :
            success_2 = False

        self.assertIs(success_2, True) # on verifie qu'un robot se trouve bien à la position recuperee p

        reconstructeur(position_robot[0], position_robot[1]+1, 3, position_robot[0], position_robot[1], 2, labyrinthe) # on appelle notre fonction,avec la nouvelle position de 'x' (on incremente la valeur de 1)

        if labyrinthe[position_robot[0]][position_robot[1]] == ' ' : # On verifie que la case sur laquelle est passe le robot soit vide apres son passage
            success_3 = True
        else :
            success_3 = False

        self.assertIs(success_3, True)

        if labyrinthe[position_robot[0]][position_robot[1]+1] == 'x' : # On verifie que le robot se trouve bien sur sa nouvelle position
            success_4 = True
        else :
            success_4 = False

        self.assertIs(success_4, True)