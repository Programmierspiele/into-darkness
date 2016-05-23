from __future__ import division
import math
import numpy as np


class LineIntersector(object):
    def perp(self, a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b

    def pretest(self, x1, y1, x2, y2, x3, y3, x4, y4):
        if x1 < x3 and x2 < x3 and x1 < x4 and x2 < x4:
            return False
        if x1 > x3 and x2 > x3 and x1 > x4 and x2 > x4:
            return False
        if y1 < y3 and y2 < y3 and y1 < y4 and y2 < y4:
            return False
        if y1 > y3 and y2 > y3 and y1 > y4 and y2 > y4:
            return False

        return True

    def seg_intersect(self, a1, a2, b1, b2):
        da = a2-a1
        db = b2-b1
        dp = a1-b1
        dap = self.perp(da)
        dbp = self.perp(db)
        denom = np.dot(dap, db)
        num = np.dot(dap, dp)

        denom2 = np.dot(dbp, da)
        num2 = np.dot(dbp, -dp)

        if denom == 0 or denom2 == 0:
            return None
        s = (num / denom)
        s2 = (num2 / denom2)
        if 0 <= s <= 1 and 0 <= s2 <= 1:
            return b1 + s * db
        return None


class Raycaster(object):
    def __init__(self, players, map):
        self.players = players
        self.lines = list(map.get_lines())
        self.map = map
        self.line_intersector = LineIntersector()

    def update(self):
        self.lines = list(self.map.get_lines_as_rects())
        for player in self.players:
            p = self.players[player]
            x3 = p.get_pose()["x"] - p.get_size() / 2.0
            y3 = p.get_pose()["y"] - p.get_size() / 2.0
            x4 = p.get_pose()["x"] + p.get_size() / 2.0
            y4 = p.get_pose()["y"] + p.get_size() / 2.0
            self.lines.append([{"x": x3, "y": y3}, {"x": x4, "y": y4}, p])
            self.lines.append([{"x": x3, "y": y4}, {"x": x4, "y": y3}, p])

    def get_lines(self):
        return self.lines

    def cast(self, ray, leave_out_player=None):
        # Vision ray line
        x1 = ray["x"]
        y1 = ray["y"]
        p1 = np.array([x1, y1])
        x2 = x1 + math.cos(ray["theta"]) * self.map.get_map_size() * 1.5
        y2 = y1 + math.sin(ray["theta"]) * self.map.get_map_size() * 1.5
        p2 = np.array([x2, y2])
        closest = None
        closest_obj = None
        for line in self.lines:
            if len(line) == 3 and line[2].name == leave_out_player:
                continue

            # Line
            x3 = line[0]["x"]
            y3 = line[0]["y"]
            x4 = line[1]["x"]
            y4 = line[1]["y"]

            if not self.line_intersector.pretest(x1, y1, x2, y2, x3, y3, x4, y4):
                continue
            intersection = self.line_intersector.seg_intersect(p1, p2, np.array([x3, y3]), np.array([x4, y4]))
            if intersection is None:
                continue
            if closest is None:
                closest = intersection
                closest_obj = line
            else:
                dx1 = x1 - intersection[0]
                dx0 = x1 - closest[0]
                dy1 = y1 - intersection[1]
                dy0 = y1 - closest[1]
                if dx0 * dx0 + dy0 * dy0 > dx1 * dx1 + dy1 * dy1:
                    closest = intersection
                    closest_obj = line

        if closest is not None:
            if len(closest_obj) > 2:
                return closest[0], closest[1], closest_obj[2]
            else:
                return closest[0], closest[1], closest_obj
        else:
            return None, None, None
