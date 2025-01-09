class Player:
    def __init__(self, name, color=None):
        self.name = name
        self.color = color
        self.position = 1

    def move(self, steps):
        new_position = self.position + steps
        if new_position > 100:
            return self.position
        self.position = new_position
        return new_position

    def set_position(self, position):
        self.position = position
