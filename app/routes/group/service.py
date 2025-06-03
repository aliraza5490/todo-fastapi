from fastapi import HTTPException
from typing import Union, List
from ...models.group import Group, GroupBase
from sqlmodel import Session, select
from ...models.user import User

class GroupService:
    @classmethod
    def create_group(cls, group: GroupBase, user: User, session: Session):
        """Create a new group with the current user as admin"""
        group_data = Group(
            **group.model_dump(),
            admin=user.id
        )
        # Add the creator to the group
        group_data.users.append(user)
        
        session.add(group_data)
        session.commit()
        session.refresh(group_data)
        return {"group_name": group.name, "group_id": group_data.id}
    
    @classmethod
    def get_group(cls, group_id: int, user: User, session: Session):
        """Get group by ID if user is a member"""
        group = cls._get_user_group(group_id, user, session)
        return group
    
    @classmethod
    def get_all_groups(cls, user: User, session: Session, q: Union[str, None] = None):
        """Get all groups that user is a member of"""
        query = select(Group).where(Group.users.any(id=user.id))
        
        if q:
            query = query.where(Group.name.ilike(f"%{q}%"))
            
        groups = session.exec(query).all()
        return {"groups": groups}
    
    @classmethod
    def update_group(cls, group_id: int, group: GroupBase, user: User, session: Session):
        """Update group if user is the admin"""
        group_data = cls._get_user_group(group_id, user, session)
        
        # Check if user is admin
        if group_data.admin != user.id:
            raise HTTPException(
                status_code=403,
                detail="Only the group admin can update this group"
            )
        
        # Update group attributes
        update_data = group.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(group_data, key, value)
            
        session.add(group_data)
        session.commit()
        session.refresh(group_data)
        
        return {"group_name": group_data.name, "group_id": group_id}
    
    @classmethod
    def delete_group(cls, group_id: int, user: User, session: Session):
        """Delete group if user is the admin"""
        group_data = cls._get_user_group(group_id, user, session)
        
        # Check if user is admin
        if group_data.admin != user.id:
            raise HTTPException(
                status_code=403,
                detail="Only the group admin can delete this group"
            )
            
        session.delete(group_data)
        session.commit()
        return {"group_id": group_id}
    
    @classmethod
    def _get_user_group(cls, group_id: int, user: User, session: Session) -> Group:
        """Helper method to check if user is a member of the group"""
        group = session.exec(
            select(Group).where(
                Group.id == group_id,
                Group.users.any(id=user.id)
            )
        ).first()
        
        if not group:
            raise HTTPException(
                status_code=404,
                detail=f"Group with id {group_id} not found or you don't have access to it."
            )
        return group

    @classmethod
    def add_user_to_group(cls, group_id: int, user_to_add_id: int, user: User, session: Session):
        """Add a user to a group if current user is admin"""
        group = cls._get_user_group(group_id, user, session)
        
        # Check if user is admin
        if group.admin != user.id:
            raise HTTPException(
                status_code=403,
                detail="Only the group admin can add users to this group"
            )
        
        # Get the user to add
        user_to_add = session.get(User, user_to_add_id)
        if not user_to_add:
            raise HTTPException(
                status_code=404,
                detail=f"User with id {user_to_add_id} not found"
            )
        
        # Check if already in group
        if user_to_add in group.users:
            return {"message": f"User {user_to_add_id} is already in group {group_id}"}
        
        # Add user to group
        group.users.append(user_to_add)
        session.add(group)
        session.commit()
        
        return {"message": f"User {user_to_add_id} added to group {group_id}"}
    
    @classmethod
    def remove_user_from_group(cls, group_id: int, user_to_remove_id: int, user: User, session: Session):
        """Remove a user from a group if current user is admin"""
        group = cls._get_user_group(group_id, user, session)
        
        # Check if user is admin
        if group.admin != user.id:
            raise HTTPException(
                status_code=403,
                detail="Only the group admin can remove users from this group"
            )
        
        # Get the user to remove
        user_to_remove = session.get(User, user_to_remove_id)
        if not user_to_remove:
            raise HTTPException(
                status_code=404,
                detail=f"User with id {user_to_remove_id} not found"
            )
        
        # Check if in group
        if user_to_remove not in group.users:
            return {"message": f"User {user_to_remove_id} is not in group {group_id}"}
        
        # Check if trying to remove admin
        if user_to_remove_id == group.admin:
            raise HTTPException(
                status_code=400,
                detail="Cannot remove the group admin from the group"
            )
        
        # Remove user from group
        group.users.remove(user_to_remove)
        session.add(group)
        session.commit()
        
        return {"message": f"User {user_to_remove_id} removed from group {group_id}"}

    @classmethod
    def get_group_members(cls, group_id: int, user: User, session: Session):
        """Get all members of a group if the user is a member"""
        group = cls._get_user_group(group_id, user, session)
        
        return {
            "group_id": group_id, 
            "group_name": group.name, 
            "members": group.users,
            "admin_id": group.admin
        }

    @classmethod
    def invite_user_to_group(cls, group_id: int, invite_data, user: User, session: Session):
        """Invite a user to a group by email if current user is admin"""
        group = cls._get_user_group(group_id, user, session)
        
        # Check if user is admin
        if group.admin != user.id:
            raise HTTPException(
                status_code=403,
                detail="Only the group admin can send invitations to this group"
            )
        
        # Get the user to invite by email
        user_to_invite = session.exec(select(User).where(User.email == invite_data.email)).first()
        if not user_to_invite:
            return {"message": f"Invitation will be sent to {invite_data.email} once they register"}
            
        # Check if already in group
        if user_to_invite in group.users:
            return {"message": f"User with email {invite_data.email} is already in group {group_id}"}
        
        # Add user to group directly if they exist
        group.users.append(user_to_invite)
        session.add(group)
        session.commit()
        
        return {"message": f"User with email {invite_data.email} added to group {group_id}"}

    @classmethod
    def search_groups(cls, search_term: str, user: User, session: Session):
        """Search for groups by name that the user is a member of"""
        if not search_term or len(search_term) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Search term must be at least 2 characters long"
            )
            
        query = select(Group).where(
            Group.users.any(id=user.id),
            Group.name.ilike(f"%{search_term}%")
        )
        
        groups = session.exec(query).all()
        return {"groups": groups, "search_term": search_term}

