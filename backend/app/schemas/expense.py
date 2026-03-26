from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

class SplitDetail(BaseModel):
    user_id: str
    amount: Decimal

class CreateExpenseRequest(BaseModel):
    description: str
    amount: Decimal
    split_type: str = "equal"
    splits: Optional[List[SplitDetail]] = None

class ExpenseSplitResponse(BaseModel):
    user_id: str
    owed_amount: Decimal
    is_settled: bool

    class Config:
        from_attributes = True

class ExpenseResponse(BaseModel):
    id: str
    description: str
    amount: Decimal
    split_type: str
    paid_by: str
    splits: List[ExpenseSplitResponse] = []

    class Config:
        from_attributes = True