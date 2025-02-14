import requests

def send_message(number, message):
    # URL da API do Z-API (modifique se necessário)
    api_url = "https://api.z-api.io/instances/3DCD168EA9FE70A00D0956C5A090F8FA/token/D5926B43FE1F841BA8A39F75/send-text"

    # Dados a serem enviados
    payload = {
        "phone": number,  # Número de telefone do destinatário (com DDD e sem espaços ou sinais)
        "message": message  # A mensagem que será enviada
    }

    
    headers = {
            "Client-Token": "F0b7eace040f941ada5ee9d11b5c81c51S",
            "Content-Type": "application/json",
        }

    # Enviar requisição POST
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Levanta um erro se a resposta não for 2xx
        print("Mensagem enviada com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar a mensagem: {e}")