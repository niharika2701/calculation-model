from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional
from pydantic import EmailStr

from app.calculations import OperationType


# ── User schemas (unchanged from Module 10) ───────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Calculation schemas ───────────────────────────────────────────────────────

class CalculationCreate(BaseModel):
    """
    What the caller sends in.

    Validations:
      - type must be one of: Add, Sub, Multiply, Divide (enum enforces this)
      - b cannot be zero when type is Divide (model_validator enforces this)
    """
    a:       float
    b:       float
    type:    OperationType
    user_id: Optional[int] = None

    @model_validator(mode="after")
    def no_division_by_zero(self) -> "CalculationCreate":
        if self.type == OperationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed — b must be non-zero")
        return self


class CalculationRead(BaseModel):
    """
    What the API returns.

    Always includes the computed result.
    Never exposes fields the caller didn't need (e.g. raw DB internals).
    """
    id:         int
    a:          float
    b:          float
    type:       OperationType
    result:     float
    user_id:    Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}