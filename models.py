from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Enum, Float
from sqlalchemy.orm import relationship
import enum
import datetime

from database import Base

class MealType(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    preferences = Column(JSON) # JSONB in Postgres

    meal_plans = relationship("MealPlan", back_populates="user")
    shopping_lists = relationship("ShoppingList", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(JSON) # Array/JSON representing list of ingredients
    instructions = Column(String)
    cost_est = Column(Float)
    prep_time = Column(Integer) # in minutes

    meal_plans = relationship("MealPlan", back_populates="recipe")

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    meal_type = Column(String) # For simplicity string, can use Enum MealType

    user = relationship("User", back_populates="meal_plans")
    recipe = relationship("Recipe", back_populates="meal_plans")

class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    items = Column(JSON)
    is_purchased = Column(Boolean, default=False)

    user = relationship("User", back_populates="shopping_lists")
