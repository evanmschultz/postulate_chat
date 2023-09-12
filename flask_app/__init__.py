from sqlalchemy import create_engine, exc, text
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import pymysql


# Function to create database if it doesn't exist
def create_database_if_not_exists(engine, db_name):
    connection = engine.connect()
    try:
        connection.execute(text(f"CREATE DATABASE {db_name}"))
        print(f"Created database {db_name}")
    except exc.ProgrammingError as e:  # Catch the exception for database already exists
        print(f"Database {db_name} already exists")
    finally:
        connection.close()


# Connect to MySQL server without database
root_engine = create_engine("mysql+pymysql://root:rootroot@localhost")

# Create database if not exists
create_database_if_not_exists(root_engine, "postulate_chat")

pymysql.install_as_MySQLdb()

app: Flask = Flask(__name__)
app.secret_key = "secret_key"

# Initialize SocketIO and attach it to the Flask app
socketio = SocketIO(
    app, cors_allowed_origins="*"
)  # TODO: Change this to the actual domain for production

# Initialize SQLAlchemy and set auto-commit configurations
# Update the password for your MySQL server
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:rootroot@localhost/postulate_chat"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_ECHO"] = True
database = SQLAlchemy(app)
