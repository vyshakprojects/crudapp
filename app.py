from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "local_data.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a simple table (model)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Item {self.name}>"

# Initialize the database (create tables)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the CRUD API!"

# Create Item (POST /items)
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_item = Item(name=data['name'], description=data.get('description'))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created', 'id': new_item.id}), 201

# Read Items (GET /items)
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_data = [{'id': item.id, 'name': item.name, 'description': item.description} for item in items]
    return jsonify(items_data)

# Update Item (PUT /items/<int:id>)
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({'message': 'Item updated'})

# Delete Item (DELETE /items/<int:id>)
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

@app.route('/health2', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(port=8082)
