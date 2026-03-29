import pygame
from classes import SpriteSheet

pygame.init()

#screen measurements
Screen_Width = 1440
Screen_Height = 720


#some random variables
BG = (50, 50, 50)
Black = (0, 0, 0)

player_pos =  pygame.Vector2(200,200)
speed = 100
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
eyvaz_mask = pygame.mask.from_surface(sprite_sheet_image)
mask_image = eyvaz_mask.to_surface()

#door animation
door_sheet = SpriteSheet(pygame.image.load("assets/images/door.png").convert_alpha())
door_anim = [door_sheet.get_image(0, 24, 24, 4, Black) ,door_sheet.get_image(1, 24, 24, 4, Black) ]
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

# boundaries (walls / forbidden zones)
walls = [

    # TOP WALL (ceiling + boards area)
    pygame.Rect(0, 0, 1440, 170),

    # LEFT WINDOW WALL
    pygame.Rect(0, 0, 180, 720),

    # RIGHT WALL
    pygame.Rect(1310, 0, 180, 720),

    # BOTTOM LIMIT
    pygame.Rect(0, 650, 1440, 70),

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
    pygame.draw.rect(screen, (255,0,0), door_rect, 2)

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

    if keys[pygame.K_s]:
        dy = speed * dt
        moving = True

    if moving == False :
        if action == 1 :
            set_action(0)
        if action == 3:
            set_action(2)
        if frame >= animation_steps[action]:
            frame = 0
    
    # ---------- MOVE X ----------
    player_pos.x += dx
    player_rect.topleft = (int(player_pos.x), int(player_pos.y))

    for wall in walls:
        if player_rect.colliderect(wall):
            if dx > 0:  # moving right
                player_rect.right = wall.left
            if dx < 0:  # moving left
                player_rect.left = wall.right
            player_pos.x = player_rect.x

    # door collision (X)
    if player_rect.colliderect(door_rect):
        if dx > 0:
            player_rect.right = door_rect.left
        if dx < 0:
            player_rect.left = door_rect.right
        player_pos.x = player_rect.x


    # ---------- MOVE Y ----------
    player_pos.y += dy
    player_rect.topleft = (int(player_pos.x), int(player_pos.y))

    for wall in walls:
        if player_rect.colliderect(wall):
            if dy > 0:  # moving down
                player_rect.bottom = wall.top
            if dy < 0:  # moving up
                player_rect.top = wall.bottom
            player_pos.y = player_rect.y

    # door collision (Y)
    if player_rect.colliderect(door_rect):
        if dy > 0:
            player_rect.bottom = door_rect.top
        if dy < 0:
            player_rect.top = door_rect.bottom
        player_pos.y = player_rect.y

    #update rect position
    player_rect.topleft = (int(player_pos.x), int(player_pos.y))

    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time

        if frame >= animation_steps[action]:
            frame = 0

    screen.blit(door_anim[door_state], (Screen_Width/2,Screen_Height/2))
    screen.blit(animation_list[action][frame], player_pos)
    
    pygame.display.update()

pygame.quit()