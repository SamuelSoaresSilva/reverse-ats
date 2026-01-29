## 🛠️ Pré-requisitos

* [Python 3.10+](https://www.python.org/downloads/)
* Uma chave de API do Google Gemini (obtenha em [Google AI Studio](https://aistudio.google.com/))

## 🚀 Instalação

1. **Clone:**
```bash
git clone https://github.com/seu-usuario/reverse-ats.git
cd reverse-ats

```


2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

```


3. **Instale as dependências:**
```bash
pip install google-genai python-dotenv

```


> **Nota:** O projeto utiliza o Tkinter para a interface gráfica, que geralmente já vem instalado com o Python. Caso encontre erros no Linux, utilize `sudo apt-get install python3-tk`.



## ⚙️ Configuração

O projeto está configurado para ignorar ficheiros sensíveis. Crie um ficheiro chamado `.env` na raiz do projeto e adicione sua chave:

```env
GEMINI_API_KEY=SUA_CHAVE_AQUI

```

## 💻 Como rodar

```bash
python main.py

```
