from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from .db import mongo
from config import Config
from .exceptions.handlers import register_error_handlers
from .api.booking_api import api as booking_ns


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    CORS(app)

    api = Api(app, version="1.0", title="Hotel Booking API", doc="/docs")
    api.add_namespace(booking_ns, path="/api/bookings")

    register_error_handlers(app)
    return app
