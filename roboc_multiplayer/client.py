# -*-coding:Utf-8 -*
from fonctionsroboc import *
from classesroboc import *
from threadclass import *
import sys
import os
import socket
import time

print(" ")
print(" ")
print("    /\ ")
print("   /  \ ")
print("  /    \ ")
print(" /      \__________ROBOC-GAME___INOINO.2.0")
print("/   ض  \     " )
print("      \    /       Multiplayer @")
print("       \  / ")
print("        \/ ")
print("         |")
print("         |")
print("         |")

ordre=[] # variable recevant l'id (chiffre) du joueur apres sa connexion au serveur

s = 0
while s != 1 :
    if s == 0 :
        print("")
        print("")
        print("")
        setp = input(" Connexion < n >  // Instructions < i > :")
        setp = setp.lower()

    if setp == 'n':
        s = 1
        connex_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connex_serveur.connect(('localhost', 12600))
        print("")
        print("Connexion au serveur reussie!")

        setupx = connex_serveur.recv(1024)
        setupx = setupx.decode()
        datax = setupx.split(",") # les differentes donnees ayant ete envoyes (côte serveur) dans une seule et même variable avec une virgule puis un point les separants, la methode split permet de faire le tri
        mapp = datax[-1] # à la suite du premier split(","), les donnees separees par un point ont ete envoyees dans un même index (le dernier), on les captures dans la variable mapp. (= id + choix de map)
        mapp = mapp.split(".") # que l'on tri à nouveau avec l'indice (".")
        # enfin, on supprime le dernier index pour ne pas fausser l'utilisation des donnees par la suite.
        del datax[-1]

        labyrinthe = loadmap(mapp[1]) # le choix de map passe en parametre de notre fonction loadmap.

        if int(mapp[0]) > 1 : # Si l'id du joueur est superieur à 1, et donc n'est pas le premier connecter(...)
            compteur = 0
            while compteur < len(datax):
                # on parcour la liste 'datax' et on recupere la position du joueur (pos1/pos2), et son id
                pos1 = int(datax[compteur])
                compteur += 1
                pos2 = int(datax[compteur])
                compteur += 1
                player = int(datax[compteur])
                compteur += 1
                reconstructeur(0, 0, 5, pos1, pos2, player,labyrinthe) # puis on passe en parametre de notre fonction 'reconstructeur' les donnees pour actualiser la map

        # L'id du joueur est envoye à notre variable 'ordre'
        ordre.append(int(mapp[0]))

    elif setp == 'i' :
        print("")
        print("Un labyrinthe (laburinthos en grec ancien, labyrinthus en latin) est un trace sinueux, muni ou non d'embranchements,"
              " d'impasses et de fausses pistes destine à perdre ou à ralentir celui qui cherche à s'y deplacer."
              "Source : Wikipedia.\n"
              "Votre mission consiste à en sortir sans trop veillir à l'interieur! \n"
              "\n"
              "Chaque robot faisant un seul mouvement par tour. Le joueur pourra toujours demander au robot d'aller trois fois vers l'est, par exemple,\n"
              "mais le jeu ne fera bouger le robot qu'une fois avant de demander le coup de l'autre joueur puis proposera de continuer l'action entamee le tour suivant.\n"
              "Remarque : Une collision (contre un mur ou un joueur) est comptabilisee comme etant un coup, soyez donc prudents.\n"
              "\n"
              "Commandes : < S(+?) > : Deplacement vers le bas de l'ecran (sud)\n"
              "          : < N(+?) > : Deplacement vers le haut de l'ecran (nord)\n"
              "          : < E(+?) > : Deplacement vers la droite de l'ecran (est) \n"
              "          : < O(+?) > : Deplacement vers la gauche de l'ecran (ouest) \n"
              "          : < M(+*) > : Murage d'une porte / * : l'ajout de la direction est indispensable! \n"
              "          : < P(+*) > : Percage d'une porte muree / * : l'ajout de la direction est indispensable! \n"
              "\n"
              "Map : 'O' correspond à un mur, impossible à franchir \n"
              "    : '.' correspond à une porte \n"
              "    : 'U' correpond à la sortie, à la victoire! \n"
              "    : 'X' correspond à ton robot, c'est toi! \n"
              "\n"
              "Bon courage.")
        print("")

    else :
        print("")
        print("Commande inconnue. Veuillez entrer une des commandes ci-dessous !")
        print("")

# on place aleatoirement le joueur sur la map avec notre fonction et ses 2 parametres : l'id et le labyrinthe
placement_x(ordre[0],labyrinthe)
x = playerposition(ordre[0],labyrinthe) # on recupere la position du joueur apres son placement aleatoire
x1, x2 = str(x[0]), str(x[1])

if ordre[0] == 1 :
    caracter = "X"
elif ordre[0] == 2 :
    caracter = "x"
elif ordre[0] == 3 :
    caracter = "*"
else :
    caracter = "+"

print("")
print("Bienvenue à toi, Joueur",ordre[0])
print("")
print("Ton robot :",caracter)
print("")
print("En attente que d'autres joueurs rejoignent la partie. . .")

# envoi de la position du joueur au serveur pour que cette derniere soit transferee aux autres clients
recup = str(0) + "," + str(0) + "," + str(5) + "," + x1 + "," + x2 + "," + str(ordre[0]) # toujours le même type de tri avec les virgules entre chaque donnee pour pouvoir utiliser la methode split à l'arrivee
msg_a_env = recup.encode()
connex_serveur.send(msg_a_env)

debut = Receive(connex_serveur,ordre[0],labyrinthe) # On lance le thread 'Receive' qui vas être en constante ecoute du serveur pour recevoir les nouvelles donnees durant le deroulement du jeu.
debut.start()
input_th = InputThread(ordre[0],debut) # demarrage du thread pour le input : " (..) entrer C pour lancer la partie "
input_th.start()

while debut.signal == False: # tant que la variable 'signal', du thread Receive renvoie false celà signifie que personne n'a entrer 'c' dans son input
    if input_th.retour == 'c':
        input_th.stop()
        debut.signal = True  # en faisant celà, les autres joueurs et le joueur en question sortiront de cette boucle (variable se trouvant dans le thread Receive)

# on "tue" le thread input,la condition de la boucle principale n'etant plus respectee le thread "s'arrête".
input_th.stop()


#########################################################################################################################################################################################
y = 0
i = 0 # condition boucle ci-dessous
# les variables 'rese_x' et 'reste' recuperent les restes de l'action entamee par le joueur ( ex : s5 ou n2 etant donnee que le deplacement est limite à une 'case' par tour )
reste_x = "0"
reste = 0
choix="" # choix commande du joueur
once = 0
##########################################################################################################################################################################################


recup = str(0) + "," + str(0) + "," + str(6) + "," + str(0) + "," + str(0) + "," + str(0)
msg_a_env = recup.encode()   # envoi du setting 6, pour mettre fin au thread input (module threadclass)
connex_serveur.send(msg_a_env)

if debut.killinput == "on":
    once = 1 # cette variable est volontairement placee à l'exterieur de la boucle car elle ne servira qu'une fois pour remplir une condition, puis sera mise à zero(explication ligne 209)

print("")
print("             ____/\_________! Debut de la partie !_________/\____ ")
print("")
if debut.tour == ordre[0]:
    pass
else:
    print("Veuillez attendre votre tour de jeu!")

while i != 1:
    if i == 0:
        time.sleep(1)
        if debut.arret == False :
            print("")
            print("Tu as perdu!")
            print("")
            print("En esperant vous revoir bientôt dans nos labyrinthes!")
            print("")
            os.system("pause")
            sys.exit()
        if debut.tour == ordre[0]: # si le numero de tour correspond à l'id du joueur (..)
            # on fait appel à notre thread Printer pour eviter les interferences lors de l'affichage suite aux ressources partagees par les differents programmes (=sys.stdout)
            th_print=Printer("\n"
                             "_________________________/ /    C'est ton tour!    \ \_________________________")
            th_print.start()
            th_print.join()

            if reste_x != "0":  # recuperation des restes de l'action entamee par le joueur lors de son coup precedent
                option = ["y","n"]
                reponse = input("Voulez-vous continuer votre coup precedent? Oui < Y > // Non < N > :")
                reponse.lower()
                while reponse not in option:
                    print("Ce n'est pas la bonne commande.")
                    reponse = input("Voulez-vous continuer votre coup precedent? Oui < Y > // Non < N > :")
                    reponse.lower()

                if reponse == "y":
                    choix = reste_x + str(reste)

                else:
                    th_print2=Printer("< N(+?) > / \ < S(+?) > / \ < E(+?) > / \ < O(+?) > / \ < M(+?) > / \ < P(+?) > \n"
                          ":")
                    th_print2.start()
                    th_print2.join()
                    choix = input()
                    choix = choix.lower()
                    reste_x = "0"
                    reste = 0
            else:
                th_print2 = Printer("< N(+?) > / \ < S(+?) > / \ < E(+?) > / \ < O(+?) > / \ < M(+?) > / \ < P(+?) > \n"
                    ":")
                th_print2.start()
                th_print2.join()

                if once == 1 :
                    # malgres la mort du thread (de sa boucle) l'input bloque le sys.stdout, de ce fait on redirige la valeur recuperee par ce dernier vers les classes commandes
                    input_th.join()
                    choix = input_th.data
                    once = 0
                    # apres celà l'input est definitivement hs
                else:
                    choix = input()
                    choix = choix.lower()
                    reste_x = "0"
                    reste = 0


####################################################################### // Exceptions // #######################################################################################


            possible = ['n', 's', 'e', 'o', 'm', 'p']

            while i != 2 :
                try:
                    if choix[0] not in possible:
                        raise ValueError
                except ValueError:
                    print("La commande entree n'existe pas! Veuillez entrer une des commandes ci-dessous.")
                    i = 0
                except IndexError:
                    print("La commande entree n'existe pas! Veuillez entrer une des commandes ci-dessous.")
                    i = 0
                else:
                    break

                th_print2 = Printer("\n"
                                    "< N(+?) > / \ < S(+?) > / \ < E(+?) > / \ < O(+?) > / \ < M(+?) > / \ < P(+?) >\n"
                                    ":")
                th_print2.start()
                th_print2.join()
                choix = input()
                choix = choix.lower()
                reste_x = "0"

            try:
                if choix[0] in possible[4:] and len(choix) == 1:  # Si "Murer" ou "Percer" est appelle sans que la direction ne soit precisee on leve une exception.
                    raise KeyError
                if choix[0] in possible[4:]:
                    assert choix[1] in possible[:4]  # Si la commande passee avec l'action "murer" ou "percer" ne fait pas partie des commandes directionnelles, on leve un exception.
                    if choix[1] in possible[:4]:  # Si l'assertion n'est pas levee, on actualise la valeur de notre variable i puis on continue de sorte à passer directement au bloc conditionnel suivant " if i == 2 : ".
                        i = 2
                        continue
                else:
                    choix_index = int(choix[1])
                    if int(choix[1:]) > 9:
                        raise ValueError

            except KeyError:
                print("Veuillez preciser la direction")
            except AssertionError:
                print("Cette commande n'est pas une direction ")
            except ValueError:

                print("")
                print(
                    "ValueError : Veuillez entrer un chiffre allant de 1 à 9 à côte de la lettre directionnelle.\n"
                    "Exemple : s5 \n"
                    "L'absence de lettre equivaut à 1.")
            # Si l'utlisateur entre une lettre directionnelle sans preciser de chiffre, il se deplacera d'une 'case' par defaut.
            except TypeError:
                choix_index = 1
                i = 2
            except IndexError:
                choix_index = 1
                i = 2
            else:
                choix_index = int(choix[1])
                i = 2


######################################################################### // Commandes // ######################################################################################


    if i == 2 :
        # Actualisation de la position du joueur.
        x = playerposition(ordre[0],labyrinthe)
        x1, x2 = str(x[0]), str(x[1])

        if choix[0] == 's':
            if choix_index > 1: # ce bloc conditionnel recupere le reste de l'action si le deplacement est superieur à une 'case'
                reste = choix_index - 1
                reste_x = "s"
            else:
                reste_x = "0"
            choix_index = 1
            # Creation de notre objet issu de la classe 'DeplacebotS'
            positionbot = DeplacebotS(x[0], x[1],ordre[0],labyrinthe)
            # avec cette incrementation on fait appel à la methode iadd de notre classe
            positionbot += choix_index
            # envoi des nouvelles donnees au serveur pour qu'il les transferes aux autres clients
            recup = str(data1[0]) + "," + str(data2[0]) + "," + str(setting[0]) + "," + x1 + "," + x2 + "," + str(ordre[0]) # toujours la même façon d'envoyer les donnees pour le split à l'arrivee
            cmd_data = recup.encode()
            connex_serveur.send(cmd_data)


        if choix[0] == 'n':
            if choix_index > 1:
                reste = choix_index - 1
                reste_x = "n"
            else:
                reste_x = "0"
            choix_index = 1
            positionbot = DeplacebotN(x[0], x[1],ordre[0],labyrinthe)
            positionbot += choix_index
            recup = str(data1[0]) + "," + str(data2[0]) + "," + str(setting[0]) + "," + x1 + "," + x2 + "," + str(ordre[0])
            cmd_data = recup.encode()
            connex_serveur.send(cmd_data)


        if choix[0] == 'e':
            if choix_index > 1:
                reste = choix_index - 1
                reste_x = "e"
            else:
                reste_x = "0"
            choix_index = 1
            positionbot = DeplacebotE(x[0], x[1],ordre[0],labyrinthe)
            positionbot += choix_index
            recup = str(data1[0]) + "," + str(data2[0]) + "," + str(setting[0]) + "," + x1 + "," + x2 + "," + str(ordre[0])
            cmd_data = recup.encode()
            connex_serveur.send(cmd_data)


        if choix[0] == 'o':
            if choix_index > 1:
                reste = choix_index - 1
                reste_x = "o"
            else:
                reste_x = "0"
            choix_index = 1
            positionbot = DeplacebotO(x[0], x[1],ordre[0],labyrinthe)
            positionbot += choix_index
            recup = str(data1[0]) + "," + str(data2[0]) + "," + str(setting[0]) + "," + x1 + "," + x2 + "," + str(ordre[0])
            cmd_data = recup.encode()
            connex_serveur.send(cmd_data)


        if choix[0] == 'm':
            actionbot = DeplacebotM(choix[1],x[0],x[1],labyrinthe)
            actionbot += 0 # Seulement pour lancer la fonction " iadd " dans notre classe.
            recup = str(data1[0]) + "," + str(data2[0]) + "," + str(setting[0]) + "," + x1 + "," + x2 + "," + str(ordre[0])
            cmd_data = recup.encode()
            connex_serveur.send(cmd_data)


        if choix[0] == 'p':
            actionbot = DeplacebotP(choix[1],x[0],x[1],labyrinthe)
            actionbot += 0 # Seulement pour lancer la fonction " iadd " dans notre classe.
            recup = str(data1[0]) + "," + str(data2[0]) + "," + str(setting[0]) + "," + x1 + "," + x2 + "," + str(ordre[0])
            cmd_data = recup.encode()
            connex_serveur.send(cmd_data)


        if int(setting[0]) == 4 :
            recup = str(data1[0]) + "," + str(data2[0]) + "," + str(4) + "," + x1 + "," + x2 + "," + str(ordre[0])
            cmd_data = recup.encode()
            connex_serveur.send(cmd_data)
            debut.ending()
            print("En esperant vous revoir bientôt dans nos labyrinthes!")
            print("")
            time.sleep(0.5)
            os.system("pause")
            sys.exit()

        i = 0
