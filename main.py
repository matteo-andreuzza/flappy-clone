import pygame
import random
import sys
import time
pygame.init()
#caricamento immagini
sfondo = pygame.image.load('immagini/sfondo.png')
uccello = pygame.image.load('immagini/uccello.png')
base = pygame.image.load('immagini/base.png')
gameover = pygame.image.load('immagini/gameover.png')
tuboGiu = pygame.image.load('immagini/tubo.png')
tuboSu = pygame.transform.flip(tuboGiu, False, True)
pause = pygame.image.load('immagini/pausa.png')
facile = 0
#costanti globali
SCHERMO = pygame.display.set_mode((288, 512))
FPS = 60
VEL = 1
FONT = pygame.font.SysFont('Comic Sans MS', 50, bold=False)
#classe tubi (contiene i tubi)
class tubi_class:
    #definisce la posizione dei tubi
    def __init__(self):
        self.x = 300
        self.y = random.randint(-10, 30)
    #disegna i tubi
    def avanza_e_disegna(self):
        self.x -= VEL
        SCHERMO.blit(tuboGiu, (self.x, self.y+210)) 
        SCHERMO.blit(tuboSu, (self.x, self.y-210)) 
    #collisione con tubo
    def collisione(self, uccello, uccellox, uccelloy):
        global facile
        facile = 2 #+ facile + facile
        uccello_lato_dx = uccellox + uccello.get_width()-facile 
        uccello_lato_sx = uccellox + facile
        tubi_lato_dx = self.x + tuboGiu.get_width()
        tubi_lato_sx = self.x
        uccello_lato_su = uccelloy + facile
        uccello_lato_giu = uccelloy + uccello.get_height() - facile
        tubi_lato_su = self.y + 110
        tubi_lato_giu = self.y + 210
        #collisione
        if uccello_lato_dx > tubi_lato_sx and uccello_lato_sx < tubi_lato_dx:
            if uccello_lato_su < tubi_lato_su or uccello_lato_giu > tubi_lato_giu: #se l'uccello sovrappone il tubo
                hai_perso() #chiama hai perso e stampa game over
                print('[debug] collisione tubo') #stmapa il motivo della collisione sulla console
    def punti_su(self, uccello, uccellox): #controlla che il tubo in questione non abbia l'uccello sovrapposto
        facile = 5
        uccello_lato_dx = uccellox + uccello.get_width()-facile 
        uccello_lato_sx = uccellox + facile
        tubi_lato_dx = self.x + tuboGiu.get_width()
        tubi_lato_sx = self.x
        if uccello_lato_dx > tubi_lato_sx and uccello_lato_sx < tubi_lato_dx: #se l'uccello sorpassa i tubi
            return True
#funzioni
def inizializza():
    #definixce le varibili globali
    global uccellox, uccelloy, uccello_vely
    global basex
    global tubi
    global punti
    global punti_su
    global facile
    uccellox, uccelloy = 60, 150 #assegna la posizione inzialaìe dell'uccello  impostando le varibili di posizione
    uccello_vely = 0
    basex = 0
    punti = 0
    tubi = [] #crea una lista con i tubi
    tubi.append(tubi_class()) #aggiunge alla lista dei tubi quelli contenuti nella classe
    punti_su = False #all'inizio i punti non salgono
    print('[debug] inizializzato') #stamap sulla console che il gioco è partito
    print('[debug] facile = ' + str(facile))
    

def disegna_oggetti():
    SCHERMO.blit(sfondo, (0,0)) #fa vedere lo sfondo
    for t in tubi:
        t.avanza_e_disegna() #per ogni tubo (t) nella lista di tubi stampa il tubo con il metodo avanza e disegna assegnato a t (tubo nella lista)
    SCHERMO.blit(uccello, (uccellox,uccelloy)) #fa vedere l'uccello nelle coodinate delle variabili
    SCHERMO.blit(base, (basex,400)) #fa vedere la base alla sua coordinata
    punti_render = FONT.render('Punti:' + str(punti), 1, (255, 255, 255)) #imposta il font della scritta dei punti
    SCHERMO.blit(punti_render, (100,0)) #fa vedere la scritta dei punti

def aggiorna():
    pygame.display.update() #aggiorna gli elementi sullo schermo
    pygame.time.Clock().tick(FPS) #sggiorna l'rologio con gli FPS

def hai_perso():
    SCHERMO.blit(gameover, (50,180)) #fa vedere l'immagine di game over
    print('[game] GAME OVER') #stampa sulla console il game over
    aggiorna() #chiama aggiorna e aggiorna tutto
    ricominciamo = False #imposta la partenza del gioco su false
    while not ricominciamo:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #se viene premuto lo spazio
                print('[debug] spazio premuto (code_ K_SPACE)') #stmapa che è stao premuto
                inizializza() #fa partire il gioco
                ricominciamo = True # porta la ripartenza del gioco su vero per uscire dal ciclo
            if event.type == pygame.QUIT: #se si esce dal gioco
                pygame.quit() #ferma il gioco e esce da pygame
                sys.exit(0) #il sitema termina il processo

def pausa():
    SCHERMO.blit(pause, (1,1)) #fa vedere l'immagine di pausa
    print('[game] PAUSA') #stampa sulla console il game over
    aggiorna() #chiama aggiorna e aggiorna tutto
    ricominciamo = False #imposta la partenza del gioco su false
    while not ricominciamo:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: #se viene premuto la p
                print('[debug] uscito da pausa (code_ K_p)') #stmapa che è stao premuto
                ricominciamo = True # porta la ripartenza del gioco su vero per uscire dal ciclo
            if event.type == pygame.QUIT: #se si esce dal gioco
                pygame.quit() #ferma il gioco e esce da pygame
                sys.exit(0) #il sitema termina il processo


inizializza() #fa partire il gioco

while True:
    basex -= VEL #la base scorre
    if basex < -45: basex = 0 #quando la base arriva alla fine, viene riportata all'inzio per dare senso di continuità
    #gravità
    uccello_vely += 0.7 #velocità dell'uccello minore o = a 0.7 (valore modificabile)
    uccelloy += uccello_vely #velocitò orizzontale dell'uccello come la velocitò dell'ucccelo
    #comandi
    for event in pygame.event.get():
        if ( event.type == pygame.KEYDOWN
            and event.key == pygame.K_UP or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) : #se si preme freccia su o spazio
            uccello_vely = -5 #fa alzare l'uccello
        elif (event.type == pygame.MOUSEBUTTONDOWN
              and event.button == 1):
            uccello_vely = -5
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            facile = 10
            print('[game] facile aumentata ' + str(facile))
        if event.type == pygame.QUIT: #se si esce
            pygame.quit() #arresta pygame
            sys.exit(0) #il sistema sopprime il processo
        if event.type == pygame.KEYDOWN  and event.key == pygame.K_p:
            pausa()
    #gestione tubi
    if tubi[-1].x < 150: tubi.append(tubi_class()) #se il l'ultimo tubo esce, si aggiunge ancora la clesse alla lista
    for t in tubi: #per ogni tubo in tubi
        t.collisione(uccello, uccellox, uccelloy) #con il metodo collisione controlla sel al tubo t è sovrapposto l'uccello
    #conteggio punti
    if not punti_su: #se punti_su è false
        for t in tubi: #per ogni tubo nella lista di tubi
            if t.punti_su(uccello, uccellox):  #controlla con il metodo punti_su che nulla sia sovrapposto al tubo
               punti_su = True #se il metodo punti_su ritorna True
               break #ferma
    if punti_su: 
        punti_su = False #la iposta su False come da default
        for t in tubi: #per ogni tubo nella lista
            if t.punti_su(uccello, uccellox):
                punti_su = True
                break
        if not punti_su:
            punti += 1 #quindi dopo tutto sto can can aumenta la variabile dei punti 
            print('[game] punto (' + str(punti) + ')') #stampa nella console di debugche si è ottenuto un punto e queanti ne si soono accumulat
    #collisione base
    if uccelloy > 380: #se la posizione vericale dell'uccello  è 380 (fine della finestra)
        hai_perso() #chiama hai perso
        print('[debug] collisione base') #stampa nella console di debug che c'è stata lac
    disegna_oggetti() #disegna gli oggetti sempre
    aggiorna() #aggiorna il display