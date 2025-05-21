from bson import ObjectId
from ..db import mongo
from ..models.booking_model import Booking
from ..logger.app_logger import setup_logger

logger = setup_logger("service")


def get_all_bookings():
    bookings = mongo.db.bookings.find()
    result = [{**b, "_id": str(b["_id"])} for b in bookings]
    logger.info("Fetched all bookings", extra={"count": len(result)})
    return result


def get_booking_by_id(booking_id):
    logger.info("Getting booking", extra={"booking_id": booking_id})
    booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})
    if booking:
        booking["_id"] = str(booking["_id"])
        return booking
    logger.warning("Booking not found", extra={"booking_id": booking_id})
    return None


def create_booking(data):
    logger.info("Creating booking", extra={"data": data})
    booking = Booking(data)
    result = mongo.db.bookings.insert_one(booking.to_dict())
    return str(result.inserted_id)


def update_booking(booking_id, data):
    logger.info("Updating booking", extra={"booking_id": booking_id, "data": data})
    mongo.db.bookings.update_one({"_id": ObjectId(booking_id)}, {"$set": data})
    return get_booking_by_id(booking_id)


def delete_booking(booking_id):
    logger.info("Deleting booking", extra={"booking_id": booking_id})
    result = mongo.db.bookings.delete_one({"_id": ObjectId(booking_id)})
    return result.deleted_count
