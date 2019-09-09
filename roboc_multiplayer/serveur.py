# -*-coding:Utf-8 -*
import socket
import select
import sys

connexion_serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connexion_serveur.bind(('',12600))
connexion_serveur.listen(5)

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
print("")
print("Bienvenue sur le Roboc_Serveur, connectez de 2 à 4 joueurs.")
s = 0
while s != 1 :
    if s == 0 :
        print("")
        setp = input(" Choix de la map < n >  // Instructions < i > :")
        setp = setp.lower()
        print("")

    if setp == 'n' or s != 0 :
        s = 1
        choyce = input("Niveau facile < E > // Niveau prison < P > : ")
        print("")
        choice = choyce.lower()
        if choice == 'p' or choice == 'e':
            pass

        else :
            print("")
            print("Commande inconnue. Veuillez entrer une des commandes ci-dessous !")
            print("")
            s = 2 # On change la valeur de ' s ' pour refaire un tour de boucle.


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
            "          : < Q(+?) > : Quitter la partie (sauvegarde automatique)\n"
            "\n"
            "Map : 'O' correspond à un mur, impossible à franchir \n"
            "    : '.' correspond à une porte \n"
            "    : 'U' correpond à la sortie, à la victoire! \n"
            "    : 'X' correspond à ton robot, c'est toi! \n"
            "\n"
            "Bon courage.")
        print("")
        print("")

    else :
        print("")
        print("Commande inconnue. Veuillez entrer une des commandes ci-dessous !")
        print("")

print("Etat serveur : Online")

##################################################################################################################################
etat = True # booleen pour lancer la boucle
clients = [] # les clients connectes au serveur sont ajoutes dans la liste
plyr = 0  # variable qui s'incremente à chaque connexion de client, ceci pour attribuer à chaque client connecte un "id" personnel
x1=[] # positions
x2=[] # positions
jplay=[] # id's des joueurs
datax = [] # recuperation des donnees contenues dans x1,x2,jvalue avec boucle for
tour = 1 # variable tour qui donnera le tour au joueur ayant l'id correspondant, elle demarre à 1
fermeture_connexion = 0
##################################################################################################################################

while etat :

    if fermeture_connexion == 0 :

        connex_demandees, wlist, xlist = select.select([connexion_serveur], [], [], 0.05)

        for connexion in connex_demandees:
            connex_client, info_connex = connexion.accept()
            clients.append(connex_client)  # ajout du nouveau client à la liste 'clients'

            plyr += 1

            if plyr > 1:  # Dans le cas ou il ne s'agit pas du premier client connecte
                for value, value2, jvalue in zip(x1, x2, jplay):  # parcour des donnees (position + id) envoyees par les differents clients pour les renvoyees aux autres
                    pass
                datax.append(str(value) + "," + str(value2) + "," + str(jvalue) + ",")
                data = "".join(datax)
                player = str(plyr)
                datacfg = player + "." + choice + "."
                datapack = data + datacfg  # concatenation des donnees separees par une virgule, et de celles separee par un point pour effectuer le tri à l'arrivee à l'aide de la methode split
                config = datapack.encode()
                connex_client.send(config)

            else:  # les donnees envoyees pour le premier client connecte :"id" et choix de la map..
                player = str(plyr)
                datacfg = player + "." + choice  # ..dans une seule et même variable separee par un point, le tri s'effectuera à l'arrivee à l'aide de la methode split
                config = datacfg.encode()
                connex_client.send(config)

    clients_a_lire = []
    try :
        clients_a_lire,wlist,xlist = select.select(clients,[],[],0.05)
    except select.error:
        pass
    else :
        # on recupere toutes les donnees en attente d'être lues en parcourant la liste 'clients_a_lire' renvoyee par la methode select
        for client in clients_a_lire:
            infosrecu = client.recv(1024)
            infosrecu = infosrecu.decode()
            recup = infosrecu.split(",")
            # apres avoir utiliser la methode split, on recupere chaque donnee à l'aide de son index
            data1 = int(recup[0])
            data2 = int(recup[1])
            setting = int(recup[2]) # la variable 'setting' contient un chiffre interprete par la fonction 'reconstructeur' comme etant un type d'action (simple deplacement, murage...)
            x1.append(int(recup[3]))
            x2.append(int(recup[4]))
            jplay.append(int(recup[5]))

            print("")
            print("")

            datapack = infosrecu + "," + str(tour) # on capture les donnees recues dans la variable et on y ajoute "tour" contenant le chiffre de l'id/joueur à qui est le tour, separer par une virgule pour le tri à l'arrivee

            for cli in clients : # On retransfere les donnees à tous les clients
                infos = datapack.encode()
                cli.send(infos)

            if setting == 4 :
                sys.exit()

            elif setting == 6 : # setting 6 etant le signal indiquant la fin du thread input "(..) entrer C pour commencer.." les joueurs ont donc commencer la partie,
                fermeture_connexion = 1 # la condition ligne 100 n'etant plus respectee, il est desormais impossible pour de nouveaux joueurs de rejoindre la partie
                print("")

            if tour > len(clients)-1 : # si la variable 'tour' est superieure au nombre de client, elle repart à 1..
                tour = 1
            else :
                tour += 1 # ..sinon le tour passe au joueur suivant
