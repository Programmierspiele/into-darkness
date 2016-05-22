import tankgame
import sys
import time

FPS = 30
game = tankgame.GameManager()

while True:
    start_time = time.time()

    # Update
    game.update()

    end_time = time.time()
    sleep_time = 1.0 / FPS - (end_time-start_time)
    if sleep_time < 0:
        print("Error cannot keep up." + str(sleep_time))
    else:
        time.sleep(sleep_time)

sys.exit(0)