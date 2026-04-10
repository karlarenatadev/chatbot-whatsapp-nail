"""
main.py — Loop principal do chatbot via Selenium + WhatsApp Web.

Como funciona:
  1. Abre o Chrome com perfil salvo (QR Code só na 1ª vez).
  2. Fica em loop verificando conversas não lidas.
  3. Ao encontrar uma, lê o texto, processa com a IA e envia a resposta.

Como rodar:
  python main.py

Para parar:
  Ctrl + C no terminal.
"""

import time
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

from whatsapp import (
    criar_driver,
    aguardar_whatsapp,
    buscar_conversas_nao_lidas,
    ler_ultima_mensagem,
    enviar_resposta,
)
from brain import processar_mensagem

# ============================================================
# CONFIGURAÇÕES DO LOOP
# ============================================================

# Intervalo (em segundos) entre cada varredura de mensagens não lidas
INTERVALO_VERIFICACAO = 5

# Pausa após abrir uma conversa (para o conteúdo carregar)
PAUSA_APOS_CLICAR = 2

# Pausa após enviar resposta (para evitar envios duplicados)
PAUSA_APOS_RESPONDER = 3

# ============================================================
# CONTROLE DE MENSAGENS JÁ PROCESSADAS
# Guarda o último texto respondido por contato para evitar
# responder a mesma mensagem duas vezes.
# ============================================================

_ultima_msg_respondida: dict[str, str] = {}


def ja_respondido(nome: str, texto: str) -> bool:
    return _ultima_msg_respondida.get(nome) == texto


def marcar_respondido(nome: str, texto: str):
    _ultima_msg_respondida[nome] = texto


# ============================================================
# LOOP PRINCIPAL
# ============================================================

def loop_principal(driver):
    print("\n[BOT] 🚀 Bot iniciado! Monitorando mensagens...\n")

    while True:
        try:
            conversas = buscar_conversas_nao_lidas(driver)

            if conversas:
                print(f"[BOT] 📬 {len(conversas)} conversa(s) não lida(s) encontrada(s).")

                for conversa in conversas:
                    try:
                        # 1. Clicar na conversa
                        conversa.click()
                        time.sleep(PAUSA_APOS_CLICAR)

                        # 2. Ler nome e última mensagem
                        nome, texto = ler_ultima_mensagem(driver)

                        if not texto:
                            print(f"[BOT] ⚠️  Conversa de '{nome}' sem texto legível. Pulando.")
                            continue

                        # 3. Verificar se já respondemos essa mensagem
                        if ja_respondido(nome, texto):
                            print(f"[BOT] ↩️  '{nome}' — mensagem já respondida. Pulando.")
                            continue

                        print(f"[BOT] 💬 '{nome}' disse: {texto[:80]}")

                        # 4. Processar com a IA (brain.py)
                        resposta = processar_mensagem(texto, nome)

                        # 5. MODO SILENCIOSO (Apenas simula o envio)
                        print("\n" + "="*40)
                        print(f"🤖 O BOT RESPONDERIA PARA {nome}:")
                        print(resposta)
                        print("="*40 + "\n")
                        
                        # Marcamos como sucesso automaticamente para ele não ficar 
                        # lendo a mesma mensagem em loop eterno
                        sucesso = True 

                        if sucesso:
                            marcar_respondido(nome, texto)
                            # time.sleep(PAUSA_APOS_RESPONDER) # Tiramos a pausa pois não há digitação

                    except Exception as e:
                        print(f"[BOT] ❌ Erro ao processar conversa: {e}")
                        continue

            else:
                # Nenhuma mensagem nova — aguarda próximo ciclo
                print(f"[BOT] 🔍 Nenhuma mensagem nova. Verificando em {INTERVALO_VERIFICACAO}s...", end="\r")

        except KeyboardInterrupt:
            raise  # Propaga para o bloco externo encerrar corretamente

        except Exception as e:
            print(f"\n[BOT] ⚠️  Erro no loop: {e}. Continuando...")

        time.sleep(INTERVALO_VERIFICACAO)


# ============================================================
# ENTRADA DO PROGRAMA
# ============================================================

def main():
    print("=" * 50)
    print("  💅 Nail Designer Bot — WhatsApp Web + IA")
    print("=" * 50)
    print("\n[BOT] Iniciando Chrome...")

    driver = criar_driver()

    try:
        # Abre o WhatsApp Web
        driver.get("https://web.whatsapp.com")

        # Aguarda carregar (na 1ª vez: escaneie o QR Code)
        carregado = aguardar_whatsapp(driver, timeout=90)

        if not carregado:
            print("\n[BOT] ❌ WhatsApp Web não carregou. Verifique o QR Code e tente novamente.")
            return

        # Inicia o loop de monitoramento
        loop_principal(driver)

    except KeyboardInterrupt:
        print("\n\n[BOT] 🛑 Bot encerrado pelo usuário. Até logo!")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
