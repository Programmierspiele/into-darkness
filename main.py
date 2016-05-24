import tankgame
import sys
import time

TPS = 15
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

start_time = time.time()
while True:
    # Update
    game.update()

    end_time = time.time()
    elapsed = end_time-start_time
    sleep_time = 1.0 / TPS - (elapsed)
    if sleep_time > 0:
        time.sleep(sleep_time)

    start_time = time.time()
    if sleep_time < 0:
        tps = int(10/elapsed) / 10.0
        if tps < 29:
            print("Error cannot keep up. " + str(tps) + " TPS")
        time.sleep(0.00001)


sys.exit(0)
