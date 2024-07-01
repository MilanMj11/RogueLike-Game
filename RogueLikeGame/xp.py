import pygame


class XP:
    def __init__(self, xp=0, level=1):
        self.xp = xp
        self.level = level

    def add_xp(self, xp):
        self.xp += xp
        if self.xp >= self.level * 100:
            self.level += 1
            self.xp = 0
            # print(f"Level up! You are now level {self.level}")
    def to_json(self):
        return {
            'xp': self.xp,
            'level': self.level
        }

