# gui.py

import tkinter as tk
from tkinter import messagebox
from auxiliar import Cpf, Arquivo

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Validador de CPF")
        self.geometry("300x200")
        self.arquivo = Arquivo()
        self.create_widgets()

    def create_widgets(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Sair", command=self.on_exit)
        self.label = tk.Label(self, text="Digite o CPF:")
        self.label.pack(pady=10)
        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)
        self.button = tk.Button(self, text="Validar", command=self.validate_cpf)
        self.button.pack(pady=10)

    def validate_cpf(self):
        cpf_input = self.entry.get()
        cpf_obj = Cpf(cpf_input)
        cpf_obj.validate()
        if cpf_obj.is_valid_format:
            if cpf_obj.is_valid_cpf:
                messagebox.showinfo("Resultado", f"{cpf_obj.formatted_cpf}\n{cpf_obj.message}")
                self.arquivo.save_valid(cpf_obj)
            else:
                messagebox.showwarning("Resultado", f"{cpf_obj.formatted_cpf}\n{cpf_obj.message}")
                self.arquivo.log_error(cpf_obj)
        else:
            messagebox.showerror("Erro", cpf_obj.message)
            self.arquivo.log_error(cpf_obj)

    def on_exit(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()
