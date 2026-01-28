

# FUNÇÃO AUXILIAR
# =========================


def extrair_texto(response):
    """
    Extrai texto do response do google.genai de forma robusta.
    """
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


# =========================
# FUNÇÃO PRINCIPAL
# =========================


def gerar_material(curriculo, contexto, descricao_vaga):
    # -------------------------
    # NORMALIZA INPUT
    # -------------------------
    def normalizar(texto, fallback):
        texto = (texto or "").strip()
        if not texto or "cole aqui" in texto.lower():
            return fallback
        return texto


    curriculo = normalizar(
        curriculo,
        "Profissional de TI com experiência em desenvolvimento de software, atuação em projetos variados e foco em boas práticas."
    )


    contexto = normalizar(
        contexto,
        "Profissional em busca de oportunidades alinhadas ao seu perfil técnico e crescimento profissional."
    )


    descricao_vaga = normalizar(
        descricao_vaga,
        "Vaga na área de tecnologia da informação com foco em desenvolvimento, manutenção de sistemas e colaboração em equipe."
    )


    # -------------------------
    # PROMPT
    # -------------------------
    prompt = f"""
Você é um especialista em recrutamento, RH estratégico e copywriting profissional, com ampla experiência em análise de currículos e adequação a vagas de tecnologia.


Analise as informações abaixo e gere conteúdos profissionais, claros e objetivos.


IMPORTANTE:
- Evite linguagem padrão de IAs, como traços e palavras reutilzadas.
- Não inventar e não retornar: experiencias profissionais, formação acadêmica, idiomas.
- Não responder em markdown.
- Nenhuma seção pode ficar vazia.
- Caso alguma informação esteja genérica, crie um conteúdo profissional coerente.
- Não explique o processo.
- Retorne APENAS no formato solicitado.


CURRÍCULO DO CANDIDATO:
{curriculo}


CONTEXTO PROFISSIONAL:
{contexto}


DESCRIÇÃO DA VAGA:
{descricao_vaga}


FORMATO DE RESPOSTA OBRIGATÓRIO:


--- PRETENSÃO SALARIAL ---
(informe uma pretensão salarial compatível com o perfil e a vaga)


--- CURRÍCULO ADAPTADO ---
(currículo completo adaptado à vaga)


--- POR QUE ME ESCOLHER PARA A VAGA ---
(texto persuasivo e profissional)
"""


    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )


    texto_resposta = extrair_texto(response)


    if not texto_resposta:
        raise RuntimeError("Resposta vazia do Gemini após extração.")


    # -------------------------
    # EXTRAÇÃO DAS SEÇÕES
    # -------------------------
    def extrair_secao(titulo):
        padrao = rf"--- {titulo} ---\s*(.*?)(?=\n---|\Z)"
        match = re.search(padrao, texto_resposta, re.DOTALL | re.IGNORECASE)
        if not match or not match.group(1).strip():
            raise RuntimeError(f"Seção '{titulo}' não retornada corretamente.")
        return match.group(1).strip()


    return {
        "pretensao_salarial": extrair_secao("PRETENSÃO SALARIAL"),
        "curriculo_adaptado": extrair_secao("CURRÍCULO ADAPTADO"),
        "porque_escolher": extrair_secao("POR QUE ME ESCOLHER PARA A VAGA"),
        "texto_completo": texto_resposta
    }


# =========================
# EXEMPLO DE USO
# =========================


if __name__ == "__main__":
    curriculo = """ """ 
    contexto = """ """
    descricao_vaga = """ """


    resultado = gerar_material(curriculo, contexto, descricao_vaga)


    print("\n--- PRETENSÃO SALARIAL ---\n")
    print(resultado["pretensao_salarial"])


    print("\n--- CURRÍCULO ADAPTADO ---\n")
    print(resultado["curriculo_adaptado"])


    print("\n--- POR QUE ME ESCOLHER PARA A VAGA ---\n")
    print(resultado["porque_escolher"])
