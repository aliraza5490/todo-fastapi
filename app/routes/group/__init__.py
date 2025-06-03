from uuid import UUID
from fastapi import APIRouter, Depends, Path, Query, Body
from typing import Union, List, Optional
from ...utilities.tags import Tags
from ...utilities.auth import get_user_from_token
from ...models.user import User
from sqlmodel import Session, SQLModel
from ...utilities.db import get_session
from ...models.group import GroupBase, GroupInvite
from .service import GroupService


group_router = APIRouter(prefix="/groups", tags=[Tags.groups])

# Group management routes
@group_router.post("/", summary="Create a new group")
def create_group(
    group: GroupBase,
    user: User = Depends(get_user_from_token), 
    session: Session = Depends(get_session)
):
    """
    Create a new group with the current user as admin
    """
    return GroupService.create_group(group, user, session)

@group_router.get("/{group_id}", summary="Get a specific group")
def read_group(
    group_id: UUID = Path(..., title="The ID of the group to retrieve"), 
    user: User = Depends(get_user_from_token), 
    session: Session = Depends(get_session)
):
    """
    Get details of a specific group if the user is a member
    """
    return GroupService.get_group(group_id, user, session)

@group_router.get("/", summary="Get all user groups")
def read_all_groups(
    q: Optional[str] = Query(None, title="Search query string"), 
    user: User = Depends(get_user_from_token), 
    session: Session = Depends(get_session)
):
    """
    Get all groups that the authenticated user is a member of
    """
    return GroupService.get_all_groups(user, session, q)

@group_router.put("/{group_id}", summary="Update a group")
def update_group(
    group_id: UUID = Path(..., title="The ID of the group to update"),
    group: GroupBase = Body(..., title="Updated group data"),
    user: User = Depends(get_user_from_token), 
    session: Session = Depends(get_session)
):
    """
    Update a group if the user is the admin
    """
    return GroupService.update_group(group_id, group, user, session)

@group_router.delete("/{group_id}", summary="Delete a group")
def delete_group(
    group_id: UUID = Path(..., title="The ID of the group to delete"),
    user: User = Depends(get_user_from_token), 
    session: Session = Depends(get_session)
):
    """
    Delete a group if the user is the admin
    """
    return GroupService.delete_group(group_id, user, session)

# Group membership routes
@group_router.post("/{group_id}/members/{user_id}", summary="Add user to group")
def add_member(
    group_id: UUID = Path(..., title="The ID of the group"),
    user_id: int = Path(..., title="The ID of the user to add"),
    user: User = Depends(get_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Add a user to a group if the current user is the admin
    """
    return GroupService.add_user_to_group(group_id, user_id, user, session)

@group_router.delete("/{group_id}/members/{user_id}", summary="Remove user from group")
def remove_member(
    group_id: UUID = Path(..., title="The ID of the group"),
    user_id: int = Path(..., title="The ID of the user to remove"),
    user: User = Depends(get_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Remove a user from a group if the current user is the admin
    """
    return GroupService.remove_user_from_group(group_id, user_id, user, session)

@group_router.get("/{group_id}/members", summary="Get group members")
def get_members(
    group_id: UUID = Path(..., title="The ID of the group"),
    user: User = Depends(get_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Get all members of a group if the user is a member
    """
    return GroupService.get_group_members(group_id, user, session)

# Group invitation route
@group_router.post("/{group_id}/invite", summary="Invite user to group by email")
def invite_to_group(
    group_id: UUID = Path(..., title="The ID of the group"),
    invite_data: GroupInvite = Body(..., title="Invitation data"),
    user: User = Depends(get_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Invite a user to a group by email if the current user is the admin
    """
    return GroupService.invite_user_to_group(group_id, invite_data, user, session)

# Search route
@group_router.get("/search/{search_term}", summary="Search for groups by name")
def search_groups(
    search_term: str = Path(..., title="The search term to look for in group names"),
    user: User = Depends(get_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Search for groups by name that the user is a member of
    """
    return GroupService.search_groups(search_term, user, session)
