from datetime import datetime

from arrow import Arrow
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from budgetize_server import data_models as bodies
from budgetize_server.currency_manager import CurrencyManager
from budgetize_server.database import engine, models
from budgetize_server.utils import get_user_from_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{token}")
async def user_general_info(token: str):
    """Returns the current dashboard data. Such as user's accounts and monthly balance."""

    user = await get_user_from_token(token, engine)

    with Session(engine) as session:
        if not user.main_currency or not user.timezone:
            return {
                "user": models.UserBase(
                    email=user.email,
                    name=user.name,
                    picture_url=user.picture_url,
                    timezone=user.timezone,
                ),
                "currency": user.main_currency,
                "accounts": [],
                "monthly_balance": 0,
                "monthly_income": 0,
                "monthly_expense": 0,
            }

        user_accounts = session.exec(
            select(models.Account)
            .where(models.Account.id_user == user.id_user)
            .where(models.Account.active == True)
        ).all()

        # Retrieve all transactions from the current month
        start_of_month = datetime.now().replace(day=1)
        end_of_month = start_of_month + relativedelta(months=1)

        monthly_transactions = session.exec(
            select(models.Transaction)
            .where(models.Transaction.id_user == user.id_user)
            .where(models.Transaction.date >= start_of_month)
            .where(models.Transaction.date < end_of_month)
        ).all()

        monthly_expense = 0.0
        monthly_income = 0.0

        mgr = CurrencyManager()
        for transaction in monthly_transactions:

            account = session.get(models.Account, transaction.id_account)

            if not account:
                return HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found.",
                )

            currency = account.currency

            convertedAmount = mgr.convert(
                currency, user.main_currency, transaction.amount
            )

            if transaction.amount < 0:
                monthly_expense += convertedAmount
            else:
                monthly_income += convertedAmount

        monthly_balance = monthly_income + monthly_expense

        return {
            "user": models.UserBase(
                email=user.email,
                name=user.name,
                picture_url=user.picture_url,
                timezone=user.timezone,
            ),
            "currency": user.main_currency,
            "accounts": user_accounts,
            "monthly_balance": monthly_balance,
            "monthly_income": monthly_income,
            "monthly_expense": monthly_expense,
        }


@router.put("/")
async def user_setup(body: bodies.SetupBody):
    """Sets up the user's main currency and timezone."""
    user = await get_user_from_token(body.token_id, engine)

    with Session(engine) as session:
        user.main_currency = body.main_currency
        user.timezone = body.timezone

        session.add(user)
        session.commit()

    return {"message": "User setup completed."}
