// ══════════════════════════════════════════════════════════════════
//  Brand Intelligence Dashboard — Seed Script
//  Inserts ~200 realistic rows per table into Supabase
//
//  Usage:  Open seed.html in a browser, or run via Node with
//          npm install @supabase/supabase-js  &&  node seed.js
// ══════════════════════════════════════════════════════════════════

// ─── Config ──────────────────────────────────────────────────────
const SUPABASE_URL  = 'https://esycprngyhprwevxzrlz.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzeWNwcm5neWhwcndldnh6cmx6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM4MjI0MjgsImV4cCI6MjA4OTM5ODQyOH0.-pM5_L--_F4SOWzbiypD876aos4Gr_HgN04fm0GmUgo';

// Detect environment (browser vs Node)
let sbClient;
if (typeof window !== 'undefined' && window.supabase) {
  sbClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);
} else {
  const { createClient } = require('@supabase/supabase-js');
  sbClient = createClient(SUPABASE_URL, SUPABASE_ANON);
}

// ─── Helpers ─────────────────────────────────────────────────────
const pick  = arr => arr[Math.floor(Math.random() * arr.length)];
const rand  = (min, max) => Math.random() * (max - min) + min;
const randI = (min, max) => Math.floor(rand(min, max + 1));
const uuid  = () => crypto.randomUUID();

function randomDate(monthsBack = 12) {
  const now = new Date();
  const past = new Date(now);
  past.setMonth(past.getMonth() - monthsBack);
  return new Date(past.getTime() + Math.random() * (now.getTime() - past.getTime())).toISOString();
}

// ─── Constants ───────────────────────────────────────────────────
const BRANDS    = ['hermes', 'chanel'];
const PLATFORMS = ['instagram', 'tiktok', 'twitter', 'trustpilot', 'reddit'];
const FORMATS   = ['reel', 'story', 'carousel', 'post'];
const COUNTRIES = ['France', 'United States', 'China', 'Japan', 'United Kingdom', 'Germany', 'Italy', 'South Korea', 'UAE', 'Brazil', 'Switzerland', 'Singapore'];
const CITIES    = {
  'France': ['Paris', 'Lyon', 'Nice', 'Marseille'],
  'United States': ['New York', 'Los Angeles', 'Miami', 'Chicago'],
  'China': ['Shanghai', 'Beijing', 'Shenzhen', 'Guangzhou'],
  'Japan': ['Tokyo', 'Osaka', 'Kyoto'],
  'United Kingdom': ['London', 'Manchester', 'Edinburgh'],
  'Germany': ['Munich', 'Berlin', 'Hamburg'],
  'Italy': ['Milan', 'Rome', 'Florence'],
  'South Korea': ['Seoul', 'Busan'],
  'UAE': ['Dubai', 'Abu Dhabi'],
  'Brazil': ['São Paulo', 'Rio de Janeiro'],
  'Switzerland': ['Geneva', 'Zurich'],
  'Singapore': ['Singapore']
};

const THEMES = ['New Collection Launch', 'Craftsmanship', 'Behind the Scenes', 'Product Showcase', 'Celebrity Endorsement', 'Heritage Story', 'Sustainability', 'Pop-up Event', 'Fashion Week', 'Holiday Campaign'];

const HASHTAGS = [
  '#Hermès', '#Chanel', '#Birkin', '#Kelly', '#QuietLuxury', '#LuxuryUnboxing',
  '#ChanelClassicFlap', '#HermèsScarf', '#ChanelNo5', '#OldMoney', '#OOTD',
  '#LuxuryFashion', '#TimelessStyle', '#ParisianChic', '#HighFashion',
  '#DesignerBags', '#Couture', '#FashionWeek', '#ChanelBeauty', '#HermèsCraftsmanship'
];

const MENTION_TEXTS_HERMES = {
  positive: [
    'The craftsmanship on this Hermès piece is absolutely incredible.',
    'Finally got my dream Birkin — worth every moment of the wait!',
    'Hermès leather quality is in a league of its own.',
    'The Hermès boutique experience in Paris was magical.',
    'This Kelly bag is everything. Hermès knows timeless elegance.',
    'Hermès silk scarves are art you can wear. Just stunning.',
    'My Hermès Arceau watch — the best investment I ever made.',
    'The attention to detail at Hermès is unmatched in luxury.',
  ],
  negative: [
    'Waited 18 months for a Birkin only to be told they had none. Ridiculous.',
    'Hermès customer service has really gone downhill lately.',
    'The gatekeeping at Hermès is absurd — felt humiliated at the store.',
    'Got a defective belt buckle from Hermès. For that price? Unacceptable.',
  ],
  neutral: [
    'Visited the Hermès store today, still deciding on a colorway.',
    'Is the Hermès purchase journey really as hard as people say?',
    'Comparing Hermès and Chanel resale values — interesting data.',
    'Hermès just opened a new boutique downtown.',
  ]
};

const MENTION_TEXTS_CHANEL = {
  positive: [
    'The Chanel 24C collection is giving everything. Love it.',
    'My Chanel Classic Flap is the most versatile bag I own.',
    'Chanel beauty never misses — these new lip shades are gorgeous.',
    'The Chanel runway show was absolutely breathtaking this season.',
    'Just got the Chanel J12 watch. An icon.',
    'Chanel tweed jacket — a wardrobe staple for life.',
  ],
  negative: [
    'Chanel raised prices AGAIN. This is getting out of hand.',
    'Quality on new Chanel bags has dropped significantly. Disappointing.',
    'The Chanel lambskin peeled after 6 months. At this price point?!',
    'Chanel is losing its identity chasing trends. Karl would be disappointed.',
    'Terrible experience at Chanel — rude staff, long waits.',
  ],
  neutral: [
    'Chanel vs Dior — which classic flap do you prefer?',
    'Checking out the new Chanel pop-up in SoHo this weekend.',
    'Chanel resale market seems to be cooling down.',
    'Interesting to see Chanel\'s new sustainability report.',
  ]
};

const COMPETITOR_CAPTIONS_HERMES = [
  'From hand to heart: the art of Hermès leather craftsmanship.',
  'The Birkin in action — 3 ways to style your everyday icon.',
  'A journey through the Hermès silk universe.',
  'Inside our atelier: where patience becomes beauty.',
  'Hermès Arceau — time, elevated.',
  'The colors of spring, woven in Hermès silk.',
  'Hermès presents: the art of the equestrian world.',
  'New season, new palette. Discover Hermès leather goods.',
];

const COMPETITOR_CAPTIONS_CHANEL = [
  'Introducing the CHANEL 24C — a modern ode to Parisian elegance.',
  'Inside the Chanel atelier — where every stitch tells a story.',
  'CHANEL N°5: the fragrance that changed everything.',
  'The Chanel Classic Flap: an icon reimagined for a new era.',
  'Tweed dreams: the Chanel jacket in motion.',
  'CHANEL Haute Couture — the art of the extraordinary.',
  'Behind the scenes at the Chanel runway.',
  'New CHANEL Beauty: bold lips for bold women.',
];

const ALERT_DESCRIPTIONS = {
  hermes: {
    bad_buzz: [
      'Negative sentiment spike around Hermès store gatekeeping practices.',
      'Social media backlash over Hermès pricing strategy in emerging markets.',
    ],
    spike: [
      '#Birkin hashtag volume surged on TikTok after celebrity sighting.',
      'Hermès mention volume spiked after new collection announcement.',
    ],
    drop: [
      'Trustpilot review volume dropped week-over-week.',
      'Instagram engagement rate declined for Hermès posts.',
    ]
  },
  chanel: {
    bad_buzz: [
      'Spike in negative sentiment around Chanel price increases.',
      'Quality complaints trending on Reddit r/luxury.',
    ],
    spike: [
      'Chanel Beauty launch caused massive mention spike across platforms.',
      '#ChanelClassicFlap trending after influencer campaign.',
    ],
    drop: [
      'Share of voice dropped as competitor campaigns dominated.',
      'Chanel Twitter engagement declining steadily.',
    ]
  }
};

// ─── Generators ──────────────────────────────────────────────────

function generateMentions(count = 200) {
  const rows = [];
  for (let i = 0; i < count; i++) {
    const brand = pick(BRANDS);
    // Hermès: 65% positive, 20% neutral, 15% negative
    // Chanel: 58% positive, 24% neutral, 18% negative
    const r = Math.random();
    let sentiment, score;
    if (brand === 'hermes') {
      if (r < 0.65)      { sentiment = 'positive'; score = rand(0.3, 1.0); }
      else if (r < 0.85) { sentiment = 'neutral';  score = rand(-0.2, 0.2); }
      else               { sentiment = 'negative'; score = rand(-1.0, -0.2); }
    } else {
      if (r < 0.58)      { sentiment = 'positive'; score = rand(0.25, 0.95); }
      else if (r < 0.82) { sentiment = 'neutral';  score = rand(-0.2, 0.2); }
      else               { sentiment = 'negative'; score = rand(-1.0, -0.2); }
    }
    const texts = brand === 'hermes' ? MENTION_TEXTS_HERMES : MENTION_TEXTS_CHANEL;
    const country = pick(COUNTRIES);
    rows.push({
      id: uuid(),
      brand,
      platform: pick(PLATFORMS),
      text: pick(texts[sentiment]),
      sentiment,
      sentiment_score: +score.toFixed(3),
      date: randomDate(),
      location_country: country,
      location_city: pick(CITIES[country]),
      source_url: `https://example.com/${brand}/${randI(1000,9999)}`,
      likes: randI(10, 50000),
      comments: randI(1, 5000),
      shares: randI(0, 3000)
    });
  }
  return rows;
}

function generateCompetitorPosts(count = 200) {
  const rows = [];
  for (let i = 0; i < count; i++) {
    const brand = pick(BRANDS);
    const captions = brand === 'hermes' ? COMPETITOR_CAPTIONS_HERMES : COMPETITOR_CAPTIONS_CHANEL;
    rows.push({
      id: uuid(),
      brand,
      platform: pick(['instagram', 'tiktok']),
      format: pick(FORMATS),
      engagement_rate: +rand(1.0, 9.5).toFixed(2),
      likes: randI(5000, 150000),
      comments: randI(100, 8000),
      shares: randI(50, 12000),
      theme: pick(THEMES),
      date: randomDate(),
      caption_text: pick(captions)
    });
  }
  return rows;
}

function generateTrends(count = 200) {
  const rows = [];
  for (let i = 0; i < count; i++) {
    const hashtag = pick(HASHTAGS);
    let related = null;
    if (hashtag.toLowerCase().includes('hermès') || hashtag.toLowerCase().includes('birkin') || hashtag.toLowerCase().includes('kelly')) related = 'hermes';
    else if (hashtag.toLowerCase().includes('chanel')) related = 'chanel';
    rows.push({
      id: uuid(),
      hashtag,
      platform: pick(PLATFORMS),
      volume: randI(5000, 350000),
      growth_rate: +rand(-15, 40).toFixed(1),
      date: randomDate(),
      related_brand: related
    });
  }
  return rows;
}

function generateEngagementStats(count = 200) {
  const rows = [];
  for (let i = 0; i < count; i++) {
    const brand = pick(BRANDS);
    const total = randI(200, 3000);
    let pct_pos, pct_neg;
    if (brand === 'hermes') { pct_pos = rand(0.6, 0.72); pct_neg = rand(0.10, 0.18); }
    else                    { pct_pos = rand(0.52, 0.64); pct_neg = rand(0.14, 0.22); }
    const pos  = Math.round(total * pct_pos);
    const neg  = Math.round(total * pct_neg);
    const neu  = total - pos - neg;
    rows.push({
      id: uuid(),
      brand,
      platform: pick(PLATFORMS),
      date: randomDate(),
      total_mentions: total,
      positive_count: pos,
      negative_count: neg,
      neutral_count: neu,
      avg_sentiment_score: +rand(brand === 'hermes' ? 0.35 : 0.25, brand === 'hermes' ? 0.65 : 0.55).toFixed(3),
      share_of_voice: +rand(30, 70).toFixed(1)
    });
  }
  return rows;
}

function generateAlerts(count = 50) {
  const rows = [];
  const types = ['bad_buzz', 'spike', 'drop'];
  const severities = ['low', 'medium', 'high', 'critical'];
  for (let i = 0; i < count; i++) {
    const brand = pick(BRANDS);
    const type  = pick(types);
    rows.push({
      id: uuid(),
      brand,
      alert_type: type,
      severity: pick(severities),
      trigger_value: +rand(-1, 30).toFixed(2),
      threshold_value: +rand(-0.5, 15).toFixed(2),
      date: randomDate(),
      description: pick(ALERT_DESCRIPTIONS[brand][type]),
      is_resolved: Math.random() < 0.35
    });
  }
  return rows;
}

// ─── Insert ──────────────────────────────────────────────────────

async function seed() {
  const tables = [
    { name: 'mentions',          data: generateMentions(200) },
    { name: 'competitor_posts',  data: generateCompetitorPosts(200) },
    { name: 'trends',            data: generateTrends(200) },
    { name: 'engagement_stats',  data: generateEngagementStats(200) },
    { name: 'alerts',            data: generateAlerts(50) },
  ];

  for (const { name, data } of tables) {
    console.log(`Seeding "${name}" — ${data.length} rows...`);
    // Supabase has a ~1000-row limit per insert, batch by 50 for safety
    for (let i = 0; i < data.length; i += 50) {
      const batch = data.slice(i, i + 50);
      const { error } = await sbClient.from(name).insert(batch);
      if (error) {
        console.error(`  ✗ ${name} batch ${i}:`, error.message);
      } else {
        console.log(`  ✓ ${name} rows ${i}–${i + batch.length - 1}`);
      }
    }
  }
  console.log('\n✅ Seed complete.');
}

seed();
