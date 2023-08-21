from flask import Flask
from database import Database
from webhook import app as webhook

def launch_app():
    # Create the Flask application
    app = Flask(__name__)

    # Instantiate the Database class

    db = Database(host=, user='your_user', password='your_password', port='your_port', database='your_database')

    # Register the blueprints for the webhook, passing the db instance as a parameter
    app.register_blueprint(webhook)

    return app

# Entry point of the application
if __name__ == '__main__':
    app = launch_app()
    app.run(port=5003)

