# COMPOUND CHEMISTRY
# An Educational Game on Balancing Equations
# Authors:
#   Dirk Hortensius
#   Chris McMahan
#   Matt Baltzell

import os, sys
import pygame
from random import choice,randint
import pickle, shelve

from Blobv2 import Blob_2
from game import run_game
from screens import rules_screen

# Sets files for atom creation
# Shelves data to a file
def set_atoms():
    atom_data = shelve.open("../data/atom_data.dat")
    atom_data["Hydrogen"]   = ["Hydrogen"  , "H" , '../images/hydrogen.png'  , 1 ]
    atom_data["Helium"]     = ["Helium"    , "He", '../images/helium.png'    , 2 ]
    atom_data["Lithium"]    = ["Lithium"   , "Li", '../images/lithium.png'   , 3 ]
    atom_data["Beryllium"]  = ["Beryllium" , "Be", '../images/beryllium.png' , 4 ]
    atom_data["Boron"]      = ["Boron"     , "B" , '../images/boron.png'     , 5 ]
    atom_data["Carbon"]     = ["Carbon"    , "C" , '../images/carbon.png'    , 6 ]
    atom_data["Nitrogen"]   = ["Nitrogen"  , "N" , '../images/nitrogen.png'  , 7 ]
    atom_data["Oxygen"]     = ["Oxygen"    , "O" , '../images/oxygen.png'    , 8 ]
    atom_data["Fluorine"]   = ["Fluorine"  , "F" , '../images/fluorine.png'  , 9 ]
    atom_data["Neon"]       = ["Neon"      , "Ne", '../images/neon.png'      , 10]
    atom_data["Sodium"]     = ["Sodium"    , "Na", '../images/sodium.png'    , 11]
    atom_data["Magnesium"]  = ["Magnesium" , "Mg", '../images/magnesium.png' , 12]
    atom_data["Aluminum"]   = ["Aluminum"  , "Al", '../images/aluminum.png'  , 13]
    atom_data["Silicon"]    = ["Silicon"   , "Si", '../images/silicon.png'   , 14]
    atom_data["Phosphorus"] = ["Phosphorus", "P" , '../images/phosphorus.png', 15]
    atom_data["Sulfur"]     = ["Sulfur"    , "S" , '../images/sulfur.png'    , 16]
    atom_data["Chlorine"]   = ["Chlorine"  , "Cl", '../images/chlorine.png'  , 17]
    atom_data["Argon"]      = ["Argon"     , "Ar", '../images/argon.png'     , 18]
    atom_data["Potassium"]  = ["Potassium" , "K" , '../images/potassium.png' , 19]
    atom_data["Calcium"]    = ["Calcium"   , "Ca", '../images/calcium.png'   , 20]
    atom_data["Titanium"]   = ["Titanium"  , "Ti", '../images/titanium.png'  , 22]
    atom_data["Iron"]       = ["Iron"      , "Fe", '../images/iron.png'      , 26]
    atom_data["Nickel"]     = ["Nickel"    , "Ni", '../images/nickel.png'    , 28]
    atom_data["Copper"]     = ["Copper"    , "Cu", '../images/copper.png'    , 29]
    atom_data["Zinc"]       = ["Zinc"      , "Zn", '../images/nickel.png'    , 30]    
    atom_data["Bromine"]    = ["Bromine"   , "Br", '../images/bromine.png'   , 35]
    atom_data["Silver"]     = ["Silver"    , "Ag", '../images/silver.png'    , 47]
    atom_data["Iodine"]     = ["Iodine"    , "I" , '../images/iodine.png'    , 53]
    atom_data["Gold"]       = ["Gold"      , "Au", '../images/gold.png'      , 79]
    
    # insert
    atom_data.sync()
    atom_data.close()

def set_equations():
    eq_data = shelve.open('../data/eq_data.dat')
    eq_data["Water1"]   = ["H^2O^1"  , "H^1+H^1O^1"]
    eq_data["Water2"]   = ["H^2O^1"  , "H^1+O^2"]
    eq_data["Salt1"]    = ["Na^1Cl^1", "Na^1+Cl^1"]
    eq_data["Ammonia1"] = ["H^3N^1"  , "H^2+N^2"]
    #eq_data["Calc1"] = ["Ca^1O^1+H^2O^1", "H^2O^2Ca^1"]
    #eq_data["Carb1"] = ["H^2C^1S^1+F^2", "C^1F^4+H^1F^1+F^6S^1"]
    #eq_data["Carb2"] = ["H^10C^4+O^2", "H^2O^1+C^1O^2"]
    eq_data["Nitro1"]   = ["N^3Na^1" , "Na^1+N^2"]
    #eq_data["Sugar"] = ["O^2+H^12C^6O^6", "H^2O^1+C^1O^2"]
    eq_data["Nitro2"]   = ["N^1O^1"  , "N^2+O^2"]
    #eq_data["Nitro3"] = ["H^1N^1O^2", "H^1N^1O^3+H^2O^1+N^1O^1"]
    #eq_data["Pot1"] = ["Cl^2+K^1I^1", "K^1Cl^1+I^2"]
    eq_data["Pho1"]     = ["Cl^2+P^4", "P^1Cl^5"]
    eq_data["Hydro1"]   = ["H^2O^2"  , "O^2+H^2O^1"]
    eq_data["Bro1"]     = ["H^2+Br^2", "H^1Br^1"]
    eq_data["Lith1"]    = ["Li^1+H^2", "H^1Li^1"]
    eq_data["Mag1"]     = ["Mg^1+N^2", "N^2Mg^3"]
    eq_data["Iron1"]    = ["Fe^1+O^2", "O^3Fe^2"]
    eq_data["Chlor1"]   = ["H^2+Cl^2", "H^1Cl^1"]
    #eq_data["Sod1"] = ["Cl^2+H^1Na^1O^1", "Na^1Cl^1O^3+Na^1Cl^1+H^2O^1"]
    
    eq_data.sync()
    eq_data.close()

def get_equations():
    sides = []
    eq_data = shelve.open('../data/eq_data.dat')

    for key in eq_data.keys():
        sides.append((eq_data[key][0], eq_data[key][1]))
        
    eq_data.close()

    return choice(sides)

def menu():
    pygame.init()

    # Mouse Constants
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

    # Music files
    music_files = []
    music_files.append('../audio/Exp-3.mp3')
    music_files.append('../audio/Revive.mp3')
    #music_files.append('audio//Deez.mp3')
    music_files.append('../audio/Aint.mp3')
    music_files.append('../audio/Requiem.mp3')
    
    # Screen Setup (bckgrd + dimensions + time
    background=pygame.image.load('../images/fusion2.jpg')
    backgroundRect=background.get_rect()
    SCREEN_WIDTH,SCREEN_HEIGHT = background.get_size()
    size = (width, height) = background.get_size()
    screen = pygame.display.set_mode(size)
    #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    clock=pygame.time.Clock()

    # Font + Files + Button setup
    label = pygame.image.load('../images/title.png').convert_alpha()
    label_image_w, label_image_h = label.get_size()
    labelRect = label.get_rect()
    
    start_base = pygame.image.load('../images/start1.png').convert_alpha()
    rules_base = pygame.image.load('../images/rules1.png').convert_alpha()
    quit_base  = pygame.image.load('../images/quit1.png').convert_alpha()

    start_hover = pygame.image.load('../images/start2.png').convert_alpha()
    rules_hover = pygame.image.load('../images/rules2.png').convert_alpha()
    quit_hover = pygame.image.load('../images/quit2.png').convert_alpha()

    start_rect = start_base.get_rect()
    rules_rect = rules_base.get_rect()
    quit_rect = rules_base.get_rect()

    start_rect.move_ip(SCREEN_WIDTH/5, SCREEN_HEIGHT/2)
    rules_rect.move_ip(2*(SCREEN_WIDTH/5), SCREEN_HEIGHT/2)
    quit_rect.move_ip(3*(SCREEN_WIDTH/5), SCREEN_HEIGHT/2)

    font = pygame.font.Font(None, 20)

    # Bckgd stuffz
    blob_files = []
    atom_data = shelve.open('../data/atom_data.dat')
    for key in atom_data.keys():
        blob_files.append(atom_data[key][2])

    atom_data.close()
            
    blob_list = []

    for i in range(10):
        blob_list.append(Blob_2(screen,choice(blob_files),
                          (randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT)),
                          (choice([-1,1]),choice([-1,1])),0.1))

    left_click = False

    #run = True
    while True:
        time_passed = clock.tick(50)

        start_image = start_base
        rules_image = rules_base
        quit_image = quit_base
        
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                sys.exit()

            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == LEFT):
                    left_click = True

            if(event.type == pygame.MOUSEBUTTONUP):
                if(event.button == LEFT):
                    left_click = False


        if(left_click):            
            if(start_rect.collidepoint(pygame.mouse.get_pos())):
                run_game(get_equations())

                screen = pygame.display.set_mode(size)
                #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    
            elif(quit_rect.collidepoint(pygame.mouse.get_pos())):
                sys.exit()

            elif(rules_rect.collidepoint(pygame.mouse.get_pos())):
                rules_screen()

                screen = pygame.display.set_mode(size)
                #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

            left_click = False

        # Hover Detection
        if(start_rect.collidepoint(pygame.mouse.get_pos())):
            start_image = start_hover
        elif(rules_rect.collidepoint(pygame.mouse.get_pos())):
            rules_image = rules_hover
        elif(quit_rect.collidepoint(pygame.mouse.get_pos())):
            quit_image = quit_hover

        screen.blit(background,backgroundRect)

        for blob in blob_list:
            blob.update(time_passed)
            blob.blitme()

        screen.blit(start_image, (SCREEN_WIDTH/5, SCREEN_HEIGHT/2))
        screen.blit(rules_image, (2*(SCREEN_WIDTH/5), SCREEN_HEIGHT/2))
        screen.blit(quit_image, (3*(SCREEN_WIDTH/5), SCREEN_HEIGHT/2))
        screen.blit(label, ((SCREEN_WIDTH/2) - (label_image_w/2), 40))
        pygame.display.flip()

        if(pygame.mixer.music.get_busy() == False):
            pygame.mixer.music.load(choice(music_files))
            pygame.mixer.music.play()

    pygame.mixer.music.stop()
    sys.exit()

def main():
    set_atoms()
    set_equations()
    menu()

main()
