"""
Training Activity Portal — Streamlit
3 sections selected via buttons at the top:
  1) Course Schedule      (existing dashboard)
  2) Course Repository    (Topic + Course → Drive folder)
  3) Reports              (Batch + Module → Drive link)

Run with: streamlit run app2.py
"""

from datetime import datetime
import base64
from pathlib import Path
import streamlit as st
import pandas as pd

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
b1, b2, b3, b4, _spacer = st.columns([1.4, 1.4, 1.4, 1.4, 2.6])
with b1:
    st.button(
        "📈  Dashbboard",
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

    def safe_ratio(done, total):
        try:
            d, t = float(done), float(total)
            if t > 0:
                return min(max(d / t, 0.0), 1.0)
        except (ValueError, TypeError):
            pass
        return None

    st.divider()
    st.subheader("Progress")

    sess_ratio = safe_ratio(completed_session, total_sessions)
    if sess_ratio is not None:
        st.write(f"Sessions: {completed_session} / {total_sessions}  ({sess_ratio*100:.0f}%)")
        st.progress(sess_ratio)
    else:
        st.write("Sessions: data not available")

    asgn_ratio = safe_ratio(assignment_released, total_assignments)
    if asgn_ratio is not None:
        st.write(f"Assignments Released: {assignment_released} / {total_assignments}  ({asgn_ratio*100:.0f}%)")
        st.progress(asgn_ratio)
    else:
        st.write("Assignments: data not available")

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
    # Home / landing — only the section buttons above are visible.
    st.markdown(
        """<div style='text-align:center; color:#0B5394; padding:3rem 1rem;'>
<h3>👋 Welcome to the Training Activity Portal</h3>
<p>Select <b>Course Schedule</b>, <b>Course Repository</b>, <b>Reports</b>, or <b>Task Tracker</b> above to get started.</p>
</div>""",
        unsafe_allow_html=True,
    )
