import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# ---------------------------------------------------------------------------
# Shared style helpers
# ---------------------------------------------------------------------------

HERMES_GOLD = "#C9A84C"
HERMES_DARK = "#1A1A2E"
INDIGO = "#4F46E5"
CHANEL_GRAY = "#6B7280"
LIGHT_GRAY = "#E5E7EB"
RED_ALERT = "#EF4444"
GREEN_OK = "#10B981"
GRID_COLOR = "#F3F4F6"
FONT_FAMILY = "Inter, sans-serif"

LIGHT_CHART = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family=FONT_FAMILY, size=12, color="#374151"),
)

def _lc(**kwargs):
    """Merge LIGHT_CHART with per-chart overrides safely."""
    return {**LIGHT_CHART, **kwargs}


def _kpi_card(label: str, value: str, delta: str = "", color: str = INDIGO) -> str:
    delta_html = (
        f'<p style="margin:0;font-size:12px;color:{color};font-weight:600;">{delta}</p>'
        if delta
        else ""
    )
    return f"""
<div style="background:white;border-radius:12px;padding:20px 16px;
            box-shadow:0 1px 4px rgba(0,0,0,0.08);border-top:3px solid {color};
            text-align:center;min-width:120px;">
  <p style="margin:0 0 4px 0;font-size:12px;color:#6B7280;font-weight:500;
             text-transform:uppercase;letter-spacing:.5px;">{label}</p>
  <p style="margin:0;font-size:26px;font-weight:700;color:#111827;">{value}</p>
  {delta_html}
</div>"""


# ---------------------------------------------------------------------------
# 1. render_crisis_tab
# ---------------------------------------------------------------------------

def render_crisis_tab(df_crise: pd.DataFrame, df_plat_c: pd.DataFrame) -> None:

    # ---- Alerte rouge ----
    st.markdown(
        """
<div style="background:#FEF2F2;border:2px solid #EF4444;border-radius:10px;
            padding:14px 20px;display:flex;align-items:center;gap:14px;margin-bottom:24px;">
  <span style="font-size:28px;">&#9888;</span>
  <div>
    <p style="margin:0;font-size:15px;font-weight:700;color:#991B1B;">
      CRISE R&#233;PUTATION EN COURS &#8212; Surveillance active
    </p>
    <p style="margin:4px 0 0 0;font-size:13px;color:#B91C1C;">
      530 publications 100&nbsp;% n&#233;gatives d&#233;tect&#233;es entre le 10 et le 26&nbsp;f&#233;vrier&nbsp;2026
      &nbsp;&#8212;&nbsp;Pic&#160;:&#160;42&nbsp;posts le 25&nbsp;f&#233;v. &nbsp;&#8212;&nbsp;4 plateformes impact&#233;es
    </p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ---- 5 KPI cards ----
    k1, k2, k3, k4, k5 = st.columns(5)
    cards = [
        ("Posts d&#233;tect&#233;s", "530", "10&#8211;26 f&#233;v. 2026", RED_ALERT),
        ("Sentiment", "100&#160;%", "n&#233;gatif", RED_ALERT),
        ("Likes&#160;/ post", "2&#160;621", "moyenne", "#F59E0B"),
        ("Fen&#234;tre crise", "16&#160;j", "dur&#233;e", "#F59E0B"),
        ("Impressions", "86&#160;k/j", "estim&#233;", RED_ALERT),
    ]
    for col, (lbl, val, delta, color) in zip([k1, k2, k3, k4, k5], cards):
        col.markdown(_kpi_card(lbl, val, delta, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Bar chart + ligne tendance ----
    dates = pd.date_range("2026-02-10", periods=16, freq="D")
    volumes = [2, 1, 3, 4, 2, 5, 7, 6, 8, 12, 15, 18, 22, 28, 35, 42]

    if not df_crise.empty and "date" in df_crise.columns and "posts" in df_crise.columns:
        dates = pd.to_datetime(df_crise["date"])
        volumes = df_crise["posts"].tolist()

    fig_bar = go.Figure()

    bar_colors = [RED_ALERT if v > 20 else "#FCA5A5" for v in volumes]

    fig_bar.add_trace(
        go.Bar(
            x=dates,
            y=volumes,
            marker_color=bar_colors,
            name="Posts / jour",
            marker_line_width=0,
        )
    )

    fig_bar.add_trace(
        go.Scatter(
            x=dates,
            y=volumes,
            mode="lines+markers",
            line=dict(color=HERMES_DARK, width=2, dash="dot"),
            marker=dict(size=5, color=HERMES_DARK),
            name="Tendance",
        )
    )

    fig_bar.add_hrect(
        y0=20,
        y1=max(volumes) * 1.1,
        fillcolor="rgba(239,68,68,0.07)",
        line_width=0,
        annotation_text="Zone alerte",
        annotation_position="top left",
        annotation_font_color=RED_ALERT,
    )

    pic_ts = pd.Timestamp("2026-02-25")
    fig_bar.add_vline(
        x=pic_ts.value,
        line_width=2,
        line_dash="dash",
        line_color=RED_ALERT,
        annotation_text="Pic&#160;: 42 posts",
        annotation_position="top right",
        annotation_font_color=RED_ALERT,
    )

    fig_bar.update_layout(
        **LIGHT_CHART,
        title=dict(text="&#201;volution journali&#232;re des publications n&#233;gatives", x=0.01),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            tickformat="%d %b",
            showgrid=False,
        ),
        yaxis=dict(gridcolor=GRID_COLOR, title="Nombre de posts"),
        bargap=0.25,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---- Donut langues  +  Engagement par plateforme ----
    col_donut, col_radar = st.columns([1, 1])

    with col_donut:
        st.markdown(
            '<p style="font-weight:600;font-size:14px;color:#374151;margin-bottom:4px;">'
            "R&#233;partition par langue</p>",
            unsafe_allow_html=True,
        )
        labels_lang = ["Fran&#231;ais", "Espagnol", "Anglais", "Autres"]
        values_lang = [61, 20, 18, 1]
        colors_lang = [INDIGO, HERMES_GOLD, "#10B981", LIGHT_GRAY]

        fig_donut = go.Figure(
            go.Pie(
                labels=labels_lang,
                values=values_lang,
                hole=0.55,
                marker=dict(colors=colors_lang, line=dict(color="white", width=2)),
                textinfo="percent",
                hovertemplate="%{label}: %{value}%<extra></extra>",
            )
        )
        fig_donut.update_layout(
            **LIGHT_CHART,
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(orientation="v", x=1, y=0.5),
            annotations=[
                dict(
                    text="Langue",
                    x=0.5,
                    y=0.5,
                    font=dict(size=13, family=FONT_FAMILY),
                    showarrow=False,
                )
            ],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_radar:
        st.markdown(
            '<p style="font-weight:600;font-size:14px;color:#374151;margin-bottom:4px;">'
            "Engagement par plateforme</p>",
            unsafe_allow_html=True,
        )

        plat_names = ["Facebook", "TikTok", "Reddit", "Twitter"]
        plat_posts = [142, 132, 128, 128]
        plat_engage = [3200, 4100, 1800, 2400]

        if not df_plat_c.empty:
            if "plateforme" in df_plat_c.columns and "posts" in df_plat_c.columns:
                plat_names = df_plat_c["plateforme"].tolist()
                plat_posts = df_plat_c["posts"].tolist()
            if "engagement" in df_plat_c.columns:
                plat_engage = df_plat_c["engagement"].tolist()

        fig_plat = go.Figure()
        fig_plat.add_trace(
            go.Bar(
                x=plat_names,
                y=plat_posts,
                name="Posts",
                marker_color=RED_ALERT,
                yaxis="y",
            )
        )
        fig_plat.add_trace(
            go.Scatter(
                x=plat_names,
                y=plat_engage,
                mode="lines+markers",
                name="Engagement moy.",
                marker=dict(size=8, color=HERMES_GOLD),
                line=dict(color=HERMES_GOLD, width=2),
                yaxis="y2",
            )
        )
        fig_plat.update_layout(
            **LIGHT_CHART,
            margin=dict(t=20, b=40, l=50, r=60),
            yaxis=dict(title="Posts", gridcolor=GRID_COLOR),
            yaxis2=dict(
                title="Engagement",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            bargap=0.3,
        )
        st.plotly_chart(fig_plat, use_container_width=True)

    # ---- Plan de r&#233;ponse ----
    st.markdown(
        """
<div style="background:white;border-radius:12px;padding:20px 24px;
            box-shadow:0 1px 4px rgba(0,0,0,0.08);margin-top:8px;">
  <p style="margin:0 0 14px 0;font-size:15px;font-weight:700;color:#111827;">
    &#128203; Plan de r&#233;ponse crise recommand&#233;
  </p>
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr style="background:#F9FAFB;">
        <th style="padding:8px 12px;text-align:left;color:#6B7280;font-weight:600;
                   border-bottom:1px solid #E5E7EB;">Horizon</th>
        <th style="padding:8px 12px;text-align:left;color:#6B7280;font-weight:600;
                   border-bottom:1px solid #E5E7EB;">Action</th>
        <th style="padding:8px 12px;text-align:left;color:#6B7280;font-weight:600;
                   border-bottom:1px solid #E5E7EB;">Responsable</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;">
          <span style="background:#FEE2E2;color:#991B1B;border-radius:6px;
                       padding:2px 8px;font-weight:600;">&lt;&#160;24&#160;h</span>
        </td>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;color:#374151;">
          Activation cellule de crise &#8212; monitoring H24 &#8212; message d&#8217;empathie initial
        </td>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;color:#6B7280;">
          DirCom + Community Manager
        </td>
      </tr>
      <tr>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;">
          <span style="background:#FEF3C7;color:#92400E;border-radius:6px;
                       padding:2px 8px;font-weight:600;">J+2</span>
        </td>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;color:#374151;">
          Communication officielle multi-canal &#8212; FAQ publique &#8212; r&#233;ponses individuelles top influenceurs
        </td>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;color:#6B7280;">
          RP + Digital
        </td>
      </tr>
      <tr>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;">
          <span style="background:#DBEAFE;color:#1E40AF;border-radius:6px;
                       padding:2px 8px;font-weight:600;">J+7</span>
        </td>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;color:#374151;">
          Bilan interm&#233;diaire &#8212; ajustement strat&#233;gie &#8212; campagne de r&#233;assurance
        </td>
        <td style="padding:8px 12px;border-bottom:1px solid #F3F4F6;color:#6B7280;">
          COMEX + RP
        </td>
      </tr>
      <tr>
        <td style="padding:8px 12px;">
          <span style="background:#D1FAE5;color:#065F46;border-radius:6px;
                       padding:2px 8px;font-weight:600;">J+30</span>
        </td>
        <td style="padding:8px 12px;color:#374151;">
          Post-mortem complet &#8212; rapport r&#233;putation &#8212; mise &#224; jour protocole crise
        </td>
        <td style="padding:8px 12px;color:#6B7280;">
          Direction G&#233;n&#233;rale
        </td>
      </tr>
    </tbody>
  </table>
</div>
""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 2. render_benchmark_tab
# ---------------------------------------------------------------------------

def render_benchmark_tab(df_topics: pd.DataFrame, df_plat_b: pd.DataFrame) -> None:

    # ---- 4 KPI cards ----
    k1, k2, k3, k4 = st.columns(4)
    cards_b = [
        ("Posts analys&#233;s", "1&#160;835", "p&#233;riode compar&#233;e", INDIGO),
        ("Part Herm&#232;s", "55&#160;%", "vs Chanel 45&#160;%", HERMES_GOLD),
        ("Avantage max", "+37&#160;%", "Exclusivit&#233;", GREEN_OK),
        ("Opportunit&#233;", "LinkedIn", "&#224; activer", HERMES_GOLD),
    ]
    for col, (lbl, val, delta, color) in zip([k1, k2, k3, k4], cards_b):
        col.markdown(_kpi_card(lbl, val, delta, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Grouped bar : Herm&#232;s vs Chanel par topic ----
    topics = ["Prix", "Service client", "Qualit&#233; cuir", "Attente boutique", "Exclusivit&#233;"]
    hermes_vals = [208, 199, 203, 206, 191]
    chanel_vals = [155, 187, 179, 168, 139]
    advantages = [34, 6, 13, 23, 37]

    if not df_topics.empty:
        if "topic" in df_topics.columns:
            topics = df_topics["topic"].tolist()
        if "hermes" in df_topics.columns:
            hermes_vals = df_topics["hermes"].tolist()
        if "chanel" in df_topics.columns:
            chanel_vals = df_topics["chanel"].tolist()
        if "avantage" in df_topics.columns:
            advantages = df_topics["avantage"].tolist()
        else:
            advantages = [
                round((h - c) / c * 100)
                for h, c in zip(hermes_vals, chanel_vals)
            ]

    fig_grouped = go.Figure()
    fig_grouped.add_trace(
        go.Bar(
            x=topics,
            y=hermes_vals,
            name="Herm&#232;s",
            marker_color=HERMES_GOLD,
            text=[f"{v}" for v in hermes_vals],
            textposition="outside",
        )
    )
    fig_grouped.add_trace(
        go.Bar(
            x=topics,
            y=chanel_vals,
            name="Chanel",
            marker_color=LIGHT_GRAY,
            text=[f"{v}" for v in chanel_vals],
            textposition="outside",
        )
    )
    fig_grouped.update_layout(
        **LIGHT_CHART,
        title=dict(text="Volume de mentions par topic &#8212; Herm&#232;s vs Chanel", x=0.01),
        barmode="group",
        bargap=0.2,
        bargroupgap=0.05,
        xaxis=dict(gridcolor=GRID_COLOR, showgrid=False),
        yaxis=dict(gridcolor=GRID_COLOR, title="Nombre de mentions"),
    )
    st.plotly_chart(fig_grouped, use_container_width=True)

    # ---- Progress bars avantage % ----
    st.markdown(
        '<p style="font-weight:700;font-size:14px;color:#111827;margin-bottom:12px;">'
        "Avantage concurrentiel Herm&#232;s par rapport &#224; Chanel</p>",
        unsafe_allow_html=True,
    )

    topic_labels_clean = ["Prix", "Service client", "Qualit&#233; cuir", "Attente boutique", "Exclusivit&#233;"]

    bars_html = '<div style="display:flex;flex-direction:column;gap:10px;">'
    for lbl, adv in zip(topic_labels_clean, advantages):
        if adv > 15:
            bar_color = GREEN_OK
            badge_bg = "#D1FAE5"
            badge_fg = "#065F46"
        elif adv > 8:
            bar_color = INDIGO
            badge_bg = "#EEF2FF"
            badge_fg = "#3730A3"
        else:
            bar_color = HERMES_GOLD
            badge_bg = "#FEF3C7"
            badge_fg = "#92400E"

        width_pct = min(adv * 2, 100)
        bars_html += f"""
<div style="background:#F9FAFB;border-radius:8px;padding:12px 16px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
    <span style="font-size:13px;font-weight:600;color:#374151;">{lbl}</span>
    <span style="background:{badge_bg};color:{badge_fg};border-radius:6px;
                 padding:2px 10px;font-size:12px;font-weight:700;">+{adv}&#160;%</span>
  </div>
  <div style="background:#E5E7EB;border-radius:999px;height:8px;">
    <div style="background:{bar_color};border-radius:999px;height:8px;
                width:{width_pct}%;transition:width .4s;"></div>
  </div>
</div>"""
    bars_html += "</div>"
    st.markdown(bars_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Radar plateformes ----
    col_radar, col_opp = st.columns([3, 2])

    with col_radar:
        st.markdown(
            '<p style="font-weight:700;font-size:14px;color:#111827;margin-bottom:4px;">'
            "Performance par plateforme</p>",
            unsafe_allow_html=True,
        )
        plat_labels = ["Twitter", "News / Forums", "Reddit", "LinkedIn"]
        hermes_plat = [264, 251, 253, 239]
        chanel_plat = [182, 220, 218, 208]

        if not df_plat_b.empty:
            if "plateforme" in df_plat_b.columns:
                plat_labels = df_plat_b["plateforme"].tolist()
            if "hermes" in df_plat_b.columns:
                hermes_plat = df_plat_b["hermes"].tolist()
            if "chanel" in df_plat_b.columns:
                chanel_plat = df_plat_b["chanel"].tolist()

        theta = plat_labels + [plat_labels[0]]
        r_hermes = hermes_plat + [hermes_plat[0]]
        r_chanel = chanel_plat + [chanel_plat[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=r_hermes,
                theta=theta,
                fill="toself",
                fillcolor="rgba(201,168,76,0.15)",
                line=dict(color=HERMES_GOLD, width=2),
                name="Herm&#232;s",
            )
        )
        fig_radar.add_trace(
            go.Scatterpolar(
                r=r_chanel,
                theta=theta,
                fill="toself",
                fillcolor="rgba(107,114,128,0.1)",
                line=dict(color=CHANEL_GRAY, width=2),
                name="Chanel",
            )
        )
        fig_radar.update_layout(
            **LIGHT_CHART,
            polar=dict(
                bgcolor="white",
                radialaxis=dict(
                    visible=True,
                    range=[0, 300],
                    gridcolor=GRID_COLOR,
                    linecolor=GRID_COLOR,
                ),
                angularaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
            ),
            margin=dict(t=30, b=30, l=40, r=40),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_opp:
        # ---- Opportunit&#233; LinkedIn ----
        st.markdown(
            f"""
<div style="background:#FFFBEB;border:2px solid {HERMES_GOLD};border-radius:12px;
            padding:20px;height:100%;box-sizing:border-box;">
  <p style="margin:0 0 8px 0;font-size:15px;font-weight:700;color:#92400E;">
    &#11088; Opportunit&#233; LinkedIn
  </p>
  <p style="margin:0 0 14px 0;font-size:13px;color:#78350F;line-height:1.6;">
    Herm&#232;s g&#233;n&#232;re <strong>239 mentions</strong> sur LinkedIn vs <strong>208 pour Chanel</strong>,
    soit un avantage de <strong>+15&#160;%</strong>.
    Ce canal professionnel reste sous-exploit&#233; au regard du potentiel de
    l&#8217;audience UHNWI et investisseurs.
  </p>
  <div style="background:white;border-radius:8px;padding:12px;">
    <p style="margin:0 0 8px 0;font-size:12px;font-weight:700;color:#374151;
              text-transform:uppercase;letter-spacing:.5px;">Actions recommand&#233;es</p>
    <ul style="margin:0;padding-left:18px;font-size:12px;color:#374151;line-height:1.8;">
      <li>Contenus savoir-faire artisanal (+CEO brand)</li>
      <li>S&#233;ries &#171;&#160;H&#233;ritage &amp; Innovation&#160;&#187;</li>
      <li>Partenariats influenceurs B2B luxe</li>
      <li>Campagnes employ&#233;s ambassadeurs</li>
    </ul>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ---- S&#233;lecteur de topic : sentiment compar&#233; ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-weight:700;font-size:14px;color:#111827;margin-bottom:8px;">'
        "Analyse d&#233;taill&#233;e par topic</p>",
        unsafe_allow_html=True,
    )

    topic_options = ["Prix", "Service client", "Qualit&#233; cuir", "Attente boutique", "Exclusivit&#233;"]
    selected = st.selectbox(
        "S&#233;lectionner un topic",
        options=topic_options,
        key="benchmark_topic_select",
    )

    topic_idx = topic_options.index(selected) if selected in topic_options else 0
    h_val = hermes_vals[topic_idx]
    c_val = chanel_vals[topic_idx]
    adv_val = advantages[topic_idx]

    sentiment_data = {
        "Prix": {"h_pos": 62, "h_neu": 28, "h_neg": 10, "c_pos": 55, "c_neu": 27, "c_neg": 18},
        "Service client": {"h_pos": 70, "h_neu": 20, "h_neg": 10, "c_pos": 68, "c_neu": 22, "c_neg": 10},
        "Qualit&#233; cuir": {"h_pos": 78, "h_neu": 15, "h_neg": 7, "c_pos": 72, "c_neu": 18, "c_neg": 10},
        "Attente boutique": {"h_pos": 45, "h_neu": 30, "h_neg": 25, "c_pos": 38, "c_neu": 35, "c_neg": 27},
        "Exclusivit&#233;": {"h_pos": 80, "h_neu": 14, "h_neg": 6, "c_pos": 65, "c_neu": 20, "c_neg": 15},
    }
    sd = sentiment_data.get(selected, sentiment_data["Prix"])

    fig_sent = go.Figure()
    brands = ["Herm&#232;s", "Chanel"]
    positifs = [sd["h_pos"], sd["c_pos"]]
    neutres = [sd["h_neu"], sd["c_neu"]]
    negatifs = [sd["h_neg"], sd["c_neg"]]

    fig_sent.add_trace(
        go.Bar(
            x=brands, y=positifs, name="Positif",
            marker_color=GREEN_OK,
            text=[f"{v}&#160;%" for v in positifs],
            textposition="inside",
        )
    )
    fig_sent.add_trace(
        go.Bar(
            x=brands, y=neutres, name="Neutre",
            marker_color=LIGHT_GRAY,
            text=[f"{v}&#160;%" for v in neutres],
            textposition="inside",
        )
    )
    fig_sent.add_trace(
        go.Bar(
            x=brands, y=negatifs, name="N&#233;gatif",
            marker_color=RED_ALERT,
            text=[f"{v}&#160;%" for v in negatifs],
            textposition="inside",
        )
    )

    fig_sent.update_layout(
        **LIGHT_CHART,
        barmode="stack",
        title=dict(
            text=f"Sentiment compar&#233; &#8212; {selected} ({h_val} vs {c_val} mentions, avantage +{adv_val}&#160;%)",
            x=0.01,
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor=GRID_COLOR, title="R&#233;partition (&#160;%&#160;)", range=[0, 110]),
    )
    st.plotly_chart(fig_sent, use_container_width=True)
