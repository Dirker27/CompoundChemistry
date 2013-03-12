# MAIN GAME
import pygame
import string
from vec2d import vec2d
from random import choice,randint
import shelve

from blob import Blob
from atom import Atom
from molecule import Molecule
from inputbox import ask
from screens import win_screen

# Returns closest sprite object to position
# Returns NONE if empty list
def get_close(position, array):
    selected = None
    if(len(array)>0):
        selected = array[0]
        low = vec2d.get_distance(array[0].pos,position)

        for arr in array:
            t = vec2d.get_distance(arr.pos,position)
            if(t < low):
                selected = arr
                low = t
                
    return selected


# Bonds two molecules
# Transfers atoms from first molecule into the second
# Returns bonded molecule
def bond(mola,molb):
    for a in mola.atomlist:
        molb.atomlist.append(a)
        
    molb.update()

    return molb

# Gets atom to be spawned
# Uses textbox to interact w/ user
# Uses Shelves to access atom identification data
def get_atom(screen, pos):
    atom_data = shelve.open('../data/atom_data.dat')
    element = ask(screen, "Atom")
    ta = None

    for key in atom_data.keys():
        name = atom_data[key][0]
        abbrev = atom_data[key][1]
        pix = atom_data[key][2]
        num = str(atom_data[key][3])

        if((element == name) or (element == abbrev) or (element == num)):
            ta = Atom(screen,pix,pos,name,abbrev,num)

    atom_data.close()

    return ta


# Trash Disposal Method
# Removes items from their arrays if inside assigned sprite
def dispose(click, trash, array):
    if click==False:
        trash_rect=trash.image.get_rect()
        for arr in array:
            position = []
            position.append(arr.pos.x)
            position.append(arr.pos.y)
            if(in_blob(trash, position)):
                array.remove(arr)


# Determines if position is within a Sprite
# Returns Boolean
def in_blob(blob, position):
    if((blob.pos.x - (blob.image_w/2) < position[0])and
       (blob.pos.x + (blob.image_w/2) > position[0])):
        if((blob.pos.y - (blob.image_h/2) < position[1])and
           (blob.pos.y + (blob.image_h/2) > position[1])):
            return True
        else:
            return False
    else:
        return False
    

#returns a str that can be used to display equation halves
def strrep(molelist):
    strrep=''
    for mole in molelist:
        mole.atomlist.sort()
        if not((str)(mole)in strrep):
            if strrep!='':
                strrep+='+1'
            else:
                strrep+='1'
            strrep+=(str)(mole)
        else:
            temprep=''
            tempint=(int)(strrep[strrep.index((str)(mole))-1])
            index=((strrep.index((str)(mole)))-1)
            temprep=strrep[0:index]
            temprep+=(str)(tempint+1)
            temprep+=strrep[index+1:len(strrep)]
            strrep=temprep
    return strrep

#used for storing equations.
def strrep2(molelist):
    strrep=''
    for mole in molelist:
        mole.atomlist.sort()
        if not((str)(mole)in strrep):
            if strrep!='':
                strrep+='+'
            strrep+=(str)(mole)
    return strrep

#send this a strrep2 of an equation side, and the stored equation string.
#checks to see if you have correct molecules in equation
def eqvalid(molestr,valstr):
    return molestr==valstr

#returns a string used for deciding whether equations are equal
def eqrep(molelist):
    eqrep=''
    eqlist=[]
    molelist.sort()
    for mole in molelist:
        eqlist.extend(sorted(mole.atomlist))
    eqmole=Molecule(eqlist,True)
    eqmole.atomlist.sort()
    eqrep=(eqmole.eqstr())
    
    return eqrep


def equationsequal(molelist1, molelist2):
    return eqrep(molelist1)==eqrep(molelist2)


def sortcompare(atom1, atom2):
    if int(atom1.atomnum) < int(atom2.atomnum):
        return -1
    elif int(atom1.atomnum) > int(atom2.atomnum):
        return 1
    else:
        return 0
    
    
def sortmolecules(mole1, mole2):
    mole1.atomlist.sort(key=sortcompare)
    mole2.atomlist.sort(key=sortcompare)
    if len(mole1.atomlist)<len(mole2.atomlist):
        return -1
    elif len(mole1.atomlist)>len(mole2.atomlist):
        return 1
    elif len(mole1.atomlist)==len(mole2.atomlist):
        i=0        
        while ((i<(len(mole1.atomlist))) and (i<(len(mole2.atomlist)))):
            if int(mole1.atomlist[i].atomnum) < int(mole2.atomlist[i].atomnum):
                return -1
            elif int(mole1.atomlist[i].atomnum) > int(mole2.atomlist[i].atomnum):
                return 1
            i+=1
        if ((i>len(mole1.atomlist)) and (i<len(mole2.atomlist))):
            return 1
        elif ((i>len(mole2.atomlist)) and (i<len(mole1.atomlist))):
            return -1
        else:
            return 0

def correct_eq(list1, list2, combo1, combo2):
    if(equationsequal(list1, list2)):
        if(eqvalid(strrep2(list1),combo1) and
           (eqvalid(strrep2(list2),combo2))):
            return True

        elif(eqvalid(strrep2(list1),combo2) and
           (eqvalid(strrep2(list2),combo1))):
            return True

        else:
            return False
    else:
       return False
        
# Runs Game (Main Loop)
# Ended when program exits
def run_game(sides):
    pygame.init()
    pygame.display.init()
    pygame.mixer.init()

    # Mouse Constants
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

    # Screen Setup (bckgrd + dimensions)
    background=pygame.image.load('../images/Atomic_Bckgrd2.jpg')
    backgroundRect=background.get_rect()
    SCREEN_WIDTH,SCREEN_HEIGHT = background.get_size()
    size = (width, height) = background.get_size()
    screen = pygame.display.set_mode(size)
    #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    # Image Files/Font/Data File Creation
    trash_file='../images/trash.png'
    font = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 20)
    
    # Music files
    music_files = []
    music_files.append('../audio//Exp-3.mp3')
    music_files.append('../audio//Revive.mp3')
    #music_files.append('audio//Deez.mp3')
    music_files.append('../audio/Aint.mp3')
    music_files.append('../audio/Requiem.mp3')

    # Trash Can
    trash_l = Blob(screen,trash_file,(20,20))
    trash_r = Blob(screen,trash_file,(SCREEN_WIDTH - 20,20))
    trash_l.update()
    trash_r.update()

    # Enter Button
    enter_base = pygame.image.load('../images/enter1.png').convert_alpha()
    enter_hover = pygame.image.load('../images/enter2.png').convert_alpha()
    enter_image_w, enter_image_h = enter_base.get_size()
    enter_rect = enter_base.get_rect()
    enter_rect.move_ip((SCREEN_WIDTH/2)-(enter_image_w/2),
                      ((3*SCREEN_HEIGHT/4) - enter_image_h))

    # Exit Button
    quit_base = pygame.image.load('../images/quit1.png').convert_alpha()
    quit_hover = pygame.image.load('../images/quit2.png').convert_alpha()
    quit_image_w, quit_image_h = quit_base.get_size()
    quit_rect = quit_base.get_rect()
    quit_rect.move_ip((SCREEN_WIDTH/2)-(quit_image_w/2), 0)

    # Spawn Buttons
    spawn_base = pygame.image.load('../images/addatom1.png').convert_alpha()
    spawn_hover = pygame.image.load('../images/addatom2.png').convert_alpha()
    spawn_image_w, spawn_image_h = spawn_base.get_size()
    spawnL_rect = spawn_base.get_rect()
    spawnR_rect = spawn_base.get_rect()
    spawnL_rect.move_ip((SCREEN_WIDTH/4)-(spawn_image_w/2),0)
    spawnR_rect.move_ip((3*SCREEN_WIDTH/4)-(spawn_image_w/2),0)

    # In-Loop variable initialization
    left_click=False    # Left click toggle (off)
    right_click=False   # Left click toggle (off)
    mid_click=False     # Left click toggle (off)
    bond1=None          # Bonding selection (null)
    bond2=None          # Bonding selection (null)
    drag = None

    # Molecule lists (left + right side)
    items_l = []
    items_r = []
                   
    #main loop
    run = True
    while run:

        enter_image = enter_base
        quit_image = quit_base      # Sets default button image (non-hover)
        spawnL_image = spawn_base
        spawnR_image = spawn_base
        
        #INPUT
        for event in pygame.event.get():
            # IF MOUSE CLICK
            if(event.type == pygame.MOUSEBUTTONDOWN):
                #Left Click
                if(event.button == LEFT):
                    left_click = True
                #Right Click
                if(event.button == RIGHT):
                    right_click = True
                #Mouse Wheel Click
                if(event.button == MIDDLE):
                    mid_click = True

            # IF CLICK RELEASE
            if(event.type == pygame.MOUSEBUTTONUP):
                left_click = False
                drag = None
            # IF EXIT
            if(event.type == pygame.QUIT):
                #exit_game()
                run = False

        # Checks for Button hover
        if(enter_rect.collidepoint(pygame.mouse.get_pos())):
            enter_image = enter_hover
        elif(quit_rect.collidepoint(pygame.mouse.get_pos())):
            quit_image = quit_hover     # Sets active image (hover)
        elif(spawnL_rect.collidepoint(pygame.mouse.get_pos())):
            spawnL_image = spawn_hover
        elif(spawnR_rect.collidepoint(pygame.mouse.get_pos())):
            spawnR_image = spawn_hover

        # If Button Click
        if((left_click)and(drag == None)):
            pos = pygame.mouse.get_pos()

            if(enter_rect.collidepoint(pos)):
                if((len(items_l)>0)and(len(items_r)>0)):
                    if(correct_eq(items_l, items_r, sides[0], sides[1])):
                        win_screen()
                        run = False
                
                left_click = False
            
            elif(quit_rect.collidepoint(pos)):
                run = False
                left_click = False

            elif(spawnL_rect.collidepoint(pos)):
                temp = []        
                pos = (randint(0,SCREEN_WIDTH/2),randint(trash_l.image_h,SCREEN_HEIGHT))
                ta = get_atom(screen, pos)

                if(ta != None):
                    temp.append(ta)
                    items_l.append(Molecule(temp,True))
                left_click = False

            elif(spawnR_rect.collidepoint(pos)):
                temp = []        
                pos = (randint(SCREEN_WIDTH/2,SCREEN_WIDTH),randint(trash_r.image_h,SCREEN_HEIGHT))
                ta = get_atom(screen, pos)

                if(ta != None):
                    temp.append(ta)
                    items_r.append(Molecule(temp,False))
                left_click = False
                        

        # LEFT CLICK (Movement)
        if(left_click):
            # Resets bonding variables
            if(bond1!=None):
                bond1=None

            mol = None                      # Mollecule to be moved
            pos = pygame.mouse.get_pos()    # Mouse position            
                 
            # SELECTS NEAREST MOLECULE (recieves None if empty list)            
            if(drag == None):
                # if clicked on left side
                if(pos[0] < SCREEN_WIDTH/2):
                    mol = get_close(pos,items_l)
                # if clicked on right side
                else:
                    mol = get_close(pos,items_r)

                drag = mol

            else:
                mol = drag

            # if a mollecule was selected
            if(mol != None):
                # moves molecule
                opos = mol.pos   # stores original position of atom
                mol.atomlist[0].pos = pos
                mol.update()


        # RIGHT CLICK (Bonding)
        if(right_click):
            pos = pygame.mouse.get_pos()
            mol = None          # mol to be chosen for bond
            if(bond1 == None):
                # accesses molecule list on respective sides (gets closest mol)
                if(pos[0] < SCREEN_WIDTH/2):
                    mol = get_close(pos, items_l)
                else:
                    mol = get_close(pos, items_r)

                # if mol was selected
                if(mol != None):
                    for i in mol.atomlist:
                        if(in_blob(i, pos)):
                            bond1 = mol
                            
            else:
                if(pos[0] < SCREEN_WIDTH/2):
                    mol = get_close(pos,items_l)
                else:
                    mol = get_close(pos,items_r)
                    
                for i in mol.atomlist:
                    if(in_blob(i, pos)):
                        if(mol.left == bond1.left):
                            if(mol != bond1):
                                bond2 = mol

                if bond2 != None:
                    if(bond1 in items_l):
                        items_l.remove(bond1)
                        items_l.append(bond(bond1,bond2))
                    else:
                        items_r.remove(bond1)
                        items_r.append(bond(bond1,bond2))
                    if(bond2 in items_l):
                        items_l.remove(bond2)
                    else:
                        items_r.remove(bond2)

                    #Reset
                    bond1=None
                    bond2=None

            right_click=False

        # MIDDLE CLICK (Spawns at mouse location)
        if(mid_click):
            temp = []        
            pos = pygame.mouse.get_pos()
            ta = get_atom(screen, pos)

            if(ta != None):            
                temp.append(ta)
                if(pos[0] < SCREEN_WIDTH/2):
                    items_l.append(Molecule(temp,True))
                else:
                    items_r.append(Molecule(temp,False))

            mid_click = False

        #items_l.sort(key=sortmolecules)
        #items_r.sort(key=sortmolecules)
        items_l.sort()
        items_r.sort()
        
        # SCREEN OUTPUT
        screen.blit(background,backgroundRect)  # Bckgrd
        trash_l.update()
        trash_r.update()
        trash_l.blitme()                        # Trash
        trash_r.blitme()
            # Atoms
        for i in items_l:
            i.update()
            i.blitme()
        for i in items_r:
            i.update()
            i.blitme()

        # Activates Trash Cans (Must be after Updates)
        dispose(left_click,trash_l,items_l)
        dispose(left_click,trash_r,items_r)

        # BUTTON OUTPUT
        screen.blit(enter_image,((SCREEN_WIDTH/2)-(enter_image_w/2),
                      ((3*SCREEN_HEIGHT/4) - enter_image_h)))
        screen.blit(quit_image,((SCREEN_WIDTH/2)-(quit_image_w/2), 0))
        screen.blit(spawnL_image,((SCREEN_WIDTH/4)-(spawn_image_w/2),0))
        screen.blit(spawnR_image,((3*SCREEN_WIDTH/4)-(spawn_image_w/2),0))

        # TEXT EQUATION
        screen.blit(font2.render(str(strrep(items_l)),True,(0,255,0)),(SCREEN_WIDTH/4,SCREEN_HEIGHT-20))
        screen.blit(font2.render(str(strrep(items_r)),True,(0,255,0)),(3*SCREEN_WIDTH/4,SCREEN_HEIGHT-20))
        screen.blit(font.render(str(sides[0]),True,(0,255,0)),(20,SCREEN_HEIGHT-40))
        screen.blit(font.render(str(sides[1]),True,(0,255,0)),((SCREEN_WIDTH/2)+20,SCREEN_HEIGHT-40))             
        pygame.display.flip()

        if(pygame.mixer.music.get_busy() == False):
            pygame.mixer.music.load(choice(music_files))
            pygame.mixer.music.play()

    #pygame.mixer.music.stop()
