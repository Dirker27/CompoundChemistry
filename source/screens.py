import pygame

def win_screen():
    pygame.init()

    # Mouse Constants
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

    # Screen Setup (bckgrd + dimensions + time
    background=pygame.image.load('../images/Star.jpg')
    backgroundRect=background.get_rect()
    SCREEN_WIDTH,SCREEN_HEIGHT = background.get_size()
    size = (width, height) = background.get_size()
    screen = pygame.display.set_mode(size)
    #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    label = pygame.image.load('../images/youwin.png')
    labelRect = label.get_rect()
    label_image_w, label_image_h = label.get_size()
    #clock=pygame.time.Clock()

    run = True
    while(run):

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False

            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == LEFT):
                    run = False

        screen.blit(background,backgroundRect)
        screen.blit(label,((SCREEN_WIDTH/2)-(label_image_w/2), 40))
        pygame.display.flip()



def rules_screen():
    pygame.init()
    
    # Mouse Constants
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

    # Screen Setup (bckgrd + dimensions + time
    background=pygame.image.load('../images/howtoplay.png')
    backgroundRect=background.get_rect()
    SCREEN_WIDTH,SCREEN_HEIGHT = background.get_size()
    size = (width, height) = background.get_size()
    screen = pygame.display.set_mode(size)
    #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    #clock=pygame.time.Clock()

    run = True
    while(run):

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False

            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == LEFT):
                    run = False

        screen.blit(background,backgroundRect)
        pygame.display.flip()
