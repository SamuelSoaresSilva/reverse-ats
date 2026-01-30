import re
import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from google import genai
from dotenv import load_dotenv

# =========================
# CONFIGURAÇÃO E AMBIENTE
# =========================

# Carrega as variáveis do arquivo .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Erro: GEMINI_API_KEY não encontrada no arquivo .env")

# Inicializa o cliente Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# =========================
# LÓGICA DE PROCESSAMENTO
# =========================

def extrair_texto(response):
    """Extrai texto do response do google.genai de forma robusta."""
    if hasattr(response, "text") and response.text:
        return response.text.strip()
    
    textos = []
    if hasattr(response, "candidates"):
        for candidate in response.candidates:
            content = getattr(candidate, "content", None)
            if content and hasattr(content, "parts"):
                for part in content.parts:
                    if hasattr(part, "text") and part.text:
                        textos.append(part.text)
    return "\n".join(textos).strip()

def gerar_material(curriculo, contexto, descricao_vaga):
    """Envia os dados ao Gemini e processa o retorno."""
    def normalizar(texto, fallback):
        texto = (texto or "").strip()
        if not texto or "cole aqui" in texto.lower():
            return fallback
        return texto

    curriculo = normalizar(curriculo, "Profissional de TI com experiência geral.")
    contexto = normalizar(contexto, "Busca de novas oportunidades.")
    descricao_vaga = normalizar(descricao_vaga, "Vaga na área de tecnologia.")

    prompt = f"""
Você é um especialista em recrutamento e RH. Analise as informações e gere conteúdos claros.
IMPORTANTE: Não invente dados, não use markdown, e retorne apenas no formato solicitado.

CURRÍCULO: {curriculo}
CONTEXTO: {contexto}
VAGA: {descricao_vaga}

FORMATO OBRIGATÓRIO:
--- PRETENSÃO SALARIAL ---
--- CURRÍCULO ADAPTADO ---
--- POR QUE ME ESCOLHER PARA A VAGA ---
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview", # Versão estável e rápida
        contents=prompt,
    )

    texto_resposta = extrair_texto(response)
    if not texto_resposta:
        raise RuntimeError("Resposta vazia do Gemini.")
    
    return texto_resposta

# =========================
# INTERFACE GRÁFICA (GUI)
# =========================

class AppATS:
    def __init__(self, root):
        self.root = root
        self.root.title("Reverse ATS - Otimizador de Currículo")
        self.root.geometry("900x850")
        
        self.setup_ui()

    def setup_ui(self):
        # Estilo de labels
        lbl_style = {"font": ("Arial", 10, "bold"), "anchor": "w", "padx": 10}
        
        tk.Label(self.root, text="Currículo Atual", **lbl_style).pack(fill="x")
        self.txt_curriculo = scrolledtext.ScrolledText(self.root, height=8)
        self.txt_curriculo.pack(fill="both", padx=10, pady=5)

        tk.Label(self.root, text="Contexto Profissional", **lbl_style).pack(fill="x")
        self.txt_contexto = scrolledtext.ScrolledText(self.root, height=4)
        self.txt_contexto.pack(fill="both", padx=10, pady=5)

        tk.Label(self.root, text="Descrição da Vaga", **lbl_style).pack(fill="x")
        self.txt_descricao = scrolledtext.ScrolledText(self.root, height=6)
        self.txt_descricao.pack(fill="both", padx=10, pady=5)

        # Frame de Botões
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)

        self.btn_gerar = tk.Button(
            frame_botoes, text="🚀 Gerar Material", command=self.iniciar_geracao,
            bg="#2b7cff", fg="white", font=("Arial", 10, "bold"), width=20
        )
        self.btn_gerar.pack(side="left", padx=5)

        tk.Button(
            frame_botoes, text="🗑️ Limpar Campos", command=self.limpar_campos,
            bg="#f44336", fg="white", width=15
        ).pack(side="left", padx=5)

        tk.Label(self.root, text="Resultado Gerado", **lbl_style).pack(fill="x")
        self.txt_saida = scrolledtext.ScrolledText(self.root, height=15, bg="#f9f9f9")
        self.txt_saida.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Button(
            self.root, text="📋 Copiar Resultado", command=self.copiar_texto,
            bg="#4CAF50", fg="white"
        ).pack(pady=5)

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
            messagebox.showinfo("Sucesso", "Texto copiado para a área de transferência!")

    def iniciar_geracao(self):
        """Inicia o processamento em uma thread separada para não travar a UI."""
        self.btn_gerar.config(state="disabled", text="⏳ Processando...")
        
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
        self.btn_gerar.config(state="normal", text="🚀 Gerar Material")

    def finalizar_erro(self, erro):
        messagebox.showerror("Erro", erro)
        self.btn_gerar.config(state="normal", text="🚀 Gerar Material")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppATS(root)
    root.mainloop()