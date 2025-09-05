CREATE TABLE webhooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    secret TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE webhook_deliveries (
    id BIGSERIAL,
    webhook_id UUID REFERENCES webhooks(id) ON DELETE CASCADE,
    payload JSONB NOT NULL,
    delivered_at TIMESTAMPTZ DEFAULT now(),
    success BOOLEAN DEFAULT false,
    PRIMARY KEY (id, delivered_at)
) PARTITION BY RANGE (delivered_at);
