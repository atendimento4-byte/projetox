from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from projetox.compartilhado.banco.config import Base

if TYPE_CHECKING:
    from projetox.compartilhado.banco.modelos.action_log import ActionLog
    from projetox.compartilhado.banco.modelos.audio_log import AudioLog
    from projetox.compartilhado.banco.modelos.pending_action import PendingAction


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    ticket_id: Mapped[str | None] = mapped_column(String(50))
    client_name: Mapped[str] = mapped_column(String(255))
    client_company: Mapped[str | None] = mapped_column(String(255))
    technician: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="active")
    type: Mapped[str | None] = mapped_column(String(50))
    started_at: Mapped[datetime] = mapped_column(default=datetime.now)
    ended_at: Mapped[datetime | None] = mapped_column()
    metadados: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    audio_logs: Mapped[list[AudioLog]] = relationship(
        back_populates="session", cascade="all, delete-orphan",
    )
    action_logs: Mapped[list[ActionLog]] = relationship(
        back_populates="session", cascade="all, delete-orphan",
    )
    pending_actions: Mapped[list[PendingAction]] = relationship(
        back_populates="session", cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'paused', 'completed', 'cancelled')",
            name="ck_sessions_status",
        ),
        Index("idx_sessions_status", "status"),
        Index("idx_sessions_ticket", "ticket_id"),
        Index("idx_sessions_started", "started_at"),
    )
