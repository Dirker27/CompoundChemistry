import pygame
from pygame.sprite import Sprite
from vec2d import vec2d

# Sprite
class Blob(Sprite):
    
    def __init__(self,screen,image_file,init_position):
        Sprite.__init__(self)
        self.screen=screen
        self.image = pygame.image.load(image_file)
        self.pos=vec2d(init_position)
        
    def update(self):
        self.pos += vec2d(0,0)
        self.image_w,self.image_h = self.image.get_size()
        bounds_rect = self.screen.get_rect().inflate(-self.image_w,-self.image_h)

        if self.pos.x < bounds_rect.left:
            self.pos.x = bounds_rect.left
        elif self.pos.x > bounds_rect.right:
            self.pos.x = bounds_rect.right
        if self.pos.y < bounds_rect.top:
            self.pos.y = bounds_rect.top
        elif self.pos.y > bounds_rect.bottom:
            self.pos.y = bounds_rect.bottom

    def blitme(self):
        draw_pos = self.image.get_rect().move(self.pos.x-(self.image_w/2),
                                              self.pos.y-(self.image_h/2))
        self.screen.blit(self.image,draw_pos)

    _counter = 0
