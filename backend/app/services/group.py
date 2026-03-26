from sqlalchemy.orm import Session
from app.models.group import Group, GroupMember
from app.models.user import User

def create_group(db: Session, name: str, currency: str, user_id: str):
    group = Group(name=name, currency=currency)
    db.add(group)
    db.flush()
    member = GroupMember(group_id=group.id, user_id=user_id)
    db.add(member)
    db.commit()
    db.refresh(group)
    return group

def get_group(db: Session, group_id: str):
    return db.query(Group).filter(Group.id == group_id).first()

def get_user_groups(db: Session, user_id: str):
    return (
        db.query(Group)
        .join(GroupMember, Group.id == GroupMember.group_id)
        .filter(GroupMember.user_id == user_id)
        .all()
    )

def get_group_members(db: Session, group_id: str):
    return (
        db.query(User)
        .join(GroupMember, User.id == GroupMember.user_id)
        .filter(GroupMember.group_id == group_id)
        .all()
    )

def add_member(db: Session, group_id: str, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None, "User not found"
    existing = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user.id
    ).first()
    if existing:
        return None, "User already in group"
    member = GroupMember(group_id=group_id, user_id=user.id)
    db.add(member)
    db.commit()
    return user, None

def is_member(db: Session, group_id: str, user_id: str) -> bool:
    return db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first() is not None