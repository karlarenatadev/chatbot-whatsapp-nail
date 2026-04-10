# Simulando um banco de dados de serviços de uma Nail Designer
SERVICOS = {
    "fibra": {"nome": "Alongamento em Fibra de Vidro", "preco": 150.00, "tempo": "2h30"},
    "gel": {"nome": "Banho de Gel", "preco": 90.00, "tempo": "1h30"},
    "manutencao": {"nome": "Manutenção (Fibra/Gel)", "preco": 80.00, "tempo": "1h45"}
}

def buscar_informacao_servico(palavra_chave):
    for key, info in SERVICOS.items():
        if key in palavra_chave.lower():
            return f"O {info['nome']} custa R$ {info['preco']:.2f} e leva cerca de {info['tempo']}."
    return None