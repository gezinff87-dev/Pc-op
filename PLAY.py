"""
PC Optimizer - Ferramenta de otimização para Windows
Autor: Seu nome
GitHub: github.com/seuusuario/pc-optimizer
"""

import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

class PCOptimizer:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("PC Optimizer v1.0")
        self.janela.geometry("600x500")
        self.janela.configure(bg='#1a1a1a')
        
        # Interface
        tk.Label(self.janela, text="⚡ PC OPTIMIZER ⚡", 
                font=('Arial', 20, 'bold'), bg='#1a1a1a', fg='#00ff00').pack(pady=15)
        
        botoes = [
            ("🗑️ Limpar Arquivos Temporários", self.limpar_temp),
            ("🚀 Gerenciar Inicialização", self.msconfig),
            ("🔧 Reparar Sistema (SFC)", self.sfc),
            ("💾 Otimizar Disco", self.defrag),
            ("📊 Diagnóstico Rápido", self.diagnostico)
        ]
        
        for texto, func in botoes:
            tk.Button(self.janela, text=texto, command=func,
                     bg='#2d2d2d', fg='white', font=('Arial', 11),
                     padx=20, pady=8, cursor='hand2').pack(pady=5, padx=40, fill='x')
        
        self.log = scrolledtext.ScrolledText(self.janela, bg='#0a0a0a', 
                                              fg='#00ff00', font=('Consolas', 9))
        self.log.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.log_msg("✅ PC Optimizer iniciado com sucesso!")
        self.janela.mainloop()
    
    def log_msg(self, msg):
        self.log.insert(tk.END, f'[{datetime.now().strftime("%H:%M:%S")}] {msg}\n')
        self.log.see(tk.END)
    
    def limpar_temp(self):
        self.log_msg("🧹 Limpando arquivos temporários...")
        pasta = os.environ.get('TEMP', '')
        total = 0
        for arq in os.listdir(pasta):
            try:
                caminho = os.path.join(pasta, arq)
                if os.path.isfile(caminho):
                    total += os.path.getsize(caminho)
                    os.remove(caminho)
            except:
                pass
        self.log_msg(f"✅ {total // (1024*1024)} MB liberados")
    
    def msconfig(self):
        self.log_msg("🚀 Abrindo gerenciador de inicialização...")
        os.system("start msconfig")
    
    def sfc(self):
        self.log_msg("🔧 Executando SFC /SCANNOW...")
        os.system("start cmd /k sfc /scannow")
        self.log_msg("✅ Verificação iniciada em nova janela")
    
    def defrag(self):
        self.log_msg("💾 Otimizando disco C:...")
        os.system("start cmd /k defrag C: /O")
    
    def diagnostico(self):
        import platform
        msg = f"""📊 Diagnóstico do Sistema:
        
Sistema: {platform.system()} {platform.release()}
Processador: {platform.processor()}
Arquitetura: {platform.machine()}
Usuário: {os.getlogin()}
        """
        messagebox.showinfo("Diagnóstico", msg)
        self.log_msg("Diagnóstico concluído")

if __name__ == "__main__":
    PCOptimizer()
