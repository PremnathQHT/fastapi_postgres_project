from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), index=True, nullable=False)
    email = Column(String(50), index=True, nullable=False)
    hash_password = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    verified=Column(Boolean,default=False)


    # Define relationship to UserRole
    roles = relationship("UserRole", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String(50), index=True, nullable=False)

    # Define relationship to UserRole
    users = relationship("UserRole", back_populates="role")

class UserRole(Base):
    __tablename__ = "userroles"
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'), primary_key=True)

    # Define relationships to User and Role
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")
