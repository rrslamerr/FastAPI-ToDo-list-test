from typing import Annotated

from app.db.session import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(get_db)]
