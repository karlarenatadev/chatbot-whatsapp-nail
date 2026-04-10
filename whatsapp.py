import requests

# Tokens fornecidos pelo painel de desenvolvedor da Meta
WHATSAPP_TOKEN = "SEU_TOKEN_DE_ACESSO_AQUI"
PHONE_NUMBER_ID = "SEU_PHONE_NUMBER_ID_AQUI"

def enviar_mensagem(telefone_destino, texto_resposta):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone_destino,
        "type": "text",
        "text": {"body": texto_resposta}
    }
    
    resposta = requests.post(url, headers=headers, json=payload)
    return resposta.status_code