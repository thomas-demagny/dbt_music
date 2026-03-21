import json
from pathlib import Path
 
import pandas as pd
import plotly.express as px
import streamlit as st
 
st.set_page_config(
    page_title="Music Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
JSON_PATH = Path(__file__).parent / "results.json"
 
@st.cache_data
def load_data():
    if not JSON_PATH.exists():
        return None
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)
 
data = load_data()
 
if data is None:
    st.error("❌ Fichier results.json introuvable. Lance d'abord generate_answers.py.")
    st.stop()
 
queries = {q["num"]: q for q in data["queries"]}
 
def get_df(num):
    q = queries.get(num, {})
    if q.get("error") or not q.get("rows"):
        return pd.DataFrame()
    return pd.DataFrame(q["rows"])
 
PLOT_LAYOUT = dict(
    plot_bgcolor  = "#0f1117",
    paper_bgcolor = "#0f1117",
    font_color    = "#e2e4ed",
    coloraxis_showscale = False,
)
 
st.markdown("""
<style>
    [data-testid="stSidebar"] { background: #0f1117; }
    .block-container { padding-top: 1.5rem; }
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.15rem !important; color: #a5b4fc; }
    .metric-card {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
    }
    .metric-card .val { font-size: 2rem; font-weight: 700; color: #6366f1; }
    .metric-card .lbl { font-size: 12px; color: #6b7280; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)
 
PAGES = {
    "🏠 Accueil":              0,
    "Q1 — Albums multi-CD":    1,
    "Q2 — Morceaux 2000/2002": 2,
    "Q3 — Rock & Jazz":        3,
    "Q4 — Top 10 albums":      4,
    "Q5 — Albums par artiste": 5,
    "Q6 — Tracks par artiste": 6,
    "Q7 — Genre années 2000":  7,
    "Q8 — Playlists > 4 min":  8,
    "Q9 — Rock en France":     9,
    "Q10 — Taille par genre":  10,
    "Q11 — Playlists < 1990":  11,
}
 
with st.sidebar:
    st.markdown("## 🎵 Music Analytics")
    st.caption(f"Données du {data['generated_at']}")
    st.divider()
    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
 
num = PAGES[page]
 
# ── ACCUEIL ──
if num == 0:
    st.title("🎵 Music Analytics Dashboard")
    st.caption(f"Données exportées depuis Snowflake le {data['generated_at']}")
    st.divider()
 
    df5 = get_df(5)
    df6 = get_df(6)
    df3 = get_df(3)
 
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="val">{len(df5)}</div><div class="lbl">Artistes</div></div>', unsafe_allow_html=True)
    with c2:
        nb_albums = df5["NB_ALBUMS"].astype(int).sum() if not df5.empty and "NB_ALBUMS" in df5.columns else "—"
        st.markdown(f'<div class="metric-card"><div class="val">{nb_albums}</div><div class="lbl">Albums</div></div>', unsafe_allow_html=True)
    with c3:
        nb_tracks = get_df(6)["NB_MORCEAUX"].astype(int).sum() if not get_df(6).empty else "—"
        st.markdown(f'<div class="metric-card"><div class="val">{nb_tracks}</div><div class="lbl">Morceaux</div></div>', unsafe_allow_html=True)
    with c4:
        nb_genres = df3["GENRE"].nunique() if not df3.empty and "GENRE" in df3.columns else "—"
        st.markdown(f'<div class="metric-card"><div class="val">{nb_genres}</div><div class="lbl">Genres</div></div>', unsafe_allow_html=True)
 
    st.divider()
 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 artistes par morceaux")
        if not df6.empty:
            df6["NB_MORCEAUX"] = df6["NB_MORCEAUX"].astype(int)
            fig = px.bar(df6.head(10), x="NB_MORCEAUX", y="ARTISTE",
                         orientation="h", color="NB_MORCEAUX",
                         color_continuous_scale="purples",
                         labels={"NB_MORCEAUX": "Nb morceaux", "ARTISTE": "Artiste"})
            fig.update_layout(**PLOT_LAYOUT, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
 
    with col2:
        st.subheader("Top 10 albums les plus longs")
        df4 = get_df(4)
        if not df4.empty:
            df4["DUREE_TOTALE_MIN"] = df4["DUREE_TOTALE_MIN"].astype(float)
            fig = px.bar(df4, x="DUREE_TOTALE_MIN", y="TITRE_ALBUM",
                         orientation="h", color="DUREE_TOTALE_MIN",
                         color_continuous_scale="teal",
                         labels={"DUREE_TOTALE_MIN": "Durée (min)", "TITRE_ALBUM": "Album"})
            fig.update_layout(**PLOT_LAYOUT, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
 
# ── Q1 à Q11 ──
else:
    q     = queries.get(num, {})
    df    = get_df(num)
    title = q.get("title", "")
 
    st.title(f"Q{num}. {title}")
    st.divider()
 
    if q.get("error"):
        st.error(f"Erreur : {q['error']}")
 
    elif df.empty:
        st.warning("Aucun résultat pour cette requête.")
 
    else:
        st.caption(f"{len(df)} ligne(s) retournée(s)")
 
        if num == 4:
            df["DUREE_TOTALE_MIN"] = df["DUREE_TOTALE_MIN"].astype(float)
            fig = px.bar(df, x="TITRE_ALBUM", y="DUREE_TOTALE_MIN",
                         color="DUREE_TOTALE_MIN", color_continuous_scale="teal",
                         labels={"DUREE_TOTALE_MIN": "Durée (min)", "TITRE_ALBUM": "Album"})
            fig.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
 
        elif num == 5:
            df["NB_ALBUMS"] = df["NB_ALBUMS"].astype(int)
            fig = px.bar(df.head(20), x="NB_ALBUMS", y="ARTISTE", orientation="h",
                         color="NB_ALBUMS", color_continuous_scale="purples",
                         labels={"NB_ALBUMS": "Nb albums", "ARTISTE": "Artiste"})
            fig.update_layout(**PLOT_LAYOUT, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
 
        elif num == 6:
            df["NB_MORCEAUX"] = df["NB_MORCEAUX"].astype(int)
            fig = px.bar(df.head(20), x="NB_MORCEAUX", y="ARTISTE", orientation="h",
                         color="NB_MORCEAUX", color_continuous_scale="magma",
                         labels={"NB_MORCEAUX": "Nb morceaux", "ARTISTE": "Artiste"})
            fig.update_layout(**PLOT_LAYOUT, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
 
        elif num == 10:
            df["TAILLE_MOYENNE_MO"] = df["TAILLE_MOYENNE_MO"].astype(float)
            fig = px.bar(df, x="GENRE", y="TAILLE_MOYENNE_MO",
                         color="TAILLE_MOYENNE_MO", color_continuous_scale="plasma",
                         labels={"TAILLE_MOYENNE_MO": "Taille moy. (Mo)", "GENRE": "Genre"})
            fig.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
 
        st.subheader("Données complètes")
        st.dataframe(df, use_container_width=True, hide_index=True)
 
