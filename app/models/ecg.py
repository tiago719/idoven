from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func, ARRAY
from sqlalchemy.orm import relationship
from . import Base


class ECG(Base):
    __tablename__ = 'ecgs'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, server_default=func.now())
    user = Column(Integer, ForeignKey('users.id'))
    zero_crossings = Column(Integer, default=0)
    processed = Column(Boolean, default=False)
    
    # Define a one-to-many relationship with leads
    leads = relationship('Lead', back_populates='ecg')


class Lead(Base):
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    num_samples = Column(Integer, default=None)
    signal = Column(ARRAY(Integer))
    
    ecg_id = Column(Integer, ForeignKey('ecgs.id'))
    ecg = relationship('ECG', back_populates='leads')