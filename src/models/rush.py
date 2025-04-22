import random
from tkinter import messagebox
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
            "bugs": -4,            
            "traction": 3,         
            "angry_investors": -6, 
            "fake_news": -8        
        }
    
    def add_startup(self, name, slogan, foundation_year):
        # verifica se ha startup com o mesmo nome
        if any(s.name.lower() == name.strip().lower for s in self.startups):
            raise ValueError(f"There is already a startup named {name}!")
        
        # cria nova startup
        new_startup =  Startup(name, slogan, foundation_year)
        
        if len(self.startups) >= 8:
            raise ValueError("Cannot add more than 8 startups.")
        
        self.startups.append(new_startup)
        return new_startup 
        
    def start_tournament(self):   
        #sorteia os pares para a primeira rodada do torneio
        try:
            if len(self.startups) < 4 or len(self.startups) > 8:
                raise ValueError("The number of startups must be between 4 and 8!")
            if len(self.startups) % 2 != 0:
                raise ValueError("The number of startups must be even!")     
            
            self.participants = self.startups.copy()
            self.current_round = 1
            self.start_new_round(self.startups) #inicia o torneio com as startups cadastradas
        except ValueError as e:
            messagebox.showerror(f"Error starting tournament: {str(e)}")
        
    def start_new_round(self, startups: List[Startup]):
        #inicia um novo round com as startups vencedoras
        if not startups:
            raise ValueError("There are not enough startups o start a new round!")
    
        if len(startups) == 1:
            self.champion = startups[0]
            return
        
        # limpa batalhas pendentes
        self.pending_battles = []
        self.ended_battles = []
        
        # Garante que temos uma lista limpa
        valid_startups = [s for s in startups if s is not None]
        
        self.round_transition(valid_startups)
    
    def get_available_events(self, battle_index: int, startup_index: int) -> List[str]:
        #retorna os eventos disponíveis para a rodada
        battle = self.pending_battles[battle_index]
        applied_events = (battle.applied_events_startup1 if startup_index == 0 else battle.applied_events_startup2)
        return [ev for ev in self.events
                if ev not in applied_events]
        
    def apply_event_to_startup(self, battle_index: int, event_name: str, startup_index: int):
        #aplica um evento especifico a uma startup
        if battle_index >= len(self.pending_battles):
            raise IndexError("Invalid battle index!")
        
        battle = self.pending_battles[battle_index]
        startup = battle.startup1 if startup_index == 0 else battle.startup2
        applied_events = battle.applied_events_startup1 if startup_index == 0 else battle.applied_events_startup2
        
        if event_name in applied_events:
            raise ValueError(f"Event already applied to {startup.name}!")
        
        points = self.events[event_name]
        startup.points += points
        startup.add_stats(event_name)
        
        applied_events.append(event_name)
        
    def shark_fight(self, battle_index: int) -> dict:
        #finalização da batalha        
        if battle_index >= len(self.pending_battles):
            raise IndexError("Invalid battle index!")
        
        battle = self.pending_battles[battle_index]
        
        #tratamento da batalha com bye
        if battle.startup2 is None:
            winner = battle.startup1
            shark_fight = False
            is_bye = True
        else:    
            # resolve a batalha
            if battle.startup1.points == battle.startup2.points:
                winner = random.choice([battle.startup1, battle.startup2])
                winner.points += 2 #bônus de 2 pontos por empate
                shark_fight = True
            else:
                winner = max(battle.startup1, battle.startup2, key=lambda s: s.points)
                shark_fight = False
            is_bye = False
        
        winner.points += 30 #bônus de 30 pontos por vitória
        battle.winner = winner #atribui o vencedor a batalha
        battle.ended = True
        
        self.pending_battles.pop(battle_index)
        self.ended_battles.append(battle)
                
        #verifica se a rodada terminou
        round_finished = len(self.pending_battles) == 0 #verifica se todas as batalhas foram finalizadas
        if round_finished:
            winners = [b.winner for b in self.ended_battles if b.winner is not None]
            self.round_transition(winners)
    
        return {
            "winner": winner,
            "shark_fight": shark_fight,
            "bye": is_bye,
            "round_finished": round_finished,
            "champion": self.champion
        }
            
    def get_round_info(self) -> dict:
        #retorna informações do round atual
        return {
            "current_round": self.current_round,
            "total_startups": len(self.startups),
            "remaining_battles": len(self.pending_battles),
            "ended_battles": len(self.ended_battles),
            "is_final": len(self.startups) == 2
        }
        
    def get_ranking(self) -> List[dict]:
        #retorna o ranking das startups ordenado por pontos
        all_startups = []
        
        #adiciona as startups que ainda estão no torneio
        for battle in self.ended_battles:
            if battle.startup1:
                all_startups.append(battle.startup1)
            if battle.startup2:
                all_startups.append(battle.startup2)
        
        #startups eliminadas em todadas anteriores 
        if hasattr(self, "participants"):
            all_startups.extend([s for s in self.participants if s not in all_startups])
        
        #ordena e remove duplicatas mantendo a última ocorrência
        unique_startups = []
        seen_names = set()
        for startup in reversed(all_startups):
            if startup.name not in seen_names:
                seen_names.add(startup.name)
                unique_startups.append(startup)
        unique_startups.reverse()
        
        return sorted(
            [s.get_stats() for s in unique_startups],
            key=lambda x: x["points"],
            reverse=True
        )
        
    def round_transition(self, winners: List[Startup]):
        if not winners:
            raise ValueError("List of winners is empty!")
        
        if len(winners) == 1:
            self.champion = winners[0]
            return
        
        # concede bye para a startup com mais pontos em caso de número impar
        if len(winners) % 2 != 0:
            auto_winner = max(winners, key=lambda s: s.points)
            auto_winner.byes += 1
            winners.remove(auto_winner)
            
            messagebox.showinfo(
                "Automatic bye",
                f"⚡ {auto_winner.name} advances automatically!\n"
                f"Points: {auto_winner.points}\n"
            )
            
            #caso sobre apenas 1, cria a final
            if len(winners) == 1:
                self.current_round += 1
                self.pending_battles = [Battle(winners[0], auto_winner, self.current_round)]
                self.ended_battles = []
                return
            
        self.current_round += 1
        random.shuffle(winners)
        
        self.pending_battles = [
            Battle(winners[i], winners[i + 1], self.current_round)
            for i in range(0, len(winners) - 1, 2)
        ]

        if len(winners) % 2 != 0:
            self.pending_battles.append(Battle(winners[-1], None, self.current_round))
            
        self.ended_battles = []        