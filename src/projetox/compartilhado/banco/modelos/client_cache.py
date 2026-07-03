from __future__ import annotations

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from projetox.compartilhado.banco.config import Base


class ClientCache(Base):
    __tablename__ = "client_cache"

    client_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(255))
    contacts: Mapped[dict] = mapped_column(JSONB, default=dict)
    last_synced: Mapped[datetime] = mapped_column(default=datetime.now)
