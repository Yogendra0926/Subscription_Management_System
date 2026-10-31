"""
Create the BrightLoop MongoDB database structure.

This creates 13 MongoDB collections and indexes corresponding to the
provided MySQL schema. It does not insert sample records.

Install:
    python -m pip install pymongo dnspython python-dotenv

Create a .env file in this script's directory or its parent MongoDB directory:
    MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-host>/
    MONGODB_DATABASE=brightloop

Run:
    python create_brightloop_mongodb.py

MongoDB notes:
- MySQL tables become MongoDB collections.
- MySQL AUTO_INCREMENT IDs become MongoDB ObjectId values (_id).
- Foreign keys become reference fields containing ObjectId values.
  MongoDB does not enforce foreign keys automatically; enforce those
  relationships in your application code.
- Store money as Decimal128 (or integer minor units), not floating point.
- Store dates as BSON Date values.
- Passwords must be bcrypt/Argon2 hashes, never plain text.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.errors import CollectionInvalid
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

MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "brightloop")

if not MONGODB_URI:
    raise RuntimeError(
        "MONGODB_URI is missing. Add your MongoDB Atlas URI to the .env file."
    )

COLLECTIONS = [
    "users",
    "customers",
    "products",
    "product_variants",
    "subscription_plans",
    "taxes",
    "discounts",
    "quotations",
    "quotation_lines",
    "subscriptions",
    "invoices",
    "payments",
    "subscription_history",
]


def ensure_collections(db):
    """Create each collection if it does not already exist."""
    existing = set(db.list_collection_names())
    for name in COLLECTIONS:
        if name not in existing:
            try:
                db.create_collection(name)
                print(f"Created collection: {name}")
            except CollectionInvalid:
                # Handles a collection created concurrently.
                print(f"Collection already exists: {name}")
        else:
            print(f"Collection already exists: {name}")


def create_indexes(db):
    """Create unique and relationship/query indexes."""
    # users
    db.users.create_index([("email", ASCENDING)], unique=True, name="uq_users_email")
    db.users.create_index([("role", ASCENDING)], name="ix_users_role")
    db.users.create_index([("status", ASCENDING)], name="ix_users_status")

    # customers
    db.customers.create_index(
        [("user_id", ASCENDING)],
        unique=True,
        partialFilterExpression={"user_id": {"$type": "objectId"}},
        name="uq_customers_user_id",
    )
    db.customers.create_index([("company_name", ASCENDING)], name="ix_customers_company")
    db.customers.create_index([("status", ASCENDING)], name="ix_customers_status")

    # products and variants
    db.products.create_index([("name", ASCENDING)], name="ix_products_name")
    db.products.create_index([("status", ASCENDING)], name="ix_products_status")
    db.product_variants.create_index(
        [("product_id", ASCENDING)], name="ix_variants_product_id"
    )

    # subscription plans, taxes, discounts
    db.subscription_plans.create_index([("status", ASCENDING)], name="ix_plans_status")
    db.taxes.create_index([("name", ASCENDING)], name="ix_taxes_name")
    db.discounts.create_index(
        [("code", ASCENDING)],
        unique=True,
        partialFilterExpression={"code": {"$type": "string"}},
        name="uq_discounts_code",
    )

    # quotations
    db.quotations.create_index(
        [("quotation_number", ASCENDING)],
        unique=True,
        name="uq_quotations_number",
    )
    db.quotations.create_index([("customer_id", ASCENDING)], name="ix_quotations_customer")
    db.quotations.create_index([("plan_id", ASCENDING)], name="ix_quotations_plan")
    db.quotations.create_index([("status", ASCENDING)], name="ix_quotations_status")

    # quotation lines
    db.quotation_lines.create_index(
        [("quotation_id", ASCENDING)], name="ix_quotation_lines_quotation"
    )
    db.quotation_lines.create_index(
        [("product_id", ASCENDING)], name="ix_quotation_lines_product"
    )
    db.quotation_lines.create_index(
        [("variant_id", ASCENDING)], name="ix_quotation_lines_variant"
    )

    # subscriptions
    db.subscriptions.create_index(
        [("subscription_number", ASCENDING)],
        unique=True,
        name="uq_subscriptions_number",
    )
    db.subscriptions.create_index(
        [("customer_id", ASCENDING)], name="ix_subscriptions_customer"
    )
    db.subscriptions.create_index([("plan_id", ASCENDING)], name="ix_subscriptions_plan")
    db.subscriptions.create_index(
        [("quotation_id", ASCENDING)], name="ix_subscriptions_quotation"
    )
    db.subscriptions.create_index([("status", ASCENDING)], name="ix_subscriptions_status")
    db.subscriptions.create_index(
        [("next_billing_date", ASCENDING)], name="ix_subscriptions_next_billing"
    )

    # invoices
    db.invoices.create_index(
        [("invoice_number", ASCENDING)], unique=True, name="uq_invoices_number"
    )
    db.invoices.create_index([("customer_id", ASCENDING)], name="ix_invoices_customer")
    db.invoices.create_index(
        [("subscription_id", ASCENDING)], name="ix_invoices_subscription"
    )
    db.invoices.create_index([("status", ASCENDING)], name="ix_invoices_status")
    # Equivalent to the MySQL subscription-period uniqueness rule, but only
    # for invoices where all three fields are present and non-null.
    db.invoices.create_index(
        [
            ("subscription_id", ASCENDING),
            ("billing_period_start", ASCENDING),
            ("billing_period_end", ASCENDING),
        ],
        unique=True,
        partialFilterExpression={
            "subscription_id": {"$type": "objectId"},
            "billing_period_start": {"$type": "date"},
            "billing_period_end": {"$type": "date"},
        },
        name="uq_invoice_subscription_period",
    )

    # payments
    db.payments.create_index(
        [("payment_reference", ASCENDING)],
        unique=True,
        name="uq_payments_reference",
    )
    db.payments.create_index([("customer_id", ASCENDING)], name="ix_payments_customer")
    db.payments.create_index([("invoice_id", ASCENDING)], name="ix_payments_invoice")
    db.payments.create_index([("payment_date", ASCENDING)], name="ix_payments_date")

    # subscription history
    db.subscription_history.create_index(
        [("subscription_id", ASCENDING), ("created_at", ASCENDING)],
        name="ix_subscription_history_timeline",
    )

    print("Indexes created/verified.")


def main():
    client = MongoClient(
        MONGODB_URI,
        server_api=ServerApi("1"),
        serverSelectionTimeoutMS=15000,
    )

    try:
        client.admin.command("ping")
        print("MongoDB Atlas connection established.")

        db = client[DATABASE_NAME]
        ensure_collections(db)
        create_indexes(db)

        print(f"\nDatabase structure ready: {DATABASE_NAME}")
        print(f"Collections: {len(COLLECTIONS)}")
        print("No documents or sample data were inserted.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
