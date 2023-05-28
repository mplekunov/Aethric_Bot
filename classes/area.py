from classes.point import Point

class Area(object):
    def __init__(self, top_left: Point, bottom_right: Point, confidence: float):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.confidence = confidence

    def __repr__(self):
        return f'{self.top_left}, {self.bottom_right}'
    
    def __lt__(self, other):
        return self.top_left < other.top_left or self.top_left == other.top_left
    
    def __eq__(self, other) -> bool:
        return self.top_left == other.top_left
    