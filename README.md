# A tank game

## Description

Tanks try to shoot each other.
There is the obvious stuff as reloading, teamplay and so forth to consider.
However, there is also a vision cone.
Tanks can only see what is roughly in the direction they are aiming.
They get clustered distance readings with meta information to see their environment.
The metainformation for players would be the name and the direction and heading, whereas they cannot be extracted from distance readings.

![Image of the game](https://raw.githubusercontent.com/penguinmenac3/into-darkness/master/into-darkness.png)

## Hackathon

The clients talk to the gameserver via TCP-Sockets on port 1337.
The socket accepts strings and reads them line by line (up to a '\n').
A line must contain a json.encoded packet-object.

Packets:

(LOBBY) register for a game:
```json
{
    "name": STRING
}
```

(LOBBY) while waiting:
```json
{
    "lobby": 
    {
        "players": [STRING],
        "timeout": INT(0, MAX_TICKS_TO_WAIT)
    }
}
```

(GAME) move:
```json
{
    "speed": FLOAT(-0.5,1),
    "turn": FLOAT(-1,1),
    "aim": FLOAT(-1,1),
    "shoot": INT(0,1,2)
}
```
if an attribute is not set it means no change or with shoot no shooting
shoot 1 is primary weapon and 2 secondary weapon (0 optional for not shooting)
turn is mathematical turn direction (positive = left, negative = right)

(GAME) gamestate transmission:
```json
{
    "remaining_ticks": INT(0, MAX_TICKS_TO_PLAY),
    "player": PLAYER,
    "players": [PLAYER],
    "projectiles": [PROJECTILE],
    "walls": [LINE],
    "ranking": {name as STRING, score as INT}
}
```

(GAME) PLAYER:
```json
{
    "x": FLOAT,
    "y": FLOAT,
    "theta": radians as FLOAT,
    "aim": radians as FLOAT,
    "health": FLOAT(0,100),
    "shootstate": INT(0,1,2),
    "respawn": INT(0, MAX_TICKS_TO_RESPAWN), <- 0 means alive
    "reload_primary": INT(0, MAX_TICKS_TO_RELOAD), <- 0 means ready
    "reload_secondary": INT(0, MAX_TICKS_TO_RELOAD), <- 0 means ready
    "name": STRING,
    "movespeed": FLOAT,
    "turnspeed": FLOAT,
    "aimspeed": FLOAT,
    "size": FLOAT(1.0), <- 1 but may change due to balancing
    "bloom": radians as FLOAT
}
```

(GAME) PROJECTILE:
```json
{
    "x": FLOAT,
    "y": FLOAT,
    "theta": radians as FLOAT,
    "owner": STRING,
    "speed": FLOAT,
    "damage": FLOAT,
    "type": INT(0,1),
    "dead": INT <- 0 if alive
}
```

(GAME) LINE:
```json
[p as {"x": FLOAT, "y" FLOAT}, q as {"x": FLOAT, "y": FLOAT}]
```


# Troubleshooting Windows

Anaconda Python (2.7, 32-Bit) instalieren, da dort Numpy enthalten ist.
WICHTIG: 32-Bit wegen pygame notwendig.

https://www.continuum.io/downloads

(OPTIONAL) Pygame installieren für die UI (32-bit).

http://www.pygame.org/download.shtml
