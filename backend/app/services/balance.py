from sqlalchemy.orm import Session
from decimal import Decimal
import heapq
from app.models.expense import Expense, ExpenseSplit
from app.models.settlement import Settlement

def compute_net_balances(db: Session, group_id: str) -> dict:
    """
    For each user, calculate: what they paid - what they owe.
    Positive = they are owed money (creditor).
    Negative = they owe money (debtor).
    """
    balances = {}

    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()

    for expense in expenses:
        paid_by = expense.paid_by
        if paid_by not in balances:
            balances[paid_by] = Decimal("0")
        balances[paid_by] += expense.amount

        for split in expense.splits:
            if not split.is_settled:
                if split.user_id not in balances:
                    balances[split.user_id] = Decimal("0")
                balances[split.user_id] -= split.owed_amount

    settlements = db.query(Settlement).filter(Settlement.group_id == group_id).all()
    for s in settlements:
        balances[s.payer_id] = balances.get(s.payer_id, Decimal("0")) + s.amount
        balances[s.payee_id] = balances.get(s.payee_id, Decimal("0")) - s.amount

    return balances

def simplify_debts(balances: dict) -> list:
    """
    Greedy debt simplification using two heaps.
    Minimizes the number of transactions needed to settle all debts.
    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    # Max heap for creditors (people owed money) — negate for Python's min heap
    creditors = []
    # Min heap for debtors (people who owe money)
    debtors = []

    for user_id, balance in balances.items():
        if balance > Decimal("0.01"):
            heapq.heappush(creditors, (-balance, user_id))
        elif balance < Decimal("-0.01"):
            heapq.heappush(debtors, (balance, user_id))

    transactions = []

    while creditors and debtors:
        credit_amt, creditor = heapq.heappop(creditors)
        debit_amt, debtor = heapq.heappop(debtors)

        credit_amt = -credit_amt
        debit_amt = -debit_amt

        settled = min(credit_amt, debit_amt)
        transactions.append({
            "from": debtor,
            "to": creditor,
            "amount": round(settled, 2)
        })

        remaining_credit = credit_amt - settled
        remaining_debit = debit_amt - settled

        if remaining_credit > Decimal("0.01"):
            heapq.heappush(creditors, (-remaining_credit, creditor))
        if remaining_debit > Decimal("0.01"):
            heapq.heappush(debtors, (-remaining_debit, debtor))

    return transactions