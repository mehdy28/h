from flask import Flask
from db import db
from blueprints.user import users_bp
from blueprints.channel import channels_bp
from blueprints.memebership import memberships_bp
from blueprints.message import messages_bp
import models
from flask_swagger_ui import get_swaggerui_blueprint
app = Flask(__name__)




### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
app.register_blueprint(users_bp)
app.register_blueprint(channels_bp)
app.register_blueprint(memberships_bp)
app.register_blueprint(messages_bp)

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create the database tables
@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()
    

if __name__ == '__main__':
    app.run(debug=True)

