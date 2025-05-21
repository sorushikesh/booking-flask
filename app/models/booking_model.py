from datetime import datetime, date


class Booking:
    def __init__(self, data):
        self.customer_name = data.get("customer_name")
        self.room_type = data.get("room_type")
        self.nights = data.get("nights")
        self.check_in_date = self.to_datetime(data.get("check_in_date"))
        self.check_out_date = self.to_datetime(data.get("check_out_date"))
        self.email = data.get("email")
        self.phone = data.get("phone")

    def to_datetime(self, value):
        if isinstance(value, date) and not isinstance(value, datetime):
            return datetime.combine(value, datetime.min.time())
        return value

    def to_dict(self):
        return {
            "customer_name": self.customer_name,
            "room_type": self.room_type,
            "nights": self.nights,
            "check_in_date": self.check_in_date,
            "check_out_date": self.check_out_date,
            "email": self.email,
            "phone": self.phone,
        }
