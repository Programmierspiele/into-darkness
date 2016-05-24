import math
import random


class Map(object):
    def __init__(self, playercount):
        self.lines = []
        intended_map_size = 20 * playercount
        intended_density = 0.1
        max_line_len = 2 + intended_map_size / 5
        min_line_len = 1 + intended_map_size / 10
        max_line_segment_count = 5
        min_line_segment_count = 2
        min_dist = max_line_len
        
        self.points = []
        for i in range(int(intended_map_size * intended_density)):
            invalid = False
            x = random.random() * intended_map_size - intended_map_size/2
            y = random.random() * intended_map_size - intended_map_size/2
            for p in self.points:
                dx = p[0] - x
                dy = p[1] - y
                if dx*dx + dy*dy < min_dist * min_dist:
                    invalid = True
                    break
            if invalid:
                continue
            theta = random.random() * math.pi
            initialTheta = theta
            line_segment_count = (random.random() * (max_line_segment_count-min_line_segment_count) + min_line_segment_count)
            for j in range(int(line_segment_count)):
                invalid = True
                while invalid:
                    llen = random.random() * (max_line_len-min_line_len) + min_line_len
                    theta += (random.random() - 0.5) * math.pi / 2
                    if abs(initialTheta-theta) > math.pi:
                        break
                    x1 = x + math.cos(theta) * llen
                    y1 = y + math.sin(theta) * llen
                    if -intended_map_size/2 < x1 < intended_map_size/2 and -intended_map_size/2 < y1 < intended_map_size/2:
                        invalid = False
                        for p in self.points:
                            if p[0] == x and p[1] == y:
                                continue
                            dx = p[0] - x1
                            dy = p[1] - y1
                            if dx*dx + dy*dy < min_dist * min_dist:
                                invalid = True
                                break
                        if not invalid:
                            self.points.append([x1, y1])
                            self.lines.append([{"x": x, "y": y}, {"x": x1, "y": y1}])
                            x = x1
                            y = y1
        
        # Create rects
        self.create_rect(self.lines, 0, 0, intended_map_size + 10, intended_map_size + 10, 0)
        #self.create_rect(15, 15, 20, 5, math.radians(30))
        #self.create_rect(1.9, 2.8, 22, 5, math.radians(55))
        #self.create_rect(-5, -15, 20, 5, math.radians(90))
        self.map_size = 0
        self.lines_as_rects = []
        for line in self.lines:
            dx = line[0]["x"] - line[1]["x"]
            dy = line[0]["y"] - line[1]["y"]
            mx = (line[0]["x"] + line[1]["x"]) / 2
            my = (line[0]["y"] + line[1]["y"]) / 2
            mlen = math.sqrt(dx*dx+dy*dy)
            mtheta = math.atan2(dy, dx)
            self.create_rect(self.lines_as_rects, mx, my, mlen + 1, 1, mtheta)
            self.map_size = max(self.map_size, 2 * abs(line[0]["x"]))
            self.map_size = max(self.map_size, 2 * abs(line[0]["y"]))
            self.map_size = max(self.map_size, 2 * abs(line[1]["x"]))
            self.map_size = max(self.map_size, 2 * abs(line[1]["y"]))

    def get_lines_as_rects(self):
        return self.lines_as_rects

    def create_rect(self, lines, x, y, width, height, theta):
        dx_width = math.cos(theta) * width
        dy_width = math.sin(theta) * width
        dx_height = math.sin(theta) * height
        dy_height = math.cos(theta) * height

        ul = {"x": x + dx_width/2 - dx_height / 2, "y": y + dy_height / 2 + dy_width / 2}
        ur = {"x": x - dx_width/2 - dx_height / 2, "y": y + dy_height / 2 - dy_width / 2}
        bl = {"x": x + dx_width/2 + dx_height / 2, "y": y - dy_height / 2 + dy_width / 2}
        br = {"x": x - dx_width/2 + dx_height / 2, "y": y - dy_height / 2 - dy_width / 2}

        lines.append([ul, ur])
        lines.append([ur, br])
        lines.append([br, bl])
        lines.append([bl, ul])

    def get_map_size(self):
        return self.map_size
        
    def get_lines(self):
        return self.lines
