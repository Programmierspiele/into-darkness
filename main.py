import tankgame
import sys
import time

FPS = 30
pw = "wasd"
port = 2016

if len(sys.argv) == 2:
    pw = sys.argv[1]
elif len(sys.argv) == 3:
    pw = sys.argv[1]
    port = int(sys.argv[2])
else:
    print("Usage: python main.py <observer_pw> [port]")
    sys.exit(0)

game = tankgame.GameManager(pw, port)

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
