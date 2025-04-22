import datetime
class Startup:
    
    def __init__(self, name: str, slogan: str, foundation_year: int):   
        #validação do nome e slogan
        if not name or not name.strip():
            raise ValueError("Name cannot be empty!")     
        if not slogan or not slogan.strip():
            raise ValueError("Slogan cannot be empty!")
        if not all(c.isalpha() or c.isspace() or c in ".,!?&-'" for c in name):
            raise ValueError("Name must contain only letters, spaces and basic characters like . , ! ? & - '")
        if not all(c.isalpha() or c.isspace()  or c in ".,!?&-'" for c in slogan):
            raise ValueError("Slogan must contain only letters, spaces and basic characters like . , ! ? & - '")
        
        #validação do ano de fundação
        current_year = datetime.datetime.now().year
        if foundation_year < 2010 or foundation_year > current_year:
            raise ValueError(f"Foundation year must be between 2010 and {current_year}.") 
        
        self.name = ' '.join(name.strip().split())
        self.slogan = ' '.join(slogan.strip().split())
        self.foundation_year = foundation_year
        self.points = 70 #pontos iniciais
        self.byes = 0
        self.stats ={
            "pitch": 0,
            "bugs": 0,
            "traction": 0,
            "fake_news": 0,
            "angry_investors": 0
        }
        
    def add_stats(self, event_type: str):
        #incrementa as estatisticas do evento
        stat_mapping = {
            "pitch": "pitch",
            "bugs": "bugs",
            "traction": "traction",
            "angry_investors": "angry_investors", 
            "fake_news": "fake_news"
    }
        if event_type in stat_mapping:
            self.stats[stat_mapping[event_type]] += 1
        
    def get_stats(self):
        #retorna as estatisticas formatadas
        return {
            "name": self.name,
            "slogan": self.slogan,
            "points": self.points,
            "pitch": self.stats["pitch"],
            "bugs": self.stats["bugs"],
            "traction": self.stats["traction"],
            "fake_news": self.stats["fake_news"],
            "angry_investors": self.stats["angry_investors"],
            "byes": self.byes
        }