from flask import Blueprint, Response, jsonify
from app.controllers.controllers import create_item, create_category  # Update the import path
from app.models.models import Product  # Update the import path
from app.webhook.webhook import send_webhook  # Import the new webhook function

# Definir un blueprint para la creación de productos
create_bp = Blueprint('create', __name__)

@create_bp.route('/items', methods=['POST'])
def create_or_update_product():
    return create_item()  # Llamar a la función que maneja la creación del producto

@create_bp.route('/categories', methods=['POST'])
def create_new_category():
    return create_category()  # Llamar a la función que maneja la creación de la categoría

@create_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify(status='OK', service='user-read'), 200

