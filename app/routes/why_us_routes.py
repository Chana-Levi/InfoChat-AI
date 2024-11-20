from flask import Blueprint, render_template

why_us_bp = Blueprint('why_us', __name__, url_prefix='/why_us')

@why_us_bp.route('/')
def why_us():
    return render_template('why_us.html')
