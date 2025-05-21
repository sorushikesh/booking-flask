from flask import jsonify, request
from pydantic import ValidationError
from bson.errors import InvalidId
from werkzeug.exceptions import HTTPException
from ..logger.app_logger import setup_logger

logger = setup_logger("exception")


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        logger.warning(
            "Validation error", extra={"errors": err.errors(), "request": request.json}
        )
        return jsonify({"error": "Validation Error", "details": err.errors()}), 400

    @app.errorhandler(InvalidId)
    def handle_invalid_id(err):
        logger.warning("Invalid ObjectId", extra={"error": str(err)})
        return jsonify({"error": "Invalid ID", "details": str(err)}), 400

    @app.errorhandler(404)
    def handle_not_found(err):
        logger.info("404 Not Found", extra={"path": request.path})
        return jsonify({"error": "Not Found", "message": "Resource not found"}), 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        logger.error("HTTP error", extra={"error": err.name, "desc": err.description})
        return jsonify({"error": err.name, "message": err.description}), err.code

    @app.errorhandler(Exception)
    def handle_exception(err):
        logger.exception("Unhandled exception")
        return jsonify({"error": "Internal Server Error", "message": str(err)}), 500
