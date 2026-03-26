from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.expense import Expense, ExpenseSplit
from app.models.group import GroupMember

def get_group_member_ids(db: Session, group_id: str):
    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    return [m.user_id for m in members]

def create_expense(db: Session, group_id: str, paid_by: str, description: str, amount: Decimal, split_type: str, splits=None):
    expense = Expense(
        group_id=group_id,
        paid_by=paid_by,
        description=description,
        amount=amount,
        split_type=split_type
    )
    db.add(expense)
    db.flush()

    member_ids = get_group_member_ids(db, group_id)

    if split_type == "equal":
        share = round(amount / len(member_ids), 2)
        for user_id in member_ids:
            db.add(ExpenseSplit(expense_id=expense.id, user_id=user_id, owed_amount=share))

    elif split_type == "exact" and splits:
        for s in splits:
            db.add(ExpenseSplit(expense_id=expense.id, user_id=s.user_id, owed_amount=s.amount))

    elif split_type == "percentage" and splits:
        for s in splits:
            owed = round(amount * s.amount / 100, 2)
            db.add(ExpenseSplit(expense_id=expense.id, user_id=s.user_id, owed_amount=owed))

    db.commit()
    db.refresh(expense)
    return expense

def get_group_expenses(db: Session, group_id: str):
    return db.query(Expense).filter(Expense.group_id == group_id).all()