import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from services import gerar_material 

class AppATS:
    def __init__(self, root):
        self.root = root
        self.root.title("Reverse ATS - Otimizador de Currículo")
        self.root.geometry("900x850")
        self.setup_ui()

    def setup_ui(self):
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
            messagebox.showinfo("Sucesso", "Texto copiado!")

    def iniciar_geracao(self):
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