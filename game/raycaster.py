from shapely.geometry import LineString
from shapely.geometry import Point

class Raycaster(object):
    def __init__(self, players, map):
        self.players = players
        self.lines = map.get_lines()

    def cast(self, ray):
        # Vision ray line
        x1 = ray.x
        y1 = ray.y
        x2 = x1 + cos(ray.theta) * 1000
        y2 = y1 + sin(ray.theta) * 1000
        rayLine = LineString([(x1,y1), (x2,y2)])
        closest = None
        for line in self.lines:
            # Map line
            x3 = line.start.x
            y3 = line.start.y
            x4 = line.end.x
            y4 = line.end.y
            lineLine = LineString([(x3,y3), (x4,y4)])

            intersection = rayLine.intersection(lineLine)
            if intersection is None:
                continue
            if closest = None:
                closest = intersection
            else:
                dx1 = closest.x -x1
                dy1 = closest.y -y1
                dx2 = intersection.x -x1
                dy2 = intersection.y -y1
                if dx1*dx1 + dy1 *dy1 > dx2*dx2 + dy1*dy1:
                    closest = intersection

        for player in self.players:
            playerpoint = LineString([(x3,y3), (x4,y4)])

            intersection = rayLine.intersection(playerpoint)
            if intersection is None:
                continue
            if closest = None:
                closest = intersection
            else:
                dx1 = closest.x -x1
                dy1 = closest.y -y1
                dx2 = intersection.x -x1
                dy2 = intersection.y -y1
                if dx1*dx1 + dy1 *dy1 > dx2*dx2 + dy1*dy1:
                    closest = intersection

        return closest
