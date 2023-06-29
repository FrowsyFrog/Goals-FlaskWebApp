from flask import Flask
from flask_login import LoginManager
import requests

# url = 'http://44.195.223.194:8000/'
url = 'http://3.214.121.253:8005/'
url2 = 'http://3.214.121.253:8000/'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testkey'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        response = requests.get(f'{url2}userid/{id}')
        if response.status_code == 200:
            response_data = response.json()
            if response_data:
                return User(data=response_data[0])
        return

    return app