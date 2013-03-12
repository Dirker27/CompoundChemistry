import os,sys
from random import choice,randint
from math import sin,cos,radians
import pygame
from pygame.sprite import Sprite
from vec2d import vec2d

#sprite == graphics object
class Blob_2(Sprite):
    def __init__(self,screen,image_file,init_position,init_direction,speed):
        Sprite.__init__(self)
        self.screen=screen
        self.speed=speed
        self.base_image=pygame.image.load(image_file)
        self.image=self.base_image
        self.position=init_position
        self.pos=vec2d(init_position)
        self.direction=vec2d(init_direction).normalized()

    def update(self,time_passed):
        self._change_direction(time_passed)
        #self.image=pygame.transform.rotate(self.base_image,-self.direction.angle)
        #rotation goes counter clockwise
        displacement=vec2d(self.direction.x * self.speed * time_passed,
                           self.direction.y * self.speed * time_passed)
        self.pos+=displacement
        self.image_w,self.image_h,=self.image.get_size()
        bounds_rect=self.screen.get_rect().inflate(-self.image_w,-self.image_h)

        if self.pos.x < bounds_rect.left:
            self.pos.x=bounds_rect.left
            self.direction.x *= -1
        elif self.pos.x > bounds_rect.right:
            self.pos.x=bounds_rect.right
            self.direction.x *= -1
        if self.pos.y < bounds_rect.top:
            self.pos.y=bounds_rect.top
            self.direction.y *= -1
        elif self.pos.y > bounds_rect.bottom:
            self.pos.y=bounds_rect.bottom
            self.direction.y *= -1

    def blitme(self):
        draw_pos=self.image.get_rect().move(self.pos.x-(self.image_w/2),self.pos.y-(self.image_h/2))
        self.screen.blit(self.image,draw_pos)

    _counter=0

    def _change_direction(self,time_passed):
        self._counter += time_passed
        if self._counter > randint(400,500):
            self.direction.rotate(45*randint(-1,1))
            self._counter=0

def exit_game():
    sys.exit()

'''def run_game():
    #Game Parameters
    SCREEN_WIDTH,SCREEN_HEIGHT=400,400
    BG_Color=150,150,80
    blob_files=['red_dot.jpg','blue_dot.jpg']
    num_blobs=10
    pygame.init()
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
    clock=pygame.time.Clock()
    #create blobs
    blobs=[]
    for i in range(num_blobs):
        blobs.append(Blob(screen,choice(blob_files),
                          (randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT)),
                          (choice([-1,1]),choice([-1,1])),0.1))
                    
    #main loop
    while True:
        time_passed = clock.tick(50)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
               exit_game()

        screen.fill(BG_Color)

        for blob in blobs:
            blob.update(time_passed)
            blob.blitme()

        pygame.display.flip()


run_game()'''
