import pygame
from classes.sprites import SpriteSheet
from classes.gameobject import GameObject

pygame.init()

#screen measurements
Screen_Width = 1440
Screen_Height = 720


#some random variables
BG = (50, 50, 50)
Black = (0, 0, 0)

player_pos =  pygame.Vector2(200,200)
speed = 150
clock= pygame.time.Clock()
dt=0

#sets screen
screen= pygame.display.set_mode((Screen_Width , Screen_Height))
pygame.display.set_caption("dinosawr")
# load background
background = pygame.image.load("assets/images/background.png").convert()
background = pygame.transform.scale(background, (Screen_Width, Screen_Height))


#gets sprites for character and animation
sprite_sheet_image = pygame.image.load("assets/images/doux.png").convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)


#gets the assets for the room
desk_books_sheet = pygame.image.load("assets/images/desk_books.png").convert_alpha()
desk_laptop_sheet = pygame.image.load("assets/images/desk_laptop.png").convert_alpha()
desk_mpt_sheet = pygame.image.load("assets/images/desk_mpt.png").convert_alpha()
desk_mptback_sheet = pygame.image.load("assets/images/desk_mptback.png").convert_alpha()
desk_notebook_sheet = pygame.image.load("assets/images/desk_notebook.png").convert_alpha()
desk_notenbook_sheet = pygame.image.load("assets/images/desk_notenbook.png").convert_alpha()
desk_tablet_sheet = pygame.image.load("assets/images/desk_tablet.png").convert_alpha()

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

#create animation, load background
background = pygame.image.load("assets/images/background.png").convert()
background = pygame.transform.scale(background, (Screen_Width, Screen_Height))
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

#gameloop
running = True

while running:

    dt = clock.tick(60)/1000

    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                door_state += f
                f = -f

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

    if moving == False :
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
    
    pygame.display.update()

pygame.quit()