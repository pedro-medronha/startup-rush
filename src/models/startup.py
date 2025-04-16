import random
from typing import Dict, List

class Startup:
    
    def __init__(self, name: str, slogan: str, foundation_year: int, points: int):
        self.name = name
        self.slogan = slogan
        self.foundation_year = foundation_year
        self.points = 70 #initial points
        self.events = {
            "pitch": 0,
            "fake_news": 0,
            "angry_investors": 0,   
            "bugs": 0,
            "traction": 0   
        }
        
    def __repr__(self):
        return f"Startup({self.name}, {self.slogan}, {self.foundation_year}, {self.points})"