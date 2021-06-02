from flask import Flask

from app.webhook.routes import webhook,display

from .extensions import mongo

# Creating our flask app
def create_app():

    app = Flask(__name__,static_url_path='',static_folder='static',)

    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(display)

    #setting up MongoDB 
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    mongo.init_app(app)
    
    return app
