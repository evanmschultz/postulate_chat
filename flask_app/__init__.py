from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app: Flask = Flask(__name__)
app.secret_key = "secret_key"

# Initialize SocketIO and attach it to the Flask app
socketio = SocketIO(
    app, cors_allowed_origins="*"
)  # TODO: Change this to the actual domain for production

# Initialize SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:rootroot@localhost/postulate_chat"
database = SQLAlchemy(app)
