    
class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __lt__(self, other):
        return self.x < other.x and self.y <= other.y
    
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y