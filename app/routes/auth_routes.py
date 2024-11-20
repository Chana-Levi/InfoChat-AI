
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from app.init import oauth 

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/', methods=['GET'])
def auth_home():
    return redirect(url_for('auth_bp.register'))

@auth_bp.route('/google_login')
def google_login():
    print("---google login function---")
    redirect_uri = url_for('auth_bp.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/google_callback')
def google_callback():
    print("---google callback function---")
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    user = User.find_by_email(user_info['email'])
    if not user:
        user = User(username=user_info['name'], email=user_info['email'], password='')
        user.save_to_db()
    session['user_email'] = user.email
    return redirect(url_for('main_bp.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if not User.is_valid_email(email):
            return """
                <script>
                    alert('Invalid email address');
                    window.location.href = '/auth/register';
                </script>
            """       
        existing_user = User.find_by_email(email)
        if existing_user:
            return """
                <script>
                    alert('User already exists');
                    window.location.href = '/auth/register';
                </script>
            """      
        new_user = User(username, password, email)
        new_user.save_to_db()
        return redirect(url_for('auth_bp.login')) 
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user = User.find_by_email(email)
        if user and user.verify_password(password):
            session['user_email'] = user.email
            session['username'] = user.username
            return redirect(url_for('main_bp.index'))
        return """
                <script>
                    alert('Invalid credentials');
                    window.location.href = '/auth/login';
                </script>
            """ 
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('username', None)
    return redirect(url_for('main_bp.index'))