from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.balance import compute_net_balances, simplify_debts
from app.services.group import is_member, get_group_members

router = APIRouter(prefix="/groups/{group_id}", tags=["balances"])

@router.get("/balances")
def get_balances(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not is_member(db, group_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this group")

    balances = compute_net_balances(db, group_id)

    members = get_group_members(db, group_id)
    member_map = {m.id: m.name for m in members}

    return {
        "balances": [
            {
                "user_id": user_id,
                "name": member_map.get(user_id, "Unknown"),
                "balance": float(balance)
            }
            for user_id, balance in balances.items()
        ]
    }

@router.get("/simplify")
def get_simplified_debts(
    group_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not is_member(db, group_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this group")

    balances = compute_net_balances(db, group_id)
    transactions = simplify_debts(balances)

    members = get_group_members(db, group_id)
    member_map = {m.id: m.name for m in members}

    return {
        "transactions": [
            {
                "from_user": member_map.get(t["from"], "Unknown"),
                "to_user": member_map.get(t["to"], "Unknown"),
                "amount": t["amount"]
            }
            for t in transactions
        ]
    }