import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hermès — Rapport Stratégique",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS SECTIONS
# ─────────────────────────────────────────────────────────────────────────────
from section_design import inject_styles, render_navbar
from section_overview import render_overview_tab
from section_crisis_benchmark import render_crisis_tab, render_benchmark_tab
from section_cx import render_cx_tab

# ─────────────────────────────────────────────────────────────────────────────
# DONNÉES COMMUNES
# ─────────────────────────────────────────────────────────────────────────────
dates_crise = pd.date_range("2026-02-10", periods=16, freq="D")
vols_crise  = [2,1,3,4,2,5,7,6,8,12,15,18,22,28,35,42]
df_crise    = pd.DataFrame({"Date": dates_crise, "Posts": vols_crise})

df_plat_c = pd.DataFrame({
    "Plateforme": ["Facebook","TikTok","Reddit","Twitter"],
    "Volume":  [142,132,128,128],
    "Likes":   [2620,2691,2648,2522],
    "Shares":  [252,224,257,235],
    "Replies": [67,77,76,85],
})

df_topics = pd.DataFrame({
    "Topic":  ["Prix","Service client","Qualit\u00e9 cuir","Attente boutique","Exclusivit\u00e9"],
    "Herm\u00e8s": [208,199,203,206,191],
    "Chanel": [155,187,179,168,139],
})
df_topics["Delta_pct"] = ((df_topics["Herm\u00e8s"]-df_topics["Chanel"])/df_topics["Chanel"]*100).round(1)

df_plat_b = pd.DataFrame({
    "Plateforme": ["Twitter","News/Forums","Reddit","LinkedIn"],
    "Herm\u00e8s": [264,251,253,239],
    "Chanel":  [182,220,218,208],
})

df_cat = pd.DataFrame({
    "Cat\u00e9gorie": ["Service client","Qualit\u00e9 cuir","Prix","Attente boutique","Exclusivit\u00e9"],
    "Note":     [3.36,3.32,3.28,3.19,3.15],
    "Pct_pos":  [52,54,50,49,48],
    "Pct_neg":  [34,32,29,35,38],
    "Obj":      [3.80,3.70,3.60,3.60,3.50],
})

df_plat_cx = pd.DataFrame({
    "Plateforme": ["Trustpilot","App Store","Avis V\u00e9rifi\u00e9s","Google Maps"],
    "Volume": [262,253,247,231],
    "Note":   [3.21,3.30,3.25,3.27],
})

# ─────────────────────────────────────────────────────────────────────────────
# STYLES + NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
inject_styles()

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white;padding:0 32px;height:60px;display:flex;align-items:center;
            justify-content:space-between;border-bottom:1px solid #F3F4F6;
            box-shadow:0 1px 3px rgba(0,0,0,0.04);margin:-32px -32px 0 -32px;">
  <div style="display:flex;align-items:center;gap:8px;">
    <div style="width:32px;height:32px;background:#4F46E5;border-radius:10px;
                display:flex;align-items:center;justify-content:center;">
      <span style="color:white;font-size:14px;font-weight:700;">H</span>
    </div>
    <span style="font-family:Georgia,serif;font-size:15px;font-weight:700;
                 color:#0F172A;letter-spacing:1px;">HERM&#200;S</span>
    <span style="font-size:11px;color:#9CA3AF;margin-left:8px;letter-spacing:1px;">
      RAPPORT STRAT&#201;GIQUE
    </span>
  </div>
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="border:1px solid #E5E7EB;border-radius:999px;padding:6px 14px;
                font-size:12px;color:#374151;background:white;">
      &#x1F4C5; Mars 2026
    </div>
    <div style="background:#4F46E5;color:white;border-radius:999px;padding:7px 18px;
                font-size:12px;font-weight:600;">
      Mensuel &#x2192;
    </div>
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="width:34px;height:34px;background:linear-gradient(135deg,#B07A0A,#D4A843);
                  border-radius:999px;display:flex;align-items:center;justify-content:center;">
        <span style="color:white;font-size:13px;font-weight:700;">H</span>
      </div>
      <div>
        <div style="font-size:12px;font-weight:600;color:#0F172A;">DG Herm&#232;s</div>
        <div style="font-size:10px;color:#9CA3AF;">Rapport COMEX</div>
      </div>
    </div>
  </div>
</div>
<div style="height:20px;"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BANDEAU COMEX — SITUATION EN 3 SECONDES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#1e1b4b 100%);
            border-radius:16px;padding:20px 28px;margin-bottom:20px;
            display:flex;align-items:center;justify-content:space-between;
            box-shadow:0 4px 20px rgba(79,70,229,0.25);">
  <div>
    <div style="font-size:11px;letter-spacing:3px;color:rgba(255,255,255,0.5);
                text-transform:uppercase;margin-bottom:4px;">Rapport ex&#233;cutif</div>
    <div style="font-size:22px;font-weight:700;color:white;">
      Situation Herm&#232;s &#8212; Mars 2026
    </div>
    <div style="font-size:13px;color:rgba(255,255,255,0.65);margin-top:4px;">
      3 358 donn&#233;es analys&#233;es &#183; Dataset 100% nettoy&#233;
    </div>
  </div>
  <div style="display:flex;gap:12px;">
    <div style="background:rgba(220,38,38,0.2);border:1px solid rgba(220,38,38,0.5);
                border-radius:12px;padding:14px 20px;text-align:center;min-width:110px;">
      <div style="font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.6);
                  text-transform:uppercase;margin-bottom:6px;">R&#233;putation</div>
      <div style="font-size:26px;font-weight:800;color:#FCA5A5;">&#128308;</div>
      <div style="font-size:11px;color:#FCA5A5;font-weight:600;margin-top:4px;">CRISE ACTIVE</div>
    </div>
    <div style="background:rgba(176,120,10,0.2);border:1px solid rgba(176,120,10,0.5);
                border-radius:12px;padding:14px 20px;text-align:center;min-width:110px;">
      <div style="font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.6);
                  text-transform:uppercase;margin-bottom:6px;">Benchmark</div>
      <div style="font-size:26px;font-weight:800;color:#FDE68A;">&#128993;</div>
      <div style="font-size:11px;color:#FDE68A;font-weight:600;margin-top:4px;">LEADER +37%</div>
    </div>
    <div style="background:rgba(5,150,105,0.2);border:1px solid rgba(5,150,105,0.5);
                border-radius:12px;padding:14px 20px;text-align:center;min-width:110px;">
      <div style="font-size:10px;letter-spacing:1px;color:rgba(255,255,255,0.6);
                  text-transform:uppercase;margin-bottom:6px;">Client</div>
      <div style="font-size:26px;font-weight:800;color:#6EE7B7;">&#128995;</div>
      <div style="font-size:11px;color:#6EE7B7;font-weight:600;margin-top:4px;">3.26/5 &#8593;</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  &#x1F3E0;  Vue G&#233;n&#233;rale  ",
    "  &#x1F6A8;  R&#233;putation & Crise  ",
    "  &#x1F4CA;  Benchmark March&#233;  ",
    "  &#x2B50;  Voix Client  ",
])

with tab1:
    render_overview_tab(df_crise, df_topics, df_cat)

with tab2:
    render_crisis_tab(df_crise, df_plat_c)

with tab3:
    render_benchmark_tab(df_topics, df_plat_b)

with tab4:
    render_cx_tab(df_cat, df_plat_cx)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:40px;padding-top:16px;border-top:1px solid #F3F4F6;
            display:flex;justify-content:space-between;align-items:center;">
  <span style="font-family:Georgia,serif;font-size:13px;font-weight:700;
               color:#0F172A;letter-spacing:2px;">HERM&#200;S</span>
  <span style="font-size:11px;color:#9CA3AF;">
    Rapport Strat&#233;gique &#183; Mars 2026 &#183; BDD Eugenia &#183; 3 358 datapoints
  </span>
  <span style="font-size:11px;color:#D1D5DB;">Dataset 100% nettoy&#233;</span>
</div>
""", unsafe_allow_html=True)
