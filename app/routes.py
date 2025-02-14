from flask import Blueprint, jsonify, request
from .services import process_webhook

main_bp = Blueprint('main', __name__)

@main_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # response_message = process_webhook(group_id, message_text)
    
    return jsonify({'status': 'sucesso', 'message': data}), 200
