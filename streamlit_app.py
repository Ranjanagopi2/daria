import os
import sys
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Ensure root directory is in python path for Streamlit Cloud deployment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"

from graph.graph import graph
from graph.state import create_initial_state
from export.docx_exporter import export_report

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="D.A.R.I.A. Engine",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom CSS — Matching Sample Image Theme & Styling
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');

/* ── Base Theme & Background ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #FAF9F6 !important;
    color: #111827;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1050px !important;
}

/* ── Page Header ── */
.page-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 1.25rem;
}
.page-header-icon {
    width: 46px; height: 46px;
    background: #FCE8E6;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.page-header-text h1 {
    font-family: 'Inter', sans-serif;
    font-size: 24px; font-weight: 700;
    color: #111827; margin: 0 0 2px 0;
    letter-spacing: -0.01em;
}
.page-header-text p {
    font-size: 11px; color: #8E24AA; margin: 0;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Header Card Placeholder (matching sample top bar) ── */
.header-placeholder-box {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    height: 44px;
    margin-bottom: 1.5rem;
}

/* ── Query Box & Input ── */
.query-label {
    font-size: 13px; font-weight: 500; color: #374151;
    margin-bottom: 8px;
}
[data-testid="stTextArea"] textarea {
    background-color: #F3F4F6 !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 14px 16px !important;
}

/* ── Run Button (Left-aligned fit-content button like sample) ── */
.stButton > button {
    background: #0B61A4 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    padding: 10px 22px !important;
    width: auto !important;
    min-width: 190px !important;
    margin-top: 6px !important;
}
.stButton > button:hover {
    background: #084C82 !important;
}

/* ── Pipeline Strip (Mint Green Pills matching sample image) ── */
.pipeline-strip {
    display: flex;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 14px 20px;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    gap: 10px;
    flex-wrap: wrap;
}
.pipe-node {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 500;
    color: #15803D;
    padding: 4px 10px;
    border-radius: 6px;
    background: #DCFCE7;
    white-space: nowrap;
}
.pipe-node.inactive {
    background: #F3F4F6; color: #9CA3AF;
}
.pipe-bullet {
    color: #CBD5E1; font-size: 14px; margin: 0 2px;
}

/* ── Metric Cards (Matching 4-card row in sample image) ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 16px 20px;
}
.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 18px; font-weight: 700; color: #111827;
}
.metric-value.accent-blue { color: #0284C7; }
.metric-value.accent-amber { color: #D97706; }
.metric-value.accent-green { color: #16A34A; }

/* ── Sidebar Styling ── */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E5E7EB !important;
}
[data-testid="stSidebar"] .sidebar-section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    color: #9CA3AF; text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 10px;
}
.agent-row {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #F3F4F6;
    font-size: 13px; color: #374151;
}
.agent-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #16A34A;
    flex-shrink: 0;
}
.agent-tag {
    margin-left: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #9CA3AF;
}

/* Checkbox accent & sidebar label visibility */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] .stCheckbox span,
[data-testid="stSidebar"] span {
    color: #111827 !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] input[type="password"],
[data-testid="stSidebar"] input[type="text"] {
    color: #111827 !important;
    background-color: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
}

[data-testid="stCheckbox"] input:checked + div {
    background-color: #E11D48 !important;
    border-color: #E11D48 !important;
}

/* ── Tab Styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 13px; font-weight: 500;
    border-radius: 7px;
    padding: 6px 14px;
    color: #6B7280;
}
.stTabs [aria-selected="true"] {
    background: #EBF1FD !important;
    color: #185FA5 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 24px;
    margin-top: 8px;
}

/* ── Section Headings inside tabs ── */
.section-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}
.section-title {
    font-size: 16px; font-weight: 600; color: #111827;
    margin-bottom: 16px;
}

/* ── Badges ── */
.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 500;
    padding: 2px 10px;
    border-radius: 6px;
}
.badge-blue  { background: #EBF1FD; color: #185FA5; }
.badge-green { background: #ECFDF5; color: #065F46; }
.badge-amber { background: #FFFBEB; color: #B45309; }
.badge-gray  { background: #F3F4F6; color: #4B5563; }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section-title">Research Engine</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-row">
        <div class="agent-dot"></div>
        RAG Agent
        <span class="agent-tag">local kb</span>
    </div>
    <div class="agent-row">
        <div class="agent-dot"></div>
        Web Agent
        <span class="agent-tag">live data</span>
    </div>
    <div class="agent-row">
        <div class="agent-dot"></div>
        Evidence Curator
        <span class="agent-tag">filter</span>
    </div>
    <div class="agent-row">
        <div class="agent-dot"></div>
        Research Critic
        <span class="agent-tag">verify</span>
    </div>
    <div class="agent-row" style="border-bottom:none;">
        <div class="agent-dot"></div>
        Summarizer
        <span class="agent-tag">output</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="sidebar-section-title">EXPORT</div>', unsafe_allow_html=True)
    export_docx = st.checkbox("Generate DOCX report", value=True)

    st.divider()

    st.markdown('<div class="sidebar-section-title">API CONFIGURATION</div>', unsafe_allow_html=True)
    gemini_key = st.text_input("GEMINI_API_KEY", value=os.getenv("GEMINI_API_KEY", ""), type="password")
    tavily_key = st.text_input("TAVILY_API_KEY", value=os.getenv("TAVILY_API_KEY", ""), type="password")
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key

    st.divider()

    st.markdown('<div class="sidebar-section-title" style="margin-bottom:8px;">SYSTEM PROFILE</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:12px; color:#4B5563; line-height:1.6;">'
        '<strong>D.A.R.I.A. Engine</strong><br>'
        '<span style="color:#6B7280; font-size:11px;">Domain-Specific Agentic Research, Intelligence & Analysis System</span>'
        '<br><br>'
        'Autonomous orchestration pipeline engineered on LangGraph. Featuring parallel multi-agent data harvest, '
        'evidence curation, iterative metric critique, and persistent semantic context updates.'
        '</p>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Page Header
# --------------------------------------------------

st.markdown("""
<div class="page-header">
    <div class="page-header-icon">🏎️</div>
    <div class="page-header-text">
        <h1>D.A.R.I.A.</h1>
        <p>Domain-Specific Agentic Research, Intelligence & Analysis System</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Rounded Header Container matching sample image top bar
st.markdown('<div class="header-placeholder-box"></div>', unsafe_allow_html=True)


# --------------------------------------------------
# Query Input
# --------------------------------------------------
st.markdown('<div class="query-label">Research query</div>', unsafe_allow_html=True)
query = st.text_area(
    label="query_input",
    label_visibility="collapsed",
    height=100,
    placeholder="Describe your research objective. Be specific — the analyst will decompose it into a structured plan.",
    key="query_input"
)
run_button = st.button("Run research pipeline →")


# --------------------------------------------------
# Pipeline Execution
# --------------------------------------------------
if run_button:
    if not query.strip():
        st.warning("Please enter a research query to continue.")
        st.stop()

    with st.spinner("Running pipeline..."):
        initial_state = create_initial_state(query=query)
        result_state = graph.invoke(initial_state)
        st.session_state["research_result"] = result_state


# --------------------------------------------------
# Pipeline Strip & Metric Display (Matching Sample)
# --------------------------------------------------
# Default display nodes (matching sample image mint green pills)
nodes = ["Memory Agent", "Information Analyst", "RAG Agent", "Web Agent",
         "Evidence Curator", "Research Critic", "Summarizer", "Memory Update"]

strip_html = '<div class="pipeline-strip">'
for i, n in enumerate(nodes):
    strip_html += f'<div class="pipe-node">{n}</div>'
    if i < len(nodes) - 1:
        strip_html += '<span class="pipe-bullet">·</span>'
strip_html += '</div>'
st.markdown(strip_html, unsafe_allow_html=True)


if "research_result" in st.session_state:
    result = st.session_state["research_result"]

    route = str(result.get("route", "HYBRID")).upper()
    critic_score = round(float(result.get("critic_score", 5.0)), 1)
    iterations = result.get("iteration_count", 2)
    memory_hit = result.get("memory_hit", True)

    score_color = "accent-green" if critic_score >= 7 else ("accent-amber" if critic_score >= 5 else "accent-blue")
    memory_label = "Hit" if memory_hit else "Miss"
    memory_color = "accent-green" if memory_hit else "accent-blue"

    # ── Metric cards row matching sample ──
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">ROUTE</div>
            <div class="metric-value accent-blue">{route}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">CRITIC SCORE</div>
            <div class="metric-value {score_color}">{critic_score} / 10</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">REFLECTION LOOPS</div>
            <div class="metric-value">{iterations}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MEMORY CACHE</div>
            <div class="metric-value {memory_color}">{memory_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "Report",
        "Trace & reflection",
        "Memory",
        "Sources"
    ])

    # ==========================================
    # Tab 1 — Report
    # ==========================================
    with tab1:
        st.markdown(result.get("final_response", "No report was generated."))

        st.divider()

        if export_docx:
            structured_summary = result.get("research_summary")
            if structured_summary:
                try:
                    report_path = export_report(state=result)
                    if os.path.exists(report_path):
                        with open(report_path, "rb") as f:
                            st.download_button(
                                label="Download DOCX report",
                                data=f,
                                file_name=os.path.basename(report_path),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=False
                            )
                    else:
                        st.error("Report file was not written to disk.")
                except Exception as e:
                    st.error(f"Export failed: {e}")
            else:
                st.info("No structured summary available to export.")

        with st.expander("Run metadata"):
            st.json({
                "route": result.get("route"),
                "iteration_count": result.get("iteration_count"),
                "critic_score": result.get("critic_score"),
                "confidence_score": result.get("confidence_score"),
                "discarded_evidence_count": result.get("discarded_evidence_count"),
            })

    # ==========================================
    # Tab 2 — Trace & Reflection
    # ==========================================
    with tab2:
        st.markdown('<div class="section-eyebrow">Planning</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Research plan</div>', unsafe_allow_html=True)

        route_badge_color = "badge-blue" if "rag" in route.lower() else "badge-amber" if "web" in route.lower() else "badge-gray"
        st.markdown(f'Route: <span class="badge {route_badge_color}">{route}</span>', unsafe_allow_html=True)

        plan_steps = result.get("research_plan", [])
        if plan_steps:
            for step in plan_steps:
                st.markdown(f"- {step}")
        else:
            st.caption("No plan steps recorded.")

        st.divider()

        st.markdown('<div class="section-eyebrow">Gaps</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Information gaps</div>', unsafe_allow_html=True)
        gaps = result.get("information_gaps", [])
        if gaps:
            for gap in gaps:
                st.markdown(f"- {gap}")
        else:
            st.success("No unresolved information gaps detected.")

        st.divider()

        st.markdown('<div class="section-eyebrow">Quality gate</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Critic evaluation</div>', unsafe_allow_html=True)

        col_score, col_spacer = st.columns([1, 3])
        with col_score:
            st.metric("Score", f"{critic_score} / 10")

        critic_text = result.get("critic_feedback", "No feedback recorded.")
        st.markdown(
            f'<div style="background:#FFFBEB; border-left:3px solid #D97706; padding:12px 16px; '
            f'border-radius:0 6px 6px 0; font-size:14px; color:#374151;">{critic_text}</div>',
            unsafe_allow_html=True
        )

        history = result.get("critic_history", [])
        if history:
            st.divider()
            st.markdown('<div class="section-eyebrow">History</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Reflection iterations</div>', unsafe_allow_html=True)
            for i, entry in enumerate(history, 1):
                with st.expander(f"Iteration {i} — score {entry.get('score', '?')}"):
                    st.write(entry.get("feedback", "—"))

    # ==========================================
    # Tab 3 — Memory
    # ==========================================
    with tab3:
        if memory_hit:
            st.markdown('<div class="section-eyebrow">Semantic match found</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Memory context</div>', unsafe_allow_html=True)

            if "memory_distance" in result:
                st.metric("Vector distance", round(float(result.get("memory_distance", 0.0)), 3))

            st.markdown(
                f'<div style="background:#F0FDF4; border:1px solid #BBF7D0; padding:14px 16px; '
                f'border-radius:8px; font-size:14px; color:#14532D;">'
                f'{result.get("memory_report", "No memory report.")}</div>',
                unsafe_allow_html=True
            )

            recs = result.get("memory_recommendations", [])
            if recs:
                st.divider()
                st.markdown('<div class="section-eyebrow">Recommendations</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">From prior research</div>', unsafe_allow_html=True)
                for item in recs:
                    st.markdown(f"- {item}")
        else:
            st.markdown(
                '<div style="padding:32px; text-align:center; color:#9CA3AF; font-size:14px;">'
                'No prior research found in memory for this query.'
                '</div>',
                unsafe_allow_html=True
            )

    # ==========================================
    # Tab 4 — Sources
    # ==========================================
    with tab4:
        st.markdown('<div class="section-eyebrow">Local knowledge base</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">RAG sources</div>', unsafe_allow_html=True)

        rag_data = result.get("rag_sources", [])
        if rag_data:
            rag_df = pd.DataFrame(rag_data)
            if not rag_df.empty:
                st.dataframe(rag_df, use_container_width=True, hide_index=True)
        else:
            st.caption("No local sources retrieved for this query.")

        st.divider()

        st.markdown('<div class="section-eyebrow">Live web retrieval</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Web sources</div>', unsafe_allow_html=True)

        web_data = result.get("web_sources", [])
        if web_data:
            web_df = pd.DataFrame(web_data)
            if not web_df.empty:
                st.dataframe(web_df, use_container_width=True, hide_index=True)
        else:
            st.caption("No web sources retrieved for this query.")
else:
    # Initial empty metric cards matching sample image when no research run yet
    st.markdown("""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">ROUTE</div>
            <div class="metric-value accent-blue">HYBRID</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">CRITIC SCORE</div>
            <div class="metric-value accent-amber">5.0 / 10</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">REFLECTION LOOPS</div>
            <div class="metric-value">2</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MEMORY CACHE</div>
            <div class="metric-value accent-green">Hit</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
