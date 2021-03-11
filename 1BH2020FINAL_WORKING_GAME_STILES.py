import pygame, sys

clock = pygame.time.Clock() #frame rate

from pygame.locals import *

#INITIALIZE
pygame.init()

#GAME TITLE
pygame.display.set_caption('Tiny Forest Vampire')

#BOUNDARIES
WINDOW_SIZE = (600,400)

#BACKGROUND
background = pygame.image.load('background.jpg')

#ICON
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#MUZAC
music = 'gamemusic.mp3'
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

#initialize screen
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
running = True

#FONT AND INSTRUCTIONS
#color
white = (255, 255, 255)
black = (0, 0, 0)
white = (255, 255, 255)
#font
font = pygame.font.Font('lolita.ttf', 24)
#surface object for text
lines_of_text = []
lines_of_text.append(font.render('PRESS the LEFT and RIGHT ARROW KEY to MOVE.' , True, white, black))
lines_of_text.append(font.render('APPROACH SKULL and PRESS + HOLD SPACE BAR', True, white, black))
lines_of_text.append(font.render('to HOLD. RELEASE SPACE BAR to PUT DOWN.', True, white, black))
lines_of_text.append(font.render('KILL the VAMPIRE.', True, white, black))

#position text
margin= 15
text_rects = []
for index in range(len(lines_of_text)):
    # create a rectangular object for the text surface object
    textRect = lines_of_text[index].get_rect()
    # set the center of the rectangular object
    textRect.topleft = (margin, margin + 32*index)
    text_rects.append(textRect)

#title text
font = pygame.font.Font('lolita.ttf', 36)
title_text = []
title_text.append(font.render('Tiny Forest Vampire' , True, white, black))
title_text.append(font.render('Press any key to START', True, white, black))

#title position text
title_text_rects = []
for index in range(len(lines_of_text)):
    # create a rectangular object for the text surface object
    textRect = lines_of_text[index].get_rect()
    # set the center of the rectangular object
    textRect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + (45*(index-1)))
    title_text_rects.append(textRect)

#player1
class Spritesheet(pygame.sprite.Sprite):
    def __init__(self, position, path):
        super(Spritesheet, self).__init__()
        self.position = position
        self.haskey = False
        self.hassword = False
        self.sprite_sheet = pygame.image.load(path).convert()
        self.walkright = []
        self.walkleft = []
        self.facefront = []
        self.walkright.append(self.get_sprite(100, 0, 50, 50))
        self.walkright.append(self.get_sprite(50, 0, 50, 50))
        self.walkleft.append(self.get_sprite(50, 50, 50, 50))
        self.walkleft.append(self.get_sprite(100, 50, 50, 50))
        self.facefront.append(self.get_sprite(0, 0, 50, 50))

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((255, 0, 0))
        sprite.blit(self.sprite_sheet,(0,0),(x, y, w, h))
        return sprite

    def equip_sword(self):
        self.sprite_sheet = pygame.image.load('spritesheet_with_sword.png').convert()
        self.walkright = []
        self.walkleft = []
        self.facefront = []
        self.walkright.append(self.get_sprite(100, 0, 50, 50))
        self.walkright.append(self.get_sprite(50, 0, 50, 50))
        self.walkleft.append(self.get_sprite(50, 50, 50, 50))
        self.walkleft.append(self.get_sprite(100, 50, 50, 50))
        self.facefront.append(self.get_sprite(0, 0, 50, 50))
        

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position, path, type='skull'):
        super(Obstacle, self).__init__()
        self.position = position
        self.type = type
        self.sprite_sheet = pygame.image.load(path).convert()
        self.image = self.get_sprite(0,0,30,30)
        self.isholding = False
        self.isinventory = False

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet,(0,0),(x, y, w, h))
        return sprite

class Enemy():
    def __init__(self, position, path):
        self.position = position
        self.type = 'vampire'
        self.sprite_sheet = pygame.image.load(path).convert()
        self.image = self.get_sprite(0,0,50,50)
        self.isholding = False
        self.isinventory = False

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet,(0,0),(x, y, w, h))
        return sprite

    def die(self):
        self.image = self.get_sprite(0,50,50,50)

def is_colliding(a,b):
    dist = 0
    if moving_right == True:
        dist = 50
    else:
        dist = 30
    if abs(a.position[0]-b.position[0]) <= dist:
        return True
    else:
        return False
    
#moving
moving_right = False
moving_left = False
current_frame = 0
picking_up = False

interactable_item = None
holding_item = None

#items
items = []

#player
player_location = [125, 350]
player1 = Spritesheet(player_location, 'spritesheet.png')

#treasure
items.append(Obstacle([375, 370], 'treasure.png', type='chest'))

#skulls
items.append(Obstacle([80,370], 'skull.png'))
items.append(Obstacle([250,370], 'skull.png'))
items.append(Obstacle([425,370], 'skull.png'))

#key
items.append(Obstacle([25,370], 'key.png', type='key'))

#vampire
items.append(Enemy([550,350], 'vampire.png'))

GAME_STATE = 'title'
while True:
    if GAME_STATE == 'title':
        #background
        screen.blit(background, (0,0))

        #instructions and text
        # copying the text surface object to the display surface object at the center coordinate.
        for index in range(len(title_text)):
            screen.blit(title_text[index], title_text_rects[index])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit(5)
            if event.type == KEYUP: #WHEN ANY KEY IS RELEASED
                GAME_STATE = 'game'
        
        pygame.display.update() #update the display
        clock.tick(60) #60 FPS
    else:
        #GAME LOOP
        while running:
            #background
            screen.blit(background, (0,0))

            #instructions and text
            # copying the text surface object to the display surface object at the center coordinate.
            for index in range(len(lines_of_text)):
                screen.blit(lines_of_text[index], text_rects[index])

            #items/sprites/player
            screen.blit(player1.facefront[0], (player1.position[0],player1.position[1]))

            #renders obstacles
            for item in items:
                #prints image on screen if it is not being held or in player inventory
                if item.isholding == False and not (item.type == 'key' and item.isinventory == True) and not (item.type == 'chest' and player1.hassword == True):
                    screen.blit(item.image, (item.position[0], item.position[1]))
                else:
                    #if being held and space bar is not being presses, place back down (skulls)
                    if picking_up == False:
                        if moving_right == True:
                            item.position[0]= player1.position[0] + 55
                        elif moving_left == True:
                            item.position[0] = player1.position[0] - 32
                        else:
                            item.position[0] = player1.position[0] - 32
                        item.isholding = False
                        holding_item = None

            #checks if items are colliding with player
            #player cannot move past the item that is set as interactable
            for item in items:
                if is_colliding(player1, item): #if colliding...
                    #set skull as interactable to give option to pick up with space
                    if item.type == 'skull':
                        interactable_item = item
                        break # exit for loop
                    #puts key in inventory when walked over
                    elif item.type == 'key':
                        item.isinventory = True
                        player1.haskey = True
                        break # exit for loop
                    #gives player sword if player has picked up the key
                    elif item.type == 'chest':
                        if player1.haskey == True:
                            player1.hassword = True
                            player1.equip_sword()
                            break # exit for loop
                        #if no key, chest is set as interactable so player cant move past to kill vampire
                        else:
                            interactable_item = item
                            break # exit for loop
                    # else the item is the vampire
                    else:
                        item.die() # kill the vampire when player collides
                interactable_item = None # if the player is not touching an item, reset the interactable item

            #if space is being pressed, there is an item nearby that isn't the chest, and the player isnt already holding something
            if picking_up == True and interactable_item != None and holding_item == None and interactable_item.type != 'chest':
                # pick up the skull
                holding_item = interactable_item
                holding_item.isholding = True
                interactable_item = None
            
            #walking and boundary flags
            if moving_right == True and player1.position[0] + 50 < 600 and (interactable_item == None or (interactable_item.position[0]<player1.position[0] or interactable_item.isholding == True)):
                screen.blit(player1.walkright[current_frame], (player1.position[0],player1.position[1]))
                player1.position[0] += 1
                if current_frame == 0:
                    current_frame = 1
                else:
                    current_frame = 0
            if moving_left == True and player1.position[0] > 0 and (interactable_item == None or (interactable_item.position[0]>player1.position[0] or interactable_item.isholding == True)):
                screen.blit(player1.walkleft[current_frame], (player1.position[0],player1.position[1]))
                player1.position[0] -= 1
                if current_frame == 0:
                    current_frame = 1
                else:
                    current_frame = 0
            if moving_left == False and moving_right == False:
                screen.blit(player1.facefront[0], (player1.position[0],player1.position[1]))

            pygame.display.update() #update the display
            clock.tick(60) #60 FPS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    print("quit")
                if event.type == KEYDOWN: #WHEN ANY KEY IS PRESSED
                    if event.key == K_RIGHT:
                        moving_right = True
                    if event.key == K_LEFT:
                        moving_left = True
                    if event.key == K_SPACE:
                        picking_up = True
                if event.type == KEYUP: #WHEN ANY KEY IS RELEASED
                    if event.key == K_RIGHT:
                        moving_right = False
                    if event.key == K_LEFT:
                        moving_left = False
                    if event.key == K_SPACE:
                        picking_up = False
                    if event.key == K_ESCAPE:
                        print("has key: " + str(player1.haskey))
                        print("has sword: " + str(player1.hassword))
