import random
import pygame


class Joueur():
    def __init__(self, equipe):
        self.typeSoldat = "soldat"
        self.insertMode = True
        self.money = 1600
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
        self.cost = 200
        self.health = 100
        self.max_health = 100
        self.attack = 20
        self.criticalAttack = 35
        self.criticalProb = 20
        if equipe == 1:
            self.image = pygame.image.load('soldat.png')
        if equipe == 2:
            self.image = pygame.image.load('soldat2.png')
        self.rect = self.image.get_rect()
        self.equipe = equipe

    def display_health(self, sizeBtwnX, sizeBtwY, surface):
        for i in range(int(self.health/5)):
            pygame.draw.line(surface, (255, 0, 0), (int((self.rect.x+0.85)*sizeBtwnX), int((self.rect.y+0.75)*sizeBtwnY-i)), (int((self.rect.x+0.95)*sizeBtwnX), int((self.rect.y+0.75)*sizeBtwnY-i)))

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

    def attaque(self, soldat):
        if soldat is not None:
            soldat.health -= self.attack
            if soldat.cost == 700:
                self.health -= int(soldat.attack/3)
            else:
                self.health -= soldat.attack
            if random.randrange(100) <= self.criticalProb:
                soldat.health -= self.criticalAttack
            if random.randrange(100) <= soldat.criticalProb:
                self.health -= soldat.criticalAttack
            return soldat


class Canon(Soldat):

    def __init__(self, equipe, range):
        super().__init__
        self.cost = 700
        self.health = 150
        self.max_health = 100
        self.attack = 80
        self.range = range
        self.criticalAttack = 20
        self.criticalProb = 20
        if equipe == 1:
            self.image = pygame.image.load('canon.png')
        if equipe == 2:
            self.image = pygame.image.load('canon.png')
        self.rect = self.image.get_rect()
        self.equipe = equipe

    def attaque(self, soldat):
        if soldat is not None:

            soldat.health -= self.attack
            if random.randrange(100) <= self.criticalProb:
                soldat.health -= self.criticalAttack
            return soldat


def hasWon():
    A = 0
    E = 0
    if len(soldats) == 0 or joueur.insertMode is True:
        return 0
    for soldat in soldats:
        if soldat.equipe == 1:
            A = 1
        else:
            E = 1
    if A != 0 and E != 0:
        return 0
    if A == 0 and E == 0:
        return 3
    elif A != 0:
        return 1
    return 2


def changeTeam(joueur, joueur1, joueur2):
    joueur.nbCoups = joueur.coupsMax
    if joueur.equipe == joueur1.equipe:
        joueur1 = joueur
        joueur = joueur2
    else:
        joueur2 = joueur
        joueur = joueur1
    return joueur


def attack(indexEnemi, isCanon):
    if joueur.nbCoups >= 3:
        print(indexEnemi)
        indexAmi = isSomeone((joueur.x, joueur.y))
        soldats[indexEnemi] = soldats[indexAmi].attaque(soldats[indexEnemi])
        if soldats[indexAmi].health <= 0 and soldats[indexEnemi].health <= 0:
            del soldats[indexAmi]
            if indexAmi < indexEnemi:
                indexEnemi -= 1
            print(indexEnemi)
            del soldats[indexEnemi]
            joueur.enterMode = False
        else:
            if soldats[indexAmi].health <= 0:
                joueur.enterMode = False
                del soldats[indexAmi]
            elif soldats[indexEnemi].health <= 0:
                if isCanon == False:
                    soldats[indexAmi].rect = soldats[indexEnemi].rect
                    joueur.x = soldats[indexEnemi].rect.x
                    joueur.y = soldats[indexEnemi].rect.y
                del soldats[indexEnemi]
        if isCanon == True:
            joueur.nbCoups -= 3
        joueur.nbCoups -= 3
    else:
        print("pas assez de coups pour attaquer")


def drawGrid(w, h, lines, rows, surface):
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwnX
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, h))
    for L in range(lines):
        y = y + sizeBtwnY
        pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    blit_alpha(surface, background, (0, 0), 128)
    drawGrid(width, height, lines, rows, surface)
    for i in range(len(soldats)):
        if soldats[i].cost == 700:
            surface.blit(soldats[i].image, ((soldats[i].rect.x)*sizeBtwnX, soldats[i].rect.y*sizeBtwnY, sizeBtwnX+30, sizeBtwnY))
            print(sizeBtwnX)
        else:
            if soldats[i].equipe == 1:
                surface.blit(soldats[i].image, ((soldats[i].rect.x)*sizeBtwnX, (soldats[i].rect.y+0.1)*sizeBtwnY, sizeBtwnY, sizeBtwnX))
            else:
                surface.blit(soldats[i].image, ((soldats[i].rect.x)*sizeBtwnX, (soldats[i].rect.y)*sizeBtwnY, sizeBtwnY, sizeBtwnX))
        soldats[i].display_health(sizeBtwnX, sizeBtwnY, surface)
    if joueur.insertMode is True:
        pygame.draw.ellipse(surface, (0, 255, 0), (joueur.x*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
    else:
        pygame.draw.ellipse(surface, (255, 0, 0), (joueur.x*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        numSoldat = isSomeone((joueur.x, joueur.y))
    if joueur.enterMode is True:
        if soldats[numSoldat].cost == 700:
            if isSomeone((joueur.x+3, joueur.y)) == "rien":
                possibilities[4] = numSoldat
                pygame.draw.ellipse(surface, (255, 0, 0), ((joueur.x+3)*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
            elif isSomeone((joueur.x+3, joueur.y)) == "mur":
                possibilities[4] = "mur"
            else:
                if isSomeone((joueur.x+3, joueur.y)) < 0:
                    possibilities[4] = isSomeone((joueur.x+3, joueur.y))
                else:
                    possibilities[4] = "allié"
            if isSomeone((joueur.x, joueur.y+3)) == "rien":
                possibilities[5] = numSoldat
                pygame.draw.ellipse(surface, (255, 0, 0), ((joueur.x)*sizeBtwnX, (joueur.y+3)*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
            elif isSomeone((joueur.x, joueur.y+3)) == "mur":
                possibilities[5] = "mur"
            else:
                if isSomeone((joueur.x, joueur.y+3)) < 0:
                    possibilities[5] = isSomeone((joueur.x, joueur.y+3))
                else:
                    possibilities[5] = "allié"
            if isSomeone((joueur.x-3, joueur.y)) == "rien":
                possibilities[6] = numSoldat
                pygame.draw.ellipse(surface, (255, 0, 0), ((joueur.x-3)*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
            elif isSomeone((joueur.x-3, joueur.y)) == "mur":
                possibilities[6] = "mur"
            else:
                if isSomeone((joueur.x-3, joueur.y)) < 0:
                    possibilities[6] = isSomeone((joueur.x-3, joueur.y))
                else:
                    possibilities[6] = "allié"
            if isSomeone((joueur.x, joueur.y-3)) == "rien":
                possibilities[7] = numSoldat
                pygame.draw.ellipse(surface, (255, 0, 0), ((joueur.x)*sizeBtwnX, (joueur.y-3)*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
            elif isSomeone((joueur.x, joueur.y-3)) == "mur":
                possibilities[7] = "mur"
            else:
                if isSomeone((joueur.x, joueur.y-3)) < 0:
                    possibilities[7] = isSomeone((joueur.x, joueur.y-3))
                else:
                    possibilities[7] = "allié"

        if isSomeone((joueur.x+1, joueur.y)) == "rien":
            possibilities[0] = numSoldat
            pygame.draw.ellipse(surface, (0, 255, 0), ((joueur.x+1)*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x+1, joueur.y)) == "mur":
            possibilities[0] = "mur"
        else:
            if isSomeone((joueur.x+1, joueur.y)) < 0:
                possibilities[0] = isSomeone((joueur.x+1, joueur.y))
            else:
                possibilities[0] = "allié"
        if isSomeone((joueur.x, joueur.y+1)) == "rien":
            possibilities[1] = numSoldat
            pygame.draw.ellipse(surface, (0, 255, 0), ((joueur.x)*sizeBtwnX, (joueur.y+1)*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x, joueur.y+1)) == "mur":
            possibilities[1] = "mur"
        else:
            if isSomeone((joueur.x, joueur.y+1)) < 0:
                possibilities[1] = isSomeone((joueur.x, joueur.y+1))
            else:
                possibilities[1] = "allié"
        if isSomeone((joueur.x-1, joueur.y)) == "rien":
            possibilities[2] = numSoldat
            pygame.draw.ellipse(surface, (0, 255, 0), ((joueur.x-1)*sizeBtwnX, joueur.y*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x-1, joueur.y)) == "mur":
            possibilities[2] = "mur"
        else:
            if isSomeone((joueur.x-1, joueur.y)) < 0:
                possibilities[2] = isSomeone((joueur.x-1, joueur.y))
            else:
                possibilities[2] = "allié"
        if isSomeone((joueur.x, joueur.y-1)) == "rien":
            possibilities[3] = numSoldat
            pygame.draw.ellipse(surface, (0, 255, 0), ((joueur.x)*sizeBtwnX, (joueur.y-1)*sizeBtwnY, sizeBtwnX, sizeBtwnY), 2)
        elif isSomeone((joueur.x, joueur.y-1)) == "mur":
            possibilities[3] = "mur"
        else:
            if isSomeone((joueur.x, joueur.y-1)) < 0:
                possibilities[3] = isSomeone((joueur.x, joueur.y-1))
            else:
                possibilities[3] = "allié"
    font = pygame.font.SysFont("comicsansms", 30)
    txt = "Equipe : " + str(joueur.equipe)
    txt2 = "nombre de coups restant : " + str(joueur.nbCoups)
    if joueur.insertMode is True:
        txt2 = "Placez vos soldats : " + str(joueur.money) + "$"
    text = font.render(txt, True, (0, 0, 0))
    text2 = font.render(txt2, True, (0, 0, 0))
    if joueur.typeSoldat == "soldat":
        txt3 = "soldat: 200$"
    else:
        txt3 = "canon: 700$"
    text3 = font.render(txt3, True, (0, 0, 0))
    surface.blit(text, (700, 500))
    surface.blit(text2, (700, 550))
    if joueur.insertMode is True:
        surface.blit(text3, (700, 600))
    pygame.display.update()


def isSomeone(pos):
    i = 0
    if pos[0] < 0 or pos[0] >= rows or pos[1] < 0 or pos[1] >= lines:
        return "mur"
    for soldat in soldats:
        if soldat.rect.x == pos[0] and soldat.rect.y == pos[1]:
            if soldat.equipe != joueur.equipe:
                return -i-1
            return i
        i = i+1
    return "rien"


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def main():
    pygame.init()
    global width, height, rows, s, snack, background, lines, soldats, sizeBtwnX, sizeBtwnY, joueur, possibilities, joueur1, joueur2
    width = 1200
    height = 660
    soldats = []
    rows = 40
    lines = 15
    sizeBtwnX = width // rows
    possibilities = []
    for i in range(8):
        possibilities.append(False)
    sizeBtwnY = height // lines
    win = pygame.display.set_mode((width, height))
    background = pygame.image.load('background.jpg')
    running = True
    joueur1 = Joueur(1)
    joueur2 = Joueur(2)
    joueur2.x = rows-1
    joueur2.y = 0
    pressed = {}
    clock = pygame.time.Clock()
    joueur = joueur1
    while running:
        gagnant = hasWon()
        switcher = {
            0: "pas de gagnant",
            1: "équipe 1",
            2: "équipe 2",
            3: "execo",
        }
        if switcher.get(gagnant) == "équipe 1":
            win.blit(pygame.image.load('changeTeam.png'), (0, 0))
            pygame.display.update()
            pygame.time.wait(2000)
        elif switcher.get(gagnant) == "équipe 2":
            win.blit(pygame.image.load('changeTeam.png'), (0, 0))
            pygame.display.update()
            pygame.time.wait(2000)
        elif switcher.get(gagnant) == "execo":
            win.blit(pygame.image.load('changeTeam.png'), (0, 0))
            pygame.display.update()
            pygame.time.wait(2000)
        elif switcher.get(gagnant) == "pas de gagnant":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    pressed[event.key] = False
            if joueur.nbCoups <= 0:
                joueur.enterMode = False
                joueur = changeTeam(joueur, joueur1, joueur2)
                win.blit(pygame.image.load('changeTeam.png'), (0, 0))
                pygame.display.update()
                pygame.time.wait(2000)
            if joueur.enterMode is True:
                if pressed.get(pygame.K_RIGHT):
                    if possibilities[4] is not False and possibilities[4] < 0:
                        attack(-possibilities[4]-1, True)
                    elif possibilities[0] == "mur":
                        print('mur')
                    elif possibilities[0] == "allié":
                        print("salut ami!")
                    elif possibilities[0] >= 0:
                        soldats[possibilities[0]].move_right()
                        joueur.move_right()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[0] < 0:
                            attack(-possibilities[0]-1, False)

                elif pressed.get(pygame.K_DOWN):
                    if possibilities[5] is not False and possibilities[5] < 0:
                        attack(-possibilities[5]-1, True)
                    elif possibilities[1] == "mur":
                        print('mur')
                    elif possibilities[1] == "allié":
                        print("salut ami!")
                    elif possibilities[1] >= 0:
                        soldats[possibilities[1]].move_down()
                        joueur.move_down()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[1] < 0:
                        attack(-possibilities[1]-1, False)

                elif pressed.get(pygame.K_LEFT):
                    if possibilities[6] is not False and possibilities[6] < 0:
                        attack(-possibilities[6]-1, True)
                    elif possibilities[2] == "mur":
                        print('mur')
                    elif possibilities[2] == "allié":
                        print("salut ami!")
                    elif possibilities[2] >= 0:
                        soldats[possibilities[2]].move_left()
                        joueur.move_left()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[2] < 0:
                        attack(-possibilities[2]-1, False)

                elif pressed.get(pygame.K_UP):
                    if possibilities[7] is not False and possibilities[7] < 0:
                        attack(-possibilities[7]-1, True)
                    elif possibilities[3] == "mur":
                        print('mur')
                    elif possibilities[3] == "allié":
                        print("salut ami!")
                    elif possibilities[3] >= 0:
                        soldats[possibilities[3]].move_up()
                        joueur.move_up()
                        joueur.nbCoups = joueur.nbCoups - 1
                    elif possibilities[3] < 0:
                        attack(-possibilities[3]-1, False)

                elif pressed.get(pygame.K_RETURN):
                    joueur.enterMode = False
                    redrawWindow(win)
                    pygame.time.wait(200)

            else:
                if pressed.get(pygame.K_SPACE):
                    if joueur.typeSoldat == "soldat":
                        joueur.typeSoldat = "canon"
                    else:
                        joueur.typeSoldat = "soldat"
                elif pressed.get(pygame.K_RIGHT) and pressed.get(pygame.K_UP):
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
                    if joueur.insertMode is True:
                        if isSomeone((joueur.x, joueur.y)) == "rien":
                            if joueur.typeSoldat == "soldat":
                                soldats.append(Soldat(joueur.equipe))
                                soldats[len(soldats)-1].rect.x = joueur.x
                                soldats[len(soldats)-1].rect.y = joueur.y
                                if joueur.equipe == 1:
                                    soldats[len(soldats)-1].image = pygame.transform.scale(soldats[len(soldats)-1].image, (int(width/rows/1.35), int(height/lines/1.25)))
                                else:
                                    soldats[len(soldats)-1].image = pygame.transform.scale(soldats[len(soldats)-1].image, (int(width/rows/1.25), int(height/lines)))
                            elif joueur.money>=700:
                                soldats.append(Canon(joueur.equipe, 3))
                                soldats[len(soldats)-1].rect.x = joueur.x
                                soldats[len(soldats)-1].rect.y = joueur.y
                                if joueur.equipe == 1:
                                    soldats[len(soldats)-1].image = pygame.transform.scale(soldats[len(soldats)-1].image, (int(width/rows/1.1), int(height/lines/1.20)))
                                else:
                                    soldats[len(soldats)-1].image = pygame.transform.scale(soldats[len(soldats)-1].image, (int(width/rows/1.1), int(height/lines/1.20)))
                            if joueur.typeSoldat == "soldat" or joueur.money>=700:
                                joueur.money -= soldats[len(soldats)-1].cost
                                if joueur == joueur1:
                                    if (joueur1.money>=200 and joueur2.money<200) is False:
                                        joueur = changeTeam(joueur, joueur1, joueur2)
                                elif joueur == joueur2:
                                    if (joueur2.money>=200 and joueur1.money<200) is False:
                                        joueur = changeTeam(joueur, joueur1, joueur2)
                                pygame.time.wait(200)
                        else:
                            print("Vous devez placer vos soldats sur des cases vides")

                    else:
                        Someone = isSomeone((joueur.x, joueur.y))
                        if type(Someone) == int:
                            if Someone >= 0:
                                joueur.enterMode = True
                                pygame.time.wait(200)

            clock.tick(10)
            redrawWindow(win)
            if joueur.insertMode is True:
                if joueur.money < 200:
                    joueur.insertMode = False
                    changeTeam(joueur, joueur1, joueur2)

    pass


main()
