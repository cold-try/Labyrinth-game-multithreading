from threading import Thread, RLock
from fonctionsroboc import *
import sys
import time

########################################################################################################################
player_number = 0 # reçoit l'id du joueur proprietaire des donnees reçues
verrou =RLock()
########################################################################################################################


class Afficheur(Thread):
    "Thread + RLock pour afficher la map sans interference pendant l'affichage"

    def __init__(self, labyrinthe):
        Thread.__init__(self)
        self.lab = labyrinthe

    def run(self):
        with verrou:
            for list in self.lab:
                print(' '.join(list))


class Printer(Thread):
    "Thread + RLock pour un print sans interference pendant l'affichage"

    def __init__(self,txt):
        Thread.__init__(self)
        self.texte = txt

    def run(self):
        with verrou:
            print(self.texte)


class Receive(Thread):
    "Thread chargé de recevoir les nouvelles donnees du labyrinthe pendant l'execution du programme principal."

    def __init__(self,serveur,ordre,labyrinthe):
        Thread.__init__(self)
        self.serveur = serveur
        self.ordre = ordre
        self.labyrinthe = labyrinthe
        self.signal = False
        self.tour = 0
        self.stopinput = True
        self.arret = True
        self.killinput = "off" # on y accedera de l'exterieur de la classe pour mettre fin au thread 'input' plutôt persistant
        self.end = False

    def run(self):

        global player_number

        while self.arret:
            infosrecu = self.serveur.recv(1024)
            infosrecu = infosrecu.decode()
            recup = infosrecu.split(",") # toujours le même type de tri à la reception des donnees ; split + acces par l'index
            data1 = int(recup[0])
            data2 = int(recup[1])
            setting = int(recup[2]) # variable 'setting' transmet à la fonction le type d'action effectue sous forme de chiffres, apres le passage de la commande dans l'une des classes commandes (Module classesroboc) du joueur
            x1 = int(recup[3])
            x2 = int(recup[4])
            player_number = int(recup[5]) # id du joueur
            self.tour = int(recup[6]) # id du joueur ayant le tour de jeu

            if setting == 4 : # victoire d'un des joueurs, fin de jeu
                labyrinthe = reconstructeur(data1, data2, setting, x1, x2, player_number,self.labyrinthe)  # actualisation de la map avec les nouvelles donnees reçues
                affichage = Afficheur(labyrinthe)
                # on lance le thread pour afficher la map actualisee
                affichage.start()
                affichage.join()
                self.ending()
                sys.exit()

            if player_number != self.ordre and setting == 5: # Si ce n'est pas le tour de jeu du joueur en question (...)
                print("")
                print("Un nouveau joueur rejoint la partie!")
                print("")
                labyrinthe = reconstructeur(data1, data2, setting, x1, x2, player_number, self.labyrinthe) # actualisation de la map avec les nouvelles donnees reçues
                affichage = Afficheur(labyrinthe)  # Thread pour l'affichage de la map actualisee sans interference
                affichage.start()
                affichage.join()
                th_print = Printer("\n"
                                    ". . à tout moment, entrer < C > pour commencer ! >>")
                th_print.start()
                th_print.join()

            elif setting == 6 : # setting 6 sert de signal pour changer les valeurs ci-dessous, "tuant" par cela, le thread input
                self.signal = True
                self.killinput="on"

            else:
                print("")
                labyrinthe = reconstructeur(data1, data2, setting, x1, x2, player_number, self.labyrinthe) # actualisation de la map avec les nouvelles donnees reçues
                affichage = Afficheur(labyrinthe) # Thread pour l'affichage de la map actualisee sans interference
                affichage.start()
                affichage.join()
                if self.ordre != self.tour and self.killinput == "on" and setting != 4:
                    th_print0 = Printer("\n"
                                       "Veuillez attendre votre tour de jeu!")
                    th_print0.start()
                    th_print0.join()
                elif self.killinput != "on" and self.ordre != 1:
                    th_print = Printer("\n"
                                       ". . à tout moment, entrer < C > pour commencer ! >>")
                    th_print.start()
                    th_print.join()
                else:
                    pass

    def stop(self):
        self.stopinput = False

    def ending(self):
        self.arret = False
        self.end = True


class InputThread(Thread):
    "Thread pour l'input lancer partie"

    def __init__(self,ordre,debut):
        Thread.__init__(self)
        self.ordre = ordre
        self.retour = ""
        self.sign = "No" # condition pour la deuxieme boucle du run()
        self.debut = debut
        self.data = "" # recupere le retour de l'input
        self.ctrl="yes" # condition pour la boucle du run()

    def run(self):

        global player_number

        while self.ctrl == "yes":
            while self.sign != "ok":  # deuxieme boucle servant à garder le joueur en attente le temps qu'il y ai le nombre suffisant de joueurs afin d'envoyer l'input
                if self.ordre > 1 or player_number > 1:  # Verifie qu'il y ai le nombre de joueurs suffisant (>2) pour lancer le input ( = .."entrer <C> pour commencer la partie")
                    self.sign = "ok"
                else:
                    pass

            print("")
            dep = input()
            print("")
            dep = dep.lower()

            while dep != "c": # tant que la reponse n'est pas 'c' on garde le joueur dans la boucle et on renvoie l'input..
                if self.ctrl == "yes":
                    print("Ce n'est pas la bonne touche!")
                    print("")
                    dep = input(". . . à tout moment, entrer < C > pour commencer ! >>")
                    print("")
                    dep = dep.lower()
                else:
                    self.data = dep  # on capture la reponse dans la variable
                    break

            self.retour = dep
            self.stop()

    def stop(self):
        self.ctrl = "stop" # met fin à la boucle principale du thread

    def stopinput(self):
        self.debut.killinput = "on" # met fin au thread (l'input bloquant toujours le sys.stdout apres la mort de la boucle on redirigera la valeur (client/ligne 209))