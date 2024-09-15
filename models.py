from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(default=..., primary_key=True)
    login: str
    provider: str = "github"
    name: str | None = None
    email: str | None = None
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
