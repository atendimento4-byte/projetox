-- Sessões de acompanhamento
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id VARCHAR(50),
    client_name VARCHAR(255) NOT NULL,
    client_company VARCHAR(255),
    technician VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'paused', 'completed', 'cancelled')),
    type VARCHAR(50),
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_sessions_ticket ON sessions(ticket_id);
CREATE INDEX idx_sessions_started ON sessions(started_at);

-- Logs de áudio
CREATE TABLE audio_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id),
    file_path TEXT NOT NULL,
    duration_seconds INT,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'recorded'
        CHECK (status IN ('recorded', 'transcribed', 'processed', 'deleted'))
);

-- Logs de auditoria (append-only)
CREATE TABLE action_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id),
    action_type VARCHAR(30) NOT NULL,
    action VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'approved', 'rejected', 'executed')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    decided_at TIMESTAMP,
    user_decision VARCHAR(20)
        CHECK (user_decision IN ('approved', 'edited', 'rejected', 'snoozed')),
    details JSONB DEFAULT '{}',
    previous_hash VARCHAR(64)
);

CREATE INDEX idx_action_logs_session ON action_logs(session_id);
CREATE INDEX idx_action_logs_status ON action_logs(status);

-- Ações pendentes de aprovação
CREATE TABLE pending_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES sessions(id),
    action_type VARCHAR(30) NOT NULL,
    title VARCHAR(255) NOT NULL,
    preview TEXT,
    action_data JSONB NOT NULL,
    urgency VARCHAR(10) NOT NULL DEFAULT 'medium'
        CHECK (urgency IN ('low', 'medium', 'high')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pending_actions_urgency ON pending_actions(urgency);

-- Configurações do sistema
CREATE TABLE config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Cache de clientes (dados do Movidesk)
CREATE TABLE client_cache (
    client_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    contacts JSONB DEFAULT '{}',
    last_synced TIMESTAMP NOT NULL DEFAULT NOW()
);
