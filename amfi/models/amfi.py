from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NAV(Base):
    __tablename__ = "nav_staging"

    id = Column(Integer, primary_key=True)
    scheme_type = Column(String(255), nullable=False)
    scheme_subtype = Column(String(255), nullable=False)
    fund_name = Column(String(255), nullable=False)
    scheme_code = Column(Integer, nullable=False)
    scheme_name = Column(String(255), nullable=False)
    isin_payout = Column(String(255), nullable=True)
    isin_reinvestment = Column(String(255), nullable=True)
    net_asset_value = Column(Float, nullable=True)
    repurchase_price = Column(Float, nullable=True)
    sale_price = Column(Float, nullable=True)
    nav_date = Column(Date, nullable=False)
