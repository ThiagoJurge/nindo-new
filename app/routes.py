from flask import Blueprint, jsonify, request
from .services import process_webhook
from .message_sender import send_message

main_bp = Blueprint('main', __name__)

@main_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()  # <-- Corrigido aqui
    
    if not data:
        return jsonify({'status': 'erro', 'message': 'Requisição inválida'}), 400

    phone = data.get("phone")
    
    if phone == "5522981013352":
        send_message(phone, "Bom dia, carioca!")  # Envia mensagem personalizada
    
    # Se precisar processar a mensagem com outro serviço
    # response_message = process_webhook(phone, data.get("message"))
    
    return jsonify({'status': 'sucesso', 'message': data}), 200
