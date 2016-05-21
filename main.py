import pygame
import tankgame
import sys
from math import pi
 
TITLE = "Tank Game"
size = [800, 600]
game = tankgame.GameManager()

pygame.init()
screen = pygame.display.set_mode(size) 
pygame.display.set_caption(TITLE)
 
#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:
    # 60 FPS
    clock.tick(60)
     
    # Check for user input aka. kill the game.
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    # Update
    game.update()
     
    # Render
    screen.fill((0,0,0))
    game.render()
    pygame.display.flip()
 
game.quit()
pygame.quit()
sys.exit(0)