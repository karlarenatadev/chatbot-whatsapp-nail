from database import buscar_informacao_servico

def processar_mensagem(texto_usuario, remetente):
    texto = texto_usuario.lower()
    
    # 1. Pensa: Qual a intenção da cliente?
    if "olá" in texto or "bom dia" in texto or "boa tarde" in texto:
        return "Olá, maravilhosa! 💅 Como posso ajudar com suas unhas hoje? Você quer saber sobre valores, agendamento ou manutenção?"
    
    elif "valor" in texto or "preço" in texto or "custa" in texto:
        # 2. Busca informações no "banco de dados"
        info = buscar_informacao_servico(texto)
        if info:
            return info
        else:
            return "Nós trabalhamos com Fibra de Vidro, Banho de Gel e Esmaltação. Qual desses você gostaria de saber o valor?"
            
    elif "agendar" in texto or "horário" in texto:
        return "Para agendamentos, eu preciso verificar a agenda. Qual dia da semana fica melhor para você?"
        
    else:
        # Resposta padrão de fallback
        return "Ainda estou aprendendo algumas coisas! Você poderia me dizer se precisa de informações sobre valores ou quer marcar um horário?"