import os
from google import genai
from dotenv import load_dotenv

# Carrega ambiente
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

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
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    texto_resposta = extrair_texto(response)
    if not texto_resposta:
        raise RuntimeError("Resposta vazia do Gemini.")
    
    return texto_resposta