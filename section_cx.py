import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def render_cx_tab(df_cat, df_plat_cx):

    # ── Alerte contre-intuitive ──────────────────────────────────────────────
    st.markdown("""
<div style="
    background: linear-gradient(135deg, #FFF7ED 0%, #FEF3C7 100%);
    border-left: 5px solid #F97316;
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 24px;
">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
        <span style="font-size:22px;">&#9888;&#65039;</span>
        <span style="font-size:15px; font-weight:700; color:#9A3412; font-family:'Inter',sans-serif;">
            INSIGHT CONTRE-INTUITIF &#8212; ACTION COMEX REQUISE
        </span>
    </div>
    <p style="margin:0 0 6px 0; font-size:14px; color:#7C2D12; font-family:'Inter',sans-serif; font-weight:600;">
        L&#8217;Exclusivit&#233; &#8212; ADN d&#8217;Herm&#232;s &#8212; est paradoxalement la <u>pire cat&#233;gorie client</u> (3.15&#9733;)
    </p>
    <p style="margin:0; font-size:13px; color:#92400E; font-family:'Inter',sans-serif; line-height:1.6;">
        Ce n&#8217;est <strong>pas</strong> le produit qui d&#233;&#231;oit : la Qualit&#233; cuir atteint 3.32&#9733;.
        C&#8217;est l&#8217;<strong>exp&#233;rience d&#8217;acc&#232;s</strong> qui g&#233;n&#232;re 38&#160;% d&#8217;avis n&#233;gatifs &#8212;
        listes d&#8217;attente opaques, rejets en boutique, sentiment d&#8217;exclusion plut&#244;t que de privil&#232;ge.
        Sans action, l&#8217;ADN de la marque devient son principal vecteur d&#8217;insatisfaction.
    </p>
</div>
""", unsafe_allow_html=True)

    # ── KPI cards ────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpi_style = """
        background:#FFFFFF;
        border:1px solid #E5E7EB;
        border-radius:10px;
        padding:16px 20px;
        text-align:center;
        box-shadow:0 1px 4px rgba(0,0,0,.06);
        font-family:'Inter',sans-serif;
    """
    with k1:
        st.markdown(f"""
<div style="{kpi_style}">
    <div style="font-size:28px; font-weight:800; color:#1F2937;">993</div>
    <div style="font-size:12px; color:#6B7280; margin-top:4px;">Avis collect&#233;s</div>
    <div style="font-size:11px; color:#9CA3AF; margin-top:2px;">4 plateformes</div>
</div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
<div style="{kpi_style}">
    <div style="font-size:28px; font-weight:800; color:#F59E0B;">3.26<span style="font-size:16px;">/5</span></div>
    <div style="font-size:12px; color:#6B7280; margin-top:4px;">Note globale</div>
    <div style="font-size:11px; color:#EF4444; margin-top:2px;">&#9660; Objectif&#160;3.65</div>
</div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
<div style="{kpi_style}">
    <div style="font-size:28px; font-weight:800; color:#10B981;">50.5<span style="font-size:16px;">%</span></div>
    <div style="font-size:12px; color:#6B7280; margin-top:4px;">Avis positifs</div>
    <div style="font-size:11px; color:#6B7280; margin-top:2px;">501 avis</div>
</div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
<div style="{kpi_style}">
    <div style="font-size:28px; font-weight:800; color:#EF4444;">33.3<span style="font-size:16px;">%</span></div>
    <div style="font-size:12px; color:#6B7280; margin-top:4px;">Avis n&#233;gatifs</div>
    <div style="font-size:11px; color:#6B7280; margin-top:2px;">331 avis</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ── Donn&#233;es locales ────────────────────────────────────────────────────────
    categories  = ["Service client", "Qualit&#233; cuir", "Prix", "Attente boutique", "Exclusivit&#233;"]
    notes       = [3.36, 3.32, 3.28, 3.19, 3.15]
    objectifs   = [3.80, 3.70, 3.60, 3.60, 3.50]
    pct_pos     = [52, 54, 50, 49, 48]
    pct_neg     = [34, 32, 29, 35, 38]

    def bar_color(n):
        if n < 3.20:
            return "#EF4444"
        elif n < 3.30:
            return "#F59E0B"
        return "#10B981"

    colors = [bar_color(n) for n in notes]

    # ── Chart principal : barres horizontales ─────────────────────────────────
    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        y=categories,
        x=notes,
        orientation="h",
        marker_color=colors,
        width=0.55,
        text=[f"<b>{n:.2f}&#9733;</b>  obj&#160;{o:.2f}" for n, o in zip(notes, objectifs)],
        textposition="outside",
        textfont=dict(family="Inter", size=12, color="#374151"),
        cliponaxis=False,
        name="Note actuelle",
        showlegend=False
    ))

    for i, (cat, obj) in enumerate(zip(categories, objectifs)):
        fig_bar.add_shape(
            type="line",
            x0=obj, x1=obj,
            y0=i - 0.38, y1=i + 0.38,
            line=dict(color="#6366F1", width=2.5, dash="dot")
        )

    fig_bar.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(symbol="line-ns", size=12, color="#6366F1",
                    line=dict(color="#6366F1", width=2.5)),
        name="Objectif"
    ))

    fig_bar.add_vline(
        x=3.26,
        line=dict(color="#9CA3AF", width=1.5, dash="dash"),
        annotation_text="Moy. 3.26",
        annotation_position="top right",
        annotation_font=dict(family="Inter", size=11, color="#6B7280")
    )

    fig_bar.update_layout(
        title=dict(
            text="<b>Performance par cat&#233;gorie</b> &#8212; Notes / 5",
            font=dict(family="Inter", size=16, color="#111827"),
            x=0
        ),
        xaxis=dict(
            range=[2.7, 4.3],
            tickfont=dict(family="Inter", size=11, color="#6B7280"),
            gridcolor="#F3F4F6",
            showgrid=True,
            zeroline=False,
            title=""
        ),
        yaxis=dict(
            tickfont=dict(family="Inter", size=12, color="#374151"),
            gridcolor="#F3F4F6",
            showgrid=False,
            autorange="reversed"
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=160, t=60, b=40),
        height=340,
        legend=dict(
            orientation="h",
            x=0, y=-0.12,
            font=dict(family="Inter", size=11, color="#6B7280")
        )
    )

    # ── Donut sentiment ───────────────────────────────────────────────────────
    fig_donut = go.Figure(go.Pie(
        labels=["Positifs", "Neutres", "N&#233;gatifs"],
        values=[501, 161, 331],
        hole=0.58,
        marker=dict(colors=["#10B981", "#F59E0B", "#EF4444"],
                    line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(family="Inter", size=12),
        direction="clockwise",
        sort=False
    ))

    fig_donut.add_annotation(
        text="<b>993</b><br><span style='font-size:10px'>avis</span>",
        x=0.5, y=0.5,
        font=dict(family="Inter", size=16, color="#1F2937"),
        showarrow=False,
        align="center"
    )

    fig_donut.update_layout(
        title=dict(
            text="<b>Sentiment global</b>",
            font=dict(family="Inter", size=16, color="#111827"),
            x=0
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=60, b=10),
        height=340,
        legend=dict(
            orientation="v",
            x=1.02, y=0.5,
            font=dict(family="Inter", size=11, color="#6B7280")
        ),
        showlegend=True
    )

    col_bar, col_donut = st.columns([3, 2])
    with col_bar:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_donut:
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Evolution 7 mois ──────────────────────────────────────────────────────
    mois = ["Sep", "Oct", "Nov", "D&#233;c", "Jan", "F&#233;v", "Mar"]

    np.random.seed(42)
    df_evol = pd.DataFrame({
        "Mois": mois,
        "Service client":    [3.52, 3.48, 3.44, 3.42, 3.40, 3.38, 3.36],
        "Qualit&#233; cuir": [3.50, 3.47, 3.44, 3.41, 3.38, 3.35, 3.32],
        "Prix":              [3.45, 3.41, 3.38, 3.35, 3.33, 3.30, 3.28],
        "Attente boutique":  [3.38, 3.34, 3.30, 3.27, 3.25, 3.22, 3.19],
        "Exclusivit&#233;":  [3.34, 3.30, 3.26, 3.23, 3.21, 3.18, 3.15],
    })

    palette = {
        "Service client":    "#6366F1",
        "Qualit&#233; cuir": "#10B981",
        "Prix":              "#F59E0B",
        "Attente boutique":  "#3B82F6",
        "Exclusivit&#233;":  "#EF4444",
    }

    fig_evol = go.Figure()
    for col, color in palette.items():
        fig_evol.add_trace(go.Scatter(
            x=df_evol["Mois"],
            y=df_evol[col],
            mode="lines+markers",
            name=col,
            line=dict(color=color, width=2),
            marker=dict(size=6, color=color),
        ))

    fig_evol.update_layout(
        title=dict(
            text="<b>&#201;volution des notes &#8212; Sep 2025 &#8594; Mar 2026</b>",
            font=dict(family="Inter", size=16, color="#111827"),
            x=0
        ),
        xaxis=dict(
            tickfont=dict(family="Inter", size=11, color="#6B7280"),
            gridcolor="#F3F4F6",
            showgrid=True,
            zeroline=False,
            title=""
        ),
        yaxis=dict(
            range=[2.9, 3.8],
            tickfont=dict(family="Inter", size=11, color="#6B7280"),
            gridcolor="#F3F4F6",
            showgrid=True,
            zeroline=False,
            title=dict(text="Note /5", font=dict(family="Inter", size=11, color="#6B7280"))
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=40),
        height=320,
        legend=dict(
            orientation="h",
            x=0, y=-0.18,
            font=dict(family="Inter", size=11, color="#6B7280")
        ),
        hovermode="x unified"
    )

    # ── Grouped bar sentiments ─────────────────────────────────────────────────
    fig_sent = go.Figure()

    fig_sent.add_trace(go.Bar(
        name="Positifs",
        x=categories,
        y=pct_pos,
        marker_color="#10B981",
        text=[f"{v}%" for v in pct_pos],
        textposition="outside",
        textfont=dict(family="Inter", size=11, color="#374151"),
        cliponaxis=False
    ))

    fig_sent.add_trace(go.Bar(
        name="N&#233;gatifs",
        x=categories,
        y=pct_neg,
        marker_color="#EF4444",
        text=[f"{v}%" for v in pct_neg],
        textposition="outside",
        textfont=dict(family="Inter", size=11, color="#374151"),
        cliponaxis=False
    ))

    fig_sent.update_layout(
        title=dict(
            text="<b>Sentiments positifs vs n&#233;gatifs par cat&#233;gorie</b>",
            font=dict(family="Inter", size=16, color="#111827"),
            x=0
        ),
        barmode="group",
        xaxis=dict(
            tickfont=dict(family="Inter", size=11, color="#374151"),
            gridcolor="#F3F4F6",
            showgrid=False,
            zeroline=False,
            title=""
        ),
        yaxis=dict(
            range=[0, 70],
            tickfont=dict(family="Inter", size=11, color="#6B7280"),
            gridcolor="#F3F4F6",
            showgrid=True,
            zeroline=False,
            title=dict(text="%", font=dict(family="Inter", size=11, color="#6B7280"))
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=60),
        height=320,
        legend=dict(
            orientation="h",
            x=0, y=-0.22,
            font=dict(family="Inter", size=11, color="#6B7280")
        )
    )

    col_evol, col_sent = st.columns(2)
    with col_evol:
        st.plotly_chart(fig_evol, use_container_width=True)
    with col_sent:
        st.plotly_chart(fig_sent, use_container_width=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Plan d'am&#233;lioration ────────────────────────────────────────────────────
    st.markdown("""
<div style="font-family:'Inter',sans-serif; margin-bottom:18px;">
    <div style="font-size:16px; font-weight:700; color:#111827; margin-bottom:14px;">
        &#128203;&#160; Plan d&#8217;am&#233;lioration prioritaire
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">

        <div style="
            background:#FFF1F2;
            border:1px solid #FECDD3;
            border-left:5px solid #EF4444;
            border-radius:8px;
            padding:16px 18px;
        ">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="
                    background:#EF4444; color:white;
                    font-size:10px; font-weight:700;
                    padding:2px 8px; border-radius:20px;
                ">PRIORIT&#201; HAUTE</span>
                <span style="font-size:13px; font-weight:700; color:#991B1B;">
                    Exclusivit&#233; &#8212; 3.15&#9733;
                </span>
            </div>
            <p style="margin:0 0 6px 0; font-size:12px; color:#7F1D1D; font-weight:600;">
                &#128274;&#160; Exp&#233;rience d&#8217;acc&#232;s
            </p>
            <ul style="margin:0; padding-left:16px; font-size:12px; color:#991B1B; line-height:1.8;">
                <li>Cr&#233;er un programme de RDV priv&#233;s en boutique</li>
                <li>Digitaliser la liste d&#8217;attente (statut transparent en temps r&#233;el)</li>
                <li>Former les &#233;quipes : rejets avec protocole de dignity&#233;</li>
            </ul>
        </div>

        <div style="
            background:#FFF7ED;
            border:1px solid #FED7AA;
            border-left:5px solid #F97316;
            border-radius:8px;
            padding:16px 18px;
        ">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="
                    background:#F97316; color:white;
                    font-size:10px; font-weight:700;
                    padding:2px 8px; border-radius:20px;
                ">PRIORIT&#201; HAUTE</span>
                <span style="font-size:13px; font-weight:700; color:#9A3412;">
                    Attente boutique &#8212; 3.19&#9733;
                </span>
            </div>
            <p style="margin:0 0 6px 0; font-size:12px; color:#7C2D12; font-weight:600;">
                &#9203;&#160; Gestion des files
            </p>
            <ul style="margin:0; padding-left:16px; font-size:12px; color:#9A3412; line-height:1.8;">
                <li>D&#233;ployer une file d&#8217;attente virtuelle (QR code)</li>
                <li>Notification SMS &#171;&#160;Votre conseiller est pr&#234;t&#160;&#187;</li>
                <li>Salon d&#8217;attente premium avec rafra&#238;chissements</li>
            </ul>
        </div>

        <div style="
            background:#FEFCE8;
            border:1px solid #FEF08A;
            border-left:5px solid #EAB308;
            border-radius:8px;
            padding:16px 18px;
        ">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="
                    background:#EAB308; color:white;
                    font-size:10px; font-weight:700;
                    padding:2px 8px; border-radius:20px;
                ">PRIORIT&#201; MOD&#201;R&#201;E</span>
                <span style="font-size:13px; font-weight:700; color:#713F12;">
                    Prix &#8212; 3.28&#9733;
                </span>
            </div>
            <p style="margin:0 0 6px 0; font-size:12px; color:#713F12; font-weight:600;">
                &#128176;&#160; Narrative de valeur
            </p>
            <ul style="margin:0; padding-left:16px; font-size:12px; color:#92400E; line-height:1.8;">
                <li>Livret post-achat : savoir-faire, tra&#231;abilit&#233; artisan</li>
                <li>Vid&#233;o coulisses atelier &#224; chaque acquisition</li>
                <li>Programme SAV &#224; vie mis en avant</li>
            </ul>
        </div>

        <div style="
            background:#F0FDF4;
            border:1px solid #BBF7D0;
            border-left:5px solid #22C55E;
            border-radius:8px;
            padding:16px 18px;
        ">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="
                    background:#22C55E; color:white;
                    font-size:10px; font-weight:700;
                    padding:2px 8px; border-radius:20px;
                ">PRIORIT&#201; MOD&#201;R&#201;E</span>
                <span style="font-size:13px; font-weight:700; color:#14532D;">
                    R&#233;putation digitale
                </span>
            </div>
            <p style="margin:0 0 6px 0; font-size:12px; color:#14532D; font-weight:600;">
                &#11088;&#160; Trustpilot &amp; Google Maps
            </p>
            <ul style="margin:0; padding-left:16px; font-size:12px; color:#166534; line-height:1.8;">
                <li>R&#233;pondre &#224; tous les avis 1&#9733;&#8211;2&#9733; sous 48&#160;h</li>
                <li>Protocole de r&#233;ponse empathique (template COMEX valid&#233;)</li>
                <li>Relance satisfaction J+30 post-achat</li>
            </ul>
        </div>

    </div>
</div>
""", unsafe_allow_html=True)
