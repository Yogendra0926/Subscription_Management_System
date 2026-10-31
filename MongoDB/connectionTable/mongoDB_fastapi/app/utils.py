from datetime import date, datetime, time, timezone
from decimal import Decimal
from bson import ObjectId, Decimal128
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

REFERENCE_FIELDS = {
    "user_id", "product_id", "quotation_id", "variant_id",
    "customer_id", "plan_id", "subscription_id", "invoice_id",
}
DATE_FIELDS = {
    "available_from", "available_until", "starts_at", "expires_at",
    "quotation_date", "expiry_date", "start_date", "next_billing_date",
    "renewal_date", "invoice_date", "due_date", "billing_period_start",
    "billing_period_end", "payment_date",
}
MONEY_FIELDS = {
    "sales_price", "cost_price", "additional_price", "price",
    "discount_value", "minimum_purchase", "subtotal", "tax_amount",
    "discount_amount", "grand_total", "unit_price", "line_total",
    "total_amount", "paid_amount", "amount",
}

def prepare_document(data: dict) -> dict:
    """Convert API JSON values to BSON types for known reference/date/money fields."""
    result = {}
    for key, value in data.items():
        if key in REFERENCE_FIELDS and value is not None:
            if not ObjectId.is_valid(str(value)):
                raise HTTPException(status_code=422, detail=f"{key} must be a valid ObjectId")
            result[key] = ObjectId(str(value))
        elif key in DATE_FIELDS and value is not None:
            if isinstance(value, datetime):
                parsed_date = value.date()
            elif isinstance(value, date):
                parsed_date = value
            else:
                try:
                    parsed_date = date.fromisoformat(str(value))
                except ValueError:
                    raise HTTPException(status_code=422, detail=f"{key} must use YYYY-MM-DD")
            # BSON has no date-only type; store date-only values as UTC midnight.
            result[key] = datetime.combine(parsed_date, time.min, tzinfo=timezone.utc)
        elif key in MONEY_FIELDS and value is not None:
            try:
                result[key] = Decimal128(str(Decimal(str(value))))
            except Exception:
                raise HTTPException(status_code=422, detail=f"{key} must be a valid decimal number")
        else:
            result[key] = value
    return result

def serialize(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, Decimal128):
        return float(value.to_decimal())
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: serialize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serialize(v) for v in value]
    return value

def public_document(document: dict) -> dict:
    document = dict(document)
    document.pop("password_hash", None)
    return serialize(document)

def handle_duplicate(error: DuplicateKeyError):
    raise HTTPException(status_code=409, detail="A record with one of these unique values already exists")
