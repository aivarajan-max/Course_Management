"""
Training Activity Portal — Streamlit
3 sections selected via buttons at the top:
  1) Course Schedule      (existing dashboard)
  2) Course Repository    (Topic + Course → Drive folder)
  3) Reports              (Batch + Module → Drive link)

Run with: streamlit run app2.py
"""

from datetime import datetime, date
import base64
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Training Activity Portal", page_icon="📊", layout="wide")

# ---------------------------------------------------------------
# Blue & white theme
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #ffffff; }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px;
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

    div[data-baseweb="select"] {
        max-width: 320px;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #0B5394 !important;
        border-radius: 6px !important;
        min-height: 36px !important;
    }

    label {
        color: #0B5394 !important;
        font-weight: 600 !important;
        margin-bottom: 0.1rem !important;
    }

    .stButton > button {
        background-color: #0B5394;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #073763;
        color: #ffffff;
    }

    div[data-testid="stMetric"] {
        background-color: #eaf2fb;
        border: 1px solid #cfe2f3;
        border-radius: 8px;
        padding: 8px 12px;
    }
    div[data-testid="stMetricLabel"] {
        color: #0B5394 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #073763 !important;
    }

    div[data-testid="stProgress"] > div > div > div > div {
        background-color: #0B5394 !important;
    }

    div[data-testid="column"] {
        padding: 0 0.4rem !important;
    }

    /* Session info cards (Previous / Today / Next) */
    .session-card {
        background-color: #eaf2fb;
        border: 1px solid #cfe2f3;
        border-left: 4px solid #0B5394;
        border-radius: 8px;
        padding: 10px 14px;
        height: 100%;
    }
    .session-card.today {
        border-left-color: #c27c0e;
        background-color: #fff7e6;
        border-color: #f5d9a8;
    }
    .session-card .label {
        color: #0B5394;
        font-weight: 700;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 4px;
    }
    .session-card.today .label { color: #b06d0a; }
    .session-card .date {
        color: #073763;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 2px;
    }
    .session-card .topic {
        color: #1f1f1f;
        font-size: 0.92rem;
        line-height: 1.3;
    }
    .session-card .empty {
        color: #888;
        font-style: italic;
        font-size: 0.9rem;
    }

    a.open-folder-btn {
        display: inline-block;
        background-color: #0B5394;
        color: #ffffff !important;
        padding: 10px 22px;
        border-radius: 6px;
        font-weight: 600;
        text-decoration: none;
        margin-top: 0.6rem;
    }
    a.open-folder-btn:hover {
        background-color: #073763;
        color: #ffffff !important;
    }
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
REPORTS_TAB = "CAG Reports"  # tab name to try in the Google Sheet for Reports

# Local fallback files (used if the corresponding tab isn't in the Google Sheet)
LOCAL_REPO_FILE = "Course_Materials-Repository.xlsx"
LOCAL_REPO_SHEET = "Handson Materials"

LOCAL_REPORTS_FILE = "CAG-Reports.xlsx"
LOCAL_REPORTS_SHEET = "Sheet1"

# Logo for the home page (place gitaa-logo.png next to app2.py)
LOGO_FILE = "gitaa-logo.png"

# ---------------------------------------------------------------
# Section state
# ---------------------------------------------------------------
if "section" not in st.session_state:
    st.session_state.section = "home"

def set_section(name: str):
    st.session_state.section = name

# ---------------------------------------------------------------
# Top bar — title + refresh
# ---------------------------------------------------------------
title_col, refresh_col = st.columns([6, 1])
with title_col:
    st.title("📊 Training Activity Portal")
with refresh_col:
    st.write("")
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Section selector buttons
b0, b1, b2, b3, b4, _spacer = st.columns([1.2, 1.4, 1.4, 1.4, 1.4, 1.2])
with b0:
    st.button(
        "🏠 Home",
        use_container_width=True,
        on_click=set_section,
        args=("home",),
        type="primary" if st.session_state.section == "home" else "secondary",
    )
with b1:
    st.button(
        "📈  Dashboard",
        use_container_width=True,
        on_click=set_section,
        args=("schedule",),
        type="primary" if st.session_state.section == "schedule" else "secondary",
    )
with b2:
    st.button(
        "📂 Repository",
        use_container_width=True,
        on_click=set_section,
        args=("repository",),
        type="primary" if st.session_state.section == "repository" else "secondary",
    )
with b3:
    st.button(
        "📑 Reports",
        use_container_width=True,
        on_click=set_section,
        args=("reports",),
        type="primary" if st.session_state.section == "reports" else "secondary",
    )
with b4:
    st.button(
        "✅ Task Update",
        use_container_width=True,
        on_click=set_section,
        args=("tasks",),
        type="primary" if st.session_state.section == "tasks" else "secondary",
    )

st.divider()

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
    """Read the local logo file and return a base64 string for inline <img>."""
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
    """Load a per-course tab (named exactly like the course) with Date + Topic columns.
    Tolerates an extra title/banner row above the real headers, and accepts columns
    in any order. Returns a DataFrame with 'Date' (datetime.date) and 'Topic' (str).
    """
    import io, requests

    # Fetch raw CSV so we can scan for the real header row.
    resp = requests.get(csv_url(SHEET_ID, course_tab), timeout=15)
    resp.raise_for_status()
    raw = resp.text
    if not raw.strip():
        raise ValueError(f"Tab '{course_tab}' appears to be empty or does not exist.")

    # Read everything as strings, no header, then locate the row that contains
    # both a 'topic' and a 'date' cell.
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
        # Fall back: try first row as header (original behavior) so we surface a useful error.
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

    # Try US format first (matches the M/D/YYYY style in the sheet), then fall back to dayfirst.
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
    """Topic/Course/Link table for Course Repository, with forward-filled Topic."""
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
    """Batch/Module/Link table for the Reports section."""
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

    # Forward-fill Batch in case of merged cells
    df["Batch"] = df["Batch"].astype("object").where(df["Batch"].notna(), None)
    df["Batch"] = df["Batch"].ffill()

    for c in ["Batch", "Module", "Link"]:
        df[c] = df[c].astype(str).str.strip()

    df = df[df["Link"].str.startswith("http")]
    df = df[(df["Batch"] != "") & (df["Module"] != "") & (df["Batch"].str.lower() != "nan")]

    return df.reset_index(drop=True)


# ===============================================================
# SECTION 1 — COURSE SCHEDULE
# ===============================================================
def render_course_schedule():
    st.header("📋 Course Schedule")

    try:
        dashboard = load_dashboard()
    except Exception as e:
        st.error(f"Could not load dashboard tab '{DASHBOARD_TAB}': {e}")
        st.info("If your dashboard tab has a different name, edit DASHBOARD_TAB at the top of app2.py.")
        return

    st.caption(
        f"Last fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  •  "
        "Click 🔄 Refresh to pull the latest from Google Sheets"
    )

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

    dd_col, _ = st.columns([2, 5])
    with dd_col:
        selected_course = st.selectbox("📂 Course Name", courses, key="sched_course")

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

    st.divider()
    st.subheader(f"📘 {selected_course}")

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"**Coordinator**  \n{coordinator}")
    c2.markdown(f"**Starting Date**  \n{starting_date}")
    c3.markdown(f"**Ending Date**  \n{ending_date}")

    status_str = str(status).strip()
    color = {"active": "🟢", "yet to start": "🟡", "completed": "🔵"}.get(status_str.lower(), "⚪")
    c4.markdown(f"**Status**  \n{color} {status_str if status_str and status_str != '—' else '—'}")

    st.divider()

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Sessions", total_sessions)
    m2.metric("Completed", completed_session)
    m3.metric("Total Assignments", total_assignments)
    m4.metric("Released", assignment_released)
    m5.metric("Online", online_session)
    m6.metric("Recorded", recorded)

    # ---- Previous / Today / Next session (from per-course tab) ----
    st.divider()
    today = date.today()
    sessions_df = None
    sessions_err = None
    try:
        sessions_df = load_course_sessions(selected_course)
    except Exception as e:
        sessions_err = str(e)

    st.markdown(
        f"<div style='color:#0B5394; font-weight:600; margin-bottom:6px;'>"
        f"🗓️ Session Timeline <span style='color:#666; font-weight:400; font-size:0.85rem;'>"
        f"(today: {today.strftime('%d %b %Y')})</span></div>",
        unsafe_allow_html=True,
    )

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
            sc1.markdown(card_html("Previous Session", prev_row), unsafe_allow_html=True)
            sc2.markdown(card_html("Today's Session", today_row, today_card=True), unsafe_allow_html=True)
            sc3.markdown(card_html("Next Session", next_row), unsafe_allow_html=True)
        else:
            sc1, sc2 = st.columns(2)
            sc1.markdown(card_html("Previous Session", prev_row), unsafe_allow_html=True)
            sc2.markdown(card_html("Next Session", next_row), unsafe_allow_html=True)

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

    # ---- Progress (donut charts) ----
    st.markdown(
        "<div style='color:#0B5394; font-weight:600; margin-top:14px; margin-bottom:2px;'>📊 Progress</div>",
        unsafe_allow_html=True,
    )

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
    st.header("📂 Course Repository")
    st.caption("Pick a Topic and a Course to open the matching Google Drive folder.")

    try:
        repo = load_repository()
    except FileNotFoundError:
        st.error(
            f"Could not find the local fallback file '{LOCAL_REPO_FILE}'. "
            "Place it next to app2.py, or add a 'Handson Materials' tab to the Google Sheet."
        )
        return
    except Exception as e:
        st.error(f"Could not load Course Repository: {e}")
        return

    if repo.empty:
        st.warning("Repository is empty.")
        return

    # Topic on the LEFT, Course on the RIGHT
    col_topic, col_course = st.columns(2)

    topics = sorted(repo["Topic"].unique().tolist())
    with col_topic:
        selected_topic = st.selectbox("📚 Topic", topics, key="repo_topic")

    available_courses = sorted(
        repo.loc[repo["Topic"] == selected_topic, "Course"].unique().tolist()
    )
    with col_course:
        selected_course_repo = st.selectbox("🎓 Course", available_courses, key="repo_course")

    match = repo[
        (repo["Topic"] == selected_topic) & (repo["Course"] == selected_course_repo)
    ]

    st.divider()

    if match.empty:
        st.warning("No folder mapped for this Topic + Course combination.")
        return

    link = match.iloc[0]["Link"]

    # Only the link button is shown — no headings, no caption, no expander
    st.markdown(
        f'<a class="open-folder-btn" href="{link}" target="_blank">🔗 Open Folder in Google Drive</a>',
        unsafe_allow_html=True,
    )


# ===============================================================
# SECTION 3 — REPORTS
# ===============================================================
def render_reports():
    st.header("📑 Reports")
    st.caption("Pick a Batch and a Module to open the matching report.")

    try:
        reports = load_reports()
    except FileNotFoundError:
        st.error(
            f"Could not find the local fallback file '{LOCAL_REPORTS_FILE}'. "
            "Place it next to app2.py, or add a 'CAG Reports' tab to the Google Sheet."
        )
        return
    except Exception as e:
        st.error(f"Could not load Reports: {e}")
        return

    if reports.empty:
        st.warning("Reports dataset is empty.")
        return

    # Batch on the LEFT, Module on the RIGHT
    col_batch, col_module = st.columns(2)

    batches = sorted(reports["Batch"].unique().tolist())
    with col_batch:
        selected_batch = st.selectbox("👥 Batch", batches, key="rep_batch")

    available_modules = sorted(
        reports.loc[reports["Batch"] == selected_batch, "Module"].unique().tolist()
    )
    with col_module:
        selected_module = st.selectbox("🧩 Module", available_modules, key="rep_module")

    match = reports[
        (reports["Batch"] == selected_batch) & (reports["Module"] == selected_module)
    ]

    st.divider()

    if match.empty:
        st.warning("No report mapped for this Batch + Module combination.")
        return

    link = match.iloc[0]["Link"]

    # Only the link button is shown
    st.markdown(
        f'<a class="open-folder-btn" href="{link}" target="_blank">🔗 Open Report in Google Drive</a>',
        unsafe_allow_html=True,
    )


# ===============================================================
# SECTION 4 — TASK TRACKER (placeholder)
# ===============================================================
def render_task_tracker():
    st.header("✅ Task Tracker")
    st.caption("Track and manage training-related tasks here.")

    st.info("🚧 This section is under construction. Task tracking features will be added soon.")


# ===============================================================
# SIDEBAR — Today's sessions across all active courses
# ===============================================================
@st.cache_data(ttl=60)
def get_todays_sessions() -> list[dict]:
    """Return [{course, date, topic}, ...] for active courses that have a
    session scheduled on today's date. Reads the Dashboard tab to find the
    list of active courses, then loads each per-course tab to look up
    today's topic. Errors on individual course tabs are silently skipped
    so the sidebar still renders for the rest.
    """
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


def render_sidebar():
    """Sidebar showing today's sessions across all active courses."""
    today = date.today()
    with st.sidebar:
        st.markdown(
            f"<div style='color:#0B5394; font-weight:700; font-size:1.05rem; margin-bottom:2px;'>"
            f"📅 Today's Sessions</div>"
            f"<div style='color:#666; font-size:0.82rem; margin-bottom:10px;'>"
            f"{today.strftime('%A, %d %b %Y')}</div>",
            unsafe_allow_html=True,
        )

        sessions = get_todays_sessions()

        if not sessions:
            st.markdown(
                "<div style='color:#888; font-style:italic; font-size:0.9rem;'>"
                "No sessions scheduled for today.</div>",
                unsafe_allow_html=True,
            )
            return

        # Simple list: course name + date + topic
        for s in sessions:
            d = s["date"].strftime("%d %b %Y")
            st.markdown(
                f"<div style='background:#eaf2fb; border:1px solid #cfe2f3; "
                f"border-left:4px solid #0B5394; border-radius:6px; "
                f"padding:8px 10px; margin-bottom:8px;'>"
                f"<div style='color:#0B5394; font-weight:700; font-size:0.92rem;'>"
                f"{s['course']}</div>"
                f"<div style='color:#073763; font-size:0.82rem; margin-top:2px;'>"
                f"🗓️ {d}</div>"
                f"<div style='color:#1f1f1f; font-size:0.88rem; margin-top:2px;'>"
                f"📘 {s['topic']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )


# ===============================================================
# HOME PAGE — welcome + 4 quick-jump dropdowns
# ===============================================================
def render_home():
    st.markdown(
        """<div style='text-align:center; color:#0B5394; padding:1.5rem 1rem 0.5rem 1rem;'>
<h2 style='margin-bottom:0.3rem;'>👋 Welcome to the Training Activity Portal</h2>
<p style='color:#444; margin-top:0;'>Use the quick filters below or pick a section above to get started.</p>
</div>""",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        "<div style='color:#0B5394; font-weight:600; margin-bottom:6px;'>"
        "🔎 Quick Jump</div>",
        unsafe_allow_html=True,
    )

    # Pre-load data for the dropdowns; tolerate failures so the home page still renders.
    courses: list[str] = []
    repo_topics: list[str] = []
    batches: list[str] = []
    modules: list[str] = []

    try:
        dashboard = load_dashboard()
        course_col = next(
            (c for c in dashboard.columns if c.lower().strip() in ("course", "course name", "course_name")),
            None,
        )
        if course_col is not None:
            courses = (
                dashboard[course_col]
                .dropna().astype(str).str.strip()
                .loc[lambda s: s != ""].tolist()
            )
    except Exception:
        pass

    try:
        repo = load_repository()
        if not repo.empty:
            repo_topics = sorted(repo["Topic"].unique().tolist())
    except Exception:
        pass

    try:
        reports = load_reports()
        if not reports.empty:
            batches = sorted(reports["Batch"].unique().tolist())
            modules = sorted(reports["Module"].unique().tolist())
    except Exception:
        pass

    # 4 dropdowns in a row: Course, Topic, Batch, Module
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.selectbox(
            "📂 Course",
            ["— Select —"] + courses,
            key="home_course",
        )
    with d2:
        st.selectbox(
            "📚 Topic",
            ["— Select —"] + repo_topics,
            key="home_topic",
        )
    with d3:
        st.selectbox(
            "👥 Batch",
            ["— Select —"] + batches,
            key="home_batch",
        )
    with d4:
        st.selectbox(
            "🧩 Module",
            ["— Select —"] + modules,
            key="home_module",
        )

    st.write("")

    # Quick-jump action buttons
    j1, j2, j3, j4 = st.columns(4)
    with j1:
        if st.button("Go to Dashboard →", key="jump_dash", use_container_width=True):
            sel = st.session_state.get("home_course", "— Select —")
            if sel and sel != "— Select —":
                st.session_state["sched_course"] = sel
            st.session_state.section = "schedule"
            st.rerun()
    with j2:
        if st.button("Go to Repository →", key="jump_repo", use_container_width=True):
            sel = st.session_state.get("home_topic", "— Select —")
            if sel and sel != "— Select —":
                st.session_state["repo_topic"] = sel
            st.session_state.section = "repository"
            st.rerun()
    with j3:
        if st.button("Go to Reports →", key="jump_rep_b", use_container_width=True):
            sel = st.session_state.get("home_batch", "— Select —")
            if sel and sel != "— Select —":
                st.session_state["rep_batch"] = sel
            st.session_state.section = "reports"
            st.rerun()
    with j4:
        if st.button("Go to Reports →", key="jump_rep_m", use_container_width=True):
            sel = st.session_state.get("home_module", "— Select —")
            if sel and sel != "— Select —":
                st.session_state["rep_module"] = sel
            st.session_state.section = "reports"
            st.rerun()


# ---------------------------------------------------------------
# Sidebar (visible on every page) — today's sessions
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
