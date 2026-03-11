from db.database import Base
from sqlalchemy import Column, String, Integer, Float
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Products(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), index=True)
    price = Column(Float)
    stock = Column(Integer)
    aisle = Column(String(100))
