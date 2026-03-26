import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS (fallback si section_design non disponible)
# ─────────────────────────────────────────────────────────────────────────────
try:
    from section_design import CSS_STYLES
except ImportError:
    CSS_STYLES = ""

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS INTERNES
# ─────────────────────────────────────────────────────────────────────────────
def _hex_to_rgba(hex_color, alpha=0.12):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _sparkline_fig(y_vals, color="#DC2626", height=60):
    x = list(range(len(y_vals)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y_vals, mode="lines",
        line=dict(color=color, width=2.5, shape="spline"),
        fill="tozeroy",
        fillcolor=_hex_to_rgba(color, 0.15),
        hovertemplate="Jour %{x}: %{y} posts<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        height=height, margin=dict(t=6, b=6, l=8, r=8),
        showlegend=False,
        font=dict(family="Inter"),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def _gauge_fig(value, max_val=100, color="#DC2626", height=220):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(
            font=dict(size=40, color="#0F172A", family="Inter"),
            suffix="/100",
        ),
        gauge=dict(
            axis=dict(
                range=[0, max_val],
                tickfont=dict(size=10, color="#9CA3AF", family="Inter"),
                tickvals=[0, 25, 50, 75, 100],
                ticktext=["0", "25", "50", "75", "100"],
            ),
            bar=dict(color=color, thickness=0.7),
            bgcolor="white",
            borderwidth=0,
            steps=[
                dict(range=[0, 33],  color="#ECFDF5"),
                dict(range=[33, 66], color="#FEF9C3"),
                dict(range=[66, 100], color="#FEF2F2"),
            ],
            threshold=dict(
                line=dict(color="#DC2626", width=3),
                thickness=0.85,
                value=value,
            ),
        ),
    ))
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        height=height, margin=dict(t=20, b=10, l=30, r=30),
        font=dict(family="Inter"),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# FONCTION PRINCIPALE
# ─────────────────────────────────────────────────────────────────────────────
def render_overview_tab(df_crise: pd.DataFrame, df_topics: pd.DataFrame, df_cat: pd.DataFrame):

    # =========================================================================
    # 1. EXECUTIVE BRIEF — 3 blocs traffic light
    # =========================================================================
    st.markdown("""
    <div style="margin-bottom:8px;">
      <div style="font-size:11px;font-weight:700;color:#9CA3AF;letter-spacing:1.5px;
                  text-transform:uppercase;margin-bottom:12px;">EXECUTIVE BRIEF</div>
    </div>
    """, unsafe_allow_html=True)

    col_r, col_o, col_g = st.columns(3, gap="medium")

    with col_r:
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:16px;padding:20px 22px;
                    box-shadow:0 2px 12px rgba(220,38,38,0.12);
                    border-left:4px solid #DC2626;border:1px solid #FECACA;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-size:20px;">&#128308;</span>
              <span style="font-size:13px;font-weight:700;color:#0F172A;">R&#233;putation</span>
            </div>
            <span style="background:#FEF2F2;color:#DC2626;font-size:10px;font-weight:700;
                         padding:3px 10px;border-radius:999px;letter-spacing:0.5px;">ACTION IMMÉD.</span>
          </div>
          <div style="font-size:48px;font-weight:800;color:#DC2626;line-height:1;margin-bottom:4px;">530</div>
          <div style="font-size:12px;font-weight:500;color:#6B7280;margin-bottom:14px;">posts 100% n&#233;gatifs</div>
          <div style="background:#FEF2F2;border-radius:10px;padding:10px 12px;">
            <div style="font-size:12px;font-weight:600;color:#DC2626;">
              &#9888; Activer la cellule de crise dans les 24h
            </div>
          </div>
          <div style="margin-top:10px;display:flex;align-items:center;gap:6px;">
            <span style="font-size:10px;color:#9CA3AF;">Urgence :</span>
            <span style="background:#DC2626;color:white;font-size:10px;font-weight:700;
                         padding:2px 8px;border-radius:999px;">CRITIQUE</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_o:
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:16px;padding:20px 22px;
                    box-shadow:0 2px 12px rgba(176,122,10,0.10);
                    border-left:4px solid #B07A0A;border:1px solid #FDE68A;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-size:20px;">&#128993;</span>
              <span style="font-size:13px;font-weight:700;color:#0F172A;">Benchmark</span>
            </div>
            <span style="background:#FEF9C3;color:#B07A0A;font-size:10px;font-weight:700;
                         padding:3px 10px;border-radius:999px;letter-spacing:0.5px;">SURVEILLER</span>
          </div>
          <div style="font-size:48px;font-weight:800;color:#B07A0A;line-height:1;margin-bottom:4px;">+37%</div>
          <div style="font-size:12px;font-weight:500;color:#6B7280;margin-bottom:14px;">avance exclusivit&#233; vs Chanel</div>
          <div style="background:#FEF9C3;border-radius:10px;padding:10px 12px;">
            <div style="font-size:12px;font-weight:600;color:#B07A0A;">
              &#8593; Renforcer le service client (+6% seulement)
            </div>
          </div>
          <div style="margin-top:10px;display:flex;align-items:center;gap:6px;">
            <span style="font-size:10px;color:#9CA3AF;">Urgence :</span>
            <span style="background:#B07A0A;color:white;font-size:10px;font-weight:700;
                         padding:2px 8px;border-radius:999px;">MODÉRÉE</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_g:
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:16px;padding:20px 22px;
                    box-shadow:0 2px 12px rgba(5,150,105,0.10);
                    border-left:4px solid #059669;border:1px solid #A7F3D0;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-size:20px;">&#128994;</span>
              <span style="font-size:13px;font-weight:700;color:#0F172A;">Voix Client</span>
            </div>
            <span style="background:#ECFDF5;color:#059669;font-size:10px;font-weight:700;
                         padding:3px 10px;border-radius:999px;letter-spacing:0.5px;">OK</span>
          </div>
          <div style="font-size:48px;font-weight:800;color:#059669;line-height:1;margin-bottom:4px;">3.26</div>
          <div style="font-size:12px;font-weight:500;color:#6B7280;margin-bottom:14px;">note moyenne sur 993 avis</div>
          <div style="background:#ECFDF5;border-radius:10px;padding:10px 12px;">
            <div style="font-size:12px;font-weight:600;color:#059669;">
              &#8593; Travailler l&#39;exclusivit&#233; per&#231;ue (3.15&#9733; pire score)
            </div>
          </div>
          <div style="margin-top:10px;display:flex;align-items:center;gap:6px;">
            <span style="font-size:10px;color:#9CA3AF;">Urgence :</span>
            <span style="background:#059669;color:white;font-size:10px;font-weight:700;
                         padding:2px 8px;border-radius:999px;">FAIBLE</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 2. SITUATION EN UN COUP D'OEIL — gauge + sparkline
    # =========================================================================
    st.markdown("""
    <div style="font-size:11px;font-weight:700;color:#9CA3AF;letter-spacing:1.5px;
                text-transform:uppercase;margin-bottom:14px;">
      SITUATION EN UN COUP D&#39;&#338;IL
    </div>
    """, unsafe_allow_html=True)

    g_left, g_right = st.columns([5, 7], gap="medium")

    with g_left:
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:16px;padding:20px 22px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.055);border:1px solid #F3F4F6;">
          <div style="font-size:13px;font-weight:700;color:#0F172A;margin-bottom:2px;">
            S&#233;v&#233;rit&#233; de crise
          </div>
          <div style="font-size:11px;color:#9CA3AF;margin-bottom:6px;">
            Score composite (r&#233;putation, volume, dur&#233;e)
          </div>
        </div>
        """, unsafe_allow_html=True)
        fig_gauge = _gauge_fig(value=82, max_val=100, color="#DC2626", height=200)
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style="background:#FEF2F2;border-radius:10px;padding:10px 14px;margin-top:-10px;
                    text-align:center;font-size:12px;font-weight:600;color:#DC2626;">
          &#128308; Niveau CRITIQUE &#8212; Intervention imm&#233;diate requise
        </div>
        """, unsafe_allow_html=True)

    with g_right:
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:16px;padding:20px 22px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.055);border:1px solid #F3F4F6;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
            <div>
              <div style="font-size:13px;font-weight:700;color:#0F172A;">&#201;volution de la crise</div>
              <div style="font-size:11px;color:#9CA3AF;">Volume quotidien de posts n&#233;gatifs (16 jours)</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:24px;font-weight:800;color:#DC2626;">86 000</div>
              <div style="font-size:10px;color:#9CA3AF;">impressions / jour</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        posts = df_crise["Posts"].tolist() if "Posts" in df_crise.columns else [2,1,3,4,2,5,7,6,8,12,15,18,22,28,35,42]
        fig_spark = _sparkline_fig(posts, color="#DC2626", height=120)
        st.plotly_chart(fig_spark, use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div style="display:flex;gap:10px;margin-top:4px;">
          <div style="flex:1;background:#FEF2F2;border-radius:10px;padding:10px 12px;text-align:center;">
            <div style="font-size:20px;font-weight:800;color:#DC2626;">530</div>
            <div style="font-size:10px;color:#9CA3AF;margin-top:2px;">Posts totaux</div>
          </div>
          <div style="flex:1;background:#FEF2F2;border-radius:10px;padding:10px 12px;text-align:center;">
            <div style="font-size:20px;font-weight:800;color:#DC2626;">16</div>
            <div style="font-size:10px;color:#9CA3AF;margin-top:2px;">Jours de crise</div>
          </div>
          <div style="flex:1;background:#FEF2F2;border-radius:10px;padding:10px 12px;text-align:center;">
            <div style="font-size:20px;font-weight:800;color:#DC2626;">100%</div>
            <div style="font-size:10px;color:#9CA3AF;margin-top:2px;">Tonalit&#233; n&#233;g.</div>
          </div>
          <div style="flex:1;background:#FEF2F2;border-radius:10px;padding:10px 12px;text-align:center;">
            <div style="font-size:20px;font-weight:800;color:#DC2626;">+21x</div>
            <div style="font-size:10px;color:#9CA3AF;margin-top:2px;">Acc&#233;l&#233;ration</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # =========================================================================
    # 3. PILIERS STRATÉGIQUES (style Medication List)
    # =========================================================================
    st.markdown("""
    <div style="font-size:11px;font-weight:700;color:#9CA3AF;letter-spacing:1.5px;
                text-transform:uppercase;margin-bottom:14px;">
      PILIERS STRAT&#201;GIQUES
    </div>
    """, unsafe_allow_html=True)

    p_left, p_right = st.columns([6, 6], gap="medium")

    with p_left:
        # Pilier Réputation — actif / rouge
        st.markdown("""
        <div style="background:#DC2626;border-radius:14px;padding:14px 16px;margin-bottom:10px;cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:42px;height:42px;border-radius:999px;background:rgba(255,255,255,0.2);
                        display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">
              &#128308;
            </div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:700;color:white;">Pilier 1 — R&#233;putation &amp; Crise</div>
              <div style="font-size:11px;color:rgba(255,255,255,0.75);margin-top:2px;">
                530 posts &#8212; 86k impressions/jour &#8212; crise active
              </div>
            </div>
            <div style="text-align:right;flex-shrink:0;">
              <div style="font-size:18px;font-weight:800;color:white;">100%</div>
              <div style="font-size:10px;color:rgba(255,255,255,0.7);">n&#233;gatif</div>
            </div>
          </div>
          <div style="background:rgba(255,255,255,0.15);border-radius:8px;padding:8px 10px;margin-top:10px;">
            <div style="font-size:11px;font-weight:600;color:white;">
              &#9658; Activer la cellule de crise &#8212; communiquer sous 24h
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Pilier Benchmark — neutre
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:14px;padding:14px 16px;margin-bottom:10px;
                    border:1px solid #F3F4F6;box-shadow:0 1px 4px rgba(0,0,0,0.04);cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:42px;height:42px;border-radius:999px;background:#FEF9C3;
                        display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">
              &#128993;
            </div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:700;color:#0F172A;">Pilier 2 — Benchmark March&#233;</div>
              <div style="font-size:11px;color:#6B7280;margin-top:2px;">
                Herm&#232;s vs Chanel &#8212; +37% exclusivit&#233;, +34% prix
              </div>
            </div>
            <div style="text-align:right;flex-shrink:0;">
              <div style="font-size:18px;font-weight:800;color:#B07A0A;">+6%</div>
              <div style="font-size:10px;color:#9CA3AF;">service client</div>
            </div>
          </div>
          <div style="background:#FEF9C3;border-radius:8px;padding:8px 10px;margin-top:10px;">
            <div style="font-size:11px;font-weight:600;color:#B07A0A;">
              &#8593; Renforcer le service client pour consolider l&#39;avance
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Pilier Voix Client — neutre
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:14px;padding:14px 16px;margin-bottom:10px;
                    border:1px solid #F3F4F6;box-shadow:0 1px 4px rgba(0,0,0,0.04);cursor:pointer;">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:42px;height:42px;border-radius:999px;background:#ECFDF5;
                        display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">
              &#128994;
            </div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:700;color:#0F172A;">Pilier 3 — Voix Client</div>
              <div style="font-size:11px;color:#6B7280;margin-top:2px;">
                993 avis &#8212; note 3.26/5 &#8212; exclusivit&#233; 3.15&#9733; pire score
              </div>
            </div>
            <div style="text-align:right;flex-shrink:0;">
              <div style="font-size:18px;font-weight:800;color:#4F46E5;">3.26</div>
              <div style="font-size:10px;color:#9CA3AF;">/ 5 moy.</div>
            </div>
          </div>
          <div style="background:#EEF2FF;border-radius:8px;padding:8px 10px;margin-top:10px;">
            <div style="font-size:11px;font-weight:600;color:#4F46E5;">
              &#9654; Am&#233;liorer l&#39;exclusivit&#233; per&#231;ue en boutique (3.15&#9733;)
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================================================================
    # 5. PLAN D'ACTION IMMÉDIAT (col droite)
    # =========================================================================
    with p_right:
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:16px;padding:20px 22px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.055);border:1px solid #F3F4F6;height:100%;">
          <div style="font-size:13px;font-weight:700;color:#0F172A;margin-bottom:4px;">
            Plan d&#39;action imm&#233;diat
          </div>
          <div style="font-size:11px;color:#9CA3AF;margin-bottom:16px;">3 priorit&#233;s &#8212; semaine du 18 mars 2026</div>

          <div style="display:flex;align-items:center;gap:10px;padding:12px;border-radius:12px;
                      background:#FEF2F2;border:1px solid #FECACA;margin-bottom:10px;">
            <div style="width:42px;height:42px;border-radius:999px;background:#DC2626;
                        display:flex;align-items:center;justify-content:center;
                        font-size:18px;flex-shrink:0;">&#128680;</div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:700;color:#DC2626;">
                1. Cellule de crise &#8212; MAINTENANT
              </div>
              <div style="font-size:11px;color:#6B7280;margin-top:2px;">
                R&#233;unir DG, Comm, Juridique &#8212; d&#233;cision de communication sous 24h
              </div>
            </div>
            <span style="background:#DC2626;color:white;font-size:10px;font-weight:700;
                         padding:3px 8px;border-radius:999px;flex-shrink:0;">J0</span>
          </div>

          <div style="display:flex;align-items:center;gap:10px;padding:12px;border-radius:12px;
                      background:#FEF9C3;border:1px solid #FDE68A;margin-bottom:10px;">
            <div style="width:42px;height:42px;border-radius:999px;background:#B07A0A;
                        display:flex;align-items:center;justify-content:center;
                        font-size:18px;flex-shrink:0;">&#127775;</div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:700;color:#B07A0A;">
                2. Plan service client &#8212; J+7
              </div>
              <div style="font-size:11px;color:#6B7280;margin-top:2px;">
                Roadmap am&#233;lioration service client, seul pilier faible vs Chanel
              </div>
            </div>
            <span style="background:#B07A0A;color:white;font-size:10px;font-weight:700;
                         padding:3px 8px;border-radius:999px;flex-shrink:0;">J+7</span>
          </div>

          <div style="display:flex;align-items:center;gap:10px;padding:12px;border-radius:12px;
                      background:#EEF2FF;border:1px solid #C7D2FE;margin-bottom:10px;">
            <div style="width:42px;height:42px;border-radius:999px;background:#4F46E5;
                        display:flex;align-items:center;justify-content:center;
                        font-size:18px;flex-shrink:0;">&#11088;</div>
            <div style="flex:1;">
              <div style="font-size:13px;font-weight:700;color:#4F46E5;">
                3. Exclusivit&#233; boutique &#8212; J+14
              </div>
              <div style="font-size:11px;color:#6B7280;margin-top:2px;">
                Programme exp&#233;rience exclusive pour hausser le score 3.15&#9733; &#8594; 3.50&#9733;
              </div>
            </div>
            <span style="background:#4F46E5;color:white;font-size:10px;font-weight:700;
                         padding:3px 8px;border-radius:999px;flex-shrink:0;">J+14</span>
          </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
