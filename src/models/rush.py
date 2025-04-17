import random
from models.startup import Startup

class Rush:
    
    def __init__(self):
        self.startups = [] # List of startups
        self.current_round = 1  # Current round of the tournament
        self.pending_battles = [] # List of pending battles
        self.champion = None # Final champion
        self.champions = [] # List of champions
        self.events = {
            "pitch": 6,
            "fake_news": -8,
            "angry_investors": -6,   
            "bugs": -4,
            "traction": 3   
        }
    
    def add_startup(self, name, slogan, foundation_year):
        #cadastra a startup
        if len(self.startups) >= 8:
            raise ValueError("Cannot add more than 8 startups.")
        
        new_startup = Startup(name, slogan, foundation_year)
        self.startups.append(new_startup)
        return new_startup # so pra verificar
        
    def start_tournament(self):
        #sorteia os pares para a primeira rodada do torneio
        if len(self.startups) < 4 or len(self.startups) % 2 != 0:
            raise ValueError("The number of startups must be even (from 4 to 8)!.")
        
        random.shuffle(self.startups) # Shuffle the startups
        self.pending_battles = [
            (self.startups[i], self.startups[i + 1])
            for i in range(0, len(self.startups), 2)
        ]
        
    def battle_management(self, battle_index):
        #processa uma batalha especificamente
        if not (0 <= battle_index < len(self.pending_battles)):
            raise ValueError("Invalid battle index!.")
        
        startup1, startup2 = self.pending_battles[battle_index]
        
        #shark fight, para caso de empate
        if startup1.points == startup2.points:
            winner = random.choice([startup1, startup2])
            winner.points += 2
        else:
            winner = startup1 if startup1.points > startup2.points else startup2
    
        winner.points += 30  
        self.champions.append(winner)
        self.pending_battles.pop(battle_index)
        return winner  
            
    def next_round(self):
        #prepara próxima fase
        if self.pending_battles:
            raise Exception("There are still battles pending, you must end them.")
        
        if len(self.champions) == 1:
            self.champion = self.champions[0]
            return False #fim do torneio
        
        self.startups = self.champions.copy()
        self.champions = []
        self.current_round += 1
        self.start_tournament() #sorteio de novos pares
        return True