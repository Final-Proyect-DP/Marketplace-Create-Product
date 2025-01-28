from flask import request, jsonify
from app.models.models import Product, Category  # Update the import path
from app.extensions.extensions import db
from app.webhook.webhook import send_webhook  # Import the new webhook function
import requests
import base64  # To encode the image in Base64

WEBHOOK_URL = "http://localhost:5003/webhook"  # Webhook URL of the get microservice

def create_item():
    data = request.form
    image = request.files.get('image')

    # Validate required fields
    if not data.get('name') or not data.get('description') or not data.get('price'):
        return jsonify({"message": "Missing required fields"}), 400

    # Validate category_id if provided
    category_id = data.get('category_id')
    if category_id:
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return jsonify({"message": "Category not found"}), 404

    # Read image in binary format
    image_data = None
    if image:
        image_data = image.read()

    # Create the new product
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        userId=data.get('userId'),
        image_data=image_data,
        category_id=category_id  # Use the category ID directly
    )

    try:
        db.session.add(new_product)
        db.session.commit()

        # Prepare data for the webhook
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

        # Send data to the get microservice webhook
        send_webhook(webhook_data)

        return jsonify({
            "message": "Product created successfully",
            "product": new_product.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating product: {str(e)}"}), 500

def create_category():
    data = request.get_json()

    # Validate that required fields are present
    if not data.get('name'):
        return jsonify({"message": "Missing required fields"}), 400

    # Create the category in the database
    new_category = Category(
        name=data['name'],
        description=data.get('description')
    )

    try:
        db.session.add(new_category)
        db.session.commit()

        # Prepare data for the webhook
        webhook_data = {
            "id": new_category.id,
            "name": new_category.name,
            "description": new_category.description
        }

        # Send data to the get microservice webhook
        send_webhook(webhook_data)

        return jsonify({
            "message": "Category created successfully",
            "category": new_category.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating category: {str(e)}"}), 500
