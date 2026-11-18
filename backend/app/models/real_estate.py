from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Property(Base):
    __tablename__ = "properties"
    
    property_id = Column(String(50), primary_key=True, index=True)
    property_type = Column(String(50), index=True)  # Villa, Apartment, Office, Plot, Warehouse, Shop
    city = Column(String(100), index=True)          # Mumbai, Pune, Ahmedabad, Surat, Vadodara, Rajkot, Anand, Bharuch, Gandhinagar, Nadiad
    locality = Column(String(100), index=True)      # Satellite, Central, Manjalpur, Bopal, New Town, Gotri, Vesu, Alkapuri
    bedrooms = Column(Integer, default=0)
    area_sqft = Column(Float, nullable=False)
    asking_price = Column(Float, nullable=False)
    listing_date = Column(Date, nullable=False)
    listing_status = Column(String(50), index=True) # Available, Under Offer, Sold, Withdrawn
    
    # Relationships
    visits = relationship("SiteVisit", back_populates="property")
    deals = relationship("Deal", back_populates="property")

class Lead(Base):
    __tablename__ = "leads"
    
    lead_id = Column(String(50), primary_key=True, index=True)
    lead_name = Column(String(150), nullable=False)
    property_type_interest = Column(String(50), index=True)
    city = Column(String(100), index=True)
    lead_source = Column(String(50), index=True)    # Walk-in, Website, Social Media, Referral, Campaign, Portal
    inquiry_date = Column(Date, nullable=False)
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    lead_status = Column(String(50), index=True)    # New, Qualified, Negotiation, Converted, Lost
    phone = Column(String(50), nullable=True)
    
    # Relationships
    visits = relationship("SiteVisit", back_populates="lead")
    deals = relationship("Deal", back_populates="lead")

class SiteVisit(Base):
    __tablename__ = "site_visits"
    
    visit_id = Column(String(50), primary_key=True, index=True)
    lead_id = Column(String(50), ForeignKey("leads.lead_id"), index=True, nullable=False)
    property_id = Column(String(50), ForeignKey("properties.property_id"), index=True, nullable=False)
    visit_date = Column(Date, nullable=False)
    visit_feedback = Column(String(50), index=True) # Positive, Neutral, Negative, Requested Second Visit
    visit_outcome = Column(String(50), index=True)  # Offer Expected, Second Visit Scheduled, Follow-up, No Interest
    agent_id = Column(String(50), index=True, nullable=False)
    
    lead = relationship("Lead", back_populates="visits")
    property = relationship("Property", back_populates="visits")

class Deal(Base):
    __tablename__ = "deals"
    
    deal_id = Column(String(50), primary_key=True, index=True)
    lead_id = Column(String(50), ForeignKey("leads.lead_id"), index=True, nullable=False)
    property_id = Column(String(50), ForeignKey("properties.property_id"), index=True, nullable=False)
    deal_date = Column(Date, nullable=False)
    deal_status = Column(String(50), index=True)    # Closed Won, Negotiation, Cancelled
    sale_price = Column(Float, nullable=False)
    commission_rate = Column(Float, nullable=False) # e.g. 0.02 = 2%
    agent_id = Column(String(50), index=True, nullable=False)
    
    lead = relationship("Lead", back_populates="deals")
    property = relationship("Property", back_populates="deals")

class AgentPerformance(Base):
    __tablename__ = "agent_performance"
    
    performance_id = Column(String(50), primary_key=True, index=True)
    agent_id = Column(String(50), index=True, nullable=False)
    period_month = Column(String(20), index=True, nullable=False) # e.g. '2026-05' to '2026-10'
    calls_made = Column(Integer, default=0)
    visits_conducted = Column(Integer, default=0)
    deals_closed = Column(Integer, default=0)
    customer_rating = Column(Float, default=0.0)
    marketing_spend = Column(Float, default=0.0)

class Expense(Base):
    __tablename__ = "expenses"
    
    expense_id = Column(String(50), primary_key=True, index=True)
    expense_date = Column(Date, nullable=False)
    project_id = Column(String(50), index=True, nullable=False)
    category = Column(String(50), index=True, nullable=False)     # Legal, Brokerage, Office Rent, Maintenance, Advertising, Travel
    amount = Column(Float, nullable=False)
    vendor = Column(String(100), nullable=True)
