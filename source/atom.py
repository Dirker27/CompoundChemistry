import pygame
from pygame.sprite import Sprite
from vec2d import vec2d

# ATOMS
class Atom(Sprite):
    
    def __init__(self, screen, image_file, init_position, atomtype, atomabbrev, atomnum):
        #SPRITE TRAITS
        Sprite.__init__(self)
        self.screen=screen
        self.image = pygame.image.load(image_file)
        self.pos = vec2d(init_position)
        #ATOM TRAITS
        self.atomtype = atomtype  #string of the atom's name
        self.atomabbrev = atomabbrev #string of the atoms abbreviation. used for molecule string results
        self.atomnum = atomnum
        self.left = None
               
    def __eq__(self,other):
        if self.atomabbrev == (str)(other):
            return True
        elif self.atomabbrev != (str)(other):
            return False

    def __lt__(self, other):
        return (self.atomnum < other.atomnum)

    def __cmp__(self,other):
        return this.atomnum > other.atomnum

    def update(self):
        self.pos += vec2d(0,0)
        self.image_w,self.image_h = self.image.get_size()

        bounds_rect = self.screen.get_rect().inflate(-self.image_w,-self.image_h)

        if(self.left):
            border_left = bounds_rect.left
            border_right = ((bounds_rect.left + bounds_rect.right)/2) - (self.image_w/2)
        else:
            border_left = ((bounds_rect.left + bounds_rect.right)/2) + (self.image_w/2)
            border_right = bounds_rect.right
        

        if self.pos.x < border_left:
            self.pos.x = border_left
        elif self.pos.x > border_right:
            self.pos.x = border_right
        if self.pos.y < bounds_rect.top:
            self.pos.y = bounds_rect.top
        elif self.pos.y > bounds_rect.bottom:
            self.pos.y = bounds_rect.bottom

    def blitme(self):       
        draw_pos = self.image.get_rect().move(self.pos.x-(self.image_w/2),
                                              self.pos.y-(self.image_h/2))
        self.screen.blit(self.image,draw_pos)

    _counter = 0
