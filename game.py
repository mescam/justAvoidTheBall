#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import random

import pygame

class GameOver(object):
    game = None
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font('assets/fonts/Pacifico.ttf', 36)

    def draw(self):
        msg1 = "Game Over"
        msg2 = "Your score: %d" % GameOver.game.score

        m1Surface = self.font.render(msg1, True, pygame.Color(102, 102, 102))
        m2Surface = self.font.render(msg2, True, pygame.Color(102, 102, 102))

        m1Rect = m1Surface.get_rect()
        m2Rect = m2Surface.get_rect()

        m1Rect.centerx = 400
        m2Rect.centerx = 400
        m1Rect.centery = 250
        m2Rect.centery = 350

        window.blit(m1Surface, m1Rect)
        window.blit(m2Surface, m2Rect)

    def reset(self):
        pass

    def handleEvents(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return 0  # change state to Menu
        return 2

class Ball(object):
    rect = pygame.Rect((0, 0), (800, 600))
    def __init__(self, window):
        self.window = window
        r = random.randint(0, 3)
        if r == 0:
            self.pos = [20, 20]
        elif r == 1:
            self.pos = [780, 20]
        elif r == 2:
            self.pos = [20, 580]
        else:
            self.pos = [780, 580]
        self.obj = pygame.draw.circle(self.window, pygame.Color(255, 0 ,0), self.pos, 20)
        self.direction = [random.randint(3, 5), random.randint(3, 5)]

    def move(self):
        nposx = self.pos[0] + self.direction[0]
        nposy = self.pos[1] + self.direction[1]
        if nposx < 0 or nposx > 780:
            self.direction[0] = -self.direction[0]
            nposx = self.pos[0] + self.direction[0]
        if nposy > 580 or nposy < 0:
            self.direction[1] = -self.direction[1]
            nposy = self.pos[1] + self.direction[1]
        return [nposx, nposy]

    def draw(self):
        self.pos = self.move()
        self.obj = pygame.draw.circle(self.window, pygame.Color(255, 0 ,0), self.pos, 20)

class Game(object):

    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font('assets/fonts/Pacifico.ttf', 16)
        self.screen_rect = pygame.Rect((0,0), (800, 600))

    def reset(self):
        self.balls = list([Ball(window) for x in xrange(1, 10)])
        self.start_time = int(time.time())
        self.player = pygame.Rect((0, 0), (20, 20))
        self.player.centerx = 400
        self.player.centery = 300
        self.playerstate = [0, 0, 0, 0]  # left top bottom right
        self.in_game = 1
        self.score = 0
        self.counter = 0

    def playerCollide(self):
        index = -1
        while True:
            index = self.player.collidelist([x.obj for x in self.balls])
            if index < 0:
                break
            self.in_game = 0
            break

    def draw(self):
        if not self.in_game:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN,
                                                 {"key":pygame.K_SPACE,
                                                  "mod":0,
                                                  "unicode":u' '}))

        np = self.player.move(self.playerstate[0]*-5 + self.playerstate[3]*5,
                              self.playerstate[1]*-5 + self.playerstate[2]*5)
        if self.screen_rect.contains(np):
            self.player = np
        # draw player pos
        pygame.draw.rect(self.window, pygame.Color(0, 0, 255), self.player)

        # draw balls
        for b in self.balls:
            b.draw()
        self.playerCollide()

        # draw score
        self.score = int(time.time()) - self.start_time
        score = "Score: %d" % self.score
        scoreSurface = self.font.render(score, True, pygame.Color(102, 102, 102))
        scoreRect = scoreSurface.get_rect()
        scoreRect.right = 790
        scoreRect.bottom = 590
        window.blit(scoreSurface, scoreRect)

        if self.counter == 60*5:
            self.balls.append(Ball(window))
            self.counter = 0
        else:
            self.counter += 1


    def handleEvents(self, event):
        if self.in_game == 0:
            return 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.playerstate[1] = 1
            elif event.key == pygame.K_DOWN:
                self.playerstate[2] = 1
            elif event.key == pygame.K_LEFT:
                self.playerstate[0] = 1
            elif event.key == pygame.K_RIGHT:
                self.playerstate[3] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.playerstate[1] = 0
            elif event.key == pygame.K_DOWN:
                self.playerstate[2] = 0
            elif event.key == pygame.K_LEFT:
                self.playerstate[0] = 0
            elif event.key == pygame.K_RIGHT:
                self.playerstate[3] = 0
        return 1


class Menu(object):

    def __init__(self, window):
        self.window = window
        self.fontTitle = pygame.font.Font('assets/fonts/Pacifico.ttf', 48)
        self.grayColor = pygame.Color(102, 102, 102)
        self.fontPress = pygame.font.Font('assets/fonts/Pacifico.ttf', 32)
        self.fontBottom = pygame.font.Font('assets/fonts/Pacifico.ttf', 16)

    def reset(self):
        pass

    def draw(self):
        # game title
        msg = "Just Avoid The Ball"
        msgSurface = self.fontTitle.render(msg, True, self.grayColor)
        msgRect = msgSurface.get_rect()
        msgRect.centerx = 400
        msgRect.top = 40
        window.blit(msgSurface, msgRect)

        # press enter...
        msg2 = "Press ENTER to play"
        msg2Surface = self.fontPress.render(msg2, True, self.grayColor)
        msg2Rect = msg2Surface.get_rect()
        msg2Rect.centerx = 400
        msg2Rect.centery = 300
        window.blit(msg2Surface, msg2Rect)

        # bottom line
        btm = "Use arrows to move - 0hgame.eu 2013 - http://mescam.github.io/justAvoidTheBall/"
        btmSurface = self.fontBottom.render(btm, True, self.grayColor)
        btmRect = btmSurface.get_rect()
        btmRect.centerx = 400
        btmRect.bottom = 570
        window.blit(btmSurface, btmRect)

    def handleEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 1
        return 0

pygame.init();
fpsClock = pygame.time.Clock()

# window modes
window = pygame.display.set_mode((800,600));
pygame.display.set_caption('Just Avoid The Ball')

# colors
white = pygame.Color(255, 255, 255)

availableStates = (Menu(window), Game(window), GameOver(window))
state = 0

GameOver.game = availableStates[1]  # simple hack

while True:
    window.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            nstate = availableStates[state].handleEvents(event)
            if nstate != state:
                state = nstate
                availableStates[state].reset()

    availableStates[state].draw()
    pygame.display.update()
    fpsClock.tick(60)

