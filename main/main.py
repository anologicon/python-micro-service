from flask import Flask
from flask import jsonify
from flask import abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
import requests, os
from producer import pub

ADMIN_URI = os.environ.get('ADMIN_URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(255))
    image = db.Column(db.String(255))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='unique_product_user')

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get(f'http://{ADMIN_URI}:8000/api/user')
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'	], product_id=id)
        db.session.add(productUser)
        db.session.commit()
    except:
        abort(400, 'Product already liked')

    pub('product_liked', id)
        

    return jsonify({'success': 'Product liked'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
