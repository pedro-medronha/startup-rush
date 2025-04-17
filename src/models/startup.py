import random
from typing import Dict, List

class Startup:
    
    def __init__(self, name: str, slogan: str, foundation_year: int):
        self.name = name
        self.slogan = slogan
        self.foundation_year = foundation_year
        self.points = 70 #initial points
        
        #falta verificar se o nome e o slogan possuem apenas letras e espaços
        if not name or not slogan:
            raise ValueError("Name and slogan cannot be empty.")
        if foundation_year < 2010 or foundation_year > 2023:
            raise ValueError("Foundation year must be between 2010 and 2023.")