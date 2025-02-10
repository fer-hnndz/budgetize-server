from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# * Should find a way to separate all these models in separate files as this is not scalable.


class Base(DeclarativeBase):
    pass


# This 3 models are used for next-auth integration.
class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )  # Not Pythonic, but This is the Way.
    type: Mapped[str] = mapped_column(nullable=False)
    provider: Mapped[str] = mapped_column(nullable=False)
    providerAccountId: Mapped[str] = mapped_column(nullable=False)
    refresh_token: Mapped[str]
    access_token: Mapped[str]
    expires_at: Mapped[float]
    token_type: Mapped[str]
    scope: Mapped[str]
    id_token: Mapped[str]
    session_state: Mapped[str]


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires: Mapped[datetime] = mapped_column(nullable=False)
    sessionToken: Mapped[str] = mapped_column(nullable=False)


class VerificationToken(Base):
    __tablename__ = "verification_token"
    id: Mapped[int] = mapped_column(primary_key=True)

    identifier: Mapped[str] = mapped_column(nullable=False)
    expires: Mapped[datetime] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    emailVerified: Mapped[datetime] = mapped_column(default=False)
    main_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    active: Mapped[bool] = mapped_column(default=True, server_default="true")
    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    accounts: Mapped["FinanceAccount"] = relationship(back_populates="user")


class FinanceAccount(Base):
    __tablename__ = "finance_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

    name: Mapped[str] = mapped_column(String(50))
    currency: Mapped[str] = mapped_column(String(3))
    icon: Mapped[str] = mapped_column(default="bank")
    active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="finance_account")
    transactions: Mapped["Transaction"] = relationship(back_populates="account")


class SharedFinanceAccount(Base):
    __tablename__ = "shared_finance_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_account: Mapped[int] = mapped_column(ForeignKey("finance_account.id"))

    write_permission: Mapped[bool] = mapped_column(default=False)
    write_others: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(back_populates="shared_finance_account")
    account: Mapped["Account"] = relationship(back_populates="shared_finance_account")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="category")
    name: Mapped[str] = mapped_column(String(50))


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_category: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    id_account: Mapped[int] = mapped_column(ForeignKey("finance_account.id"))

    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    deleted: Mapped[bool] = mapped_column(default=False)

    # * This represents if a transaction is taken into account for budget/monthly balance.
    # * Transactions like transfers or initial balances are created with visible set to false
    # * since those don't represent an expense or income.
    visible: Mapped[bool] = mapped_column(default=True)

    account: Mapped["Account"] = relationship(back_populates="transaction")
    user: Mapped["User"] = relationship(back_populates="transaction")
    category: Mapped["Category"] = relationship(back_populates="transaction")


class Budget(Base):
    __tablename__ = "budgets"

    id_budget: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))


class BudgetCategory(Base):
    __tablename__ = "budget_category"

    id_budget_category: Mapped[int] = mapped_column(primary_key=True)
    id_budget: Mapped[int] = mapped_column(ForeignKey("budgets.id_budget"))
    id_category: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    limit: Mapped[float] = mapped_column(nullable=False)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id_subscription: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    started: Mapped[datetime] = mapped_column(nullable=False)
    ends: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="subscription")
