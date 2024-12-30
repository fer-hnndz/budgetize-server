from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

# * Should find a way to separate all these models in separate files as this is not scalable.


class UserBase(SQLModel):
    id_user: int = Field(primary_key=True)
    email: str
    provider_id: str
    name: str
    main_currency: str = Field(max_length=3)
    timezone: str = Field(default="UTC")


class User(UserBase, table=True):
    id_user: int = Field(primary_key=True)
    provider_id: str
    active: bool = Field(default=True)


class Account(SQLModel, table=True):
    id_account: int = Field(primary_key=True)
    id_user: int = Field(foreign_key="user.id_user")
    name: str = Field(max_length=80)
    currency: str = Field(max_length=3)
    icon: str = Field(default="bank")
    deleted: bool = Field(default=False)


class SharedAccountUser(SQLModel, table=True):
    id_account_user: int = Field(primary_key=True)
    id_user: int = Field(foreign_key="user.id_user")
    id_account: int = Field(foreign_key="account.id_account")
    write: bool = Field(default=False)


class Category(SQLModel, table=True):
    id_category: int = Field(primary_key=True)
    id_user: int = Field(foreign_key="user.id_user")
    name: str = Field(max_length=50)


class Transaction(SQLModel, table=True):
    id_transaction: int = Field(primary_key=True)
    id_account: int = Field(foreign_key="account.id_account")
    id_user: int = Field(foreign_key="user.id_user")
    id_category: int = Field(foreign_key="category.id_category")
    amount: float
    description: Optional[str] = Field(max_length=100)
    date: datetime
    deleted: bool = Field(default=False)


class Budget(SQLModel, table=True):
    id_budget: int = Field(primary_key=True)
    id_user: int = Field(foreign_key="user.id_user")


class BudgetCategory(SQLModel, table=True):
    id_budget_category: int = Field(primary_key=True)
    id_budget: int = Field(foreign_key="budget.id_budget")
    id_category: int = Field(foreign_key="category.id_category")
    limit: float


class Subscription(SQLModel, table=True):
    id_subscription: int = Field(primary_key=True)
    id_user: int = Field(foreign_key="user.id_user")
    ends: Optional[datetime]
