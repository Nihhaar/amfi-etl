from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NAV(Base):
    __tablename__ = "nav_staging"

    id = Column(Integer, primary_key=True)
    scheme_type = Column(String, nullable=False)
    scheme_subtype = Column(String, nullable=False)
    fund_name = Column(String, nullable=False)
    scheme_code = Column(Integer, nullable=False)
    scheme_name = Column(String, nullable=False)
    isin_payout = Column(String, nullable=True)
    isin_reinvestment = Column(String, nullable=True)
    net_asset_value = Column(Float, nullable=True)
    repurchase_price = Column(Float, nullable=True)
    sale_price = Column(Float, nullable=True)
    nav_date = Column(Date, nullable=False)
