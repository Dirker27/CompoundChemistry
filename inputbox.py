# Original by Timothy Downs, edited by Matt Baltzell for own purposes

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import os, sys

def display_box(screen, prompt, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                    ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
    pygame.draw.rect(screen, (255,0,0),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
    screen.blit(fontobject.render(prompt, 1, (0,200,0)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 30))
    if(len(message) != 0):
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()

def ask(screen, question):
    "ask(screen, question) -> answer"
    shift = False
    enter = False
    pygame.font.init()
    current_string = ""
    display_box(screen, question, current_string)
    while True:
        for event in pygame.event.get():
            if(event.type == KEYDOWN):
                inkey = event.key
                if((inkey == K_RSHIFT) or (inkey == K_LSHIFT)):
                    shift = True
                elif(inkey == K_BACKSPACE):
                    current_string = current_string[0:-1]
                elif(inkey == K_RETURN):
                    enter = True
                    break
                elif(inkey <= 127):
                    if((shift) and (inkey >= 97) and (inkey <= 122)):
                        current_string += chr(inkey - 32)
                    else:
                        current_string += chr(inkey)
            elif(event.type == KEYUP):
                inkey = event.key
                if((inkey == K_RSHIFT) or (inkey == K_LSHIFT)):
                    shift = False
        display_box(screen, question, current_string)
        if(enter):
            break
    return current_string

def main():
    screen = pygame.display.set_mode((320,240))
    print(ask(screen, "Name") + " was entered")
    sys.exit()

if(__name__ == '__main__'):
    main()


