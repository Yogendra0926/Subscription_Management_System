"""
Insert linked sample/testing data into the BrightLoop MongoDB database.

Install:
    python -m pip install pymongo dnspython python-dotenv bcrypt

.env in this script's directory or its parent MongoDB directory:
    MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-host>/
    MONGODB_DATABASE=brightloop

Run:
    python sample_testing_data.py

Demo login password for both sample users:
    Demo@123!

IMPORTANT:
- This script only replaces documents carrying sample_data=True.
- It does not delete real/application documents.
- Sample users are for local/demo testing only. Change their passwords
  and remove sample records before production use.
"""

import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import bcrypt
from dotenv import load_dotenv
from bson import ObjectId, Decimal128
from pymongo import MongoClient
from pymongo.server_api import ServerApi


BASE_DIR = Path(__file__).resolve().parent
ENV_FILES = (
    BASE_DIR / ".env",
    BASE_DIR.parent / ".env",
    BASE_DIR.parent.parent / ".env",
)

for env_file in ENV_FILES:
    if env_file.is_file():
        load_dotenv(env_file, override=False)

URI = os.getenv("MONGODB_URI", "").strip()
DB_NAME = os.getenv("MONGODB_DATABASE", "brightloop")

if not URI:
    raise RuntimeError("MONGODB_URI is missing from .env")

now = datetime.now(timezone.utc)
today = datetime.combine(now.date(), datetime.min.time(), tzinfo=timezone.utc)
demo_password_hash = bcrypt.hashpw(
    b"Demo@123!", bcrypt.gensalt()
).decode("utf-8")


def money(value):
    return Decimal128(Decimal(str(value)))


def tagged(document):
    document["sample_data"] = True
    return document


client = MongoClient(
    URI,
    server_api=ServerApi("1"),
    serverSelectionTimeoutMS=15000,
)

try:
    client.admin.command("ping")
    db = client[DB_NAME]

    # Remove only data previously inserted by this sample script.
    collection_names = [
        "users", "customers", "products", "product_variants",
        "subscription_plans", "taxes", "discounts", "quotations",
        "quotation_lines", "subscriptions", "invoices", "payments",
        "subscription_history",
    ]
    for name in collection_names:
        db[name].delete_many({"sample_data": True})

    # USERS
    admin_id, staff_id, customer_user_id = ObjectId(), ObjectId(), ObjectId()
    db.users.insert_many([
        tagged({
            "_id": admin_id, "role": "admin", "full_name": "Aarav Sharma",
            "email": "admin@brightloop.test", "password_hash": demo_password_hash,
            "phone": "+91-9000000001", "status": "active",
            "created_at": now, "updated_at": now,
        }),
        tagged({
            "_id": staff_id, "role": "staff", "full_name": "Priya Verma",
            "email": "staff@brightloop.test", "password_hash": demo_password_hash,
            "phone": "+91-9000000002", "status": "active",
            "created_at": now, "updated_at": now,
        }),
        tagged({
            "_id": customer_user_id, "role": "customer", "full_name": "Rohan Mehta",
            "email": "rohan@brightloop.test", "password_hash": demo_password_hash,
            "phone": "+91-9000000003", "status": "active",
            "created_at": now, "updated_at": now,
        }),
    ])

    # CUSTOMERS
    customer1, customer2 = ObjectId(), ObjectId()
    db.customers.insert_many([
        tagged({
            "_id": customer1, "user_id": customer_user_id,
            "company_name": "Mehta Digital Solutions",
            "customer_type": "business", "address": "21 MG Road",
            "city": "Indore", "state": "Madhya Pradesh", "country": "India",
            "postal_code": "452001", "tax_gst_number": "23ABCDE1234F1Z5",
            "internal_notes": "Sample business customer", "status": "active",
            "created_at": now,
        }),
        tagged({
            "_id": customer2, "user_id": None,
            "company_name": "Ananya Kapoor", "customer_type": "individual",
            "address": "Vijay Nagar", "city": "Indore",
            "state": "Madhya Pradesh", "country": "India",
            "postal_code": "452010", "tax_gst_number": None,
            "internal_notes": "Sample individual customer", "status": "active",
            "created_at": now,
        }),
    ])

    # PRODUCTS
    product1, product2, product3 = ObjectId(), ObjectId(), ObjectId()
    db.products.insert_many([
        tagged({
            "_id": product1, "name": "Website Maintenance",
            "product_type": "Service", "sales_price": money("2500.00"),
            "cost_price": money("1200.00"),
            "description": "Monthly website maintenance service",
            "internal_notes": "Sample product", "status": "active",
            "created_at": now,
        }),
        tagged({
            "_id": product2, "name": "Cloud Storage",
            "product_type": "Digital Service", "sales_price": money("999.00"),
            "cost_price": money("400.00"),
            "description": "Cloud storage subscription",
            "internal_notes": "Sample product", "status": "active",
            "created_at": now,
        }),
        tagged({
            "_id": product3, "name": "Technical Support",
            "product_type": "Service", "sales_price": money("1500.00"),
            "cost_price": money("700.00"),
            "description": "Priority technical support",
            "internal_notes": "Sample product", "status": "active",
            "created_at": now,
        }),
    ])

    # PRODUCT VARIANTS
    variant1, variant2 = ObjectId(), ObjectId()
    db.product_variants.insert_many([
        tagged({
            "_id": variant1, "product_id": product1, "name": "Standard",
            "additional_price": money("0"), "description": "Standard support",
            "status": "active",
        }),
        tagged({
            "_id": variant2, "product_id": product1, "name": "Priority",
            "additional_price": money("500"), "description": "Priority support",
            "status": "active",
        }),
    ])

    # SUBSCRIPTION PLANS
    plan_monthly, plan_yearly = ObjectId(), ObjectId()
    db.subscription_plans.insert_many([
        tagged({
            "_id": plan_monthly, "name": "Monthly Business Plan",
            "description": "Monthly website and support package",
            "price": money("3000"), "billing_cycle": "monthly",
            "minimum_quantity": 1, "available_from": today,
            "available_until": None, "auto_close": False,
            "early_close_allowed": True, "pause_allowed": True,
            "renewal_allowed": True, "status": "active",
        }),
        tagged({
            "_id": plan_yearly, "name": "Annual Business Plan",
            "description": "Annual cloud and support package",
            "price": money("30000"), "billing_cycle": "yearly",
            "minimum_quantity": 1, "available_from": today,
            "available_until": None, "auto_close": False,
            "early_close_allowed": True, "pause_allowed": True,
            "renewal_allowed": True, "status": "active",
        }),
    ])

    # TAXES AND DISCOUNTS
    tax_id, discount_id = ObjectId(), ObjectId()
    db.taxes.insert_one(tagged({
        "_id": tax_id, "name": "GST", "percentage": Decimal128("18.00"),
        "tax_type": "GST", "description": "Sample GST rate",
        "status": "active",
    }))
    db.discounts.insert_one(tagged({
        "_id": discount_id, "name": "Welcome Discount",
        "code": "WELCOME10", "discount_type": "percentage",
        "discount_value": money("10"), "minimum_purchase": money("1000"),
        "minimum_quantity": 1, "starts_at": today,
        "expires_at": today + timedelta(days=90),
        "usage_limit": 100, "usage_count": 1,
        "description": "Sample 10 percent welcome discount",
        "status": "active",
    }))

    # QUOTATION AND LINES
    quotation_id = ObjectId()
    db.quotations.insert_one(tagged({
        "_id": quotation_id, "quotation_number": "QUO-DEMO-0001",
        "customer_id": customer1, "plan_id": plan_monthly,
        "quotation_date": today, "expiry_date": today + timedelta(days=15),
        "payment_terms": "Due within 15 days",
        "notes": "Sample quotation", "terms": "Demo terms and conditions",
        "subtotal": money("3000"), "tax_amount": money("540"),
        "discount_amount": money("0"), "grand_total": money("3540"),
        "status": "confirmed",
    }))
    db.quotation_lines.insert_many([
        tagged({
            "_id": ObjectId(), "quotation_id": quotation_id,
            "product_id": product1, "variant_id": variant1,
            "description": "Website maintenance - Standard",
            "quantity": 1, "unit_price": money("2500"),
            "discount_percent": Decimal128("0"),
            "tax_percent": Decimal128("18"),
            "line_total": money("2500"),
        }),
        tagged({
            "_id": ObjectId(), "quotation_id": quotation_id,
            "product_id": product3, "variant_id": None,
            "description": "Technical support",
            "quantity": 1, "unit_price": money("500"),
            "discount_percent": Decimal128("0"),
            "tax_percent": Decimal128("18"),
            "line_total": money("500"),
        }),
    ])

    # SUBSCRIPTION
    subscription_id = ObjectId()
    start_date = today - timedelta(days=10)
    next_billing = today + timedelta(days=20)
    db.subscriptions.insert_one(tagged({
        "_id": subscription_id, "subscription_number": "SUB-DEMO-0001",
        "customer_id": customer1, "plan_id": plan_monthly,
        "quotation_id": quotation_id, "start_date": start_date,
        "expiry_date": today + timedelta(days=20),
        "next_billing_date": next_billing,
        "renewal_date": next_billing, "billing_cycle": "monthly",
        "payment_terms": "Net 15", "total_amount": money("3540"),
        "status": "active",
    }))

    # INVOICE
    invoice_id = ObjectId()
    period_start = start_date
    period_end = today + timedelta(days=19)
    db.invoices.insert_one(tagged({
        "_id": invoice_id, "invoice_number": "INV-DEMO-0001",
        "customer_id": customer1, "subscription_id": subscription_id,
        "invoice_date": today - timedelta(days=5),
        "due_date": today + timedelta(days=10),
        "billing_period_start": period_start,
        "billing_period_end": period_end,
        "subtotal": money("3000"), "tax_amount": money("540"),
        "discount_amount": money("0"), "total_amount": money("3540"),
        "paid_amount": money("3540"), "status": "paid",
    }))

    # PAYMENT
    db.payments.insert_one(tagged({
        "_id": ObjectId(), "payment_reference": "PAY-DEMO-0001",
        "customer_id": customer1, "invoice_id": invoice_id,
        "payment_method": "upi", "amount": money("3540"),
        "payment_date": today - timedelta(days=4),
        "transaction_reference": "UPI-DEMO-123456",
        "notes": "Sample successful UPI payment",
        "status": "completed",
    }))

    # SUBSCRIPTION HISTORY
    db.subscription_history.insert_many([
        tagged({
            "_id": ObjectId(), "subscription_id": subscription_id,
            "previous_status": None, "new_status": "draft",
            "note": "Sample subscription created",
            "created_at": now - timedelta(days=10),
        }),
        tagged({
            "_id": ObjectId(), "subscription_id": subscription_id,
            "previous_status": "draft", "new_status": "active",
            "note": "Sample subscription activated after confirmation",
            "created_at": now - timedelta(days=9),
        }),
    ])

    print("\nSample data inserted successfully!")
    print(f"Database: {DB_NAME}")
    for name in collection_names:
        count = db[name].count_documents({"sample_data": True})
        print(f"{name}: {count} sample document(s)")

    print("\nDemo login accounts (same password for both):")
    print("Admin:    admin@brightloop.test")
    print("Staff:    staff@brightloop.test")
    print("Customer: rohan@brightloop.test")
    print("Password: Demo@123!")

finally:
    client.close()
