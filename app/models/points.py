from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime, timedelta
from models import Base
from sqlalchemy.orm import relationship


class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Float, nullable=False)
    description = Column(String, nullable=True)  # Reason or description for points
    created_at = Column(DateTime, default=lambda: datetime.now())

    # Relationship with Users model
    user = relationship("Users", back_populates="points_history")
