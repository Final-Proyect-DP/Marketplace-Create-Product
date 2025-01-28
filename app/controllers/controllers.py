from flask import request, jsonify
from app.models.models import Product, Category  # Update the import path
from app.extensions.extensions import db
import requests
import base64  # Para codificar la imagen en Base64

WEBHOOK_URL = "http://localhost:5003/webhook"  # URL del webhook del microservicio get


def create_item():
    data = request.form
    image = request.files.get('image')

    # Validar campos requeridos
    if not data.get('name') or not data.get('description') or not data.get('price'):
        return jsonify({"message": "Missing required fields"}), 400

    # Validar category_id si se proporciona
    category_id = data.get('category_id')
    if category_id:
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return jsonify({"message": "Category not found"}), 404

    # Leer imagen en formato binario
    image_data = None
    if image:
        image_data = image.read()

    # Crear el nuevo producto
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        userId=data.get('userId'),
        image_data=image_data,
        category_id=category_id  # Usar directamente el ID de la categoría
    )

    try:
        db.session.add(new_product)
        db.session.commit()

        # Preparar los datos para el webhook
        webhook_data = {
            "id": new_product.id,
            "name": new_product.name,
            "description": new_product.description,
            "price": str(new_product.price),
            "userId": new_product.userId,
            "image_data": base64.b64encode(new_product.image_data).decode('utf-8') if new_product.image_data else None,
            "created_at": new_product.created_at.isoformat(),
            "category_id": new_product.category_id
        }

        # Enviar los datos al webhook del microservicio get
        response = requests.post(WEBHOOK_URL, json=webhook_data)
        if response.status_code != 200:
            print(f"Error sincronizando producto: {response.text}")

        return jsonify({
            "message": "Product created successfully",
            "product": new_product.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating product: {str(e)}"}), 500



def create_category():
    data = request.get_json()

    # Validar que los campos obligatorios estén presentes
    if not data.get('name'):
        return jsonify({"message": "Missing required fields"}), 400

    # Crear la categoría en la base de datos
    new_category = Category(
        name=data['name'],
        description=data.get('description')
    )

    try:
        db.session.add(new_category)
        db.session.commit()

        # Preparar los datos para el webhook
        webhook_data = {
            "id": new_category.id,
            "name": new_category.name,
            "description": new_category.description
        }

        # Enviar los datos al webhook del microservicio get
        response = requests.post(WEBHOOK_URL, json=webhook_data)
        if response.status_code != 200:
            print(f"Error sincronizando categoría: {response.text}")

        return jsonify({
            "message": "Category created successfully",
            "category": new_category.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating category: {str(e)}"}), 500
