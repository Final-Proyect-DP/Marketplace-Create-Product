from flask import Flask
from .config.config import Config
from .extensions.extensions import db
from .controllers.controllers import create_item
from app.routes.routes import create_bp  # Update the import path
from flasgger import Swagger
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar la base de datos
    db.init_app(app)
    
    # Inicializar Swagger
    Swagger(app, template_file='swagger/swagger_config.yaml')
    
    # Habilitar CORS para todas las rutas
    CORS(app)

    # Registrar el Blueprint para las rutas de creación y obtener la imagen
    app.register_blueprint(create_bp)

    return app
