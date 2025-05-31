from .validation import User, UserLogin
from fastapi import status, HTTPException
from sqlmodel import select, Session
from ...utilities.auth import pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta
from .validation import User as UserModel 

class AuthController:
    @classmethod
    def register(cls, user: User, session: Session):
        # Check if user with this email already exists
        existing_user = session.exec(select(UserModel).where(
            UserModel.email == user.email
        )).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user with hashed password
        new_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=pwd_context.hash(user.password),
            full_name=user.full_name,
            isActive=True
        )
        
        # Add to database and commit
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "message": "User registered successfully"
        }
    
    @classmethod
    def protected(cls, user: User):
        print(user)
        return {"message": "Protected route accessed"}

    @classmethod
    def login(cls, user: UserLogin, session: Session):
        user_data = session.exec(select(UserModel).where(
            UserModel.email == user.email, 
            UserModel.isActive == True
        )).first()
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        does_pass_match = pwd_context.verify(user.password, user_data.hashed_password)
        if not does_pass_match:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"email": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
