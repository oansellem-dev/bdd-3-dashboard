/* ================================================================
   components.js — Shared Navbar + Sidebar
   Usage: initComponents('page-id')
   Pages: dashboard | sentiment | share-of-voice | competitors |
          crisis-alert | trends | reports
   ================================================================ */

const _NAV_PAGES = [
  { id: 'dashboard',      label: 'Dashboard',      href: 'index.html' },
  { id: 'sentiment',      label: 'Sentiment',       href: 'sentiment.html' },
  { id: 'share-of-voice', label: 'Share of Voice',  href: 'share-of-voice.html' },
  { id: 'competitors',    label: 'Competitors',     href: '#' },
  { id: 'crisis-alert',   label: 'Crisis Alert',    href: 'crisis-alert.html' },
  { id: 'trends',         label: 'Trends',          href: 'trends.html' },
  { id: 'reports',        label: 'Reports',         href: 'reports.html' },
];

const _PAGE_TO_ICON = {
  'dashboard':      'home',
  'sentiment':      'chart',
  'share-of-voice': 'pie',
  'competitors':    'users',
  'crisis-alert':   'bell',
  'trends':         'trending',
  'reports':        'folder',
};

const _SIDE_ITEMS = [
  {
    id: 'home', href: 'index.html',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9L9 3l6 6"/><path d="M5 7v8h4v-4h4v4h4V7"/></svg>`
  },
  {
    id: 'chart', href: 'sentiment.html',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><rect x="3" y="11" width="3" height="4"/><rect x="7.5" y="7" width="3" height="8"/><rect x="12" y="3" width="3" height="12"/></svg>`
  },
  {
    id: 'pie', href: 'share-of-voice.html',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="9" cy="9" r="6"/><path d="M9 3v6l4 2" stroke-linecap="round"/></svg>`
  },
  {
    id: 'users', href: '#',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="7" cy="7" r="3"/><path d="M1 17c0-3 2.7-5 6-5s6 2 6 5"/><path d="M13 5a3 3 0 010 6M17 17c0-2.5-1.5-4-4-4.5"/></svg>`
  },
  {
    id: 'bell', href: 'crisis-alert.html',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M9 3a5 5 0 015 5c0 4 1.5 5 1.5 5h-13S4 12 4 8a5 5 0 015-5z"/><path d="M7 16a2 2 0 004 0"/></svg>`
  },
  {
    id: 'trending', href: 'trends.html',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 13 7 5 11 10 15 3"/></svg>`
  },
  {
    id: 'folder', href: 'reports.html',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2 6a2 2 0 012-2h3l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>`
  },
  { id: 'gap' },
  {
    id: 'settings', href: '#',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="3"/><path d="M9 1v2M9 15v2M1 9h2M15 9h2M3.2 3.2l1.4 1.4M13.4 13.4l1.4 1.4M3.2 14.8l1.4-1.4M13.4 4.6l1.4-1.4"/></svg>`
  },
  {
    id: 'logout', href: '#',
    svg: `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M11 4H5a2 2 0 00-2 2v8a2 2 0 002 2h6M15 9H7M12 6l3 3-3 3"/></svg>`
  },
];

/* ── CSS injection ────────────────────────────────────────── */
function _injectCSS() {
  if (document.getElementById('_comp-css')) return;
  const s = document.createElement('style');
  s.id = '_comp-css';
  s.textContent = `
    /* ── Unified navbar override ── */
    nav.nav {
      background: rgba(245,240,232,.96) !important;
      backdrop-filter: blur(14px) !important;
      -webkit-backdrop-filter: blur(14px) !important;
      border-bottom: 1px solid rgba(0,0,0,.06) !important;
    }

    /* ── Nav links ── */
    .cn-logo {
      width: 36px; height: 36px;
      display: flex; align-items: center; justify-content: center;
      margin-right: 16px; flex-shrink: 0;
    }
    .cn-sep {
      color: #999; font-size: 14px; padding: 0 1px;
      font-weight: 300; flex-shrink: 0;
    }
    .cn-link {
      padding: 6px 13px; border-radius: 20px;
      font-size: 14px; font-weight: 500;
      color: rgba(0,0,0,.55);
      cursor: pointer; white-space: nowrap;
      text-decoration: none;
      font-family: 'Inter', sans-serif;
      background: none; border: none;
      transition: background .15s, color .15s;
    }
    .cn-link:hover { color: #000; background: rgba(0,0,0,.04); }
    .cn-link.on    { background: #E8383D; color: #fff; font-weight: 600; }

    /* ── Nav right ── */
    .cn-r {
      margin-left: auto;
      display: flex; align-items: center; gap: 8px;
    }
    .cn-toggle {
      display: flex; align-items: center; gap: 5px;
      background: rgba(0,0,0,.06); border-radius: 20px;
      padding: 6px 12px; cursor: pointer;
    }
    .cn-toggle svg { color: #1A1A1A; }
    .cn-bell {
      width: 34px; height: 34px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer; position: relative; color: #1A1A1A;
    }
    .cn-dot {
      position: absolute; top: 5px; right: 5px;
      width: 8px; height: 8px;
      background: #E8383D; border-radius: 50%;
      border: 2px solid rgba(245,240,232,.96);
    }
    .cn-av {
      width: 36px; height: 36px; border-radius: 50%;
      background: linear-gradient(145deg, #7B5B3A, #4A2E15);
      overflow: hidden; display: flex; align-items: center;
      justify-content: center; cursor: pointer; flex-shrink: 0;
    }

    /* ── Sidebar override ── */
    aside.side {
      background: #F5F0E8 !important;
      border-right: 1px solid rgba(0,0,0,.07) !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      padding: 16px 0 !important;
      gap: 4px !important;
    }

    /* ── Sidebar icons ── */
    .cs-ico {
      width: 38px; height: 38px; border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      color: #999; cursor: pointer; transition: .15s;
      text-decoration: none; flex-shrink: 0;
    }
    .cs-ico:hover  { background: rgba(0,0,0,.06); color: #555; }
    .cs-ico.on     { background: rgba(0,0,0,.08); color: #1A1A1A; }
    .cs-gap        { flex: 1; }
  `;
  document.head.appendChild(s);
}

/* ── Render navbar ────────────────────────────────────────── */
function renderNavbar(activePage) {
  const logoSVG = `
    <svg viewBox="0 0 32 32" fill="none" width="28" height="28">
      <path d="M5 26L12 6h4L10 26H5z" fill="#E8383D"/>
      <path d="M13 26L20 6h4L18 26h-5z" fill="#1A1A1A" opacity=".45"/>
    </svg>`;

  let links = '';
  _NAV_PAGES.forEach((p, i) => {
    if (i > 0) links += `<span class="cn-sep">/</span>`;
    const isActive = p.id === activePage;
    if (isActive) {
      links += `<span class="cn-link on">${p.label}</span>`;
    } else {
      links += `<a href="${p.href}" class="cn-link">${p.label}</a>`;
    }
  });

  const right = `
    <div class="cn-r">
      <div class="cn-toggle">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">
          <circle cx="7" cy="7" r="2.5"/>
          <path d="M7 1.5v1M7 11v1M1.5 7h1M11 7h1M3.1 3.1l.7.7M10.2 10.2l.7.7M3.1 10.9l.7-.7M10.2 3.8l.7-.7"/>
        </svg>
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">
          <path d="M12 12a6 6 0 01-6-6 4.5 4.5 0 106 6z"/>
        </svg>
      </div>
      <div class="cn-bell">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <path d="M9 3a5 5 0 015 5c0 4 1.5 5 1.5 5h-13S4 12 4 8a5 5 0 015-5z"/>
          <path d="M7 16a2 2 0 004 0"/>
        </svg>
        <div class="cn-dot"></div>
      </div>
      <div class="cn-av">
        <svg width="18" height="18" fill="none" stroke="rgba(255,255,255,.7)" stroke-width="1.4">
          <circle cx="9" cy="7" r="3"/>
          <path d="M3.5 17c0-3 2.5-4.5 5.5-4.5s5.5 1.5 5.5 4.5"/>
        </svg>
      </div>
    </div>`;

  return `<div class="cn-logo">${logoSVG}</div>${links}${right}`;
}

/* ── Render sidebar ───────────────────────────────────────── */
function renderSidebar(activeIconId) {
  return _SIDE_ITEMS.map(item => {
    if (item.id === 'gap') return `<div class="cs-gap"></div>`;
    const isOn = item.id === activeIconId ? ' on' : '';
    return `<a href="${item.href}" class="cs-ico${isOn}">${item.svg}</a>`;
  }).join('');
}

/* ── Main init ────────────────────────────────────────────── */
function initComponents(activePage) {
  _injectCSS();

  const activeIcon = _PAGE_TO_ICON[activePage] || 'home';

  // Inject navbar
  const nav = document.querySelector('nav.nav');
  if (nav) nav.innerHTML = renderNavbar(activePage);

  // Inject sidebar
  const side = document.querySelector('aside.side');
  if (side) side.innerHTML = renderSidebar(activeIcon);
}
