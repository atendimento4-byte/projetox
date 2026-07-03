from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from projetox.compartilhado.banco.config import Base

if TYPE_CHECKING:
    from projetox.compartilhado.banco.modelos.sessao import Session


class ActionLog(Base):
    __tablename__ = "action_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False,
    )
    action_type: Mapped[str] = mapped_column(String(30))
    action: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    decided_at: Mapped[datetime | None] = mapped_column()
    user_decision: Mapped[str | None] = mapped_column(String(20))
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
    previous_hash: Mapped[str | None] = mapped_column(String(64))

    session: Mapped[Session] = relationship(back_populates="action_logs")

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected', 'executed')",
            name="ck_action_logs_status",
        ),
        CheckConstraint(
            "user_decision IN ('approved', 'edited', 'rejected', 'snoozed')",
            name="ck_action_logs_user_decision",
        ),
        Index("idx_action_logs_session", "session_id"),
        Index("idx_action_logs_status", "status"),
    )
