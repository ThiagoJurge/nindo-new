def process_webhook(group_id, message_text):
    # Exemplo de processamento da mensagem
    if message_text.lower() == 'oi':
        return 'Olá, como posso te ajudar?'
    return 'Mensagem recebida!'
