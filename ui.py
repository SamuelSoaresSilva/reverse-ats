import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk 
import pygame  # Biblioteca para tocar o MP3
import os      # Para verificar se o arquivo existe
from services import gerar_material 

# Configuração de Aparência Material 3 (Light)
ctk.set_appearance_mode("Light")  

class AppATS:
    def __init__(self, root):
        self.root = root
        self.root.title("Fudedor de Robo 2000")
        self.root.geometry("950x920")
        
        # Inicializa o mixer de áudio
        pygame.mixer.init()
        
        # Paleta Material Design 3
        self.bg_color = "#F7F9FF"
        self.card_color = "#FFFFFF"
        self.primary_color = "#5b49cd"
        self.secondary_container = "#D8E2FF"
        self.text_main = "#1A1C1E"
        
        self.root.configure(fg_color=self.bg_color)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.setup_ui()

    def setup_ui(self):
        # Container Principal
        self.main_container = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Cabeçalho
        ctk.CTkLabel(
            self.main_container, 
            text="Fudedor de Robo 2000", 
            font=("Roboto", 30, "bold"),
            text_color=self.text_main
        ).grid(row=0, column=0, pady=(0, 24), sticky="w")

        card_settings = {"fg_color": self.card_color, "corner_radius": 28, "border_width": 0}
        lbl_font = ("Roboto", 14, "bold")

        # --- Seção: Currículo ---
        self.card_1 = ctk.CTkFrame(self.main_container, **card_settings)
        self.card_1.grid(row=1, column=0, sticky="ew", pady=8)
        self.card_1.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.card_1, text="📄 Currículo Atual", font=lbl_font, text_color=self.primary_color).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 8))
        self.txt_curriculo = ctk.CTkTextbox(self.card_1, height=200, fg_color="#F1F3F9", corner_radius=16)
        self.txt_curriculo.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="ew")

        # --- Seção: Contexto e Vaga ---
        self.row_inputs = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.row_inputs.grid(row=2, column=0, sticky="ew", pady=8)
        self.row_inputs.grid_columnconfigure((0, 1), weight=1)

        self.card_ctx = ctk.CTkFrame(self.row_inputs, **card_settings)
        self.card_ctx.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ctk.CTkLabel(self.card_ctx, text="💼 Contexto", font=lbl_font, text_color=self.primary_color).pack(anchor="w", padx=24, pady=(20, 8))
        self.txt_contexto = ctk.CTkTextbox(self.card_ctx, height=200, fg_color="#F1F3F9", corner_radius=16)
        self.txt_contexto.pack(fill="both", padx=24, pady=(0, 20))

        self.card_vaga = ctk.CTkFrame(self.row_inputs, **card_settings)
        self.card_vaga.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ctk.CTkLabel(self.card_vaga, text="🎯 Vaga", font=lbl_font, text_color=self.primary_color).pack(anchor="w", padx=24, pady=(20, 8))
        self.txt_descricao = ctk.CTkTextbox(self.card_vaga, height=200, fg_color="#F1F3F9", corner_radius=16)
        self.txt_descricao.pack(fill="both", padx=24, pady=(0, 20))

        # --- Ações ---
        self.frame_actions = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frame_actions.grid(row=3, column=0, pady=32)

        self.btn_gerar = ctk.CTkButton(
            self.frame_actions, text="🚀 Gerar Otimização", command=self.iniciar_geracao,
            font=("Roboto", 15, "bold"), height=56, width=280, corner_radius=28,
            fg_color=self.primary_color, hover_color="#4839a9"
        )
        self.btn_gerar.pack(side="left", padx=12)

        self.btn_limpar = ctk.CTkButton(
            self.frame_actions, text="Limpar", command=self.limpar_campos,
            fg_color=self.secondary_container, text_color="#001D3E", 
            width=120, height=56, corner_radius=28
        )
        self.btn_limpar.pack(side="left", padx=12)

        # --- Seção: Resultado ---
        self.card_res = ctk.CTkFrame(self.main_container, **card_settings)
        self.card_res.grid(row=4, column=0, sticky="ew", pady=8)
        self.card_res.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.card_res, text="✨ Sugestões da IA", font=lbl_font, text_color=self.primary_color).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 8))
        self.txt_saida = ctk.CTkTextbox(self.card_res, height=350, fg_color="#F1F3F9", corner_radius=16)
        self.txt_saida.grid(row=1, column=0, padx=24, pady=(0, 16), sticky="ew")

        self.btn_copiar = ctk.CTkButton(
            self.card_res, text="📋 Copiar Resultado", command=self.copiar_texto,
            fg_color="transparent", text_color=self.primary_color, 
            hover_color="#E0E7FF", border_width=1, border_color=self.primary_color,
            corner_radius=20, height=40
        )
        self.btn_copiar.grid(row=2, column=0, pady=(0, 24))

    def tocar_sino(self):
        try:
            if os.path.exists("sound/tu.mp3"):
                pygame.mixer.music.load("sound/tu.mp3")
                pygame.mixer.music.play()
        except Exception as e:
            print(f"Erro ao tocar áudio: {e}")

    def limpar_campos(self):
        self.txt_curriculo.delete("1.0", tk.END)
        self.txt_contexto.delete("1.0", tk.END)
        self.txt_descricao.delete("1.0", tk.END)
        self.txt_saida.delete("1.0", tk.END)

    def copiar_texto(self):
        conteudo = self.txt_saida.get("1.0", tk.END).strip()
        if conteudo:
            self.root.clipboard_clear()
            self.root.clipboard_append(conteudo)
            messagebox.showinfo("Sucesso", "Copiado!")

    def iniciar_geracao(self):
        self.btn_gerar.configure(state="disabled", text="⏳ Analisando...")
        curriculo = self.txt_curriculo.get("1.0", tk.END)
        contexto = self.txt_contexto.get("1.0", tk.END)
        descricao = self.txt_descricao.get("1.0", tk.END)
        thread = threading.Thread(target=self.processar, args=(curriculo, contexto, descricao))
        thread.start()

    def processar(self, curriculo, contexto, descricao):
        try:
            resultado = gerar_material(curriculo, contexto, descricao)
            self.root.after(0, lambda: self.finalizar_sucesso(resultado))
        except Exception as e:
            self.root.after(0, lambda: self.finalizar_erro(str(e)))

    def finalizar_sucesso(self, resultado):
        self.txt_saida.delete("1.0", tk.END)
        self.txt_saida.insert(tk.END, resultado)
        self.btn_gerar.configure(state="normal", text="🚀 Gerar Otimização")
        self.tocar_sino()

    def finalizar_erro(self, erro):
        messagebox.showerror("Erro", erro)
        self.btn_gerar.configure(state="normal", text="🚀 Gerar Otimização")
