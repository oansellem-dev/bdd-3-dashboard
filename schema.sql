-- ══════════════════════════════════════════════════════════════════
--  Brand Intelligence Dashboard — Supabase Schema
--  Run this in Supabase SQL Editor to create all tables
-- ══════════════════════════════════════════════════════════════════

-- 1. Mentions
CREATE TABLE IF NOT EXISTS mentions (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  brand            text NOT NULL CHECK (brand IN ('hermes', 'chanel')),
  platform         text NOT NULL CHECK (platform IN ('instagram', 'tiktok', 'twitter', 'trustpilot', 'reddit')),
  text             text,
  sentiment        text CHECK (sentiment IN ('positive', 'negative', 'neutral')),
  sentiment_score  float CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0),
  date             timestamptz DEFAULT now(),
  location_country text,
  location_city    text,
  source_url       text,
  likes            integer DEFAULT 0,
  comments         integer DEFAULT 0,
  shares           integer DEFAULT 0
);

-- 2. Competitor Posts
CREATE TABLE IF NOT EXISTS competitor_posts (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  brand           text NOT NULL,
  platform        text NOT NULL,
  format          text CHECK (format IN ('reel', 'story', 'carousel', 'post')),
  engagement_rate float,
  likes           integer DEFAULT 0,
  comments        integer DEFAULT 0,
  shares          integer DEFAULT 0,
  theme           text,
  date            timestamptz DEFAULT now(),
  caption_text    text
);

-- 3. Trends
CREATE TABLE IF NOT EXISTS trends (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  hashtag       text NOT NULL,
  platform      text NOT NULL,
  volume        integer DEFAULT 0,
  growth_rate   float,
  date          timestamptz DEFAULT now(),
  related_brand text
);

-- 4. Engagement Stats
CREATE TABLE IF NOT EXISTS engagement_stats (
  id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  brand              text NOT NULL,
  platform           text NOT NULL,
  date               timestamptz DEFAULT now(),
  total_mentions     integer DEFAULT 0,
  positive_count     integer DEFAULT 0,
  negative_count     integer DEFAULT 0,
  neutral_count      integer DEFAULT 0,
  avg_sentiment_score float,
  share_of_voice     float
);

-- 5. Alerts
CREATE TABLE IF NOT EXISTS alerts (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  brand           text NOT NULL,
  alert_type      text CHECK (alert_type IN ('bad_buzz', 'spike', 'drop')),
  severity        text CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  trigger_value   float,
  threshold_value float,
  date            timestamptz DEFAULT now(),
  description     text,
  is_resolved     boolean DEFAULT false
);

-- ─── Indexes for common queries ──────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_mentions_brand_date      ON mentions (brand, date DESC);
CREATE INDEX IF NOT EXISTS idx_mentions_platform        ON mentions (platform);
CREATE INDEX IF NOT EXISTS idx_mentions_sentiment        ON mentions (sentiment);
CREATE INDEX IF NOT EXISTS idx_mentions_country          ON mentions (location_country);
CREATE INDEX IF NOT EXISTS idx_competitor_brand_date     ON competitor_posts (brand, date DESC);
CREATE INDEX IF NOT EXISTS idx_trends_volume             ON trends (volume DESC);
CREATE INDEX IF NOT EXISTS idx_engagement_brand_date     ON engagement_stats (brand, date DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_brand_severity     ON alerts (brand, severity);
CREATE INDEX IF NOT EXISTS idx_alerts_resolved           ON alerts (is_resolved);

-- ─── RLS (Row Level Security) — allow anon read ──────────────────
ALTER TABLE mentions          ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitor_posts  ENABLE ROW LEVEL SECURITY;
ALTER TABLE trends            ENABLE ROW LEVEL SECURITY;
ALTER TABLE engagement_stats  ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts            ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow anon read" ON mentions          FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON competitor_posts  FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON trends            FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON engagement_stats  FOR SELECT USING (true);
CREATE POLICY "Allow anon read" ON alerts            FOR SELECT USING (true);

-- For seeding: allow anon insert (remove in production)
CREATE POLICY "Allow anon insert" ON mentions          FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON competitor_posts  FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON trends            FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON engagement_stats  FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon insert" ON alerts            FOR INSERT WITH CHECK (true);
