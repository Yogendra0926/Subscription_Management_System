from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import ping_database, close_database
from app.routers import auth, users
from app.routers import (
    customers, products, product_variants, subscription_plans, taxes,
    discounts, quotations, quotation_lines, subscriptions, invoices,
    payments, subscription_history,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ping_database()
    yield
    close_database()

app = FastAPI(
    title="BrightLoop Subscription Management API",
    description="JWT-secured REST API backed by MongoDB Atlas.",
    version="1.0.0",
    lifespan=lifespan,
)

# Restrict this list to your real frontend origin(s) before deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in [
    auth, users, customers, products, product_variants, subscription_plans,
    taxes, discounts, quotations, quotation_lines, subscriptions, invoices,
    payments, subscription_history,
]:
    app.include_router(module.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "BrightLoop API is running", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health():
    ping_database()
    return {"status": "ok", "database": "connected"}
