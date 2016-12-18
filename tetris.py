
import pygame, sys
from pygame.locals import *
import math
import time

pygame.init()

DISP = (600,1000)
DISPLAYSURF = pygame.display.set_mode(DISP)
pygame.display.set_caption('planetris - tetris made on a plane')

WHITE = (255,255,255)
GREEN = (0, 255, 0)
LGREEN = (128, 128, 128)
BLACK = (0, 0, 0)

circx = 40
circy = 40

key_pressed = ''

Shapes = [{'square':[(0,0),(1,0),(1,1),(0,1)]},
          {'elllll':[(0,0),(1,0),(1,1),(1,2)]},
          {'square':[(0,0),(1,0),(2,0),(3,0)]},
          {'square':[(0,0),(0,1),(1,1),(2,1)]}]

CellsX = 12
CellsY = 24
Deathreshold = CellsY-1

class Tetris():
    def __init__(self,pygame):
        self.pygame = pygame
        self.falling_shape = []
        self.time_last = time.time()
        self.time_secs = 0.0
        self.translation = 0
        self.rotation = 0
        self.key_hold = False
        self.current_shape = []
        self.death_map = []
        self.kill_shape = False
        self.time_color = 0
        self.speed = 4.5
        
    def generate_grid(self):
        for y in range(CellsY):
            for x in range(CellsX):
                xint = (DISP[0]/(CellsX))
                yint = (DISP[1]/(CellsY))
                grid = ((xint*x+xint/2),(yint)*y+yint/2)
                self.pygame.draw.circle(DISPLAYSURF, BLACK, grid, 2)

    def set_pixel(self,xin,yin):
        for y in range(CellsY):
            for x in range(CellsX):
                xint = (DISP[0]/(CellsX))
                yint = (DISP[1]/(CellsY))
                grid = ((xint*x+xint/2),(yint)*y+yint/2)

                if xin == x and yin == y:
                    self.pygame.draw.circle(DISPLAYSURF, self.time_color, grid, 10)
        
    def generate_shape(self):
        # Don't judge my shitty random number generator, i'm on a plane
        time_now = int(str(time.time())[11:])
        shape = time_now%len(Shapes)
        #print Shapes[shape].values()

        self.falling_shape = Shapes[shape].values()[0]

    def read_time(self):
        time_now = time.time()
        time_diff = time_now-self.time_last
        self.time_secs = (time_diff % 60)*self.speed
        self.time_color = ((int(self.time_secs*60)%255), (int(self.time_secs*20)%255), (int(self.time_secs*100)%255))
        
    def render_shape(self):
        self.current_shape = []

        pivot_x = self.falling_shape[0][0]
        pivot_y = self.falling_shape[0][1]

        for point in self.falling_shape:
            point_x = point[0]
            point_y = point[1]

            # Rotation
            if self.rotation > 3:
                self.rotation = 0
                
            if self.rotation == 1:
                tmp = point_y
                point_y = point_x
                point_x = -tmp
            elif self.rotation == 2:
                tmp = point_y
                point_y = -point_y
                point_x = -point_x
            elif self.rotation == 3:
                tmp = point_y
                point_y = -point_x
                point_x = tmp
            else:
                pass

            if point_x+self.translation > CellsX-1:
                self.translation -= 1
            if point_x+self.translation < 0:
                self.translation += 1
            
                
            # Translation
            self.set_pixel(point_x+self.translation,point_y+int(self.time_secs))
            self.current_shape.append((point_x+self.translation,point_y+int(self.time_secs)))

    def potentially_kill_shape(self):
        for point in self.current_shape:
            x = point[0]
            y = point[1]

            if y == Deathreshold or ((x,y+1) in self.death_map):
                self.kill_shape = True
                break
            else:
                self.kill_shape = False

        if self.kill_shape:
            for point in self.current_shape:
                if point not in self.death_map:
                    self.death_map.append(point)
                print self.death_map
            self.falling_shape = []
            self.time_last = time.time()

    def render_deathmap(self):
        for point in self.death_map:
            self.set_pixel(point[0], point[1])

    def clean_deathmap(self):
        tmpdeath_map = self.death_map
        killstreak = 0
        for point in self.death_map:
            pointx = point[0]
            pointy = point[1]

            for x in range(CellsX):
                if (x,pointy) in self.death_map:
                    killstreak += 1
                else:
                    killstreak = 0

            print "killstreak: "+str(killstreak)+" cellsx: "+str(CellsX)
                    
            if killstreak >= CellsX:
                tmpdeath_map = []
                for point2 in self.death_map:
                    if point2[1] != pointy:
                        if point2[1] < pointy:
                            tmpdeath_map.append((point2[0],point2[1]+1))
                        else:
                            tmpdeath_map.append((point2[0],point2[1]))

        self.death_map = tmpdeath_map
                

    def modify_shape(self):
        if key_pressed == 'left' and not self.key_hold:
            self.translation -= 1
            self.key_hold = True
        if key_pressed == 'right' and not self.key_hold:
            self.translation += 1
            self.key_hold = True
        if key_pressed == 'up' and not self.key_hold:
            self.rotation += 1
            self.key_hold = True
        if key_pressed == 'down':
            self.speed = self.speed*1.007
        if key_pressed == '':
            self.speed = 4.5
            self.key_hold = False
            
    def main_game(self):
        if self.falling_shape == []:
            self.generate_shape()

        self.read_time()
        self.modify_shape()
        self.render_shape()
        self.potentially_kill_shape()
        self.render_deathmap()
        self.clean_deathmap()


if __name__ == '__main__':
    tet = Tetris(pygame)
    while True: # main game loop

        DISPLAYSURF.fill(BLACK)
        
        tet.main_game()
           
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_pressed = 'left'
                elif event.key == pygame.K_RIGHT:
                    key_pressed = 'right'
                elif event.key == pygame.K_UP:
                    key_pressed = 'up'
                elif event.key == pygame.K_DOWN:
                    key_pressed = 'down'
                else:
                    key_pressed = ''
            else:
                key_pressed = ''
                    
                    
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
