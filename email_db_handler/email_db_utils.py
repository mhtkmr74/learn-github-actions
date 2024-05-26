from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Define the SQLite URL
DATABASE_URL = 'sqlite:///email_processor.db'

# Create an engine that connects to the SQLite database
engine = create_engine(DATABASE_URL)

# Define a base class for declarative class definitions
Base = declarative_base()

# Define a sample table
class Email(Base):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    email_identifier = Column(String(100))
    sender = Column(String(100))
    reciever = Column(String(100))
    subject = Column(String(100))
    received_date = Column(DateTime)
    body = Column(Text)

# Create the table in the database
Base.metadata.create_all(engine)

def add_email_in_db(incoming_email):
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        email = Email(
            email_identifier = incoming_email["email_id"],
            sender = incoming_email["sender"],
            reciever = incoming_email["reciever"],
            subject = incoming_email["subject"],
            received_date = incoming_email["received_date"],
            body = incoming_email["email_body"],
        )
        session.add(email)
        session.commit()
    except Exception as e:
        logger.error(f"Error Occurred in write email to db - {str(e)}")
        session.rollback()
        session.close()
        raise e


def fetch_value_from_email_object(email):
    return {
        "email_id": email.email_identifier,
        "sender": email.sender,
        "reciever": email.reciever,
        "subject": email.subject,
        "received_date": email.received_date,
        "body": email.body
    }


def fetch_email_from_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    now = datetime.now()
    today_emails = []
    for email in session.query(Email).filter(Email.received_date >= datetime(now.year, now.month, now.day)).all():
        today_emails.append(fetch_value_from_email_object(email))
    return today_emails
