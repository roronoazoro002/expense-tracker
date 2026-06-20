from pydantic import BaseModel
from typing import Optional, List
from datetime import date as date_type
from decimal import Decimal


# ---- Category schemas ----

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    is_fixed: bool = False
    monthly_budget: Optional[Decimal] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# ---- Transaction item schemas ----

class TransactionItemBase(BaseModel):
    category_id: Optional[int] = None
    amount: Decimal
    notes: Optional[str] = None


class TransactionItemCreate(TransactionItemBase):
    pass


class TransactionItemOut(TransactionItemBase):
    id: int

    class Config:
        from_attributes = True


# ---- Transaction schemas ----

class TransactionBase(BaseModel):
    date: date_type
    description: str
    account: Optional[str] = None


class TransactionCreate(TransactionBase):
    items: List[TransactionItemCreate]  # at least one line item required


class TransactionOut(TransactionBase):
    id: int
    source: str
    items: List[TransactionItemOut]

    class Config:
        from_attributes = True