from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50), unique=True, nullable=False, index=True)
    email         = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    # One user → many calculations
    calculations  = relationship("Calculation", back_populates="user")


class Calculation(Base):
    """
    Stores inputs, operation type, and the computed result.

    Design decision: we STORE the result rather than recomputing on demand.
    Reason: audit trail — you know exactly what was computed at that moment,
    even if the formula logic changes later.

    user_id is nullable — a calculation can exist without a logged-in user,
    but if provided it must reference a real User row (foreign key enforced).
    """
    __tablename__ = "calculations"

    id         = Column(Integer, primary_key=True, index=True)
    a          = Column(Float, nullable=False)
    b          = Column(Float, nullable=False)
    type       = Column(String(20), nullable=False)
    result     = Column(Float, nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="calculations")