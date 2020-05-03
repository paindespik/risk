import math
import random
import pygame


class Joueur():
    def __init__(self, equipe):
        self.x = 0
        self.y = 0
        self.enterMode = False
        self.equipe = equipe
        self.nbCoups = 15
        self.coupsMax = 15

    def move_right(self):
        if self.x != rows-1:
            self.x = self.x + 1

    def move_left(self):
        if self.x != 0:
            self.x = self.x - 1

    def move_up(self):
        if self.y != 0:
            self.y = self.y - 1

    def move_down(self):
        if self.y != lines-1:
            self.y = self.y + 1


class Soldat(pygame.sprite.Sprite):

    def __init__(self, equipe):
        super().__init__
        self.health = 100
        self.max_health = 100
        self.attack = 10
        if equipe == 1:
            self.image = pygame.image.load('soldier.jpg')
        if equipe == 2:
            self.image = pygame.image.load('soldatEnemi.png')
        self.rect = self.image.get_rect()
        self.equipe = equipe

    def move_right(self):
        if self.rect.x != rows-1:
            self.rect.x = self.rect.x + 1

    def move_left(self):
        if self.rect.x != 0:
            self.rect.x = self.rect.x - 1

    def move_up(self):
        if self.rect.y != 0:
            self.rect.y = self.rect.y - 1

    def move_down(self):
        if self.rect.y != lines-1:
            self.rect.y = self.rect.y + 1

    def attack(self, soldat):
        if soldat != None:
            soldat.healt


def changeTeam(joueur, joueur1, joueur2):
    joueur.nbCoups = joueur.coupsMax
    if joueur.equipe == joueur1.equipe:
        joueur1 = joueur
        joueur = joueur2
    else:
        joueur2 = joueur
        joueur = joueur1
    return joueur



def drawGrid(w, h, lines, rows, surface):
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwnX
        pygame.draw.line(surface, (0,0,0), (x,0),(x,h))
    for L in range(lines):
        y = y + sizeBtwnY
        pygame.draw.line(surface, (0,0,0), (0,y), (w,y))

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    surface.blit(background, (0,0))
    drawGrid(width, height, lines, rows, surface)
    for i in range(len(soldats)):
        surface.blit(soldats[i].image, (soldats[i].rect.x*sizeBtwnX, soldats[i].rect.y*sizeBtwnY, sizeBtwnX, sizeBtwnY))
    pygame.draw.ellipse(surface, (255,0,0), (joueur.x*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
    numSoldat = isSomeone((joueur.x, joueur.y))
    if joueur.enterMode is True:
        if isSomeone((joueur.x+1, joueur.y)) == "rien":
            possibilities[0] = numSoldat
            pygame.draw.ellipse(surface, (0,255,0), ((joueur.x+1)*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x+1, joueur.y))=="mur":
            possibilities[0] = "mur"
        else:
            if isSomeone((joueur.x+1, joueur.y))<0:
                possibilities[0] = isSomeone((joueur.x+1, joueur.y))
            else:
                possibilities[0] = "allié"
        if isSomeone((joueur.x, joueur.y+1)) == "rien":
            possibilities[1] = numSoldat
            pygame.draw.ellipse(surface, (0,255,0), ((joueur.x)*sizeBtwnX, (joueur.y+1)*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x, joueur.y+1)) == "mur":
            possibilities[1] = "mur"
        else:
            if isSomeone((joueur.x, joueur.y+1))<0:
                possibilities[1] = isSomeone((joueur.x, joueur.y+1))
            else:
                possibilities[1] = "allié"
        if isSomeone((joueur.x-1, joueur.y)) == "rien":
            possibilities[2] = numSoldat
            pygame.draw.ellipse(surface, (0,255,0), ((joueur.x-1)*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x-1, joueur.y)) == "mur":
            possibilities[2] = "mur"
        else:
            if isSomeone((joueur.x-1, joueur.y))<0:
                possibilities[2] = isSomeone((joueur.x-1, joueur.y))
            else:
                possibilities[2] = "allié"
        if isSomeone((joueur.x, joueur.y-1)) =="rien":
            possibilities[3] = numSoldat
            pygame.draw.ellipse(surface, (0,255,0), ((joueur.x)*sizeBtwnX, (joueur.y-1)*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x, joueur.y-1))=="mur":
            possibilities[3] = "mur"
        else:
            if isSomeone((joueur.x, joueur.y-1))<0:
                possibilities[3] = isSomeone((joueur.x, joueur.y-1))
            else:
                possibilities[3] = "allié"
    font = pygame.font.SysFont("comicsansms", 30)
    txt = "Equipe : " + str(joueur.equipe)
    txt2 = "nombre de coups restant : " + str(joueur.nbCoups)
    text = font.render(txt, True, (0, 0, 0))
    text2 = font.render(txt2, True,(0, 0, 0))
    surface.blit(text, (900, 550))
    surface.blit(text2, (900, 600))
    pygame.display.update()


def isSomeone(pos):
    i=0
    if pos[0]<0 or pos[0]>=rows or pos[1]<0 or pos[1]>=lines:
        return "mur"
    for soldat in soldats:
        if soldat.rect.x == pos[0] and soldat.rect.y == pos[1]:
            if soldat.equipe != joueur.equipe:
                return -i-1
            return i
        i=i+1
    return "rien"


def main():
    pygame.init()
    global width, height, rows, s, snack, background, lines, soldats, sizeBtwnX, sizeBtwnY, joueur, possibilities, joueur1, joueur2
    width = 1200
    height = 660
    soldats = []
    rows = 40
    lines = 20
    sizeBtwnX = width // rows
    possibilities = []
    for i in range(4):
        possibilities.append(False)
    sizeBtwnY = height // lines
    win = pygame.display.set_mode((width, height))
    background = pygame.image.load('background.jpg')
    running = True
    joueur1 = Joueur(1)
    joueur2 = Joueur(2)
    pressed = {}
    for i in range(lines):
        soldats.append(Soldat(1))
        soldats[i].rect.y = i
        soldats[i].rect.x = i
        soldats[i].image = pygame.transform.scale(soldats[i].image, (int(width/rows), int(height/lines)))


    for i in range(lines):
        soldats.append(Soldat(2))
        soldats[len(soldats)-1].rect.x = rows-2
        soldats[len(soldats)-1].rect.y = i
        soldats[len(soldats)-1].image = pygame.transform.scale(soldats[len(soldats)-1].image, (int(width/rows), int(height/lines)))
    clock = pygame.time.Clock()
    joueur = joueur1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                pressed[event.key] = True
            elif event.type == pygame.KEYUP:
                pressed[event.key] = False

        if joueur.enterMode is True:
            if joueur.nbCoups <= 0:
                joueur.enterMode = False
                joueur = changeTeam(joueur, joueur1, joueur2)
                win.blit(pygame.image.load('changeTeam.png'), (0,0))
                pygame.display.update()
                pygame.time.wait(2000)
            else:
                if pressed.get(pygame.K_RIGHT):
                    if possibilities[0] == "mur":
                        print('mur')
                    elif possibilities[0] == "allié":
                        print("salut ami!")
                    elif possibilities[0] >= 0:
                        soldats[possibilities[0]].move_right()
                        joueur.move_right()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[0] < 0:
                        print("attack")

                elif pressed.get(pygame.K_DOWN):
                    if possibilities[1] == "mur":
                        print('mur')
                    elif possibilities[1] == "allié":
                        print("salut ami!")
                    elif possibilities[1] >= 0:
                        soldats[possibilities[1]].move_down()
                        joueur.move_down()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[1] < 0:
                        print("attack")

                elif pressed.get(pygame.K_LEFT):
                    if possibilities[2] == "mur":
                        print('mur')
                    elif possibilities[2] == "allié":
                        print("salut ami!")
                    elif possibilities[2] >= 0:
                        soldats[possibilities[2]].move_left()
                        joueur.move_left()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[2] < 0:
                        print("attack")

                elif pressed.get(pygame.K_UP):
                    if possibilities[3] == "mur":
                        print('mur')
                    elif possibilities[3] == "allié":
                        print("salut ami!")
                    elif possibilities[3] >= 0:
                        soldats[possibilities[3]].move_up()
                        joueur.move_up()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[3] < 0:
                        print("attack")

                elif pressed.get(pygame.K_RETURN):
                    joueur.enterMode = False
                    redrawWindow(win)
                    pygame.time.wait(200)

        else:
            if pressed.get(pygame.K_RIGHT) and pressed.get(pygame.K_UP):
                if joueur.x != rows-1 and joueur.y != 0:
                    joueur.move_up()
                    joueur.move_right()
                elif joueur.x != rows-1:
                    joueur.move_right()
                elif joueur.y != 0:
                    joueur.move_up()
            elif pressed.get(pygame.K_RIGHT) and pressed.get(pygame.K_DOWN):
                if joueur.x != rows-1 and joueur.y != lines-1:
                    joueur.move_down()
                    joueur.move_right()
                elif joueur.x != rows-1:
                    joueur.move_right()
                elif joueur.y != lines-1:
                    joueur.move_down()
            elif pressed.get(pygame.K_LEFT) and pressed.get(pygame.K_DOWN):
                if joueur.x != 0 and joueur.y != lines-1:
                    joueur.move_down()
                    joueur.move_left()
                elif joueur.x != 0:
                    joueur.move_left()
                elif joueur.y != lines-1:
                    joueur.move_down()
            elif pressed.get(pygame.K_LEFT) and pressed.get(pygame.K_UP):
                if joueur.x != 0 and joueur.y != 0:
                    joueur.move_up()
                    joueur.move_left()
                elif joueur.x != 0:
                    joueur.move_left()
                elif joueur.y != 0:
                    joueur.move_up()
            elif pressed.get(pygame.K_RIGHT):
                if joueur.x != rows-1:
                    joueur.move_right()
            elif pressed.get(pygame.K_LEFT):
                if joueur.x != 0:
                    joueur.move_left()
            elif pressed.get(pygame.K_UP):
                if joueur.y != 0:
                    joueur.move_up()
            elif pressed.get(pygame.K_DOWN):
                if joueur.y != lines-1:
                    joueur.move_down()
            elif pressed.get(pygame.K_RETURN):
                Someone = isSomeone((joueur.x, joueur.y))
                if type(Someone) == int:
                    if Someone >=0 :
                        joueur.enterMode = True
                        pygame.time.wait(200)

        clock.tick(10)
        redrawWindow(win)

    pass


main()