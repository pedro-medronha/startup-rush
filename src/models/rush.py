import random
from typing import List, Tuple
from models import battle
from models import startup
from models.battle import Battle
from models.startup import Startup

class Rush:
    
    def __init__(self):
        self.startups: List[Startup] = [] # List of startups
        self.current_round = 1  # Current round of the tournament
        self.pending_battles: List[Battle] = [] # List of pending battles
        self.champion: Startup = None # Final champion
        self.ended_battles: List[Battle] = [] # List of ended battles
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
        
    def start_tournament(self) -> List[Tuple[str, str]]:    
        #sorteia os pares para a primeira rodada do torneio
        if len(self.startups) < 4 or len(self.startups) % 2 != 0:
            raise ValueError("The number of startups must be even (from 4 to 8)!.")
        
        random.shuffle(self.startups) # Shuffle the startups
        self.pending_battles = [
            Battle(self.startups[i], self.startups[i + 1], self.current_round)
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
            
    def next_round(self) -> bool:
        #prepara próxima fase ou retorna falso se o torneio acabou
        if self.pending_battles:
            raise Exception("There are still battles pending, you must end them.")
        
        if len(self.ended_battles) == 1: # fim do torneio
            self.champion = self.ended_battles[0].winner
            return False #torneio terminou  
        
        # preparando próxima fase
        winners = [battle.winner for battle in self.ended_battles]
        self.startups = winners
        self.current_round += 1
        self.ended_battles = [] # reseta as batalhas finalizadas pro proximo round
        self.start_tournament() # começa outro round
        return True
    
    def get_available_events(self, battle_index: int) -> List[str]:
        #retorna os eventos disponíveis para a rodada
        battle = self.pending_battles[battle_index]
        return [ev for ev in self.events
                if ev not in battle.applied_events]
        
    def apply_event_to_startup(self, battle_index: int, event_name: str, startup_index: int):
        #aplica um evento especifico a uma startup
        battle.self.pending_battles[battle_index]
        startup = battle.startup1 if startup_index == 0 else battle.startup2
        
        if event_name in battle.applied_events:
            raise ValueError("Event already applied in this turn!.")
        
        startup.points += self.events[event_name]
        battle.applied_events.append(event_name)
        
    def shark_fight(self, battle_index: int) -> Startup:
        #finalização da batalha
        battle = self.pending_battles[battle_index]
        
        if battle.startup1.points == battle.startup2.points:
            winner = random.choice([battle.startup1, battle.startup2])
            winner.points += 2 #bônus de 2 pontos do shark fight em caso de empate
            
        winner = max(battle.startup1, battle.startup2, key=lambda s: s.points)
        winner.points += 30 #bônus de 30 pontos por vitória
        
        self.ended_battles.append(battle)
        self.pending_battles.pop(battle_index)
        return winner #retorna o vencedor desta batalha