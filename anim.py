import pygame
from classes import SpriteSheet

pygame.init()

#screen measurements
Screen_Width = 1440
Screen_Height = 720


#some random variables
BG = (50, 50, 50)
Black = (0, 0, 0)

player_pos =  pygame.Vector2(Screen_Width/2,Screen_Height/2)
speed = 100
clock= pygame.time.Clock()
dt=0

#sets screen
screen= pygame.display.set_mode((Screen_Width , Screen_Height))
pygame.display.set_caption("dinosawr")

#gets sprites for character and animation
sprite_sheet_image = pygame.image.load("assets/images/doux.png").convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

#door animation
door_sheet = SpriteSheet(pygame.image.load("assets/images/door.png").convert_alpha())
door_anim = [door_sheet.get_image(0, 24, 24, 4, Black) ,door_sheet.get_image(1, 24, 24, 4, Black) ]
door_state = 0
f = 1

#create animation list
animation_list = []
animation_steps = [4, 6, 4, 6] #animations places in sheet such as running, jumping etc.
action = 0 #what is player doing (stayin, jumping, etc.)
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, Black))
        step_counter += 1
    animation_list.append(temp_img_list)


#gameloop
running = True

while running:

    screen.fill(BG)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                door_state += f
                f = -f

    moving = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= speed * dt
        if action == 2:
            action = 3
        if action == 0:
            action = 1
        moving = True
    if keys[pygame.K_s]:
        player_pos.y += speed * dt
        if action == 0:
            action = 1
        if action == 2:
            action = 3
        moving = True
    if keys[pygame.K_a]:
        player_pos.x -= speed *dt
        action = 1
        moving = True
    if keys[pygame.K_d]:
        player_pos.x += speed * dt
        action = 3
        moving = True


    if moving == False :
        if action == 1 :
            action = 0
        if action == 3:
            action = 2
        if frame >= animation_steps[action]:
            frame = 0
    

    dt = clock.tick(60) / 1000
            

pygame.quit()