from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

# * Should find a way to separate all these models in separate files as this is not scalable.


class UserBase(SQLModel):
    email: str
    name: str
    picture_url: str | None = None


class User(UserBase, table=True):
    id_user: int = Field(primary_key=True)
    main_currency: str | None = Field(max_length=3)
    timezone: str | None = Field(default="UTC")
    active: bool = Field(default=True)


class Account(SQLModel, table=True):
    id_account: int = Field(primary_key=True)
    id_user: int = Field(foreign_key="user.id_user")
    name: str = Field(max_length=80)
    currency: str = Field(max_length=3)
    icon: str = Field(default="bank")
    active: bool = Field(default=True)


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

    # * This represents if a transaction is taken into account for budget/monthly balance.
    # * Transactions like transfers or initial balances are created with visible set to false
    # * since those don't represent an expense or income.
    visible: bool = Field(default=True)


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
    started: datetime
    ends: Optional[datetime]
