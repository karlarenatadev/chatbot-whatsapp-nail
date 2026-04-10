from fastapi import FastAPI, Request
from brain import processar_mensagem
from whatsapp import enviar_mensagem

app = FastAPI()

# Rota para a Meta verificar seu Webhook (necessário na configuração)
@app.get("/webhook")
async def verify_webhook(request: Request):
    verify_token = "meu_token_secreto_123"
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            return int(challenge)
    return {"status": "error"}, 403

# Rota que RECEBE as mensagens das clientes
@app.post("/webhook")
async def receive_message(request: Request):
    dados = await request.json()
    
    try:
        # Navegando no JSON complexo que o WhatsApp envia
        mensagem_info = dados['entry'][0]['changes'][0]['value']['messages'][0]
        telefone_cliente = mensagem_info['from']
        texto_recebido = mensagem_info['text']['body']
        
        # O bot entra em ação: Pensa -> Busca Info -> Gera Resposta
        resposta = processar_mensagem(texto_recebido, telefone_cliente)
        
        # O bot responde
        enviar_mensagem(telefone_cliente, resposta)
        
    except KeyError:
        # Ignora status de leitura/entrega (que não têm a chave 'messages')
        pass
        
    return {"status": "ok"}