"""
whatsapp.py — Controla o WhatsApp Web via Selenium.

Responsabilidades:
  - Abrir o Chrome com perfil salvo (para não escanear QR toda vez)
  - Ficar em loop monitorando conversas com mensagens não lidas
  - Ler o texto recebido
  - Digitar e enviar a resposta

ATENÇÃO — XPATHs:
  O WhatsApp Web atualiza o HTML com frequência.
  Se o bot parar de funcionar, inspecione a página (F12) e atualize
  as constantes de XPATH abaixo.
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)
from webdriver_manager.chrome import ChromeDriverManager

# ============================================================
# XPATHs DO WHATSAPP WEB
# Se o bot parar de funcionar, atualize estes valores
# inspecionando os elementos em web.whatsapp.com (F12).
# ============================================================

# Conversas com badge de mensagem não lida (bolinhas verdes)
XPATH_CONV_NAO_LIDA = '//span[@aria-label and contains(@aria-label, "mensagen") or @data-testid="icon-unread-count"]/..'

# Alternativa mais robusta — pega qualquer badge numérico na lista
XPATH_BADGE_GERAL = '//span[contains(@aria-label, "não lida") or contains(@aria-label, "unread")]/..'

# Nome/número do remetente no topo da conversa aberta
XPATH_NOME_CONTATO  = '//header//span[@dir="auto" and @title]'

# Último balão de mensagem recebida (não enviada por nós)
XPATH_ULTIMA_MSG    = '(//div[contains(@class,"message-in")]//span[@class="selectable-text"])[last()]'

# Caixa de digitação
XPATH_CAIXA_TEXTO   = '//div[@contenteditable="true"][@data-tab="10"]'

# Botão de enviar (fallback caso o Enter não funcione)
XPATH_BTN_ENVIAR    = '//button[@data-testid="send"]'

# Tela de carregamento inicial do WhatsApp Web
XPATH_TELA_CARREGAMENTO = '//div[@data-testid="intro-md-beta-logo-dark"]'

# ============================================================
# CAMINHO DO PERFIL CHROME (para salvar sessão / evitar QR)
# ============================================================
DIRETORIO_ATUAL = os.path.abspath(os.path.dirname(__file__))
CHROME_PROFILE_PATH = os.path.join(DIRETORIO_ATUAL, "chrome_profile")


# ============================================================
# INICIALIZAR DRIVER
# ============================================================

def criar_driver() -> webdriver.Chrome:
    """
    Cria e retorna o Chrome WebDriver com perfil persistente.
    Na primeira execução: escaneie o QR Code que aparecer.
    Nas próximas, a sessão já estará salva.
    """
    opcoes = Options()
    opcoes.add_experimental_option("detach", True)

    # Perfil persistente — mantém a sessão do WhatsApp Web entre execuções
    opcoes.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
    opcoes.add_argument("--profile-directory=Default")

    opcoes.add_argument("--start-maximized")

    # Desativa notificações do Chrome
    opcoes.add_argument("--disable-notifications")
    opcoes.add_argument("--disable-popup-blocking")

    # Silencia logs desnecessários do Chrome no terminal
    opcoes.add_experimental_option("excludeSwitches", ["enable-logging"])
    opcoes.add_argument("--log-level=3")

    # Desativa notificações do Chrome
    opcoes.add_argument("--disable-notifications")

    servico = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=servico, options=opcoes)
    
    return driver 

# ============================================================
# AGUARDAR CARREGAMENTO DO WHATSAPP WEB
# ============================================================

def aguardar_whatsapp(driver: webdriver.Chrome, timeout: int = 60) -> bool:
    """
    Aguarda o WhatsApp Web carregar completamente.
    Retorna True se carregou, False se deu timeout.
    """
    print("[WA] Aguardando WhatsApp Web carregar...")
    try:
        # Espera a lista de conversas aparecer
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
        )
        print("[WA] ✅ WhatsApp Web carregado!")
        return True
    except TimeoutException:
        print("[WA] ❌ Timeout — verifique se o QR foi escaneado.")
        return False


# ============================================================
# BUSCAR CONVERSAS NÃO LIDAS
# ============================================================

def buscar_conversas_nao_lidas(driver: webdriver.Chrome) -> list:
    """
    Retorna uma lista de elementos (conversas) que possuem badge de não lida.
    """
    try:
        badges = driver.find_elements(By.XPATH, XPATH_BADGE_GERAL)
        conversas = []
        for badge in badges:
            try:
                # Sobe na árvore DOM até encontrar o elemento clicável da conversa
                conversa = badge.find_element(By.XPATH, "./ancestor::div[@role='listitem'][1]")
                conversas.append(conversa)
            except NoSuchElementException:
                continue
        return conversas
    except Exception as e:
        print(f"[WA] Erro ao buscar conversas: {e}")
        return []


# ============================================================
# LER ÚLTIMA MENSAGEM DA CONVERSA ABERTA
# ============================================================

def ler_ultima_mensagem(driver: webdriver.Chrome) -> tuple[str, str]:
    """
    Lê a última mensagem recebida na conversa atualmente aberta.
    Retorna (nome_contato, texto_mensagem).
    """
    try:
        # Nome do contato
        nome_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, XPATH_NOME_CONTATO))
        )
        nome = nome_el.get_attribute("title") or nome_el.text

        # Última mensagem recebida
        msg_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, XPATH_ULTIMA_MSG))
        )
        texto = msg_el.text.strip()

        return nome, texto

    except TimeoutException:
        return "Desconhecido", ""
    except Exception as e:
        print(f"[WA] Erro ao ler mensagem: {e}")
        return "Desconhecido", ""


# ============================================================
# ENVIAR RESPOSTA NA CONVERSA ABERTA
# ============================================================

def enviar_resposta(driver: webdriver.Chrome, texto: str) -> bool:
    """
    Digita e envia uma resposta na conversa atualmente aberta.
    Retorna True se enviou com sucesso.
    """
    try:
        caixa = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_CAIXA_TEXTO))
        )
        caixa.click()

        # Digitar linha a linha (suporte a quebras de linha com Shift+Enter)
        linhas = texto.split("\n")
        for i, linha in enumerate(linhas):
            caixa.send_keys(linha)
            if i < len(linhas) - 1:
                caixa.send_keys(Keys.SHIFT + Keys.ENTER)

        time.sleep(0.4)  # Pequena pausa antes de enviar

        # Enviar com Enter
        caixa.send_keys(Keys.ENTER)

        print(f"[WA] ✅ Resposta enviada.")
        return True

    except TimeoutException:
        print("[WA] ❌ Caixa de texto não encontrada.")
        return False
    except Exception as e:
        print(f"[WA] ❌ Erro ao enviar: {e}")
        return False
