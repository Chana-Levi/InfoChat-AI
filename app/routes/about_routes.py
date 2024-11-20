
from flask import Blueprint, render_template

# Define the blueprint: 'about', set its url prefix: app.url/about
about_bp = Blueprint('about', __name__, url_prefix='/about')

# Define a route for the 'about' page
@about_bp.route('/')
def about():
    return render_template('about.html')
