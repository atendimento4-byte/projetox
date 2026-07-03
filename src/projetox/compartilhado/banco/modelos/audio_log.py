from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from projetox.compartilhado.banco.config import Base

if TYPE_CHECKING:
    from projetox.compartilhado.banco.modelos.sessao import Session


class AudioLog(Base):
    __tablename__ = "audio_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False,
    )
    file_path: Mapped[str] = mapped_column(Text)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column()
    ended_at: Mapped[datetime | None] = mapped_column()
    status: Mapped[str] = mapped_column(String(20), default="recorded")

    session: Mapped[Session] = relationship(back_populates="audio_logs")

    __table_args__ = (
        CheckConstraint(
            "status IN ('recorded', 'transcribed', 'processed', 'deleted')",
            name="ck_audio_logs_status",
        ),
    )
