from app.extensions.extensions import db  # Update the import path

class Product(db.Model):
    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    userId = db.Column(db.String(255))
    image_data = db.Column(db.LargeBinary)  # Here we store the image in binary format
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=True)  # Relationship with the Category table

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "userId": self.userId,
            "image_data": self.image_data.decode('latin1') if self.image_data else None,  # Decode if necessary
            "created_at": self.created_at,
            "category_id": self.category_id
        }

class Category(db.Model):
    __tablename__ = 'Categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    products = db.relationship('Product', backref='category', lazy=True)  # Relationship with the Product table

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
