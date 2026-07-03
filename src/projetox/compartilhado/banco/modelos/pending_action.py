from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from projetox.compartilhado.banco.config import Base

if TYPE_CHECKING:
    from projetox.compartilhado.banco.modelos.sessao import Session


class PendingAction(Base):
    __tablename__ = "pending_actions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False,
    )
    action_type: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(255))
    preview: Mapped[str | None] = mapped_column(Text)
    action_data: Mapped[dict] = mapped_column(JSONB)
    urgency: Mapped[str] = mapped_column(String(10), default="medium")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    session: Mapped[Session] = relationship(back_populates="pending_actions")

    __table_args__ = (
        CheckConstraint(
            "urgency IN ('low', 'medium', 'high')",
            name="ck_pending_actions_urgency",
        ),
        Index("idx_pending_actions_urgency", "urgency"),
    )
