class Vector2:
    x:int
    y:int

    def __init__(self, x:int = 0, y:int = 0):
        self.x = x
        self.y = y

    def Get(self):
        return [self.x, self.y]
