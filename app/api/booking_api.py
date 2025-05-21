from flask_restx import Namespace, Resource, fields
from flask import request
from pydantic import ValidationError
from ..schemas.booking_schema import BookingSchema
from ..services import booking_service

api = Namespace("bookings", description="Booking operations")

booking_model = api.model(
    "Booking",
    {
        "customer_name": fields.String(required=True),
        "room_type": fields.String(required=True, enum=["single", "double", "suite"]),
        "nights": fields.Integer(required=True),
        "check_in_date": fields.String(required=True),
        "check_out_date": fields.String(required=True),
        "email": fields.String(required=True),
        "phone": fields.String(),
    },
)


@api.route("/")
class BookingList(Resource):
    def get(self):
        return booking_service.get_all_bookings()

    @api.expect(booking_model)
    def post(self):
        try:
            booking = BookingSchema(**request.get_json())
        except ValidationError as e:
            return {"errors": e.errors()}, 400
        booking_id = booking_service.create_booking(booking.dict())
        return {"message": "Created", "id": booking_id}, 201


@api.route("/<string:booking_id>")
class BookingDetail(Resource):
    def get(self, booking_id):
        booking = booking_service.get_booking_by_id(booking_id)
        return booking or ({"message": "Not found"}, 404)

    @api.expect(booking_model)
    def put(self, booking_id):
        try:
            booking = BookingSchema(**request.get_json())
        except ValidationError as e:
            return {"errors": e.errors()}, 400
        updated = booking_service.update_booking(booking_id, booking.dict())
        return updated

    def delete(self, booking_id):
        deleted = booking_service.delete_booking(booking_id)
        return {"message": "Deleted"} if deleted else ({"message": "Not found"}, 404)
