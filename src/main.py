import tkinter as tk
from tkinter import ttk, messagebox
from models.rush import Rush

class Main:
    def __init__(self, root):
        self.root = root
        self.tournament = Rush()
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Startup Rush - Registration")
        self.root.geometry("800x600")
        
        # abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # aba de cadastro
        self.setup_registration_tab()
        
        # aba de torneio
        self.setup_tournament_tab()
        
    def setup_registration_tab(self):
        #funcionalidade de cadastro de startups
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Registration")
        
        tk.Label(tab, text="Name:").pack()
        self.name_entry = tk.Entry(tab)
        self.name_entry.pack()
        
        tk.Label(tab, text="Slogan:").pack()
        self.slogan_entry = tk.Entry(tab)
        self.slogan_entry.pack()
        
        tk.Label(tab, text="Foundation year:").pack()
        self.year_entry = tk.Entry(tab)
        self.year_entry.pack()
        
        tk.Button(
            tab, 
            text="Register Startup", 
            command=self.register_startup
        ).pack(pady=10)
        
        # lista as startups cadastradas
        self.listbox = tk.Listbox(tab)
        self.listbox.pack(expand=True, fill=tk.BOTH)
        
        # mostra o status da quantidade de startups
        self.status_label = tk.Label(tab, text=f"Startups: {len(self.tournament.startups)}/8")
        self.status_label.pack()
        
        # botao pra iniciar o torneio
        self.start_button = tk.Button(
            tab,
            text="Start Tournament",
            command=self.start_tournament,
            state=tk.DISABLED
        )
        self.start_button.pack(pady=10)
    
    def register_startup(self):
        try:
            name = self.name_entry.get()
            slogan = self.slogan_entry.get()
            year = int(self.year_entry.get())
            
            startup = self.tournament.add_startup(name, slogan, year)
            self.listbox.insert(tk.END, f"{startup.name} ({startup.foundation_year})")
            
            # atualiza o status da label
            self.status_label.config(text=f"Startups: {len(self.tournament.startups)}/8")
            
            #habilita inicio de outro torneio se tiver startups suficientes
            if 4 <= len(self.tournament.startups) <= 8:
                self.start_button.config(state=tk.NORMAL)
            
            # limpeza dos campos de entrada
            self.name_entry.delete(0, tk.END)
            self.slogan_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            
        except ValueError as err:
            messagebox.showerror("Error!", str(err))
        except Exception as err:
            messagebox.showerror("Unexpected error!", str(err))
            
    def setup_tournament_tab(self):
        # funcionalidade de gerenciamento do torneio
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Tournament")
        
        # espaço das batalhas
        self.battle_frame = ttk.LabelFrame(tab, text="Current Battles")
        self.battle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # lista as batalhas
        self.battle_tree = ttk.Treeview(
            self.battle_frame,
            columns=("startup1", "startup2", "round"),
            show="headings"
        )
        self.battle_tree.heading("startup1", text="Startup 1")
        self.battle_tree.heading("startup2", text="Startup 2")
        self.battle_tree.heading("round", text="Round")
        self.battle_tree.pack(fill=tk.BOTH, expand=True)
        
        # controles da batalha
        control_frame = ttk.Frame(self.battle_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Ceventos disponíveis
        tk.Label(control_frame, text="Select Event:").pack(side=tk.LEFT)
        self.event_combobox = ttk.Combobox(control_frame, state="readonly")
        self.event_combobox.pack(side=tk.LEFT, padx=5)
        
        # botao que aplica evento
        self.apply_event_button = tk.Button(
            control_frame,
            text="Apply Event",
            command=self.apply_event,
            state=tk.DISABLED
        )
        self.apply_event_button.pack(side=tk.LEFT, padx=5)
        
        # botao que finaliza a batalha
        self.resolve_button = tk.Button(
            control_frame,
            text="Resolve Battle",
            command=self.resolve_battle,
            state=tk.DISABLED
        )
        self.resolve_button.pack(side=tk.RIGHT, padx=5)
        
        # Área de status
        self.round_label = tk.Label(tab, text=f"Current Round: {self.tournament.current_round}")
        self.round_label.pack()
        
    def start_tournament(self):
        #inicia o torneio e atualiza a lista de batalhas
        try:
            self.tournament.start_tournament()
            self.update_battle_list()
            self.notebook.select(1)  # Switch to tournament tab
            messagebox.showinfo("Tournament started successfully!")
            
            self.apply_event_button.config(state=tk.NORMAL)
            self.resolve_button.config(state=tk.NORMAL)    
        except ValueError as e:
            messagebox.showerror("Error!", str(e))
            
    def update_battle_list(self):
        #atualiza a lista de batalhas
        self.battle_tree.delete(*self.battle_tree.get_children())
        for i, battle in enumerate(self.tournament.pending_battles):
            self.battle_tree.insert(
                "", tk.END,
                values=(battle.startup1.name, battle.startup2.name, battle.round),
                tags=(i,)  # guarda o index da batalha
            )
        self.round_label.config(text=f"Current Round: {self.tournament.current_round}")
        
    def apply_event(self):
    # aplica o evento selecionado à startup
        try:
            # get da batalha selecionada
            selected_item = self.battle_tree.focus()
            if not selected_item:
                raise ValueError("You must select a battle!")
            
            battle_index = int(self.battle_tree.item(selected_item, "tags")[0])
            event = self.event_combobox.get()
            
            # dialogo para escolher a startup que receberá o evento
            startup_choice = self.ask_startup(battle_index)
            if startup_choice is None:  # caso nao selecione
                return
                
            # implementa a função da classe Rush
            self.tournament.apply_event_to_startup(battle_index, event, startup_choice)
            
            # atualiza a lista de batalhas e eventos disponíveis
            self.update_battle_list()
            self.update_events(battle_index)
            messagebox.showinfo("Event '{event}' applied!")
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected error", str(e))

    def ask_startup(self, battle_index):
        # criação de um diálogo para escolher a startup
        battle = self.tournament.pending_battles[battle_index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Startup")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Which Startup would you like to apply the event?").pack(pady=10)
        
        choice = None
        
        def set_choice(index):
            nonlocal choice
            choice = index
            dialog.destroy()
        
        tk.Button(dialog, text=battle.startup1.name, command=lambda: set_choice(0)).pack(side=tk.LEFT, padx=10)
        tk.Button(dialog, text=battle.startup2.name, command=lambda: set_choice(1)).pack(side=tk.RIGHT, padx=10)
        
        dialog.transient(self.root)  # dialogo modal 
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return choice   

    def uptade_events(self, battle_index):
        # atualiza os eventos disponíveis
        available_events = self.tournament.get_available_events(battle_index)
        self.event_combobox["values"] = available_events
        if available_events:
            self.event_combobox.set(available_events[0])
            
    def resolve_battle(self):
        #resolve a batalha utilizando o Shark Fight
        try:
            selected_item = self.battle_tree.focus()
            if not selected_item:
                raise ValueError("You must select a battle!")
            
            battle_index = int(self.battle_tree.item(selected_item, "tags")[0])
            winner = self.tournament.shark_fight(battle_index)
            
            # atualiza a lista de batalhas e o status
            self.update_battle_list()
            messagebox.showinfo("Battle resolved!", f"The winner is {winner.name} with {winner.points} points!")
            
            # verifica se o torneio acabou  
            if self.tournament.champion:
                messagebox.showinfo("The champion is {self.tournament.champion.name}!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()