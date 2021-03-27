import math, time
from tkinter import Tk, Canvas

# TRAITEMENT DU FICHIER NOEUDS.CSV
fichier_noeuds = 'Noeuds.csv'

# PRAMETRES DEPENDANT DU FICHIER EN ENTREE

LesNoeuds = open(fichier_noeuds, "r")
# format du fichier : numero du noeud \t longitude \t latitude \n
tousLesNoeuds = LesNoeuds.readlines()
LesNoeuds.close()

# On initialise les listes a vide
Longitude = []
Latitude = []

minLong = 1
maxLong = 0
minLat = 1
maxLat = 0

for un_noeud in tousLesNoeuds:
    un_noeud.strip("\n")
    ce_noeud = un_noeud.split('\t')

    # On converti ces valeurs en float
    long = float(ce_noeud[1]) * (math.pi / 180)
    lat = float(ce_noeud[2]) * (math.pi / 180)

    Longitude.append(long)
    Latitude.append(lat)

    if (minLat > lat): minLat = lat
    if (maxLat < lat): maxLat = lat
    if (minLong > long): minLong = long
    if (maxLong < long): maxLong = long

# TRAITEMENT DU FICHIER ARC.CSV
fichier_arc = 'Arcs.csv'

# PRAMETRES DEPENDANT DU FICHIER EN ENTREE

LesArcs = open(fichier_arc, "r")
# format du fichier : origine \t destination \t longueur \t dangerosite \n
tousLesArcs = LesArcs.readlines()
LesArcs.close()

Origine = []
Destination = []
Longueur = []
Dangerosite = []

for un_arc in tousLesArcs:
    un_arc.strip('\n')
    cet_arc = un_arc.split("\t")

    Orig = int(cet_arc[0])
    Origine.append(Orig)

    Dest = int(cet_arc[1])
    Destination.append(Dest)

    Long = int(cet_arc[2])
    Longueur.append(Long)

    Dang = int(cet_arc[3].strip('\n'))
    Dangerosite.append(Dang)

# NbSommets = max(max(Origine), max(Destination)) + 1
NbSommets = len(tousLesNoeuds)
Succ = [[] for j in range(NbSommets)]

for u in range(0, len(Origine)):
    orig = Origine[u]
    dest = Destination[u]
    Succ[orig].append(dest)


# print(Succ[1703])

# Methode qui renvoie le numero de l'arc reliant i a j, si l'arc n'existe pas
# renvoie -1
def Arc(i, j):
    for l in range(len(Origine)):
        if Origine[l] == i and Destination[l] == j:
            return l
    return  -1


# print(Arc(1704, 14814))
# print(Arc(1704, 1481))


# ########################################################
# Dessin du graphe
# ########################################################

print('*****************************************')
print('* Dessin du graphe                      *')
print('*****************************************')


def cercle(x, y, r, couleur):
    can.create_oval(x - r, y - r, x + r, y + r, outline=couleur, fill=couleur)


def TraceCercle(j, couleur, rayon):
    x = (Longitude[j] - minLong) * ratioWidth + border
    y = ((Latitude[j] - minLat) * ratioHeight) + border
    y = winHeight - y
    cercle(x, y, rayon, couleur)


def TraceSegment(i, j, color):
    # Coordonnees de i
    x1 = (Longitude[i] - minLong) * ratioWidth + border
    y1 = ((Latitude[i] - minLat) * ratioHeight) + border
    y1 = winHeight - y1

    # Coordonnees de j
    x2 = (Longitude[j] - minLong) * ratioWidth + border
    y2 = ((Latitude[j] - minLat) * ratioHeight) + border
    y2 = winHeight - y2

    can.create_line(x1, y1, x2, y2, fill=color)


fen = Tk()
fen.title('Graphe')
coul = "dark green"  # ['purple','cyan','maroon','green','red','blue','orange','yellow']

Delta_Long = maxLong - minLong
Delta_Lat = maxLat - minLat
border = 20  # taille en px des bords
winWidth_int = 800
winWidth = winWidth_int + 2 * border  # largeur de la fenetre
winHeight_int = 800
winHeight = winHeight_int + 2 * border  # hauteur de la fenetre : recalculee en fonction de la taille du graphe
# ratio= 1.0          # rapport taille graphe / taille fenetre
ratioWidth = winWidth_int / (maxLong - minLong)  # rapport largeur graphe/ largeur de la fenetre
ratioHeight = winHeight_int / (maxLat - minLat)  # rapport hauteur du graphe hauteur de la fenetre

can = Canvas(fen, width=winWidth, height=winHeight, bg='dark grey')
can.pack(padx=5, pady=5)

#  cercles
rayon = 1  # rayon pour dessin des sommets
rayon_od = 5  # rayon pour sommet origine et destination
# Affichage de tous les sommets
for i in range(0, NbSommets):
    TraceCercle(i, 'black', rayon)

# On trace tous les arcs de la ville en noir
for i in range(NbSommets):
    for succ in Succ[i]:
        TraceSegment(i, succ, "black")

def Disjkstra(sommet_depart, sommet_destination):
    Pi = [INFINITY for i in range(NbSommets)]
    PiPrime = [INFINITY for i in range(NbSommets)]
    LePere = [UNDEFINED for i in range(NbSommets)]
    marque = [0 for i in range(NbSommets)]

    #
    Pi[sommet_depart] = 0
    PiPrime[sommet_depart] = 0
    for j in Succ[sommet_depart]:
        Pi[j] = Longueur[Arc(sommet_depart, j)]
        LePere[j] = sommet_depart

    nb_sommets_explores = 0
    fini = False

    while nb_sommets_explores < NbSommets and not fini:
        # Fini passera a vrai quand on aura trouve le sommet_destination
        # On boucle quand même sur le nb_sommets_explores < NbSommets au cas ou le graphe ne serait pas
        # connexe. Si pas de chemin entre sommet_origine et sommet_dest

        le_min = INFINITY

        for sommet in range(NbSommets):
            if PiPrime[sommet] == INFINITY:
                if Pi[sommet] < le_min:
                    le_min = Pi[sommet]
                    sommet_retenu = sommet
        # print(Pi[sommet_retenu], sommet_retenu)
        marque[sommet_retenu] = 1
        # PiPrime[sommet_retenu] = Longueur[Arc(sommet, sommet_retenu)]
        PiPrime[sommet_retenu] = Pi[sommet_retenu]
        TraceCercle(sommet_retenu, 'yellow', 1)
        if sommet_retenu == sommet_destination:
            fini = True
        for k in Succ[sommet_retenu]:
            if (marque[k] == 0):
                long = Longueur[Arc(sommet_retenu, k)]
                if Pi[sommet_retenu] + long < Pi[k]:
                    Pi[k] = Pi[sommet_retenu] + Longueur[Arc(sommet_retenu, k)]
                    LePere[k] = sommet_retenu

    # for s in range(NbSommets):
    #     if marque[s] == 1:
    #         TraceCercle(s, 'yellow', 1)
    #         # for k in Succ[s]:
    #         #     if marque[s] == 1 and marque[k] == 1:
    #         #         TraceSegment(s, k, 'yellow')



# print(Succ)
sommet_depart = 3000
# sommet_destination = 11342
sommet_destination = 22279
time_start = time.process_time()
TraceCercle(sommet_depart, 'green', rayon_od)

TraceCercle(sommet_destination, 'red', rayon_od)
INFINITY = float('inf')


UNDEFINED = -1


Disjkstra(sommet_depart, sommet_destination)
time_end = time.process_time()
print('Duree du processus', time_end - time_start)
fen.mainloop()
