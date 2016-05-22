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