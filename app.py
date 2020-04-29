from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from views import render_ordered, render_account, render_add_to_cart, render_cart, render_index, render_login,\
    render_logout, render_register, render_remove_from_cart

if __name__ == '__main__':
    app.run()
