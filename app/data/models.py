# app/data/models.py
from datetime import datetime
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Text, Float)
from sqlalchemy.orm import relationship
from app.data.db import Base

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True)
    tg_id         = Column(Integer, unique=True, index=True)
    username      = Column(String, nullable=True)
    credits       = Column(Integer, default=0)
    is_verified   = Column(Boolean, default=False)
    referred_by   = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at    = Column(DateTime, default=datetime.utcnow)
    entitlements  = relationship("Entitlement", back_populates="user")

class Studio(Base):
    __tablename__ = "studios"
    id    = Column(Integer, primary_key=True)
    name  = Column(String, unique=True, index=True)
    sets  = relationship("Set", back_populates="studio")

class Girl(Base):
    __tablename__ = "girls"
    id        = Column(Integer, primary_key=True)
    name      = Column(String, index=True)
    age       = Column(Integer, index=True)
    ethnicity = Column(String, index=True)
    sets      = relationship("Set", back_populates="girl")

class Set(Base):
    __tablename__ = "sets"
    id         = Column(Integer, primary_key=True)
    title      = Column(String)
    studio_id  = Column(Integer, ForeignKey("studios.id"))
    girl_id    = Column(Integer, ForeignKey("girls.id"))
    era        = Column(String, index=True)          # e.g. "2004"
    quality    = Column(String, default="sd")        # sd/hd/remaster
    price      = Column(Float, default=0.0)
    is_rare    = Column(Boolean, default=False)
    is_full    = Column(Boolean, default=False)
    thumb      = Column(String, nullable=True)
    preview    = Column(String, nullable=True)
    studio     = relationship("Studio", back_populates="sets")
    girl       = relationship("Girl", back_populates="sets")
    clips      = relationship("Clip", back_populates="set")

class Clip(Base):
    __tablename__ = "clips"
    id      = Column(Integer, primary_key=True)
    set_id  = Column(Integer, ForeignKey("sets.id"))
    path    = Column(String)                          # encoded path
    runtime = Column(Integer, default=0)
    set     = relationship("Set", back_populates="clips")

class Order(Base):
    __tablename__ = "orders"
    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey("users.id"))
    set_id     = Column(Integer, ForeignKey("sets.id"))
    amount     = Column(Float)
    rail       = Column(String)                        # shipstars / usdt
    status     = Column(String, default="pending")     # pending/paid/failed
    ref        = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Entitlement(Base):
    __tablename__ = "entitlements"
    id       = Column(Integer, primary_key=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    set_id   = Column(Integer, ForeignKey("sets.id"))
    granted  = Column(DateTime, default=datetime.utcnow)
    user     = relationship("User", back_populates="entitlements")

class Review(Base):
    __tablename__ = "reviews"
    id       = Column(Integer, primary_key=True)
    user_id  = Column(Integer, ForeignKey("users.id"))
    set_id   = Column(Integer, ForeignKey("sets.id"))
    stars    = Column(Integer)
    text     = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)