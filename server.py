from flask_app import app, socketio, database
from flask_app.controllers import chats, users, settings

# Create tables
with app.app_context():
    database.create_all()

if __name__ == "__main__":
    socketio.run(app, debug=True)
