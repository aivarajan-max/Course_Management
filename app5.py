"""
Training Activity Portal — Streamlit
Redesigned layout (same color palette).

Sections:
  1) Course Schedule      (existing dashboard)
  2) Course Repository    (Topic + Course → Drive folder)
  3) Reports              (Batch + Module → Drive link)
  4) Task Update          (placeholder)

Run with: streamlit run app5.py
"""

from datetime import datetime, date
import base64
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Training Activity Portal", page_icon="📊", layout="wide")

# ---------------------------------------------------------------
# Blue & white theme — SAME COLORS, NEW LAYOUT
# Palette:
#   Primary blue:    #0B5394
#   Deep blue:       #073763
#   Light blue bg:   #eaf2fb
#   Border blue:     #cfe2f3
#   White:           #ffffff
#   Today accent:    #c27c0e / #fff7e6 / #f5d9a8 / #b06d0a
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Base ---------- */
    .stApp { background-color: #ffffff; }

    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 1.2rem !important;
        max-width: 1240px;
    }

    h1, h2, h3, h4 {
        color: #0B5394 !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.4rem !important;
    }

    hr {
        border-color: #cfe2f3 !important;
        margin: 0.6rem 0 !important;
    }

    label {
        color: #0B5394 !important;
        font-weight: 600 !important;
        margin-bottom: 0.1rem !important;
    }

    /* ---------- Selects ---------- */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cfe2f3 !important;
        border-radius: 8px !important;
        min-height: 40px !important;
        transition: border-color 0.15s ease;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #0B5394 !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background-color: #ffffff;
        color: #0B5394;
        border: 1px solid #cfe2f3;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.45rem 1rem;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        background-color: #eaf2fb;
        color: #073763;
        border-color: #0B5394;
    }
    /* Primary buttons (active nav) */
    .stButton > button[kind="primary"] {
        background-color: #0B5394;
        color: #ffffff;
        border: 1px solid #0B5394;
        box-shadow: 0 2px 6px rgba(11,83,148,0.18);
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #073763;
        color: #ffffff;
        border-color: #073763;
    }

    /* ---------- Top Header Bar ---------- */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, #0B5394 0%, #073763 100%);
        color: #ffffff;
        padding: 18px 24px;
        border-radius: 12px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(11,83,148,0.15);
        min-height: 72px;
    }
    .app-header .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-header .brand-icon {
        font-size: 1.7rem;
    }
    .app-header .brand-title {
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: 0.2px;
    }
    .app-header .brand-sub {
        font-size: 0.78rem;
        opacity: 0.85;
        margin-top: -2px;
    }

    /* ---------- Metric cards ---------- */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #cfe2f3;
        border-top: 3px solid #0B5394;
        border-radius: 10px;
        padding: 10px 14px;
        box-shadow: 0 1px 3px rgba(11,83,148,0.06);
    }
    div[data-testid="stMetricLabel"] {
        color: #0B5394 !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #073763 !important;
        font-size: 1.6rem !important;
    }

    /* ---------- Progress ---------- */
    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #0B5394 !important;
    }

    div[data-testid="column"] {
        padding: 0 0.4rem !important;
    }

    /* ---------- Info pill cards (Coordinator / Dates / Status) ---------- */
    .info-pill {
        background-color: #ffffff;
        border: 1px solid #cfe2f3;
        border-radius: 10px;
        padding: 12px 14px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(11,83,148,0.05);
    }
    .info-pill .ip-label {
        color: #0B5394;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .info-pill .ip-value {
        color: #073763;
        font-size: 1.0rem;
        font-weight: 600;
    }

    /* ---------- Session Timeline cards ---------- */
    .session-card {
        background-color: #ffffff;
        border: 1px solid #cfe2f3;
        border-left: 4px solid #0B5394;
        border-radius: 10px;
        padding: 12px 16px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(11,83,148,0.05);
    }
    .session-card.today {
        border-left-color: #c27c0e;
        background-color: #fff7e6;
        border-color: #f5d9a8;
        box-shadow: 0 2px 6px rgba(194,124,14,0.12);
    }
    .session-card .label {
        color: #0B5394;
        font-weight: 700;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .session-card.today .label { color: #b06d0a; }
    .session-card .date {
        color: #073763;
        font-weight: 700;
        font-size: 1.0rem;
        margin-bottom: 4px;
    }
    .session-card .topic {
        color: #1f1f1f;
        font-size: 0.9rem;
        line-height: 1.35;
    }
    .session-card .empty {
        color: #888;
        font-style: italic;
        font-size: 0.9rem;
    }

    /* ---------- Section title (with left bar) ---------- */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 18px 0 10px 0;
    }
    .section-title .bar {
        width: 4px;
        height: 22px;
        background-color: #0B5394;
        border-radius: 2px;
    }
    .section-title .text {
        color: #0B5394;
        font-weight: 700;
        font-size: 1.05rem;
    }
    .section-title .meta {
        color: #666;
        font-weight: 400;
        font-size: 0.85rem;
        margin-left: 6px;
    }

    /* ---------- Selection panels (Repository & Reports) ---------- */
    .selection-panel {
        background-color: #eaf2fb;
        border: 1px solid #cfe2f3;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }
    .panel-result {
        background-color: #ffffff;
        border: 1px solid #cfe2f3;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-top: 8px;
    }

    /* ---------- Open Folder / Report button ---------- */
    a.open-folder-btn {
        display: inline-block;
        background-color: #0B5394;
        color: #ffffff !important;
        padding: 12px 28px;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        margin-top: 0.6rem;
        box-shadow: 0 2px 6px rgba(11,83,148,0.18);
        transition: all 0.15s ease;
    }
    a.open-folder-btn:hover {
        background-color: #073763;
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(11,83,148,0.25);
    }

    /* ---------- Home hero ---------- */
    .home-hero {
        background: linear-gradient(135deg, #eaf2fb 0%, #ffffff 100%);
        border: 1px solid #cfe2f3;
        border-radius: 14px;
        padding: 32px 28px;
        text-align: center;
        margin-bottom: 18px;
    }
    .home-hero h2 {
        color: #0B5394 !important;
        margin: 0 0 6px 0 !important;
        font-size: 1.6rem;
    }
    .home-hero p {
        color: #444;
        margin: 0;
        font-size: 0.98rem;
    }

    /* ---------- Home tile ---------- */
    .home-tile {
        background-color: #ffffff;
        border: 1px solid #cfe2f3;
        border-radius: 12px;
        padding: 18px 18px 14px 18px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(11,83,148,0.05);
        transition: all 0.15s ease;
    }
    .home-tile:hover {
        border-color: #0B5394;
        box-shadow: 0 4px 12px rgba(11,83,148,0.12);
    }
    .home-tile .tile-icon {
        font-size: 1.6rem;
        margin-bottom: 6px;
    }
    .home-tile .tile-title {
        color: #0B5394;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 4px;
    }
    .home-tile .tile-desc {
        color: #555;
        font-size: 0.85rem;
        margin-bottom: 10px;
        line-height: 1.35;
    }

    /* ---------- Sidebar polish ---------- */
    section[data-testid="stSidebar"] {
        background-color: #f7faff;
        border-right: 1px solid #cfe2f3;
    }
    .sidebar-header {
        background: linear-gradient(135deg, #0B5394 0%, #073763 100%);
        color: #ffffff;
        padding: 14px 14px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    .sidebar-header .sh-title {
        font-weight: 700;
        font-size: 1.0rem;
    }
    .sidebar-header .sh-date {
        font-size: 0.78rem;
        opacity: 0.9;
        margin-top: 2px;
    }
    .sidebar-empty {
        color: #888;
        font-style: italic;
        font-size: 0.9rem;
        text-align: center;
        padding: 14px;
        background-color: #ffffff;
        border: 1px dashed #cfe2f3;
        border-radius: 8px;
    }

    /* ---------- Task tracker placeholder ---------- */
    .task-placeholder {
        background: linear-gradient(135deg, #eaf2fb 0%, #ffffff 100%);
        border: 1px dashed #0B5394;
        border-radius: 14px;
        padding: 40px 24px;
        text-align: center;
    }
    .task-placeholder .tp-icon { font-size: 3rem; margin-bottom: 8px; }
    .task-placeholder .tp-title { color: #0B5394; font-weight: 700; font-size: 1.2rem; margin-bottom: 4px; }
    .task-placeholder .tp-desc  { color: #555; font-size: 0.95rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------
SHEET_ID = "1ybsQD3OBMf9TAKddMmJjx-aWKJaekutCFGtimZRVC38"
DASHBOARD_TAB = "Dashboard"
REPOSITORY_TAB = "Handson Materials"
REPORTS_TAB = "CAG Reports"

LOCAL_REPO_FILE = "Course_Materials-Repository.xlsx"
LOCAL_REPO_SHEET = "Handson Materials"

LOCAL_REPORTS_FILE = "CAG-Reports.xlsx"
LOCAL_REPORTS_SHEET = "Sheet1"

LOGO_FILE = "gitaa-logo.png"

# ---------------------------------------------------------------
# Section state
# ---------------------------------------------------------------
if "section" not in st.session_state:
    st.session_state.section = "home"

def set_section(name: str):
    st.session_state.section = name

# ---------------------------------------------------------------
# TOP HEADER — branded gradient bar with title + refresh
# ---------------------------------------------------------------
hdr_left, hdr_right = st.columns([6, 1])
with hdr_left:
    st.markdown(
        """
        <div class="app-header">
            <div class="brand">
                <div class="brand-icon">📊</div>
                <div>
                    <div class="brand-title">Training Activity Portal</div>
                    <div class="brand-sub">Schedules · Repository · Reports · Tasks</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hdr_right:
    st.write("")
    st.write("")
    if st.button("🔄  Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ---------------------------------------------------------------
# NAV TABS — pill-style row
# ---------------------------------------------------------------
nav_cols = st.columns(5)
nav_items = [
    ("home",       "🏠  Home"),
    ("schedule",   "📈  Dashboard"),
    ("repository", "📂  Repository"),
    ("reports",    "📑  Reports"),
    ("tasks",      "✅  Task Update"),
]
for col, (key, label) in zip(nav_cols, nav_items):
    with col:
        st.button(
            label,
            use_container_width=True,
            on_click=set_section,
            args=(key,),
            key=f"nav_{key}",
            type="primary" if st.session_state.section == key else "secondary",
        )

st.write("")  # small spacer below the nav

# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------
def csv_url(sheet_id: str, tab: str) -> str:
    return (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        f"/gviz/tq?tqx=out:csv&sheet={tab}"
    )

@st.cache_data
def load_logo_b64(path: str) -> str | None:
    try:
        data = Path(path).read_bytes()
        return base64.b64encode(data).decode("utf-8")
    except Exception:
        return None

@st.cache_data(ttl=60)
def load_dashboard() -> pd.DataFrame:
    df = pd.read_csv(csv_url(SHEET_ID, DASHBOARD_TAB))
    df = df.dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return df

@st.cache_data(ttl=60)
def load_course_sessions(course_tab: str) -> pd.DataFrame:
    import io, requests

    resp = requests.get(csv_url(SHEET_ID, course_tab), timeout=15)
    resp.raise_for_status()
    raw = resp.text
    if not raw.strip():
        raise ValueError(f"Tab '{course_tab}' appears to be empty or does not exist.")

    probe = pd.read_csv(io.StringIO(raw), header=None, dtype=str, keep_default_na=False)

    header_row_idx = None
    for i in range(min(len(probe), 10)):
        cells = [str(x).strip().lower() for x in probe.iloc[i].tolist()]
        has_topic = any(c in ("topic", "topics", "session topic", "session", "title") for c in cells)
        has_date  = any(c in ("date", "session date", "class date") for c in cells)
        if has_topic and has_date:
            header_row_idx = i
            break

    if header_row_idx is None:
        df = pd.read_csv(io.StringIO(raw))
    else:
        df = pd.read_csv(io.StringIO(raw), header=header_row_idx)

    df = df.dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]

    date_col  = next((c for c in df.columns if c.lower() in ("date", "session date", "class date")), None)
    topic_col = next(
        (c for c in df.columns if c.lower() in ("topic", "topics", "session topic", "session", "title")),
        None,
    )

    if date_col is None or topic_col is None:
        raise ValueError(
            f"Course tab '{course_tab}' must have Date and Topic columns. "
            f"Detected columns: {list(df.columns)}"
        )

    out = df[[date_col, topic_col]].rename(columns={date_col: "Date", topic_col: "Topic"})

    parsed_us = pd.to_datetime(out["Date"], errors="coerce", dayfirst=False)
    if parsed_us.notna().sum() == 0:
        parsed_us = pd.to_datetime(out["Date"], errors="coerce", dayfirst=True)
    out["Date"] = parsed_us
    out = out.dropna(subset=["Date"])
    out["Date"] = out["Date"].dt.date

    out["Topic"] = out["Topic"].astype(str).str.strip()
    out = out[(out["Topic"] != "") & (out["Topic"].str.lower() != "nan")]
    out = out.sort_values("Date").reset_index(drop=True)
    return out

@st.cache_data(ttl=60)
def load_repository() -> pd.DataFrame:
    df = None
    try:
        df = pd.read_csv(csv_url(SHEET_ID, REPOSITORY_TAB))
        if df is None or df.empty or len(df.columns) < 3:
            df = None
    except Exception:
        df = None

    if df is None:
        df = pd.read_excel(LOCAL_REPO_FILE, sheet_name=LOCAL_REPO_SHEET)

    df.columns = [str(c).strip() for c in df.columns]

    topic_col  = next((c for c in df.columns if c.lower() in ("topic", "topic name")), None)
    course_col = next((c for c in df.columns if c.lower() in ("course", "course name")), None)
    link_col   = next((c for c in df.columns if c.lower() in ("link", "url", "drive link")), None)

    if not (topic_col and course_col and link_col):
        raise ValueError(f"Repository must have Topic / Course / Link columns. Got: {list(df.columns)}")

    df = df[[topic_col, course_col, link_col]].rename(
        columns={topic_col: "Topic", course_col: "Course", link_col: "Link"}
    )

    df["Topic"] = df["Topic"].astype("object").where(df["Topic"].notna(), None)
    df["Topic"] = df["Topic"].ffill()

    for c in ["Topic", "Course", "Link"]:
        df[c] = df[c].astype(str).str.strip()

    df = df[df["Link"].str.startswith("http")]
    df = df[(df["Topic"] != "") & (df["Course"] != "") & (df["Topic"].str.lower() != "nan")]

    return df.reset_index(drop=True)

@st.cache_data(ttl=60)
def load_reports() -> pd.DataFrame:
    df = None
    try:
        df = pd.read_csv(csv_url(SHEET_ID, REPORTS_TAB))
        if df is None or df.empty or len(df.columns) < 3:
            df = None
    except Exception:
        df = None

    if df is None:
        df = pd.read_excel(LOCAL_REPORTS_FILE, sheet_name=LOCAL_REPORTS_SHEET)

    df.columns = [str(c).strip() for c in df.columns]

    batch_col  = next((c for c in df.columns if c.lower() in ("batch", "batch name")), None)
    module_col = next((c for c in df.columns if c.lower() in ("module", "module name")), None)
    link_col   = next((c for c in df.columns if c.lower() in ("link", "url", "drive link")), None)

    if not (batch_col and module_col and link_col):
        raise ValueError(f"Reports must have Batch / Module / Link columns. Got: {list(df.columns)}")

    df = df[[batch_col, module_col, link_col]].rename(
        columns={batch_col: "Batch", module_col: "Module", link_col: "Link"}
    )

    df["Batch"] = df["Batch"].astype("object").where(df["Batch"].notna(), None)
    df["Batch"] = df["Batch"].ffill()

    for c in ["Batch", "Module", "Link"]:
        df[c] = df[c].astype(str).str.strip()

    df = df[df["Link"].str.startswith("http")]
    df = df[(df["Batch"] != "") & (df["Module"] != "") & (df["Batch"].str.lower() != "nan")]

    return df.reset_index(drop=True)


def section_title(text: str, meta: str = ""):
    meta_html = f"<span class='meta'>{meta}</span>" if meta else ""
    st.markdown(
        f"<div class='section-title'><div class='bar'></div>"
        f"<div class='text'>{text}</div>{meta_html}</div>",
        unsafe_allow_html=True,
    )


# ===============================================================
# SECTION 1 — COURSE SCHEDULE
# ===============================================================
def render_course_schedule():
    st.markdown(
        "<h2 style='margin-bottom:0;'>📋 Course Schedule</h2>"
        f"<div style='color:#666; font-size:0.85rem; margin-bottom:10px;'>"
        f"Last fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  •  "
        f"Click 🔄 Refresh to pull the latest from Google Sheets</div>",
        unsafe_allow_html=True,
    )

    try:
        dashboard = load_dashboard()
    except Exception as e:
        st.error(f"Could not load dashboard tab '{DASHBOARD_TAB}': {e}")
        st.info("If your dashboard tab has a different name, edit DASHBOARD_TAB at the top of app5.py.")
        return

    course_col = next(
        (c for c in dashboard.columns if c.lower().strip() in ("course", "course name", "course_name")),
        None,
    )
    if course_col is None:
        st.error(f"Could not find a 'Course' column in the dashboard. Columns found: {list(dashboard.columns)}")
        return

    courses = (
        dashboard[course_col]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda s: s != ""]
        .tolist()
    )

    # Course selector inside a selection panel for visual grouping
    st.markdown('<div class="selection-panel">', unsafe_allow_html=True)
    dd_col, _ = st.columns([2, 5])
    with dd_col:
        selected_course = st.selectbox("📂 Course Name", courses, key="sched_course")
    st.markdown('</div>', unsafe_allow_html=True)

    row = dashboard[dashboard[course_col].astype(str).str.strip() == selected_course]
    if row.empty:
        st.warning("No row found for this course.")
        return
    row = row.iloc[0]

    def get(col_options, default="—"):
        for opt in col_options:
            for c in dashboard.columns:
                if c.lower().strip() == opt.lower().strip():
                    val = row[c]
                    if pd.isna(val):
                        return default
                    try:
                        f = float(val)
                        if f.is_integer():
                            return int(f)
                    except (ValueError, TypeError):
                        pass
                    return val
        return default

    coordinator         = get(["Coordinator"])
    starting_date       = get(["Starting Date", "Start Date"])
    ending_date         = get(["Ending Date", "End Date"])
    total_sessions      = get(["Total Number of session", "Total Number of Sessions", "Total Sessions"])
    completed_session   = get(["Completed Session", "Completed Sessions"])
    total_assignments   = get(["Total Number of Assignment", "Total Number of Assignments", "Total Assignments"])
    assignment_released = get(["Assignment released", "Assignments Released", "Assignment Released"])
    online_session      = get(["Online Session", "Online Sessions"])
    recorded            = get(["Recorded", "Recorded Session", "Recorded Sessions"])
    status              = get(["Status"])

    # Course title
    st.markdown(
        f"<h3 style='margin-top:6px;'>📘 {selected_course}</h3>",
        unsafe_allow_html=True,
    )

    # ----- Info pill cards (Coordinator / Start / End / Status) -----
    status_str = str(status).strip()
    color = {"active": "🟢", "yet to start": "🟡", "completed": "🔵"}.get(status_str.lower(), "⚪")
    status_display = f"{color} {status_str if status_str and status_str != '—' else '—'}"

    pill_data = [
        ("Coordinator",   "👤", coordinator),
        ("Starting Date", "📅", starting_date),
        ("Ending Date",   "🏁", ending_date),
        ("Status",        "📌", status_display),
    ]
    pc1, pc2, pc3, pc4 = st.columns(4)
    for col, (lbl, icon, val) in zip([pc1, pc2, pc3, pc4], pill_data):
        col.markdown(
            f"<div class='info-pill'>"
            f"<div class='ip-label'>{icon}  {lbl}</div>"
            f"<div class='ip-value'>{val}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ----- Metrics -----
    section_title("Key Metrics")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Sessions", total_sessions)
    m2.metric("Completed", completed_session)
    m3.metric("Total Assignments", total_assignments)
    m4.metric("Released", assignment_released)
    m5.metric("Online", online_session)
    m6.metric("Recorded", recorded)

    # ----- Session Timeline -----
    today = date.today()
    sessions_df = None
    sessions_err = None
    try:
        sessions_df = load_course_sessions(selected_course)
    except Exception as e:
        sessions_err = str(e)

    section_title("Session Timeline", f"today: {today.strftime('%d %b %Y')}")

    if sessions_err or sessions_df is None or sessions_df.empty:
        if sessions_err:
            st.warning(
                f"⚠️ Couldn't load schedule for **{selected_course}**. "
                f"Most common causes: tab name doesn't exactly match the course name "
                f"(check spaces/case/underscores), or the sheet isn't shared with link access."
            )
            with st.expander("Show technical details"):
                st.code(sessions_err)
        else:
            st.info(
                f"No session rows found for **{selected_course}**. "
                f"Make sure the tab '{selected_course}' has **Date** and **Topic** columns with data."
            )
    else:
        prev_row  = sessions_df[sessions_df["Date"] < today].tail(1)
        today_row = sessions_df[sessions_df["Date"] == today].head(1)
        next_row  = sessions_df[sessions_df["Date"] > today].head(1)

        def card_html(label, df_row, today_card=False):
            cls = "session-card today" if today_card else "session-card"
            if df_row.empty:
                return (
                    f"<div class='{cls}'>"
                    f"<div class='label'>{label}</div>"
                    f"<div class='empty'>—</div></div>"
                )
            d = df_row.iloc[0]["Date"].strftime("%d %b %Y")
            t = df_row.iloc[0]["Topic"]
            return (
                f"<div class='{cls}'>"
                f"<div class='label'>{label}</div>"
                f"<div class='date'>{d}</div>"
                f"<div class='topic'>{t}</div></div>"
            )

        if not today_row.empty:
            sc1, sc2, sc3 = st.columns(3)
            sc1.markdown(card_html("◀ Previous Session", prev_row), unsafe_allow_html=True)
            sc2.markdown(card_html("● Today's Session", today_row, today_card=True), unsafe_allow_html=True)
            sc3.markdown(card_html("Next Session ▶", next_row), unsafe_allow_html=True)
        else:
            sc1, sc2 = st.columns(2)
            sc1.markdown(card_html("◀ Previous Session", prev_row), unsafe_allow_html=True)
            sc2.markdown(card_html("Next Session ▶", next_row), unsafe_allow_html=True)

    # ----- Progress donuts -----
    def safe_ratio(done, total):
        try:
            d, t = float(done), float(total)
            if t > 0:
                return min(max(d / t, 0.0), 1.0)
        except (ValueError, TypeError):
            pass
        return None

    def donut(ratio, title):
        pct = ratio * 100
        fig = go.Figure(
            data=[
                go.Pie(
                    values=[pct, 100 - pct],
                    labels=["Completed", "Remaining"],
                    hole=0.65,
                    marker=dict(colors=["#0B5394", "#cfe2f3"], line=dict(color="#ffffff", width=2)),
                    textinfo="none",
                    hovertemplate="%{label}: %{value:.0f}%<extra></extra>",
                    sort=False,
                    direction="clockwise",
                )
            ]
        )
        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor="center",
                       font=dict(color="#0B5394", size=15)),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                        font=dict(size=11)),
            annotations=[
                dict(text=f"<b>{pct:.0f}%</b>", x=0.5, y=0.5,
                     font=dict(size=22, color="#073763"), showarrow=False)
            ],
            margin=dict(t=40, b=10, l=10, r=10),
            height=240,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    section_title("Progress")
    sess_ratio = safe_ratio(completed_session, total_sessions)
    asgn_ratio = safe_ratio(assignment_released, total_assignments)

    p1, p2 = st.columns(2)
    with p1:
        if sess_ratio is not None:
            st.plotly_chart(
                donut(sess_ratio, f"Sessions ({completed_session}/{total_sessions})"),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.info("Sessions: data not available")
    with p2:
        if asgn_ratio is not None:
            st.plotly_chart(
                donut(asgn_ratio, f"Assignments ({assignment_released}/{total_assignments})"),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.info("Assignments: data not available")

    with st.expander("🔍 Show raw row from dashboard"):
        st.dataframe(row.to_frame().T, use_container_width=True)


# ===============================================================
# SECTION 2 — COURSE REPOSITORY
# ===============================================================
def render_course_repository():
    st.markdown(
        "<h2 style='margin-bottom:0;'>📂 Course Repository</h2>"
        "<div style='color:#666; font-size:0.9rem; margin-bottom:14px;'>"
        "Pick a Topic and a Course to open the matching Google Drive folder.</div>",
        unsafe_allow_html=True,
    )

    try:
        repo = load_repository()
    except FileNotFoundError:
        st.error(
            f"Could not find the local fallback file '{LOCAL_REPO_FILE}'. "
            "Place it next to app5.py, or add a 'Handson Materials' tab to the Google Sheet."
        )
        return
    except Exception as e:
        st.error(f"Could not load Course Repository: {e}")
        return

    if repo.empty:
        st.warning("Repository is empty.")
        return

    # Selection panel
    st.markdown('<div class="selection-panel">', unsafe_allow_html=True)
    col_topic, col_course = st.columns(2)

    topics = sorted(repo["Topic"].unique().tolist())
    with col_topic:
        selected_topic = st.selectbox("📚 Topic", topics, key="repo_topic")

    available_courses = sorted(
        repo.loc[repo["Topic"] == selected_topic, "Course"].unique().tolist()
    )
    with col_course:
        selected_course_repo = st.selectbox("🎓 Course", available_courses, key="repo_course")
    st.markdown('</div>', unsafe_allow_html=True)

    match = repo[
        (repo["Topic"] == selected_topic) & (repo["Course"] == selected_course_repo)
    ]

    if match.empty:
        st.warning("No folder mapped for this Topic + Course combination.")
        return

    link = match.iloc[0]["Link"]

    # Result panel — centered card with the action button
    st.markdown(
        f"""
        <div class="panel-result">
            <div style='color:#0B5394; font-weight:700; font-size:1.0rem; margin-bottom:4px;'>
                📁 {selected_topic} — {selected_course_repo}
            </div>
            <div style='color:#666; font-size:0.85rem; margin-bottom:12px;'>
                Folder is ready to open in Google Drive.
            </div>
            <a class="open-folder-btn" href="{link}" target="_blank">🔗 Open Folder in Google Drive</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===============================================================
# SECTION 3 — REPORTS
# ===============================================================
def render_reports():
    st.markdown(
        "<h2 style='margin-bottom:0;'>📑 Reports</h2>"
        "<div style='color:#666; font-size:0.9rem; margin-bottom:14px;'>"
        "Pick a Batch and a Module to open the matching report.</div>",
        unsafe_allow_html=True,
    )

    try:
        reports = load_reports()
    except FileNotFoundError:
        st.error(
            f"Could not find the local fallback file '{LOCAL_REPORTS_FILE}'. "
            "Place it next to app5.py, or add a 'CAG Reports' tab to the Google Sheet."
        )
        return
    except Exception as e:
        st.error(f"Could not load Reports: {e}")
        return

    if reports.empty:
        st.warning("Reports dataset is empty.")
        return

    # Selection panel
    st.markdown('<div class="selection-panel">', unsafe_allow_html=True)
    col_batch, col_module = st.columns(2)

    batches = sorted(reports["Batch"].unique().tolist())
    with col_batch:
        selected_batch = st.selectbox("👥 Batch", batches, key="rep_batch")

    available_modules = sorted(
        reports.loc[reports["Batch"] == selected_batch, "Module"].unique().tolist()
    )
    with col_module:
        selected_module = st.selectbox("🧩 Module", available_modules, key="rep_module")
    st.markdown('</div>', unsafe_allow_html=True)

    match = reports[
        (reports["Batch"] == selected_batch) & (reports["Module"] == selected_module)
    ]

    if match.empty:
        st.warning("No report mapped for this Batch + Module combination.")
        return

    link = match.iloc[0]["Link"]

    # Result panel
    st.markdown(
        f"""
        <div class="panel-result">
            <div style='color:#0B5394; font-weight:700; font-size:1.0rem; margin-bottom:4px;'>
                📄 {selected_batch} — {selected_module}
            </div>
            <div style='color:#666; font-size:0.85rem; margin-bottom:12px;'>
                Report is ready to open in Google Drive.
            </div>
            <a class="open-folder-btn" href="{link}" target="_blank">🔗 Open Report in Google Drive</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===============================================================
# SECTION 4 — TASK TRACKER (placeholder)
# ===============================================================
def render_task_tracker():
    st.markdown(
        "<h2 style='margin-bottom:0;'>✅ Task Tracker</h2>"
        "<div style='color:#666; font-size:0.9rem; margin-bottom:14px;'>"
        "Track and manage training-related tasks here.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="task-placeholder">
            <div class="tp-icon">🚧</div>
            <div class="tp-title">Coming Soon</div>
            <div class="tp-desc">Task tracking features will be added here shortly.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===============================================================
# SIDEBAR — Today's sessions across all active courses
# ===============================================================
@st.cache_data(ttl=60)
def get_todays_sessions() -> list[dict]:
    today = date.today()
    out: list[dict] = []

    try:
        dashboard = load_dashboard()
    except Exception:
        return out

    course_col = next(
        (c for c in dashboard.columns if c.lower().strip() in ("course", "course name", "course_name")),
        None,
    )
    status_col = next(
        (c for c in dashboard.columns if c.lower().strip() == "status"),
        None,
    )
    if course_col is None:
        return out

    df = dashboard.copy()
    if status_col is not None:
        df = df[df[status_col].astype(str).str.strip().str.lower() == "active"]

    courses = (
        df[course_col]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda s: s != ""]
        .tolist()
    )

    for course in courses:
        try:
            sessions_df = load_course_sessions(course)
        except Exception:
            continue
        if sessions_df is None or sessions_df.empty:
            continue
        today_row = sessions_df[sessions_df["Date"] == today]
        if today_row.empty:
            continue
        out.append({
            "course": course,
            "date": today_row.iloc[0]["Date"],
            "topic": today_row.iloc[0]["Topic"],
        })

    return out


@st.cache_data(ttl=60)
def get_sessions_on(target_date: date) -> list[dict]:
    """
    Look across all ACTIVE courses (Dashboard tab) and return any sessions
    whose Date matches `target_date`. Each item: {course, date, topic}.
    """
    out: list[dict] = []

    try:
        dashboard = load_dashboard()
    except Exception:
        return out

    course_col = next(
        (c for c in dashboard.columns if c.lower().strip() in ("course", "course name", "course_name")),
        None,
    )
    status_col = next(
        (c for c in dashboard.columns if c.lower().strip() == "status"),
        None,
    )
    if course_col is None:
        return out

    df = dashboard.copy()
    if status_col is not None:
        df = df[df[status_col].astype(str).str.strip().str.lower() == "active"]

    courses = (
        df[course_col]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda s: s != ""]
        .tolist()
    )

    for course in courses:
        try:
            sessions_df = load_course_sessions(course)
        except Exception:
            continue
        if sessions_df is None or sessions_df.empty:
            continue
        match_row = sessions_df[sessions_df["Date"] == target_date]
        if match_row.empty:
            continue
        out.append({
            "course": course,
            "date": match_row.iloc[0]["Date"],
            "topic": match_row.iloc[0]["Topic"],
        })

    return out


def _session_card_html(course: str, date_str: str, topic: str) -> str:
    return (
        f"<div style='background:#ffffff; border:1px solid #cfe2f3; "
        f"border-left:4px solid #0B5394; border-radius:8px; "
        f"padding:10px 12px; margin-bottom:8px; "
        f"box-shadow:0 1px 3px rgba(11,83,148,0.05);'>"
        f"<div style='color:#0B5394; font-weight:700; font-size:0.92rem;'>"
        f"📘 {topic}</div>"
        f"<div style='color:#073763; font-size:0.80rem; margin-top:4px;'>"
        f"👥 {course}</div>"
        f"<div style='color:#666; font-size:0.76rem; margin-top:3px;'>"
        f"🗓️ {date_str}</div>"
        f"</div>"
    )


def render_sidebar():
    today = date.today()
    with st.sidebar:
        # ---------- Today's Sessions (auto) ----------
        st.markdown(
            f"""
            <div class="sidebar-header">
                <div class="sh-title">📅  Today's Sessions</div>
                <div class="sh-date">{today.strftime('%A, %d %b %Y')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sessions = get_todays_sessions()

        if not sessions:
            st.markdown(
                "<div class='sidebar-empty'>No sessions scheduled for today.</div>",
                unsafe_allow_html=True,
            )
        else:
            for s in sessions:
                d = s["date"].strftime("%d %b %Y")
                st.markdown(
                    f"<div style='background:#ffffff; border:1px solid #cfe2f3; "
                    f"border-left:4px solid #0B5394; border-radius:8px; "
                    f"padding:10px 12px; margin-bottom:8px; "
                    f"box-shadow:0 1px 3px rgba(11,83,148,0.05);'>"
                    f"<div style='color:#0B5394; font-weight:700; font-size:0.92rem;'>"
                    f"{s['course']}</div>"
                    f"<div style='color:#073763; font-size:0.78rem; margin-top:3px;'>"
                    f"🗓️ {d}</div>"
                    f"<div style='color:#1f1f1f; font-size:0.86rem; margin-top:4px;'>"
                    f"📘 {s['topic']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        # ---------- Lookup by Date ----------
        st.markdown(
            "<div style='height:1px; background:#cfe2f3; margin:14px 0 12px 0;'></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sidebar-header" style="background: linear-gradient(135deg, #073763 0%, #0B5394 100%);">
                <div class="sh-title">🔎  Lookup by Date</div>
                <div class="sh-date">Pick any date to view sessions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        picked_date = st.date_input(
            "Select date",
            value=today,
            key="sidebar_date_picker",
            format="DD/MM/YYYY",
        )

        # Only run the heavy lookup when the user picks a non-today date,
        # otherwise reuse the today section (avoid duplicate cards).
        if picked_date == today:
            st.markdown(
                "<div class='sidebar-empty'>Showing today's sessions above. "
                "Pick a different date to look up.</div>",
                unsafe_allow_html=True,
            )
        else:
            picked_sessions = get_sessions_on(picked_date)
            d_str = picked_date.strftime("%d %b %Y")

            if not picked_sessions:
                st.markdown(
                    f"<div class='sidebar-empty'>No sessions found on {d_str}.</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div style='color:#0B5394; font-weight:700; font-size:0.85rem; "
                    f"margin:4px 0 8px 0;'>📌 {len(picked_sessions)} session"
                    f"{'s' if len(picked_sessions) != 1 else ''} on {d_str}</div>",
                    unsafe_allow_html=True,
                )
                for s in picked_sessions:
                    st.markdown(
                        _session_card_html(
                            course=s["course"],
                            date_str=s["date"].strftime("%d %b %Y"),
                            topic=s["topic"],
                        ),
                        unsafe_allow_html=True,
                    )


# ===============================================================
# HOME PAGE — welcome hero only
# ===============================================================
def render_home():
    st.markdown(
        """
        <div class="home-hero">
            <h2>👋 Welcome to the Training Activity Portal</h2>
            <p>Use the navigation above to access Dashboard, Repository, Reports, or Task Update.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------
# Sidebar (visible on every page)
# ---------------------------------------------------------------
render_sidebar()

# ---------------------------------------------------------------
# Route
# ---------------------------------------------------------------
if st.session_state.section == "schedule":
    render_course_schedule()
elif st.session_state.section == "repository":
    render_course_repository()
elif st.session_state.section == "reports":
    render_reports()
elif st.session_state.section == "tasks":
    render_task_tracker()
else:
    render_home()
