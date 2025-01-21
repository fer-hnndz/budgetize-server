from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from budgetize_server import data_models as bodies
from budgetize_server.database import engine, models
from budgetize_server.utils import get_user_from_token

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@router.get("/{token}")
async def get_accounts(token: str):
    """Returns the list of accounts for the user."""
    user = await get_user_from_token(token, engine)

    with Session(engine) as session:
        user_accounts = session.exec(
            select(models.Account)
            .where(models.Account.id_user == user.id_user)
            .where(models.Account.active == True)
        ).all()

        return user_accounts


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_account(account: bodies.AccountCreate):
    """Creates a new account for the user."""
    user = await get_user_from_token(account.user_token, engine)

    with Session(engine) as session:
        new_account = models.Account(
            name=account.name,
            id_user=user.id_user,
            currency=account.currency,
            active=True,
        )

        session.add(new_account)
        session.commit()

        if account.initial_balance:
            t = models.Transaction(
                id_user=user.id_user,
                id_account=new_account.id_account,
                amount=account.initial_balance,
                description="Initial Balance",
                visible=False,
            )
            session.add(t)

        return new_account
