import point
class line:
    def __init__(self, distance, angle,p1:point.Point,q1:point.Point):
        # distance from based horizon line
        # =0 means endless
        self.distance = distance
        # angle between vertical line
        self.angle = angle
        self.p1= p1
        self.q1 = q1
