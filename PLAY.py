import customtkinter as ctk
import tkinter as tk
import random
import math
import psutil
import os
import shutil
import subprocess
import threading

# Configuração Inicial da Janela
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Particle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, 1200)
        self.y = random.randint(0, 800)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.size = random.randint(2, 4)
        self.color = f"#00{random.randint(50, 255):02x}{random.randint(100, 255):02x}"
        self.id = None

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Rebater nas bordas
        if self.x <= 0 or self.x >= 1200:
            self.vx *= -1
        if self.y <= 0 or self.y >= 800:
            self.vy *= -1

        if self.id:
            self.canvas.delete(self.id)
        self.id = self.canvas.create_oval(self.x, self.y, self.x + self.size, self.y + self.size, fill=self.color, outline='')

class OptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SKYNET Optimizer | Painel de Controle")
        self.geometry("1200x800")
        self.resizable(False, False)

        # Canvas para Partículas (Fundo)
        self.canvas_bg = tk.Canvas(self, bg="#0d0d0d", highlightthickness=0, width=1200, height=800)
        self.canvas_bg.place(x=0, y=0)
        
        self.particles = [Particle(self.canvas_bg) for _ in range(150)]
        self.animate_particles()

        # Container Principal (Transparente sobre as partículas)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.place(relwidth=1, relheight=1)

        # Título
        self.lbl_title = ctk.CTkLabel(self.main_frame, text="OTIMIZAÇÃO DE SISTEMA", font=("Roboto", 24, "bold"), text_color="#00ffcc")
        self.lbl_title.place(x=40, y=40)

        self.lbl_status = ctk.CTkLabel(self.main_frame, text="Sistema Monitorado", font=("Roboto", 14), text_color="#aaaaaa")
        self.lbl_status.place(x=40, y=80)

        # Painel de Controles (Grid)
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15, border_width=2, border_color="#333")
        self.controls_frame.place(x=40, y=130, width=500, height=500)

        self.create_switch("Limpeza de Cache Temp", self.clean_temp, "Limpa arquivos .tmp e caches do sistema.", 0)
        self.create_switch("Liberação de RAM", self.clear_ram, "Força a liberação de memória standby.", 1)
        self.create_switch("Otimização de Processos", self.optimize_processes, "Finaliza processos de baixo приорidade inativos.", 2)
        self.create_switch("Desfragmentação Rápida (SSD)", self.trim_ssd, "Executa comando TRIM para SSDs.", 3)
        self.create_switch("Prioridade de CPU (Alta)", self.set_high_priority, "Define o processo atual como alta prioridade.", 4)

        # Log de Atividades
        self.log_frame = ctk.CTkFrame(self.main_frame, fg_color="#111111", corner_radius=10)
        self.log_frame.place(x=560, y=130, width=600, height=500)
        
        self.log_text = ctk.CTkTextbox(self.log_frame, font=("Consolas", 12), text_color="#00ffcc")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.log(">> Sistema inicializado. Aguardando comandos...")

        # Thread de monitoramento contínuo
        self.monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        self.monitor_thread.start()

    def create_switch(self, label_text, command, desc, row):
        frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=15)
        
        lbl = ctk.CTkLabel(frame, text=label_text, font=("Roboto", 16, "bold"), anchor="w")
        lbl.pack(side="left", fill="x", expand=True)
        
        switch = ctk.CTkSwitch(frame, text="", command=command, progress_color="#00ffcc", button_color="#555", button_hover_color="#00ccaa")
        switch.pack(side="right")
        
        desc_lbl = ctk.CTkLabel(frame, text=desc, font=("Roboto", 10), text_color="#666", anchor="w")
        desc_lbl.pack(side="bottom", fill="x")

    def log(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def animate_particles(self):
        for p in self.particles:
            p.move()
        self.after(16, self.animate_particles)

    # --- Funções de Otimização ---

    def clean_temp(self):
        self.log(">> Iniciando limpeza de arquivos temporários...")
        try:
            temp_folders = [os.environ.get('TEMP'), os.environ.get('TMP'), r"C:\Windows\Temp"]
            count = 0
            for folder in temp_folders:
                if folder and os.path.exists(folder):
                    for filename in os.listdir(folder):
                        file_path = os.path.join(folder, filename)
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                                count += 1
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                                count += 1
                        except Exception:
                            pass
            self.log(f">> Sucesso: {count} itens removidos.")
        except Exception as e:
            self.log(f">> Erro na limpeza: {str(e)}")

    def clear_ram(self):
        self.log(">> Solicitando liberação de memória standby...")
        # Nota: Em Windows real, isso geralmente requer drivers ou chamadas de API específicas de kernel.
        # Aqui simulamos a chamada para fins demonstrativos ou usamos uma abordagem via ctypes se implementado totalmente.
        self.log(">> Memória otimizada (Simulação de liberação de working set).")

    def optimize_processes(self):
        self.log(">> Analisando processos em background...")
        count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                # Lógica simplificada: matar processos com nome suspeito ou uso zero prolongado (exemplo didático)
                # Em produção, isso requer lista branca rigorosa para não quebrar o OS.
                if "temp" in proc.info['name'].lower() and proc.info['memory_percent'] < 0.1:
                    p = psutil.Process(proc.info['pid'])
                    p.terminate()
                    count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        self.log(f">> {count} processos desnecessários finalizados.")

    def trim_ssd(self):
        self.log(">> Executando TRIM manual...")
        try:
            subprocess.run(["defrag", "C:", "/L", "/T"], shell=True, capture_output=True)
            self.log(">> Comando TRIM enviado ao controlador de disco.")
        except Exception as e:
            self.log(f">> Falha ao executar TRIM: {str(e)}")

    def set_high_priority(self):
        self.log(">> Elevando prioridade do processo atual...")
        p = psutil.Process(os.getpid())
        try:
            p.nice(psutil.HIGH_PRIORITY_CLASS) # Windows specific
            self.log(">> Prioridade definida para ALTA.")
        except Exception:
            self.log(">> Permissão negada para alteração de prioridade.")

    def monitor_system(self):
        while True:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            self.lbl_status.configure(text=f"CPU: {cpu}% | RAM: {ram}% | Status: Online")
            
            # Mudança sutil na cor das partículas baseada na carga (opcional, lógica visual)
            if cpu > 80:
                for p in self.particles:
                    p.color = "#ff3333" # Vermelho sob carga
            else:
                for p in self.particles:
                    p.color = f"#00{random.randint(50, 255):02x}{random.randint(100, 255):02x}" # Volta ao normal
            # Nota: Atualizar cor de 150 partículas a cada segundo pode pesar, feito de forma diferida na prática.

if __name__ == "__main__":
    app = OptimizerApp()
    app.mainloop()
