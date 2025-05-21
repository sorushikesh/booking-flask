from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import date


class BookingSchema(BaseModel):
    customer_name: str = Field(..., min_length=1)
    room_type: str = Field(..., pattern="^(single|double|suite)$")  # <-- fixed here
    nights: int = Field(..., ge=1)
    check_in_date: date
    check_out_date: date
    email: EmailStr
    phone: Optional[str] = Field(default=None, pattern=r"^\+?[1-9]\d{1,14}$")

    @validator("check_out_date")
    def validate_dates(cls, v, values):
        if "check_in_date" in values and v <= values["check_in_date"]:
            raise ValueError("check_out_date must be after check_in_date")
        return v
