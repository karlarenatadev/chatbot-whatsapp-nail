"""
brain.py — Motor de raciocínio do chatbot da @naildesignerjuli.
"""

import os
import google.generativeai as genai
from database import (
    buscar_informacao_servico,
    listar_todos_servicos,
    listar_pagamentos,
    get_contexto_completo,
    STUDIO,
)

# ============================================================
# CONFIGURAÇÃO DO GOOGLE GEMINI AI
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

# ============================================================
# HISTÓRICO DE CONVERSAS (por nome do contato)
# ============================================================

_historico: dict[str, list[dict]] = {}

def _get_historico(contato: str) -> list[dict]:
    if contato not in _historico:
        _historico[contato] = []
    return _historico[contato]

def _adicionar_ao_historico(contato: str, role: str, content: str):
    # O Gemini usa 'user' e 'model' como roles
    h = _get_historico(contato)
    h.append({"role": role, "parts": [content]})
    
    # Mantém as últimas 10 interações para economizar tokens
    if len(h) > 10:
        _historico[contato] = h[-10:]

# ============================================================
# RESPOSTAS RÁPIDAS (sem IA — instantâneas e sem custo)
# ============================================================

def _resposta_rapida(texto: str) -> str | None:
    t = texto.lower().strip()

    saudacoes = ["olá", "oi", "bom dia", "boa tarde", "boa noite", "hey", "ola", "oii", "oiii", "boa"]
    if any(s in t for s in saudacoes):
        return (
            f"Olá, maravilhosa! 💅✨\n"
            f"Que bom ter você por aqui! Sou a Juliana, a {STUDIO['instagram']}.\n\n"
            f"Como posso te ajudar hoje?\n"
            f"1️⃣ Ver serviços e valores\n"
            f"2️⃣ Agendar horário\n"
            f"3️⃣ Formas de pagamento\n"
            f"4️⃣ Outras dúvidas"
        )

    if t in ["1", "serviços", "servicos", "valores", "preços", "precos", "tabela"]:
        return listar_todos_servicos()

    if t in ["2", "agendar", "agendamento", "marcar", "horário", "horario", "quero agendar"]:
        return (
            "Fico feliz que queira agendar! 🥰\n\n"
            "Me conta:\n"
            "📌 Qual serviço você tem interesse?\n"
            "📅 Qual dia e horário fica melhor pra você?\n\n"
            "Assim eu verifico a minha agenda! 💕"
        )

    if t in ["3", "pagamento", "pagamentos", "pix", "cartão", "cartao", "dinheiro"]:
        return listar_pagamentos()

    resultado = buscar_informacao_servico(texto)
    if resultado:
        return resultado

    if any(p in t for p in ["sinal", "confirmar", "reservar", "entrada", "50"]):
        return (
            "Para confirmar seu horário, solicito um sinal de R$ 50,00. 🌸\n"
            "Esse valor é descontado integralmente no total do procedimento no dia.\n\n"
            f"PIX: {STUDIO['pix']} 💅"
        )

    if any(p in t for p in ["cancelar", "remarcar", "desmarcar", "cancelamento", "remarcação"]):
        return (
            "Imprevistos acontecem, tudo bem! 💕\n\n"
            "Só te peço que avise com pelo menos *24 horas de antecedência* para "
            "remarcar sem perda do sinal.\n\n"
            "Cancelamentos com menos de 24h ou no-show resultam na perda do valor do sinal. 🌸"
        )

    if any(p in t for p in ["atraso", "atrasar", "me atrasei", "atrasada", "atrasei"]):
        return (
            "Temos uma tolerância máxima de 15 minutos. ⏱️\n"
            "Após esse período o horário será cancelado e o sinal não poderá ser reembolsado. 💕"
        )

    if any(p in t for p in ["acompanhante", "filha", "filho", "criança", "crianca", "bebe", "bebê"]):
        return (
            "Para garantir uma experiência tranquila e focada em você, "
            "pedimos que venha sem acompanhantes. 🌸\n\n"
            "Nosso ambiente é preparado para que seu atendimento seja uma pausa "
            "relaxante e especial só sua. 💅"
        )

    if any(p in t for p in ["outra profissional", "outra nail", "já fiz em outro", "fiz em outro"]):
        return (
            "Não realizamos manutenção em procedimentos feitos por outra profissional. 💕\n"
            "Nesses casos fazemos a remoção completa e uma nova aplicação.\n\n"
            "Quer que eu te passe os valores? 😊"
        )

    return None


# ============================================================
# MOTOR GEMINI AI
# ============================================================

def _acionar_gemini(contato: str, mensagem_usuario: str) -> str:
    if not GEMINI_API_KEY:
        return "Ainda estou aprendendo a responder todas as dúvidas! Você poderia me dizer se precisa de informações sobre a *tabela de valores* (digite 1) ou *agendamento* (digite 2)?"

    instrucoes_sistema = f"""Você é a assistente virtual da Juliana, profissional de nail design em Catu-BA ({STUDIO['instagram']}).

Personalidade ao responder:
- Carinhosa, acolhedora e feminina — como a própria Juliana
- Use expressões como "maravilhosa", "linda", com emojis como 💅🌸💕✨ de forma natural
- Respostas CURTAS e diretas — é WhatsApp, não e-mail
- Sem formatação markdown como **negrito** ou # títulos — apenas texto simples
- Nunca invente informações fora do contexto abaixo
- Se não souber algo, indique o Instagram: {STUDIO['instagram']} ou telefone: {STUDIO['telefone']}
- Para agendamentos, colete: qual serviço, qual dia e horário de preferência
- Sempre em português brasileiro, tom próximo e humano

A filosofia da Juliana:
"Não se trata apenas de fazer unhas, mas de como elas fazem você se sentir.
Meu objetivo é transformar o seu estado de espírito — criar um momento só seu."

--- INFORMAÇÕES COMPLETAS DO ESTÚDIO ---
{get_contexto_completo()}
"""

    try:
        modelo = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=instrucoes_sistema
        )
        
        historico = _get_historico(contato)
        chat = modelo.start_chat(history=historico)
        
        resposta = chat.send_message(mensagem_usuario)
        return resposta.text

    except Exception as e:
        print(f"[ERRO Gemini API] {e}")
        return (
            f"Estou com uma instabilidade agora. 😔\n"
            f"Me chama no Instagram: {STUDIO['instagram']} 💅"
        )


# ============================================================
# FUNÇÃO PRINCIPAL — chamada pelo main.py
# ============================================================

def processar_mensagem(texto_usuario: str, contato: str) -> str:
    print(f"[BRAIN] De '{contato}': {texto_usuario}")

    resposta = _resposta_rapida(texto_usuario)

    if resposta is None:
        print(f"[BRAIN] Acionando Gemini para '{contato}'...")
        resposta = _acionar_gemini(contato, texto_usuario)

    _adicionar_ao_historico(contato, "user", texto_usuario)
    _adicionar_ao_historico(contato, "model", resposta)

    print(f"[BRAIN] Resposta: {resposta[:80]}...")
    return resposta