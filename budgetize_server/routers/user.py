from datetime import datetime

from arrow import Arrow
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from budgetize_server.data_models import TokenBody
from budgetize_server.database import engine, models
from budgetize_server.utils import verify_google_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{id_token}")
async def get_current_user(id_token: str):
    """Returns the current dashboard data. Such as user's accounts and monthly balance."""

    user_data = verify_google_token(id_token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    with Session(engine) as session:
        users = session.exec(
            select(models.User).where(models.User.email == user_data.email)
        ).first()

        print("Users", users)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user_accounts = session.exec(
            select(models.Account).where(models.Account.id_user == users.id_user)
        ).all()

        # Retrieve all transactions from the current month
        start_of_month = datetime.now().replace(day=1)
        end_of_month = start_of_month + relativedelta(months=1)

        monthly_transactions = session.exec(
            select(models.Transaction)
            .where(models.Transaction.id_user == users.id_user)
            .where(models.Transaction.date >= start_of_month)
            .where(models.Transaction.date < end_of_month)
        ).all()

        monthly_expense = 0.0
        monthly_income = 0.0

        for transaction in monthly_transactions:
            if transaction.amount < 0:
                monthly_expense += transaction.amount
            else:
                monthly_income += transaction.amount

        monthly_balance = monthly_income + monthly_expense

        return {
            "user": users,
            "accounts": user_accounts,
            "currency": users.main_currency,
            "monthly_balance": monthly_balance,
            "monthly_income": monthly_income,
            "monthly_expense": monthly_expense,
        }


@router.post("/auth")
async def auth_user(data: TokenBody):
    """Allows User to authenticate themselves."""

    print("recieved token: ", data)
    user_data = verify_google_token(data.token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    with Session(engine) as session:
        user = session.exec(
            select(models.User).where(models.User.email == user_data.email)
        ).first()

        if not user:
            user = models.User(
                email=user_data.email,
                name=user_data.name,
                picture_url=user_data.picture_url,
            )
            session.add(user)
            session.commit()

    out = {
        "name": user_data.name,
        "email": user_data.email,
        "picture_url": user_data.picture_url,
    }

    print("Returning", out)
    return out
