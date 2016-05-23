import pygame
import ui.tankgame
import sys
from math import pi

host = "localhost"
port = 2016
pw = "wasd"

if len(sys.argv) == 4:
    host = sys.argv[1]
    port = int(sys.argv[2])
    pw = sys.argv[3]
elif len(sys.argv) == 3:
    host = sys.argv[1]
    pw = sys.argv[2]
else:
    print("Usage: python ui.py <host> [port] <password>")
    sys.exit(0)

TITLE = "Tank Game"
size = [800, 600]
game = ui.tankgame.GameManager(host, port, pw)

pygame.init()
infoObject = pygame.display.Info()
fullscreen_size = (infoObject.current_w, infoObject.current_h)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption(TITLE)

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:
    # 60 FPS
    clock.tick(30)

    # Check for user input aka. kill the game.
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_q):
            done = True
        #if (event.type is pygame.KEYDOWN and event.key == pygame.K_f):
        #    if screen.get_flags() & pygame.FULLSCREEN:
        #        pygame.display.set_mode(size, pygame.RESIZABLE)
        #    else:
        #        pygame.display.set_mode(fullscreen_size, pygame.FULLSCREEN)
        if (event.type is pygame.VIDEORESIZE):
            if screen.get_flags() & pygame.FULLSCREEN:
                pass
            else:
                size = (event.w, event.h)
                pygame.display.set_mode(size, pygame.RESIZABLE)

        if (event.type is pygame.KEYDOWN and event.key == pygame.K_0):
            game.select_player(0)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_1):
            game.select_player(1)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_2):
            game.select_player(2)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_3):
            game.select_player(3)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_4):
            game.select_player(4)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_5):
            game.select_player(5)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_6):
            game.select_player(6)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_7):
            game.select_player(7)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_8):
            game.select_player(8)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_9):
            game.select_player(9)
        if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            game.select_player(-1)
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode(size, pygame.RESIZABLE)

    # Render
    screen.fill((45, 45, 45))
    if screen.get_flags() & pygame.FULLSCREEN:
        game.render(screen, fullscreen_size[0], fullscreen_size[1])
    else:
        game.render(screen, size[0], size[1])
    pygame.display.flip()

game.quit()
pygame.quit()
sys.exit(0)
