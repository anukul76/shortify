from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Text
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    deleted_on = Column(DateTime)

    users = relationship("User", back_populates="role_obj")


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    social_auth = Column(Boolean, default=False)
    social_auth_type = Column(String)
    social_auth_token = Column(String)
    role = Column(Integer, ForeignKey("role.id"))
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    deleted_on = Column(DateTime)

    role_obj = relationship("Role", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    links = relationship("UserLinks", back_populates="user")
    subscriptions = relationship("UserSubscriptions", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    username = Column(String, nullable=False)
    profile_pic = Column(String)
    age = Column(Integer)
    gender = Column(String)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    deleted_on = Column(DateTime)

    user = relationship("User", back_populates="profile")


class UserLinks(Base):
    __tablename__ = "user_links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    link = Column(String, nullable=False)
    short_link = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    expiry_timestamp = Column(DateTime)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    deleted_on = Column(DateTime)

    user = relationship("User", back_populates="links")


class UserSubscriptions(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    subscription_mode = Column(String, nullable=False)  # TRIAL, PREMIUM, ENTERPRISE
    expiry = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    deleted_on = Column(DateTime)

    user = relationship("User", back_populates="subscriptions")


class NotificationTemplates(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, nullable=False)
    template_slug = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    variables = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    deleted_on = Column(DateTime)

    notifications = relationship("Notifications", back_populates="template")


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    message_template_id = Column(Integer, ForeignKey("notification_templates.id"))
    status = Column(String)  # SCHEDULED, SUCCESS, FAILED
    failure_msg = Column(String)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    template = relationship("NotificationTemplates", back_populates="notifications")
