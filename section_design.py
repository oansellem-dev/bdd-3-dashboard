import streamlit as st

CSS_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #F5F6FA !important;
    color: #0F172A;
}

[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

footer {
    display: none !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ===== NAVBAR ===== */
.hd-navbar {
    display: flex;
    align-items: center;
    gap: 0px;
    background: #FFFFFF;
    border-bottom: 1px solid #F3F4F6;
    padding: 0 32px;
    height: 64px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.hd-navbar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    flex-shrink: 0;
}

.hd-logo-circle {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: #4F46E5;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    font-family: 'Inter', sans-serif;
}

.hd-logo-title {
    font-size: 20px;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.5px;
    font-family: 'Inter', sans-serif;
}

.hd-logo-title span {
    color: #B07A0A;
}

.hd-navbar-tabs {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-left: 40px;
    flex: 1;
}

.hd-tab {
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #6B7280;
    cursor: pointer;
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
    white-space: nowrap;
    font-family: 'Inter', sans-serif;
}

.hd-tab:hover {
    background: #F3F4F6;
    color: #0F172A;
}

.hd-tab.active {
    background: #EEF2FF;
    color: #4F46E5;
    font-weight: 600;
}

.hd-navbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-shrink: 0;
}

.hd-search-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 8px 14px;
    width: 220px;
}

.hd-search-bar input {
    border: none;
    background: transparent;
    outline: none;
    font-size: 13px;
    color: #6B7280;
    font-family: 'Inter', sans-serif;
    width: 100%;
}

.hd-search-icon {
    color: #9CA3AF;
    font-size: 14px;
    flex-shrink: 0;
}

.hd-icon-btn {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background: #F3F4F6;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    color: #6B7280;
    transition: background 0.15s;
    border: none;
}

.hd-icon-btn:hover {
    background: #E5E7EB;
}

.hd-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    color: #FFFFFF;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    flex-shrink: 0;
}

/* ===== PAGE WRAPPER ===== */
.hd-page {
    padding: 28px 32px;
    background: #F5F6FA;
    min-height: calc(100vh - 64px);
}

/* ===== CARDS ===== */
.hd-card {
    background: #FFFFFF;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.055);
    border: 1px solid #F3F4F6;
    padding: 24px;
    height: 100%;
}

.hd-card-sm {
    background: #FFFFFF;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.055);
    border: 1px solid #F3F4F6;
    padding: 18px 20px;
}

/* ===== METRIC CARDS ===== */
.hd-metric-card {
    background: #FFFFFF;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.055);
    border: 1px solid #F3F4F6;
    padding: 22px 24px 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 0px;
    min-height: 160px;
    position: relative;
    overflow: hidden;
}

.hd-metric-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 4px;
}

.hd-metric-title {
    font-size: 13px;
    font-weight: 500;
    color: #6B7280;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.01em;
}

.hd-metric-badge {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.02em;
}

.hd-metric-value-row {
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin-top: 2px;
}

.hd-metric-value {
    font-size: 38px;
    font-weight: 700;
    color: #4F46E5;
    line-height: 1.1;
    letter-spacing: -1px;
    font-family: 'Inter', sans-serif;
}

.hd-metric-unit {
    font-size: 15px;
    font-weight: 500;
    color: #9CA3AF;
    font-family: 'Inter', sans-serif;
    margin-bottom: 4px;
}

.hd-metric-goal-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 6px;
}

.hd-metric-goal-label {
    font-size: 12px;
    color: #9CA3AF;
    font-family: 'Inter', sans-serif;
}

.hd-metric-goal-value {
    font-size: 12px;
    font-weight: 600;
    color: #0F172A;
    font-family: 'Inter', sans-serif;
}

.hd-metric-progress {
    width: 100%;
    height: 6px;
    background: #F3F4F6;
    border-radius: 999px;
    margin-top: 10px;
    overflow: hidden;
}

.hd-metric-progress-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s ease;
}

.hd-metric-sub {
    font-size: 11.5px;
    color: #9CA3AF;
    margin-top: 8px;
    font-family: 'Inter', sans-serif;
}

.hd-metric-accent-strip {
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    border-radius: 16px 0 0 16px;
}

/* ===== LIST ITEMS ===== */
.hd-list-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.hd-list-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    border-radius: 12px;
    cursor: pointer;
    transition: background 0.15s;
    background: transparent;
}

.hd-list-item:hover {
    background: #F9FAFB;
}

.hd-list-item.active {
    background: #4F46E5;
}

.hd-list-item.active .hd-item-title {
    color: #FFFFFF;
}

.hd-list-item.active .hd-item-sub {
    color: rgba(255,255,255,0.7);
}

.hd-item-icon-wrap {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.hd-item-text {
    flex: 1;
    min-width: 0;
}

.hd-item-title {
    font-size: 14px;
    font-weight: 600;
    color: #0F172A;
    font-family: 'Inter', sans-serif;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.hd-item-sub {
    font-size: 12px;
    color: #9CA3AF;
    font-family: 'Inter', sans-serif;
    margin-top: 1px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.hd-badge {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    flex-shrink: 0;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.01em;
}

/* ===== CALENDAR PILLS ===== */
.hd-cal-strip {
    display: flex;
    gap: 6px;
    align-items: center;
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 2px;
}

.hd-cal-day {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 56px;
    border-radius: 12px;
    cursor: pointer;
    background: #F9FAFB;
    border: 1.5px solid transparent;
    transition: background 0.15s, border-color 0.15s;
    flex-shrink: 0;
}

.hd-cal-day:hover {
    background: #EEF2FF;
    border-color: #C7D2FE;
}

.hd-cal-day.active {
    background: #4F46E5;
    border-color: #4F46E5;
}

.hd-cal-day-letter {
    font-size: 10px;
    font-weight: 500;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-family: 'Inter', sans-serif;
}

.hd-cal-day.active .hd-cal-day-letter {
    color: rgba(255,255,255,0.75);
}

.hd-cal-day-num {
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    font-family: 'Inter', sans-serif;
    line-height: 1.2;
}

.hd-cal-day.active .hd-cal-day-num {
    color: #FFFFFF;
}

/* ===== ALERT DARK CARD ===== */
.hd-alert-dark {
    background: #0F172A;
    border-radius: 16px;
    padding: 22px 24px;
    color: #FFFFFF;
    position: relative;
    overflow: hidden;
}

.hd-alert-dark-glow {
    position: absolute;
    top: -30px;
    right: -30px;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(79,70,229,0.35) 0%, transparent 70%);
    pointer-events: none;
}

.hd-alert-dark-glow2 {
    position: absolute;
    bottom: -20px;
    left: 30px;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(176,122,10,0.2) 0%, transparent 70%);
    pointer-events: none;
}

.hd-alert-dark-icon {
    font-size: 28px;
    margin-bottom: 10px;
    display: block;
}

.hd-alert-dark-title {
    font-size: 16px;
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    margin-bottom: 6px;
}

.hd-alert-dark-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.5);
    font-family: 'Inter', sans-serif;
    margin-bottom: 16px;
    line-height: 1.5;
}

.hd-alert-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.hd-alert-tag {
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.02em;
}

.hd-alert-tag-indigo {
    background: rgba(79,70,229,0.25);
    color: #A5B4FC;
    border: 1px solid rgba(79,70,229,0.35);
}

.hd-alert-tag-gold {
    background: rgba(176,122,10,0.2);
    color: #FCD34D;
    border: 1px solid rgba(176,122,10,0.35);
}

.hd-alert-tag-ghost {
    background: rgba(255,255,255,0.07);
    color: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.12);
}

/* ===== SECTION TITLES ===== */
.hd-section-title {
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    font-family: 'Inter', sans-serif;
    margin-bottom: 14px;
    letter-spacing: -0.2px;
}

.hd-section-subtitle {
    font-size: 12px;
    color: #9CA3AF;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    margin-left: 8px;
}

/* ===== PROGRESS BARS ===== */
.hd-progress-item {
    margin-bottom: 14px;
}

.hd-progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.hd-progress-label {
    font-size: 13px;
    font-weight: 500;
    color: #374151;
    font-family: 'Inter', sans-serif;
}

.hd-progress-pct {
    font-size: 12px;
    font-weight: 600;
    color: #6B7280;
    font-family: 'Inter', sans-serif;
}

.hd-progress-track {
    width: 100%;
    height: 8px;
    background: #F3F4F6;
    border-radius: 999px;
    overflow: hidden;
}

.hd-progress-bar {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s ease;
}

/* ===== DIVIDER ===== */
.hd-divider {
    height: 1px;
    background: #F3F4F6;
    margin: 16px 0;
    border: none;
}

/* ===== KPI BANNER ===== */
.hd-kpi-banner {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    border-radius: 16px;
    padding: 24px 28px;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    box-shadow: 0 4px 24px rgba(79,70,229,0.25);
}

.hd-kpi-banner-text h2 {
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}

.hd-kpi-banner-text p {
    font-size: 13px;
    color: rgba(255,255,255,0.7);
    font-family: 'Inter', sans-serif;
}

.hd-kpi-banner-stat {
    text-align: right;
    flex-shrink: 0;
}

.hd-kpi-banner-stat-value {
    font-size: 36px;
    font-weight: 800;
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    letter-spacing: -1px;
    line-height: 1;
}

.hd-kpi-banner-stat-label {
    font-size: 12px;
    color: rgba(255,255,255,0.6);
    font-family: 'Inter', sans-serif;
    margin-top: 3px;
}

/* ===== STREAMLIT OVERRIDES ===== */
.stColumns > div {
    padding: 0 6px !important;
}

.element-container {
    margin: 0 !important;
}

div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    padding: 0 !important;
}
</style>
"""


def render_navbar(active_tab="Vue G&#233;n&#233;rale"):
    tabs = [
        "Vue G&#233;n&#233;rale",
        "Activit&#233;",
        "Finances",
        "&#201;quipe",
        "Strat&#233;gie",
    ]
    tabs_html = ""
    for tab in tabs:
        cls = "hd-tab active" if tab == active_tab else "hd-tab"
        tabs_html += f'<a class="{cls}" href="#">{tab}</a>'

    return f"""
<div class="hd-navbar">
  <div class="hd-navbar-logo">
    <div class="hd-logo-circle">H</div>
    <span class="hd-logo-title">Herm&#232;s<span>.</span></span>
  </div>
  <nav class="hd-navbar-tabs">
    {tabs_html}
  </nav>
  <div class="hd-navbar-right">
    <div class="hd-search-bar">
      <span class="hd-search-icon">&#128269;</span>
      <input type="text" placeholder="Rechercher..." />
    </div>
    <button class="hd-icon-btn" title="Notifications">&#128276;</button>
    <button class="hd-icon-btn" title="Param&#232;tres">&#9881;</button>
    <div class="hd-avatar" title="Profil">DG</div>
  </div>
</div>
"""


def render_metric_card(
    title,
    value,
    unit,
    goal_label,
    goal_value,
    sub,
    color="#4F46E5",
    progress_pct=None,
    badge_label=None,
    badge_color="#16A34A",
    badge_bg="#DCFCE7",
):
    strip_html = (
        f'<div class="hd-metric-accent-strip" style="background:{color};"></div>'
    )

    badge_html = ""
    if badge_label:
        badge_html = f'<span class="hd-metric-badge" style="background:{badge_bg};color:{badge_color};">{badge_label}</span>'

    if progress_pct is None:
        try:
            num_val = float(str(value).replace(",", ".").replace(" ", ""))
            num_goal = float(str(goal_value).replace(",", ".").replace(" ", "").replace("%", ""))
            progress_pct = min(100, round((num_val / num_goal) * 100)) if num_goal > 0 else 0
        except Exception:
            progress_pct = 0

    progress_html = f"""
<div class="hd-metric-progress">
  <div class="hd-metric-progress-fill" style="width:{progress_pct}%;background:{color};"></div>
</div>
"""

    return f"""
<div class="hd-metric-card">
  {strip_html}
  <div style="padding-left:8px;">
    <div class="hd-metric-top">
      <span class="hd-metric-title">{title}</span>
      {badge_html}
    </div>
    <div class="hd-metric-value-row">
      <span class="hd-metric-value" style="color:{color};">{value}</span>
      <span class="hd-metric-unit">{unit}</span>
    </div>
    <div class="hd-metric-goal-row">
      <span class="hd-metric-goal-label">{goal_label}</span>
      <span class="hd-metric-goal-value">{goal_value}</span>
    </div>
    {progress_html}
    <div class="hd-metric-sub">{sub}</div>
  </div>
</div>
"""


def render_list_item(
    icon,
    bg_icon,
    title,
    sub,
    badge,
    badge_color,
    badge_bg,
    active=False,
):
    active_cls = " active" if active else ""

    if active:
        badge_color_final = "#FFFFFF"
        badge_bg_final = "rgba(255,255,255,0.25)"
    else:
        badge_color_final = badge_color
        badge_bg_final = badge_bg

    return f"""
<div class="hd-list-item{active_cls}">
  <div class="hd-item-icon-wrap" style="background:{bg_icon};">
    <span>{icon}</span>
  </div>
  <div class="hd-item-text">
    <div class="hd-item-title">{title}</div>
    <div class="hd-item-sub">{sub}</div>
  </div>
  <span class="hd-badge" style="background:{badge_bg_final};color:{badge_color_final};">{badge}</span>
</div>
"""


def render_cal_day(day_letter, day_num, active=False):
    active_cls = " active" if active else ""
    return f"""
<div class="hd-cal-day{active_cls}">
  <span class="hd-cal-day-letter">{day_letter}</span>
  <span class="hd-cal-day-num">{day_num}</span>
</div>
"""


def render_cal_strip(days, active_index=None):
    days_html = ""
    for i, (letter, num) in enumerate(days):
        days_html += render_cal_day(letter, num, active=(i == active_index))
    return f'<div class="hd-cal-strip">{days_html}</div>'


def render_alert_dark(tags):
    tags_html = ""
    for tag_text, tag_style in tags:
        if tag_style == "indigo":
            cls = "hd-alert-tag hd-alert-tag-indigo"
        elif tag_style == "gold":
            cls = "hd-alert-tag hd-alert-tag-gold"
        else:
            cls = "hd-alert-tag hd-alert-tag-ghost"
        tags_html += f'<span class="{cls}">{tag_text}</span>'

    return f"""
<div class="hd-alert-dark">
  <div class="hd-alert-dark-glow"></div>
  <div class="hd-alert-dark-glow2"></div>
  <span class="hd-alert-dark-icon">&#9888;&#65039;</span>
  <div class="hd-alert-dark-title">Points d&#8217;attention</div>
  <div class="hd-alert-dark-sub">
    Indicateurs n&#233;cessitant une action imm&#233;diate
  </div>
  <div class="hd-alert-tags">
    {tags_html}
  </div>
</div>
"""


def render_progress_bar(label, pct, color="#4F46E5"):
    safe_pct = min(100, max(0, pct))
    return f"""
<div class="hd-progress-item">
  <div class="hd-progress-header">
    <span class="hd-progress-label">{label}</span>
    <span class="hd-progress-pct">{safe_pct}&#37;</span>
  </div>
  <div class="hd-progress-track">
    <div class="hd-progress-bar" style="width:{safe_pct}%;background:{color};"></div>
  </div>
</div>
"""


def render_kpi_banner(headline, sub, stat_value, stat_label):
    return f"""
<div class="hd-kpi-banner">
  <div class="hd-kpi-banner-text">
    <h2>{headline}</h2>
    <p>{sub}</p>
  </div>
  <div class="hd-kpi-banner-stat">
    <div class="hd-kpi-banner-stat-value">{stat_value}</div>
    <div class="hd-kpi-banner-stat-label">{stat_label}</div>
  </div>
</div>
"""


def inject_styles():
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
