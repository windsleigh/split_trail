from pydantic import BaseModel
from typing import List, Optional

class CreateGroupRequest(BaseModel):
    name: str
    currency: str = "USD"

class AddMemberRequest(BaseModel):
    email: str

class GroupResponse(BaseModel):
    id: str
    name: str
    currency: str

    class Config:
        from_attributes = True

class MemberResponse(BaseModel):
    id: str
    email: str
    name: str

    class Config:
        from_attributes = True

class GroupDetailResponse(BaseModel):
    id: str
    name: str
    currency: str
    members: List[MemberResponse] = []

    class Config:
        from_attributes = True