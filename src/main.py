import tkinter as tk
from tkinter import ttk, messagebox
from models import battle
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
            self.notebook.select(1)  # troca pra aba do torneio
            
            # verificação de consistência
            for battle in self.tournament.pending_battles:
                if not hasattr(battle, "startup1") or not hasattr(battle, "startup2"):
                    raise AttributeError("Battle doesn't have startups defined correctly.")
            
            #atualiza os eventos da batalha
            if self.tournament.pending_battles:
                self.update_events(0, 0)
            
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
                values=(battle.startup1.name, battle.startup2.name, battle.round_number),
                tags=(i, )  # guarda o index da batalha
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
            
            # retorna startup e o evento selecionado
            startup_index, event = self.ask_startup(battle_index)
            
            if None in (startup_index, event):
                return # pra quando o usuario cancelar a janela de eventos
            
            # implementa a função da classe Rush
            self.tournament.apply_event_to_startup(battle_index, event, startup_index)
            
            # atualiza a lista de batalhas e exibição
            self.update_battle_list()
            messagebox.showinfo(f"Event '{event}' applied to {self.tournament.pending_battles[battle_index].startup1.name if startup_index == 0 else self.tournament.pending_battles[battle_index].startup2.name}!")
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected error", str(e))

    def ask_startup(self, battle_index):
        # criação de um diálogo para escolher a startup
        battle = self.tournament.pending_battles[battle_index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Apply Event")
        dialog.geometry("400x300")
        
        #variavel pra armazenar a startup selecionada
        self.selected_startup = {
            'startup_index': None,
            'event': None
        }
        
        #selecionar startup
        startup_frame = ttk.LabelFrame(dialog, text="Select Startup")
        startup_frame.pack(pady=10, padx=10, fill=tk.X)
        
        startup_var = tk.IntVar(value=0)  
              
        # radiobuttons para selecionar as startups
        ttk.Radiobutton(
            startup_frame,
            text=f"{battle.startup1.name} (Points: {battle.startup1.points})",
            variable=startup_var,
            value=0,
        ).pack(anchor=tk.W)

        ttk.Radiobutton(
            startup_frame,
            text=f"{battle.startup2.name} (Points: {battle.startup2.points})",
            variable=startup_var,
            value=1,
        ).pack(anchor=tk.W) 
        
        # janela para selecionar eventos
        event_frame = ttk.LabelFrame(dialog, text="Select Event")
        event_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        #mostra os eventos disponíveis
        event_listbox = tk.Listbox(event_frame)
        event_listbox.pack(fill=tk.BOTH, expand=True)   
        
        #preenche a lista de eventos disponíveis
        for event in self.tournament.events:
           event_listbox.insert(tk.END, f"{event} ({'+' if self.tournament.events[event] > 0 else ''}{self.tournament.events[event]} pts)")

        #botao de confirmação
        def confirmation():
            selected_event_index = event_listbox.curselection()
            if not selected_event_index:
                messagebox.showwarning("Select an event!")
                return
            
            selected_event =  list(self.tournament.events.keys())[selected_event_index[0]]  
            
            selected_startup = startup_var.get()
            applied_events = battle.applied_events_startup1 if selected_startup == 0 else battle.applied_events_startup2
            
            if selected_event in applied_events:
                messagebox.showerror(f"Event already applied to {battle.startup1.name if selected_startup == 0 else battle.startup2.name}!")
                return
            
            self.selected_startup = {
                'startup_index': selected_startup,
                'event': selected_event
            }
            dialog.destroy()
            
        ttk.Button(
            dialog,
            text="Apply Event",
            command=confirmation
        ).pack(pady=10)
            
        dialog.transient(self.root)  # faz o dialog ficar em cima da janela principal
        dialog.grab_set()
        self.root.wait_window(dialog)  # espera o dialog ser fechado
            
        return self.selected_startup['startup_index'], self.selected_startup['event']
                    
    def update_events(self, battle_index: int, startup_index: int):
        # atualiza os eventos disponíveis
        try:
            availabe_events = self.tournament.get_available_events(battle_index, startup_index)
            self.event_combobox["values"] = availabe_events
            
            if availabe_events:
                self.event_combobox.set(availabe_events[0]) 
                self.apply_event_button.config(state=tk.NORMAL)       
            else:
                self.event_combobox.set('')
                self.apply_event_button.config(state=tk.DISABLED)
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to update events: {str(e)}")

    def resolve_battle(self):
        #finaliza a batalha utilizando o Shark Fight
        try:
            selected_item = self.battle_tree.focus()
            if not selected_item:
                messagebox.showwarning("You must select a battle!")
                return
            
            battle_index = int(self.battle_tree.item(selected_item, "tags")[0])
            
            #verificação de segurança adicional
            if battle_index >= len(self.tournament.pending_battles):
                raise IndexError("Index out of range!")
            
            #finaliza a batalha
            winner = self.tournament.shark_fight(battle_index)
            
            #atualiza interface
            self.update_battle_list()
            
            #mostra resultado da batalha
            message = f"Battle resolved! {winner.name} won with {winner.points} points!"
            battle = self.tournament.ended_battles[-1]  # a última batalha finalizada
            if battle.startup1.points == battle.startup2.points:
                message += "\nThe battle was resolved with a Shark Fight!"
                
            messagebox.showinfo("Battle result", message)
            
            # verifica se o torneio acabou  
            if self.tournament.champion:
                messagebox.showinfo(f"The champion is {self.tournament.champion.name}!")
                
                self.resolve_button.config(state=tk.DISABLED)
                self.apply_event_button.config(state=tk.DISABLED)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()