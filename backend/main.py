from __future__ import annotations

import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Contact
from schemas import ContactCreate, ContactResponse
from services.sheets_service import append_contact_to_sheet
from services.email_service import send_contact_notification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:8080,http://127.0.0.1:8080",
).split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Drop and recreate tables to apply schema changes (safe — only test data exists)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables recreated with updated schema.")
    yield


app = FastAPI(
    title="Jason Patino Realty API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/contact", response_model=ContactResponse, status_code=201)
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    """Save a contact form submission, push to Google Sheets, and send email notification."""
    try:
        contact = Contact(
            first_name=payload.first_name,
            last_name=payload.last_name,
            business_name=payload.business_name,
            phone=payload.phone,
            email=payload.email,
            interest=payload.interest,
            message=payload.message,
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
        logger.info(f"Contact saved: {contact.id} — {contact.first_name} {contact.last_name}")
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save contact.")

    full_name = f"{contact.first_name} {contact.last_name}"

    # Google Sheets — fire and log errors, don't block the response
    try:
        append_contact_to_sheet(
            first_name=contact.first_name,
            last_name=contact.last_name,
            business_name=contact.business_name or "",
            phone=contact.phone,
            email=contact.email,
            interest=contact.interest,
            message=contact.message or "",
            created_at=contact.created_at.isoformat(),
        )
    except Exception as e:
        logger.error(f"Sheets export failed: {e}")

    # Email notification — fire and log errors, don't block the response
    try:
        send_contact_notification(
            first_name=contact.first_name,
            last_name=contact.last_name,
            business_name=contact.business_name or "",
            phone=contact.phone,
            email=contact.email,
            interest=contact.interest,
            message=contact.message or "",
        )
    except Exception as e:
        logger.error(f"Email notification failed: {e}")

    return contact


@app.get("/api/contacts", response_model=list[ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    """List all contact submissions (for admin use)."""
    return db.query(Contact).order_by(Contact.created_at.desc()).all()
