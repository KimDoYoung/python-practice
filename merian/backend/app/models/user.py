from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'edi_user'
    __table_args__ = {'schema': 'public'}

    
    id = Column(String, primary_key=True, index=True)
    pw = Column(String)
    nm = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String, default='ROLE_USER')
    created_by = Column(String)
    created_on = Column(DateTime, default=func.now())

    def verify_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.pw.encode('utf-8'))
