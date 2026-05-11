import pygame
import sys
from classes.sprites import SpriteSheet
from classes.gameobject import GameObject

pygame.init()

#screen measurements
Screen_Width = 1440
Screen_Height = 720


#some random variables
BG = (50, 50, 50)
Black = (0, 0, 0)

player_pos =  pygame.Vector2(1100,200)
speed = 150
clock= pygame.time.Clock()
dt=0

#sets screen
screen= pygame.display.set_mode((Screen_Width , Screen_Height))
pygame.display.set_caption("dinosawr")
# load background
background_closed = pygame.image.load(r"pygame_learning-eyvazawayout\assets\images\background.png").convert()
background_closed = pygame.transform.scale(background_closed, (Screen_Width, Screen_Height))
background_open = pygame.image.load(r"pygame_learning-eyvazawayout\assets\images\background_door_open.png").convert()
background_open = pygame.transform.scale(background_open, (Screen_Width, Screen_Height))
desk_laptop_upclose = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_laptop_upclose.jpg").convert_alpha()
desk_laptop_upclose = pygame.transform.scale(desk_laptop_upclose, (Screen_Width, Screen_Height))
desk_tablet_upclose = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_tablet_upclose.jpg").convert_alpha()
desk_tablet_upclose = pygame.transform.scale(desk_tablet_upclose, (Screen_Width, Screen_Height))
password_screen = pygame.image.load("pygame_learning-eyvazawayout/assets/images/password_screen.png").convert_alpha()
password_screen = pygame.transform.scale(password_screen, (540, Screen_Height))
background = background_closed

#gets sprites for character and animation
sprite_sheet_image = pygame.image.load("pygame_learning-eyvazawayout/assets/images/doux.png").convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)


#gets the assets for the room
desk_books_sheet = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_books.png").convert_alpha()
desk_laptop_sheet = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_laptop.png").convert_alpha()
desk_mpt_sheet = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_mpt.png").convert_alpha()
desk_mptback_sheet = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_mptback.png").convert_alpha()
desk_notebook_sheet = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_notebook.png").convert_alpha()
desk_notenbook_sheet = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_notenbook.png").convert_alpha()
desk_tablet_sheet = pygame.image.load("pygame_learning-eyvazawayout/assets/images/desk_tablet.png").convert_alpha()

objects = []

objects.append(GameObject(desk_books_sheet, 645, 225))
objects.append(GameObject(desk_laptop_sheet, 645, 390))
objects.append(GameObject(desk_mptback_sheet, 645, 565))
objects.append(GameObject(desk_mptback_sheet, 945, 400))
objects.append(GameObject(desk_notebook_sheet, 945, 560))
objects.append(GameObject(desk_notenbook_sheet, 345, 400))
objects.append(GameObject(desk_tablet_sheet, 345, 560))

door_state = 0
f = 1

#create animation
animation_list = []
animation_steps = [4, 6, 4, 6] #animations places in sheet such as running, jumping etc.
action = 0 #what is player doing (stayin, jumping, etc.)
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
step_counter = 0

#collision
player_rect = pygame.Rect(player_pos.x, player_pos.y, 72, 72)
door_rect = pygame.Rect(800,300, 96, 96)
'''
desk_mptback_sheet_rect = pygame.Rect(800,300, 24, 4)
desk_laptop_sheet_rect = pygame.Rect(800,300, 24, 4)
desk_books_sheet_rect = pygame.Rect(800,300, 24, 4)
desk_notebook_sheet_rect = pygame.Rect(800,300, 24, 4)
desk_mpt_sheet_rect = pygame.Rect(800,300, 24, 4)
desk_notenbook_sheet_rect = pygame.Rect(800,300, 24, 4)
desk_tablet_sheet_rect = pygame.Rect(800,300, 24, 4)
'''

# boundaries (walls / forbidden zones)
walls = [
    # TOP WALL (ceiling + boards area)
    pygame.Rect(0, 0, 1440, 170),
    # LEFT WINDOW WALL
    pygame.Rect(0, 0, 180, 720),
    # RIGHT WALL
    pygame.Rect(1310, 0, 180, 720),
    # BOTTOM LIMIT
    pygame.Rect(0, 650, 1440, 10),
]

#creates a matrix with anim sprites for each action
for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, Black))
        step_counter += 1
    animation_list.append(temp_img_list)

def set_action(new_action):
    global action, frame, last_update
    if new_action != action:
        action = new_action
        frame = 0
        last_update = pygame.time.get_ticks()


#parolscreen gameloop
def parol_screen():
    global screen, password_screen
    background_color = (30, 30, 30)

    text_color = (0,0,0)
    text_pos = (700, 302)
    font = pygame.font.SysFont("Calibri", 30)
    
    # Yazilan sifre
    entered_password = ""
    printed_password = ""

    # Dogru sifre
    correct_password = "3112"



    running = True
    while running:
        global door_locked, clock
        screen.fill(background_color)
        screen.blit(password_screen,(450,0))
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #close the screen
                if event.key == pygame.K_ESCAPE:
                    running = False

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

                if len(entered_password)<4 and mouse_pos.x >= 666 and mouse_pos.x <= 704 and mouse_pos.y >= 355 and mouse_pos.y <= 390:
                    entered_password += "1"
                    printed_password += "1 "
                if len(entered_password)<4 and mouse_pos.x >= 720 and mouse_pos.x <= 758 and mouse_pos.y >= 355 and mouse_pos.y <= 390:
                    entered_password += "2"
                    printed_password += "2 "
                if len(entered_password)<4 and mouse_pos.x >= 774 and mouse_pos.x <= 812 and mouse_pos.y >= 355 and mouse_pos.y <= 390:
                    entered_password += "3"
                    printed_password += "3 "
                if len(entered_password)<4 and mouse_pos.x >= 666 and mouse_pos.x <= 704 and mouse_pos.y >= 405 and mouse_pos.y <= 440:
                    entered_password += "4"
                    printed_password += "4 "
                if len(entered_password)<4 and mouse_pos.x >= 720 and mouse_pos.x <= 758 and mouse_pos.y >= 405 and mouse_pos.y <= 440:
                    entered_password += "5"
                    printed_password += "5 "
                if len(entered_password)<4 and mouse_pos.x >= 774 and mouse_pos.x <= 812 and mouse_pos.y >= 405 and mouse_pos.y <= 440:
                    entered_password += "6"
                    printed_password += "6 "
                if len(entered_password)<4 and mouse_pos.x >= 666 and mouse_pos.x <= 704 and mouse_pos.y >= 455 and mouse_pos.y <= 490:
                    entered_password += "7"
                    printed_password += "7 "
                if len(entered_password)<4 and mouse_pos.x >= 720 and mouse_pos.x <= 758 and mouse_pos.y >= 455 and mouse_pos.y <= 490:
                    entered_password += "8"
                    printed_password += "8 "
                if len(entered_password)<4 and mouse_pos.x >= 774 and mouse_pos.x <= 812 and mouse_pos.y >= 455 and mouse_pos.y <= 490:
                    entered_password += "9"
                    printed_password += "9 "
                
                if mouse_pos.x >= 663 and mouse_pos.x <= 730 and mouse_pos.y >= 503 and mouse_pos.y <= 541:
                    entered_password = ""
                    printed_password = ""
                if len(entered_password) == 4 and mouse_pos.x >= 745 and mouse_pos.x <= 815 and mouse_pos.y >= 503 and mouse_pos.y <= 541:
                    if entered_password == correct_password:
                        door_locked = False
                        printed_password = "UNLOCKED"
                        text_color = (0,255,0)
                    else:
                        printed_password = "INCORRECT"
                        entered_password = ""
                        text_color = (255,0,0)
                        text_start_time = current_time

                    text_pos = (670,302)
                        
        
        if printed_password == "INCORRECT":
            if current_time - text_start_time > 1000:
                printed_password = ""
                text_color = (0,0,0)
                text_pos = (700, 302)

        rendered_text = font.render(printed_password, True, text_color)
        screen.blit(rendered_text, text_pos)

        pygame.display.update()

#laptop screen code piece
def code_screen1():
    global screen, desk_laptop_upclose
    
    running = True
    while running:
        screen.blit(desk_laptop_upclose,(0,0))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #close the screen
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

def code_screen2():
    global screen, desk_tablet_upclose
    
    running = True
    while running:
        screen.blit(desk_tablet_upclose,(0,0))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #close the screen
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()



#texts
font = pygame.font.SysFont("Arial", 30)
locked_door_text = font.render("Hmm... the door seems locked, maybe I could find the password in here...", True, (0,0,0))
note_text1 = font.render("press W,A,S,D to move", True, (0,0,0))
note_text2 = font.render("press F to interact", True, (0,0,0))
note_text3 = font.render("press E to open the door", True, (0,0,0))
show_note_text = True
show_door_text = False #for temp door text
door_locked = True

#gameloop
running = True

while running:

    dt = clock.tick(60)/1000
    if door_state == 0:
        background = background_closed
    else:
        background = background_open
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            show_note_text = False
            if event.key == pygame.K_e and player_pos.x >= 1200 and player_pos.y >= 300 and player_pos.y <= 420: #opens and closes the door
                if door_locked:
                    show_door_text = True
                    text_start_time = current_time
                else:
                    door_state += f
                    f = -f
            
            if event.key == pygame.K_f:
                if player_pos.x >= 1200 and player_pos.y >= 300 and player_pos.y <= 420 and door_locked:
                    parol_screen()
                if player_pos.x >= 630 and player_pos.y >= 400 and player_pos.x <= 760 and player_pos.y <= 490:
                    code_screen1()
                if player_pos.x >= 265 and player_pos.y >= 550 and player_pos.x <= 550:
                    code_screen2()

    moving = False

    keys = pygame.key.get_pressed()

    new_pos = player_pos.copy()

    dx = 0
    dy = 0

    if keys[pygame.K_d]:
        dx = speed * dt
        moving = True
        set_action(3)

    if keys[pygame.K_a]:
        dx = -speed * dt
        moving = True
        set_action(1)

    if keys[pygame.K_w]:
        dy = -speed * dt
        moving = True
        if action == 0 :
            set_action(1)
        if action == 2:
            set_action(3)

    if keys[pygame.K_s]:
        dy = speed * dt
        moving = True
        if action == 0 :
            set_action(1)
        if action == 2:
            set_action(3)

    if not moving:
        if action == 1 :
            set_action(0)
        if action == 3:
            set_action(2)
        if frame >= animation_steps[action]:
            frame = 0

    for obj in objects:
        obj.draw(screen)

    # PLAYER + DOOR MASKS
    player_image = animation_list[action][frame]
    player_mask = pygame.mask.from_surface(player_image)


    # ---------- MOVE X ----------
    future_rect = player_rect.copy()
    future_rect.x += int(dx)

    blocked = False

    # walls
    for wall in walls:
        if future_rect.colliderect(wall):
            blocked = True
            break

    # objects
    if not blocked:
        for obj in objects:
            offset = (
                obj.rect.x - future_rect.x,
                obj.rect.y - future_rect.y
            )
            if player_mask.overlap(obj.mask, offset):
                blocked = True
                break

    if not blocked:
        player_rect.x = future_rect.x

    # ---------- MOVE Y ----------
    future_rect = player_rect.copy()
    future_rect.y += int(dy)

    blocked = False

    # walls
    for wall in walls:
        if future_rect.colliderect(wall):
            blocked = True
            break

    # objects
    if not blocked:
        for obj in objects:
            offset = (
                obj.rect.x - future_rect.x,
                obj.rect.y - future_rect.y
            )
            if player_mask.overlap(obj.mask, offset):
                blocked = True
                break

    if not blocked:
        player_rect.y = future_rect.y

    # FINAL SYNC
    player_pos.xy = player_rect.topleft

    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time

        if frame >= animation_steps[action]:
            frame = 0

    screen.blit(player_image, player_rect.topleft)
    if show_note_text:
        screen.blit(note_text1, (300, 200))
        screen.blit(note_text2, (300, 240))
        screen.blit(note_text3, (300, 280))
    

    if show_door_text:
        screen.blit(locked_door_text, (340, 660))
        if current_time - text_start_time > 3000:
            show_door_text = False

    pygame.display.update()

pygame.quit()