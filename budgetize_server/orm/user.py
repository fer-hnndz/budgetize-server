from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from budgetize_server import db


class User(db.Model):  # pylint: disable=too-few-public-methods
    """Database ORM for users table. Represents a user of the application."""

    id: Mapped[str] = mapped_column(primary_key=True)
    preffered_currency: Mapped[str] = mapped_column(String(3))
    entered_on: Mapped[float]
    # The user's timestamp in UTC when
    # the user was created on the database.
    # This is saved since users who have been in the database
    # for more than 2 hours are deleted
    # This is done as a cleanup to not exceed any limits on free hosting.

    def __repr__(self) -> str:
        """String representation of the User object."""
        return f"<User(id={self.id}, preffered_currency={self.preffered_currency}, entered_on={self.entered_on})>"
