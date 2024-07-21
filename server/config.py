from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'
app.json.compact = False

# Initialize extensions
bcrypt = Bcrypt(app)
db = SQLAlchemy(app, metadata=MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}))
migrate = Migrate(app, db)
api = Api(app)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500"]}})
