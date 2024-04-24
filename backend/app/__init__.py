from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_jwt_extended import jwt_required, JWTManager, get_jwt
from flask_cors import CORS


app = Flask(__name__)
jwt = JWTManager(app)

# Configurações para permitir credenciais no CORS
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = "2ibma*<6{8i*]slz5^217p(q4z=&4$xv_d_:[)j=+=24[8e!|0{`>634+r[%bg2"
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(hours=1)


# Configurações para permitir cookies de sessão com SameSite=None e Secure=True
app.config['SECRET_KEY'] = '2ibma*<6{8i*]slz5^217p(q4z=&4$xv_d_:[)j=+=24[8e!|0{`>634+r[%bg2'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=2)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Inicialização da extensão SQLAlchemy
db = SQLAlchemy(app)

from app.models.database.db import User, Hairdressers, Services, Scheduling
from app.router.users_route import read_user, update_user
from app.router.login_route import login, recovery, new_passwords, acess_token_validation
from app.router.hairdressers_route import create_hairdressers, read_hairdressers, update_hairdressers, delete_hairdressers, login_hairdressers
from app.router.services_route import create_services, read_service, update_service, delete_service
from app.router.scheduling_route import create_scheduling, read_schedulin, delete_scheduling