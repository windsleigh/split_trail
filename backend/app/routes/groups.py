from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.group import CreateGroupRequest, AddMemberRequest, GroupResponse, GroupDetailResponse, MemberResponse
from app.services.group import create_group, get_group, get_user_groups, get_group_members, add_member, is_member

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("", response_model=GroupResponse, status_code=201)
def create(payload: CreateGroupRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_group(db, payload.name, payload.currency, current_user.id)

@router.get("", response_model=list[GroupResponse])
def list_groups(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_groups(db, current_user.id)

@router.get("/{group_id}", response_model=GroupDetailResponse)
def get(group_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    group = get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not is_member(db, group_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this group")
    members = get_group_members(db, group_id)
    return GroupDetailResponse(id=group.id, name=group.name, currency=group.currency, members=members)

@router.post("/{group_id}/members", response_model=MemberResponse, status_code=201)
def add(group_id: str, payload: AddMemberRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_member(db, group_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this group")
    user, error = add_member(db, group_id, payload.email)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return user