from flask import Blueprint, jsonify, request
from .services import process_webhook
from .message_sender import send_message

main_bp = Blueprint('main', __name__)

@main_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json
    
    phone = data.get("phone")
    if phone == "5522981013352":
        send_message(phone, "bom dia carioca")
    
    
    # response_message = process_webhook(group_id, message_text)
    
    return jsonify({'status': 'sucesso', 'message': data}), 200
