from flask import Blueprint, jsonify, request
from .services import process_webhook
from .message_sender import send_message

main_bp = Blueprint('main', __name__)

@main_bp.route("/webhook-receiver", methods=["POST"])
def webhook_receiver():
    try:
        # Captura os dados recebidos no webhook
        data = request.json

        # Armazena os valores em variáveis
        phone = data.get("phone")
        
        if phone == "5522981013352":
            send_message(phone, "Bom dia, carioca!")  # Envia mensagem personalizada

        
        return jsonify({'status': 'sucesso', 'message': data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
