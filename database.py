"""
database.py — Base de conhecimento da @naildesignerjuli (Juliana)
Catu - Bahia
"""

# ============================================================
# DADOS DO ESTÚDIO
# ============================================================

STUDIO = {
    "nome":         "Nail Designer Juli",
    "profissional": "Juliana",
    "instagram":    "@naildesignerjuli",
    "telefone":     "(71) 99643-1107",
    "email":        "julisacra57@gmail.com",
    "cidade":       "Catu - Bahia - Brasil",
    "pix":          "julisacra57@gmail.com",
}

# ============================================================
# SERVIÇOS E PREÇOS
# ============================================================

SERVICOS = [
    {
        "nome":  "Alongamento Molde F1",
        "preco": 150.00,
        "obs":   "",
    },
    {
        "nome":  "Alongamento Fibra de Vidro",
        "preco": 170.00,
        "obs":   "",
    },
    {
        "nome":  "Esmaltação em Gel",
        "preco": 65.00,
        "obs":   "",
    },
    {
        "nome":  "Banho em Gel",
        "preco": 90.00,
        "obs":   "",
    },
    {
        "nome":  "Manutenção Molde F1",
        "preco": None,
        "obs":   "Valores variados — consultar no WhatsApp",
    },
    {
        "nome":  "Manutenção Fibra de Vidro",
        "preco": None,
        "obs":   "Valores variados — consultar no WhatsApp",
    },
]

# ============================================================
# FORMAS DE PAGAMENTO
# ============================================================

PAGAMENTOS = [
    "PIX (julisacra57@gmail.com)",
    "Dinheiro",
    "Cartão de débito (acréscimo na maquininha)",
    "Cartão de crédito (acréscimo na maquininha)",
]

# ============================================================
# POLÍTICA DE AGENDAMENTO
# ============================================================

POLITICAS = {
    "sinal": (
        "Para confirmar o horário é solicitado um sinal de R$ 50,00. "
        "Esse valor é abatido integralmente no total do procedimento no dia."
    ),
    "cancelamento": (
        "Remarcações ou cancelamentos devem ser feitos com no mínimo 24 horas de antecedência."
    ),
    "no_show": (
        "Não comparecimento sem aviso prévio resulta na perda do valor do sinal. "
        "Um novo agendamento exigirá novo pagamento de sinal."
    ),
    "atraso": (
        "Tolerância máxima de 15 minutos. Após esse período o horário será cancelado "
        "e o sinal não será reembolsado."
    ),
    "manutencao_outra": (
        "Não realizamos manutenção em procedimentos feitos por outra profissional. "
        "Nesses casos é feita remoção completa e nova aplicação."
    ),
    "acompanhantes": (
        "Pedimos que venha sem acompanhantes. O ambiente é preparado para uma "
        "experiência tranquila e focada no seu conforto."
    ),
}

# ============================================================
# COMO FUNCIONA O ATENDIMENTO
# ============================================================

COMO_FUNCIONA = [
    {
        "etapa":     "1. Agendamento",
        "descricao": (
            "Entre em contato pelo WhatsApp para consultar disponibilidade e reservar seu horário. "
            "Em caso de dúvidas sobre qual técnica escolher, a Juliana está à disposição para uma consultoria."
        ),
    },
    {
        "etapa":     "2. Confirmação",
        "descricao": (
            "Após escolher o horário, é solicitado um sinal de R$ 50,00 via PIX ou dinheiro "
            "para garantir sua reserva. O valor é abatido no total no dia do atendimento."
        ),
    },
    {
        "etapa":     "3. Atendimento",
        "descricao": (
            "O momento é seu! Venha sem acompanhantes para uma experiência tranquila e relaxante, "
            "com foco total nos detalhes e no seu conforto."
        ),
    },
    {
        "etapa":     "4. Cuidado pós-serviço",
        "descricao": (
            "Ao final do serviço você recebe orientações detalhadas de pós-cuidado "
            "para manter o alongamento perfeito e saudável até a próxima manutenção."
        ),
    },
]

# ============================================================
# FAQ
# ============================================================

FAQ = [
    {
        "pergunta": "Como faço para agendar?",
        "resposta": (
            "É só me chamar aqui no WhatsApp! Verifico a disponibilidade e, "
            "para confirmar o horário, solicito um sinal de R$ 50,00 que é descontado no dia. 💅"
        ),
    },
    {
        "pergunta": "Qual a diferença entre Molde F1 e Fibra de Vidro?",
        "resposta": (
            "O Molde F1 usa uma estrutura de molde descartável para criar o comprimento. "
            "A Fibra de Vidro usa uma manta de fibra que dá resistência extra à unha. "
            "Posso te ajudar a escolher a melhor técnica para o seu caso! 😊"
        ),
    },
    {
        "pergunta": "Fazem manutenção de serviço feito por outra profissional?",
        "resposta": (
            "Não realizamos manutenção em procedimentos feitos por outra profissional. "
            "Nesses casos fazemos a remoção completa e uma nova aplicação. "
            "Me chama para conversarmos sobre o melhor caminho para suas unhas! 💕"
        ),
    },
    {
        "pergunta": "Posso levar acompanhante?",
        "resposta": (
            "Pedimos que venha sozinha. O ambiente é preparado para que seu atendimento "
            "seja uma pausa relaxante e especial só para você. 🌸"
        ),
    },
    {
        "pergunta": "E se eu precisar cancelar?",
        "resposta": (
            "Imprevistos acontecem! Só te peço que avise com pelo menos 24 horas de antecedência "
            "para remarcar sem perda do sinal. ❤️"
        ),
    },
    {
        "pergunta": "Qual o valor da manutenção?",
        "resposta": (
            "Os valores de manutenção variam conforme o estado das unhas. "
            "Me chama no WhatsApp para eu te passar o valor certinho! 💅"
        ),
    },
]

# ============================================================
# FUNÇÕES DE BUSCA — usadas pelo brain.py
# ============================================================

def buscar_informacao_servico(texto: str) -> str | None:
    """Busca um serviço específico mencionado no texto da cliente."""
    texto = texto.lower()

    palavras_chave = {
        "molde":  "Alongamento Molde F1",
        "f1":     "Alongamento Molde F1",
        "fibra":  "Alongamento Fibra de Vidro",
        "vidro":  "Alongamento Fibra de Vidro",
        "gel":    "Esmaltação em Gel",
        "esmal":  "Esmaltação em Gel",
        "banho":  "Banho em Gel",
        "manut":  "Manutenção",
    }

    nome_encontrado = None
    for chave, nome in palavras_chave.items():
        if chave in texto:
            nome_encontrado = nome
            break

    if not nome_encontrado:
        return None

    # Manutenção sem serviço específico
    if nome_encontrado == "Manutenção":
        return (
            "Os valores de manutenção variam conforme o estado das unhas. 🌸\n"
            "Me chama aqui no WhatsApp para eu te passar o valor certinho!\n\n"
            f"📲 {STUDIO['telefone']}"
        )

    for s in SERVICOS:
        if nome_encontrado.lower() in s["nome"].lower():
            preco_str = f"R$ {s['preco']:.2f}" if s["preco"] else "Consultar no WhatsApp"
            return (
                f"✨ *{s['nome']}*\n"
                f"💰 Valor: {preco_str}\n"
                + (f"📌 {s['obs']}\n" if s["obs"] else "")
                + f"\nQuer agendar? Me conta qual dia fica melhor! 😊"
            )

    return None


def listar_todos_servicos() -> str:
    linhas = ["💅 *Serviços disponíveis:*\n"]
    for s in SERVICOS:
        preco = f"R$ {s['preco']:.2f}" if s["preco"] else "Consultar"
        linhas.append(f"• {s['nome']}: {preco}")
    linhas.append("\nQual te interessa? Me conta e eu te ajudo! 😍")
    return "\n".join(linhas)


def listar_pagamentos() -> str:
    metodos = "\n".join(f"• {p}" for p in PAGAMENTOS)
    return f"💳 *Formas de Pagamento:*\n\n{metodos}"


def get_contexto_completo() -> str:
    """Contexto completo para alimentar a IA."""
    servicos_fmt = "\n".join(
        f"  - {s['nome']}: {'R$ ' + str(s['preco']) if s['preco'] else 'Consultar'}"
        + (f" ({s['obs']})" if s["obs"] else "")
        for s in SERVICOS
    )
    pagamentos_fmt = "\n".join(f"  - {p}" for p in PAGAMENTOS)
    politicas_fmt  = "\n".join(f"  - {v}" for v in POLITICAS.values())
    faq_fmt        = "\n".join(
        f"  P: {f['pergunta']}\n  R: {f['resposta']}" for f in FAQ
    )
    como_fmt = "\n".join(
        f"  {e['etapa']}: {e['descricao']}" for e in COMO_FUNCIONA
    )

    return f"""
PROFISSIONAL: {STUDIO['profissional']} — {STUDIO['instagram']}
Telefone / WhatsApp: {STUDIO['telefone']}
Email: {STUDIO['email']}
Cidade: {STUDIO['cidade']}
PIX: {STUDIO['pix']}

SERVIÇOS E PREÇOS:
{servicos_fmt}

COMO FUNCIONA O ATENDIMENTO:
{como_fmt}

FORMAS DE PAGAMENTO:
{pagamentos_fmt}

POLÍTICAS:
{politicas_fmt}

PERGUNTAS FREQUENTES:
{faq_fmt}
""".strip()
