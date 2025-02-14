from flask import Flask, request, jsonify
import logging

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configura o log
logging.basicConfig(level=logging.INFO)

# Rota para receber os webhooks
@app.route('/webhook', methods=['POST'])
def webhook():
    # Verifica se a requisição é POST
    if request.method == 'POST':
        data = request.get_json()
        
        # Exibe os dados recebidos no log
        app.logger.info(f"Recebido webhook: {data}")
        
        # Processar os dados (aqui você pode implementar a lógica de tratamento)
        
        # Retorna uma resposta para confirmar o recebimento
        return jsonify({'status': 'sucesso', 'message': 'Webhook recebido com sucesso'}), 200
    else:
        return jsonify({'status': 'erro', 'message': 'Método inválido'}), 405

if __name__ == '__main__':
    app.run(debug=True, host='::', port=5000)
