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
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")
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
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            message=payload.message,
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
        logger.info(f"Contact saved: {contact.id} — {contact.name}")
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save contact.")

    # Google Sheets — fire and log errors, don't block the response
    try:
        append_contact_to_sheet(
            name=contact.name,
            email=contact.email,
            phone=contact.phone or "",
            message=contact.message,
            created_at=contact.created_at.isoformat(),
        )
    except Exception as e:
        logger.error(f"Sheets export failed: {e}")

    # Email notification — fire and log errors, don't block the response
    try:
        send_contact_notification(
            name=contact.name,
            email=contact.email,
            phone=contact.phone or "",
            message=contact.message,
        )
    except Exception as e:
        logger.error(f"Email notification failed: {e}")

    return contact


@app.get("/api/contacts", response_model=list[ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    """List all contact submissions (for admin use)."""
    return db.query(Contact).order_by(Contact.created_at.desc()).all()
