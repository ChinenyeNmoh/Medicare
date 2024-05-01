"""models"""
import uuid
from datetime import datetime
from app import db

class BaseModel():
    """base model super class"""
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, *args, **kwargs):
        """initialises the class"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now() 
        self.updated_at = datetime.now()
        
