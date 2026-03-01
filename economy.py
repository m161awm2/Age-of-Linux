# economy.py

class Economy:
    def __init__(self):
        self.gold = 10
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= 1:
            self.gold += 1
            self.timer -= 1

    def reward(self, unit):
        self.gold += unit.cost // 2