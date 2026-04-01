// ══════════════════════════════════════════════════════════════════
//  Brand Intelligence Dashboard — Supabase Configuration & Queries
// ══════════════════════════════════════════════════════════════════

// ─── 1. Configuration ────────────────────────────────────────────
const SUPABASE_URL  = 'https://esycprngyhprwevxzrlz.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzeWNwcm5neWhwcndldnh6cmx6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM4MjI0MjgsImV4cCI6MjA4OTM5ODQyOH0.-pM5_L--_F4SOWzbiypD876aos4Gr_HgN04fm0GmUgo';

const supabase = window.supabase
  ? window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON)
  : null;

if (!supabase) {
  console.warn('[supabase-config] Supabase JS not loaded — all queries will return fallback data.');
}

// ─── 2. Helper ───────────────────────────────────────────────────
function applyDateRange(query, start, end, col = 'date') {
  if (start) query = query.gte(col, start);
  if (end)   query = query.lte(col, end);
  return query;
}

// ─── 3. Query Functions ──────────────────────────────────────────

/**
 * getMentions — raw mentions with optional filters
 */
async function getMentions({ brand, platform, startDate, endDate } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('mentions').select('*');
    if (brand)    q = q.eq('brand', brand);
    if (platform) q = q.eq('platform', platform);
    q = applyDateRange(q, startDate, endDate);
    q = q.order('date', { ascending: false }).limit(500);
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    return data;
  } catch (e) {
    console.warn('[getMentions] fallback —', e.message);
    return FALLBACK.mentions;
  }
}

/**
 * getSentimentStats — aggregated positive/negative/neutral percentages
 */
async function getSentimentStats({ brand, platform, startDate, endDate } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('engagement_stats').select('positive_count,negative_count,neutral_count,avg_sentiment_score');
    if (brand)    q = q.eq('brand', brand);
    if (platform) q = q.eq('platform', platform);
    q = applyDateRange(q, startDate, endDate);
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    const totP = data.reduce((s, r) => s + r.positive_count, 0);
    const totNeg = data.reduce((s, r) => s + r.negative_count, 0);
    const totNeu = data.reduce((s, r) => s + r.neutral_count, 0);
    const total = totP + totNeg + totNeu || 1;
    return {
      positive_pct: Math.round(totP / total * 100),
      negative_pct: Math.round(totNeg / total * 100),
      neutral_pct:  Math.round(totNeu / total * 100),
      avg_score:    +(data.reduce((s, r) => s + r.avg_sentiment_score, 0) / data.length).toFixed(2),
      total_mentions: total
    };
  } catch (e) {
    console.warn('[getSentimentStats] fallback —', e.message);
    return brand === 'chanel' ? FALLBACK.sentimentChanel : FALLBACK.sentimentHermes;
  }
}

/**
 * getShareOfVoice — SOV Hermès vs Chanel over a period
 */
async function getShareOfVoice({ startDate, endDate } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('engagement_stats').select('brand,total_mentions,share_of_voice');
    q = applyDateRange(q, startDate, endDate);
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    const byBrand = {};
    data.forEach(r => {
      if (!byBrand[r.brand]) byBrand[r.brand] = { mentions: 0, sov_sum: 0, count: 0 };
      byBrand[r.brand].mentions += r.total_mentions;
      byBrand[r.brand].sov_sum += r.share_of_voice;
      byBrand[r.brand].count++;
    });
    const result = {};
    for (const [b, v] of Object.entries(byBrand)) {
      result[b] = {
        total_mentions: v.mentions,
        avg_share_of_voice: +(v.sov_sum / v.count).toFixed(1)
      };
    }
    return result;
  } catch (e) {
    console.warn('[getShareOfVoice] fallback —', e.message);
    return FALLBACK.shareOfVoice;
  }
}

/**
 * getCompetitorPosts — competitor content filtered
 */
async function getCompetitorPosts({ brand, platform, startDate, endDate } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('competitor_posts').select('*');
    if (brand)    q = q.eq('brand', brand);
    if (platform) q = q.eq('platform', platform);
    q = applyDateRange(q, startDate, endDate);
    q = q.order('date', { ascending: false }).limit(200);
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    return data;
  } catch (e) {
    console.warn('[getCompetitorPosts] fallback —', e.message);
    return FALLBACK.competitorPosts;
  }
}

/**
 * getTrends — hashtags sorted by volume desc
 */
async function getTrends({ platform, startDate, endDate } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('trends').select('*');
    if (platform) q = q.eq('platform', platform);
    q = applyDateRange(q, startDate, endDate);
    q = q.order('volume', { ascending: false }).limit(100);
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    return data;
  } catch (e) {
    console.warn('[getTrends] fallback —', e.message);
    return FALLBACK.trends;
  }
}

/**
 * getAlerts — active alerts filtered by brand / severity / resolved
 */
async function getAlerts({ brand, severity, resolved } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('alerts').select('*');
    if (brand)    q = q.eq('brand', brand);
    if (severity) q = q.eq('severity', severity);
    if (resolved !== undefined) q = q.eq('is_resolved', resolved);
    q = q.order('date', { ascending: false }).limit(50);
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    return data;
  } catch (e) {
    console.warn('[getAlerts] fallback —', e.message);
    return FALLBACK.alerts;
  }
}

/**
 * getEngagementStats — aggregated engagement data
 */
async function getEngagementStats({ brand, platform, startDate, endDate } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('engagement_stats').select('*');
    if (brand)    q = q.eq('brand', brand);
    if (platform) q = q.eq('platform', platform);
    q = applyDateRange(q, startDate, endDate);
    q = q.order('date', { ascending: false });
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    return data;
  } catch (e) {
    console.warn('[getEngagementStats] fallback —', e.message);
    return FALLBACK.engagementStats;
  }
}

/**
 * getSentimentByLocation — avg sentiment grouped by country (for heatmap)
 */
async function getSentimentByLocation({ brand, startDate, endDate } = {}) {
  try {
    if (!supabase) throw new Error('no client');
    let q = supabase.from('mentions').select('location_country,sentiment_score');
    if (brand) q = q.eq('brand', brand);
    q = applyDateRange(q, startDate, endDate);
    const { data, error } = await q;
    if (error) throw error;
    if (!data || data.length === 0) throw new Error('empty');
    const grouped = {};
    data.forEach(r => {
      if (!r.location_country) return;
      if (!grouped[r.location_country]) grouped[r.location_country] = { sum: 0, n: 0 };
      grouped[r.location_country].sum += r.sentiment_score;
      grouped[r.location_country].n++;
    });
    return Object.entries(grouped).map(([country, v]) => ({
      country,
      avg_sentiment: +(v.sum / v.n).toFixed(3),
      mention_count: v.n
    })).sort((a, b) => b.mention_count - a.mention_count);
  } catch (e) {
    console.warn('[getSentimentByLocation] fallback —', e.message);
    return FALLBACK.sentimentByLocation;
  }
}

// ─── 4. Fallback Data ────────────────────────────────────────────
const FALLBACK = {
  sentimentHermes: {
    positive_pct: 65, negative_pct: 15, neutral_pct: 20,
    avg_score: 0.52, total_mentions: 8420
  },
  sentimentChanel: {
    positive_pct: 58, negative_pct: 18, neutral_pct: 24,
    avg_score: 0.41, total_mentions: 9130
  },
  shareOfVoice: {
    hermes: { total_mentions: 8420, avg_share_of_voice: 42.3 },
    chanel: { total_mentions: 9130, avg_share_of_voice: 57.7 }
  },
  mentions: [
    { id: 'f-1', brand: 'hermes', platform: 'instagram', text: 'The new Birkin colorway is absolutely stunning — Hermès never disappoints.', sentiment: 'positive', sentiment_score: 0.87, date: '2026-03-28T14:22:00Z', location_country: 'France', location_city: 'Paris', likes: 2340, comments: 187, shares: 54 },
    { id: 'f-2', brand: 'hermes', platform: 'tiktok', text: 'Unboxing my first Kelly — the leather quality is unreal 🧡', sentiment: 'positive', sentiment_score: 0.91, date: '2026-03-27T09:10:00Z', location_country: 'United States', location_city: 'New York', likes: 18200, comments: 943, shares: 312 },
    { id: 'f-3', brand: 'chanel', platform: 'twitter', text: 'Chanel raised prices AGAIN. At this point it\'s getting ridiculous.', sentiment: 'negative', sentiment_score: -0.72, date: '2026-03-26T18:44:00Z', location_country: 'United Kingdom', location_city: 'London', likes: 1820, comments: 412, shares: 198 },
    { id: 'f-4', brand: 'hermes', platform: 'trustpilot', text: 'Waited 14 months for a bag that arrived with scratches. Customer service was dismissive.', sentiment: 'negative', sentiment_score: -0.81, date: '2026-03-25T11:05:00Z', location_country: 'Germany', location_city: 'Munich', likes: 45, comments: 12, shares: 3 },
    { id: 'f-5', brand: 'chanel', platform: 'instagram', text: 'The Chanel 24C collection is giving old Chanel vibes — love it.', sentiment: 'positive', sentiment_score: 0.76, date: '2026-03-24T16:30:00Z', location_country: 'France', location_city: 'Paris', likes: 5670, comments: 321, shares: 88 },
    { id: 'f-6', brand: 'hermes', platform: 'reddit', text: 'Is the Hermès purchase experience really that gatekept? Seems absurd for 2026.', sentiment: 'neutral', sentiment_score: 0.05, date: '2026-03-23T20:15:00Z', location_country: 'United States', location_city: 'Los Angeles', likes: 890, comments: 234, shares: 0 },
    { id: 'f-7', brand: 'chanel', platform: 'tiktok', text: 'Chanel lipstick haul — the new rouge shades are gorgeous', sentiment: 'positive', sentiment_score: 0.68, date: '2026-03-22T12:00:00Z', location_country: 'China', location_city: 'Shanghai', likes: 9400, comments: 510, shares: 201 },
    { id: 'f-8', brand: 'hermes', platform: 'instagram', text: 'Hermès Arceau watch on the wrist — timeless elegance.', sentiment: 'positive', sentiment_score: 0.82, date: '2026-03-21T08:45:00Z', location_country: 'Japan', location_city: 'Tokyo', likes: 3100, comments: 98, shares: 42 }
  ],
  competitorPosts: [
    { id: 'cp-1', brand: 'chanel', platform: 'instagram', format: 'carousel', engagement_rate: 4.2, likes: 45200, comments: 1230, shares: 890, theme: 'New Collection Launch', date: '2026-03-27T10:00:00Z', caption_text: 'Introducing the CHANEL 24C collection — a modern ode to timeless Parisian elegance.' },
    { id: 'cp-2', brand: 'hermes', platform: 'instagram', format: 'reel', engagement_rate: 5.8, likes: 62000, comments: 2100, shares: 1450, theme: 'Craftsmanship', date: '2026-03-26T14:00:00Z', caption_text: 'From hand to heart: the art of Hermès leather craftsmanship.' },
    { id: 'cp-3', brand: 'chanel', platform: 'tiktok', format: 'reel', engagement_rate: 7.1, likes: 112000, comments: 4500, shares: 8900, theme: 'Behind the Scenes', date: '2026-03-25T18:30:00Z', caption_text: 'Inside the Chanel atelier — where every stitch tells a story.' },
    { id: 'cp-4', brand: 'hermes', platform: 'tiktok', format: 'reel', engagement_rate: 6.3, likes: 89000, comments: 3200, shares: 5600, theme: 'Product Showcase', date: '2026-03-24T11:00:00Z', caption_text: 'The Birkin in action — 3 ways to style your everyday icon.' }
  ],
  trends: [
    { id: 't-1', hashtag: '#Hermès', platform: 'instagram', volume: 284000, growth_rate: 12.4, date: '2026-03-28T00:00:00Z', related_brand: 'hermes' },
    { id: 't-2', hashtag: '#Chanel', platform: 'instagram', volume: 312000, growth_rate: 8.1, date: '2026-03-28T00:00:00Z', related_brand: 'chanel' },
    { id: 't-3', hashtag: '#Birkin', platform: 'tiktok', volume: 198000, growth_rate: 24.6, date: '2026-03-28T00:00:00Z', related_brand: 'hermes' },
    { id: 't-4', hashtag: '#QuietLuxury', platform: 'tiktok', volume: 156000, growth_rate: 31.2, date: '2026-03-28T00:00:00Z', related_brand: null },
    { id: 't-5', hashtag: '#ChanelClassicFlap', platform: 'instagram', volume: 89000, growth_rate: -3.2, date: '2026-03-28T00:00:00Z', related_brand: 'chanel' },
    { id: 't-6', hashtag: '#LuxuryUnboxing', platform: 'tiktok', volume: 245000, growth_rate: 18.7, date: '2026-03-28T00:00:00Z', related_brand: null }
  ],
  alerts: [
    { id: 'a-1', brand: 'chanel', alert_type: 'bad_buzz', severity: 'high', trigger_value: -0.72, threshold_value: -0.5, date: '2026-03-26T19:00:00Z', description: 'Spike in negative sentiment around Chanel price increases on Twitter/X.', is_resolved: false },
    { id: 'a-2', brand: 'hermes', alert_type: 'spike', severity: 'medium', trigger_value: 24.6, threshold_value: 15.0, date: '2026-03-25T08:00:00Z', description: '#Birkin hashtag volume surged +24.6% in 7 days on TikTok.', is_resolved: false },
    { id: 'a-3', brand: 'hermes', alert_type: 'drop', severity: 'low', trigger_value: -8.1, threshold_value: -10.0, date: '2026-03-20T06:00:00Z', description: 'Trustpilot review volume dropped 8% week-over-week.', is_resolved: true }
  ],
  engagementStats: [
    { id: 'es-1', brand: 'hermes', platform: 'instagram', date: '2026-03-28T00:00:00Z', total_mentions: 1240, positive_count: 806, negative_count: 186, neutral_count: 248, avg_sentiment_score: 0.54, share_of_voice: 43.2 },
    { id: 'es-2', brand: 'chanel', platform: 'instagram', date: '2026-03-28T00:00:00Z', total_mentions: 1630, positive_count: 945, negative_count: 293, neutral_count: 392, avg_sentiment_score: 0.38, share_of_voice: 56.8 },
    { id: 'es-3', brand: 'hermes', platform: 'tiktok', date: '2026-03-28T00:00:00Z', total_mentions: 980, positive_count: 637, negative_count: 147, neutral_count: 196, avg_sentiment_score: 0.51, share_of_voice: 41.0 },
    { id: 'es-4', brand: 'chanel', platform: 'tiktok', date: '2026-03-28T00:00:00Z', total_mentions: 1410, positive_count: 818, negative_count: 254, neutral_count: 338, avg_sentiment_score: 0.39, share_of_voice: 59.0 }
  ],
  sentimentByLocation: [
    { country: 'France',        avg_sentiment: 0.61, mention_count: 2840 },
    { country: 'United States', avg_sentiment: 0.48, mention_count: 2310 },
    { country: 'China',         avg_sentiment: 0.55, mention_count: 1920 },
    { country: 'Japan',         avg_sentiment: 0.63, mention_count: 1180 },
    { country: 'United Kingdom',avg_sentiment: 0.39, mention_count: 980 },
    { country: 'Germany',       avg_sentiment: 0.42, mention_count: 720 },
    { country: 'Italy',         avg_sentiment: 0.57, mention_count: 650 },
    { country: 'South Korea',   avg_sentiment: 0.51, mention_count: 540 },
    { country: 'UAE',           avg_sentiment: 0.58, mention_count: 430 },
    { country: 'Brazil',        avg_sentiment: 0.44, mention_count: 310 }
  ]
};
