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

# Set the speed increments...
speed_increment = 0.1

#Font
font = pygame.font.Font(None, 36)

# Initalize the score ...
score = 0
exploding = False
explosion_frame = 0

# Define messages ...
good_message = font.render("Nice!", True, (255, 255, 255))
miss_message = font.render("Miss!", True, (255,0,0)) # Red for misses...
message_timer = 0 #Timer to control message display
message_display_time = 30 #Frames to display the message
current_message = None

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

                pumpkin_speed += speed_increment

                #Set the great message to display...
                current_message = good_message
                message_timer = message_display_time

    #Move the pumpkin down...
    if not exploding:
        pumpkin_rect.y += pumpkin_speed

        #If the pumpkin reaches the bottom, reset its position...
        if pumpkin_rect.top > screen_height:
            pumpkin_rect.topleft = (random.randint(0, screen_width - pumpkin_rect.width), 0)

            score = 0
            pumpkin_speed += speed_increment #Increase the speed for the next fall...

            #Set the miss message to display...
            current_message = miss_message
            message_timer = message_display_time

    #Clear the screen with sky color or grass color...
    if exploding:
        screen.fill((255, 204, 0)) #Explosion color
    else:
        #Assuming the pumpkin is falling, set the sky color...
        screen.fill((135, 206, 235))

    # Draw the grass ...
    grass_rect = pygame.Rect(0, screen.get_height() // 2, screen.get_width(), screen.get_height() // 2)
    pygame.draw.rect(screen, (0, 153, 0), grass_rect) # Grass color

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

    #Display the current message...
    if current_message:
        screen.blit(current_message, (screen_width // 2 - current_message.get_width() // 2, screen_height // 4))

    #Decrease the timer and clear messages...
    message_timer -= 1
    if message_timer <= 0:
        current_message = None

    #Update the display...
    pygame.display.flip()

    #Cap the frame rate ...
    pygame.time.Clock().tick(30)

#Quit Pygame...
pygame.quit()
sys.exit()