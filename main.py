import numpy as np # este o biblioteca care adauga diferite functionalitati, in special pt. siruri si matrici
import random
import pygame # un modul cu diferite biblioteci pentru scrierea jocurilor video
import sys # un modul cu diferite variabile si functii pt. manipularea diferitelor parti a PRE (Python Runtime Environment)
from pygame.locals import *
from constants import CP

N = 4
grid = np.zeros((N, N), dtype=int) # declaram matricea de 4 linii si 4 coloane si o initializam cu 0 pe toate pozitiile, declarand valorile de tip int
W = 400 # latime
H = W # inaltime
SPACING = 10

pygame.init() # initializarea tuturor modulelor pygame importante
pygame.display.set_caption("2048") # titlul de fereastra a display-ului
pygame.font.init() # initializare font a joculuri, pt. a putea sa vedem (cifrele din patratele, scorul, etc...)

myfont = pygame.font.SysFont("Calibri", 30) # nume font si marimea caracterelor
screen = pygame.display.set_mode((W, H))  # rezolutia jocului

def new_number(k=1): # Marian, k = 1 pt. ca sa se afiseze un singur numar la fiecare mutare
    free_poss = list(zip(*np.where(grid == 0))) # np.where returneaza pozitiile elementelor, zip grupeaza linia cu coloana, list este un constructor care returneaza o lista
    for pos in random.sample(free_poss, k=k): # random.sample(lista, n) returneaza n elemente random din lista ta
        # random.random() returneaza un numar intre [0.0, 1.0]
        if random.random() < .1:
            grid[pos] = 4
        else:
            grid[pos] = 2

def _get_nums(this): # Sergiu
    this_n = this[this != 0]
    this_n_sum = []
    skip = False
    
    for j in range(len(this_n)):
        if skip:
            skip = False
            continue
        if j != len(this_n) - 1 and this_n[j] == this_n[j + 1]:  # verificam vecinii
            new_n = this_n[j] * 2
            skip = True
        else:
            new_n = this_n[j]
        this_n_sum.append(new_n)
        
    return np.array(this_n_sum)  # returnam noua lista in numpy

def make_move(move): # Sergiu
    for i in range(N):
        if move in "lr": # stanga/dreapta
            this = grid[i, :] # lucram pe linii
        else: # sus/jos
            this = grid[:, i] # lucram pe coloane
            
        flipped = False
        
        if move in "rd": # dreapta/jos => o intoarcem pt. a avea acelasi algoritm cu stanga/sus
            flipped = True
            this = this[::-1]
            
        this_n = _get_nums(this)
        new_this = np.zeros_like(this) # initializam lista cu valori de 0 de dimensiunea listei primite
        new_this[:len(this_n)] = this_n
        
        if flipped:
            new_this = new_this[::-1]  # o intoarcem din nou ca sa fie ca la inceput
        if move in "lr":
            grid[i, :] = new_this # salvam pe linii
        else:
            grid[:, i] = new_this # salvam pe coloane

def draw_game(): # Marian
    screen.fill(CP["background"])  # culorile din background
    
    for i in range(N):
        for j in range(N):
            n = grid[i][j]
            
            rect_x = j * W // N + SPACING
            rect_y = i * H // N + SPACING
            rect_w = W // N - 2 * SPACING
            rect_h = H // N - 2 * SPACING
            
            # cu Rect manipulam ce este in interiorul formelor pe care le desenam
            pygame.draw.rect(screen,
                             CP[n],
                             pygame.Rect(rect_x, rect_y, rect_w, rect_h), # left, top, width, height 
                             border_radius=8)
            
            if n == 0:
                continue
            text_surface = myfont.render(str(n), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
            screen.blit(text_surface, text_rect) # blit = desenam

def wait_for_key(): # Marian
    while True:
        for event in pygame.event.get():  # verifica toate evenimentele din pygame
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:  # cand o tasta este apasata
                if event.key == K_UP:
                    return "u"
                elif event.key == K_RIGHT:
                    return "r"
                elif event.key == K_LEFT:
                    return "l"
                elif event.key == K_DOWN:
                    return "d"
                elif event.key == K_q or event.key == K_ESCAPE:  # o oprire fortata cu tasta q (de exemplu)
                    end()

def game_over(): # David
    global grid
    grid_bu = grid.copy()
    for move in 'lrud':
        make_move(move)
        # daca dupa prima mutare, matricea se schimba, nu mai trebuie sa le verificam si restul posibilelor mutari
        if not all((grid == grid_bu).flatten()):  # flatten = matricea devine linie pt. a face compararile mai usor
            grid = grid_bu
            return False
    return True

def game_over_text(): # David
    screen.fill(CP["menu"])
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # daca apas pe X (Close) o sa inchida jocul
                end() 
        text = myfont.render("Ai pierdut!", True, CP["textfinish"])
        textpos = text.get_rect() # pt. ca suprafetele nu au o pozitie, trebuie stocate in blit
        textpos.center = (W // 2, H // 2)
        screen.blit(text, textpos)
        pygame.display.update()

def end(): # David
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def play(): # David
    new_number(k=2) # initializam 2 valori
    while True:
        draw_game()
        pygame.display.flip() # updateaza continutul intregului display (altfel este blackscreen)
        cmd = wait_for_key()
        old_grid = grid.copy()
        make_move(cmd)
        # print(grid) # daca dorim sa observam mutarea tablei in consola
        if game_over():
            game_over_text()
        if not all((grid == old_grid).flatten()): # daca mai putem misca matricea in oricare dintre cele 4 directii
            new_number() # atunci la fiecare miscare, se genereaza un numar, 2 sau 4, pe o pozitie random

play()
