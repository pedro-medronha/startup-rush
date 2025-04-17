import tkinter as tk
from tkinter import messagebox
from models.rush import Rush

class Main:
    def __init__(self, root):
        self.root = root
        self.tournament = Rush()
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Startup Rush - Cadastro")
        self.root.geometry("400x300")
        
        # Widgets
        tk.Label(self.root, text="Nome:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        
        tk.Label(self.root, text="Slogan:").pack()
        self.slogan_entry = tk.Entry(self.root)
        self.slogan_entry.pack()
        
        tk.Label(self.root, text="Ano de Fundação:").pack()
        self.year_entry = tk.Entry(self.root)
        self.year_entry.pack()
        
        tk.Button(
            self.root, 
            text="Cadastrar Startup", 
            command=self.register_startup
        ).pack(pady=10)
        
        # Lista de startups cadastradas
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(expand=True, fill=tk.BOTH)
        
        self.status_label = tk.Label(self.root, text=f"Startups: {len(self.tournament.startups)}/8")
        self.status_label.pack()

        # Atualize após cada cadastro:
        self.status_label.config(text=f"Startups: {len(self.tournament.startups)}/8")
    
    def register_startup(self):
        try:
            name = self.name_entry.get()
            slogan = self.slogan_entry.get()
            year = int(self.year_entry.get())
            
            startup = self.tournament.add_startup(name, slogan, year)
            self.listbox.insert(tk.END, f"{startup.name} ({startup.foundation_year})")
            
            # Limpa os campos
            self.name_entry.delete(0, tk.END)
            self.slogan_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()