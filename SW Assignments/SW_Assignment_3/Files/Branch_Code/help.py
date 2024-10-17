class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"({self.x},{self.y})"
    
d = {i:Point(i,i) for i in range(10)}

print(d)