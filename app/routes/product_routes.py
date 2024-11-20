from flask import Blueprint, render_template

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/')
def product():
    return render_template('product.html')
