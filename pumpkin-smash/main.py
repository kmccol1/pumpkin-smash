import pygame
import sys
import random

# Initalize Pygame
pygame.init()

# Set up the game window...
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pumpkin Smash")

#Load pumpkin image...
try:
    pumpkin_image = pygame.image.load('pumpkin-03.png')
    explosion_images = [pygame.image.load(f'explosion-{i}.png') for i in range (1,3)]
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit()

pumpkin_rect = pumpkin_image.get_rect()

#Ensure the pumpkin image fits within the screen dimensions ...
if pumpkin_rect.width > screen_width:
    print("Pumpkin image is too wide for the screen!")
    sys.exit()

# Set the initial position of the pumpkin...
try:
    pumpkin_rect.topleft = (random.randint(0, screen_width - pumpkin_rect.width), 0)
except ValueError as e:
    print(f"Value error: {e}")
    sys.exit()

# Set the speed of the falling pumpkin ...
pumpkin_speed = 5

# Initalize the score ...
score = 0
exploding = False
explosion_frame = 0

# Set up the font for the score display...
font = pygame.font.Font(None, 36)

#Main game loop...
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pumpkin_rect.collidepoint(event.pos):
                print("Pumpkin smashed!")
                score += 1
                exploding = True
                pumpkin_rect.topleft = (random.randint(0, screen_width - pumpkin_rect.width), 0)

    #Move the pumpkin down...
    if not exploding:
        pumpkin_rect.y += pumpkin_speed

        #If the pumpkin reaches the bottom, reset its position...
        if pumpkin_rect.top > screen_height:
            pumpkin_rect.topleft = (random.randint(0, screen_width - pumpkin_rect.width), 0)

    #Clear the screen with sky color or grass color...
    if exploding:
        screen.fill((255, 204, 0))
    else:
        screen.fill((0, 153, 0))

    #Fill the screen with a color (e.g., black)
    #screen.fill((0, 0, 0))

    #Draw the pumpkin or explosion frames ...
    if exploding:
        if explosion_frame < len(explosion_images):
            screen.blit(explosion_images[explosion_frame], pumpkin_rect)
            explosion_frame += 1
        else:
            exploding = False
            explosion_frame = 0
    else:
        screen.blit(pumpkin_image, pumpkin_rect)

    #Render the score ...
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10,10))

    #Update the display...
    pygame.display.flip()

    #Cap the frame rate ...
    pygame.time.Clock().tick(30)

#Quit Pygame...
pygame.quit()
sys.exit()