from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.expense import CreateExpenseRequest, ExpenseResponse
from app.services.expense import create_expense, get_group_expenses
from app.services.group import is_member
from app.schemas.expense import CreateExpenseRequest, ExpenseResponse, SplitDetail


router = APIRouter(prefix="/groups/{group_id}/expenses", tags=["expenses"])

@router.post("", response_model=ExpenseResponse, status_code=201)
def add_expense(
    group_id: str,
    payload: CreateExpenseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not is_member(db, group_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this group")
    return create_expense(db, group_id, current_user.id, payload.description, payload.amount, payload.split_type, payload.splits)

@router.get("", response_model=list[ExpenseResponse])
def list_expenses(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not is_member(db, group_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this group")
    return get_group_expenses(db, group_id)

@router.post("/{expense_id}/splits")
def add_split(
    group_id: str,
    expense_id: str,
    payload: SplitDetail,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not is_member(db, group_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    from app.models.expense import Expense, ExpenseSplit
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    existing = db.query(ExpenseSplit).filter(
        ExpenseSplit.expense_id == expense_id,
        ExpenseSplit.user_id == payload.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already has a split for this expense")

    split = ExpenseSplit(expense_id=expense_id, user_id=payload.user_id, owed_amount=payload.amount)
    db.add(split)
    db.commit()
    return {"message": "Split added"}