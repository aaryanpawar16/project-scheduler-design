import streamlit as st
import pandas as pd
import os
import io
import re
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

from src.similarity import find_similar_projects
from src.retrieval import get_schedule_context
from src.llm_agent import generate_schedule, refine_schedule

# --- UI Config ---
st.set_page_config(page_title="Intelligent Schedule Designer", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .main .block-container { max-height: 100vh; overflow-y: auto; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4259; }
    .chat-bubble { padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #3e4259; color: white; }
    .user-msg { background-color: #262730; }
    .ai-msg { background-color: #0e1117; border-left: 5px solid #4dabf7; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Project Schedule Designer")

if "history" not in st.session_state: st.session_state.history = []
if "messages" not in st.session_state: st.session_state.messages = []
if "current_schedule" not in st.session_state: st.session_state.current_schedule = None
if "initial_markdown" not in st.session_state: st.session_state.initial_markdown = None
if "similar_data" not in st.session_state: st.session_state.similar_data = None

@st.cache_data
def load_data():
    try:
        m = pd.read_csv("data/Project_JOB_meta_data.csv")
        s = pd.read_csv("data/Project_Schedule_Data.csv")
        return m, s
    except: return None, None

meta_df, schedule_df = load_data()

# 🛡️ Safe UI cleaning: Only hide the actual raw data tags
def clean_ui_text(raw_text):
    # Cut ONLY at the hidden data tag
    text = raw_text.split('<CSV_START>')[0].strip()
    # Remove any residual labels that LLM might add at the very end
    text = re.sub(r'(Updated CSV|Data Block|Final CSV).*$', '', text, flags=re.IGNORECASE | re.DOTALL).strip()
    return text

# --- Sidebar ---
st.sidebar.header("Input Parameters")
if meta_df is not None:
    with st.sidebar.form("input_form"):
        region = st.selectbox("Region", meta_df['REGION_NAME'].dropna().unique())
        market = st.selectbox("Market", meta_df['CORE_MARKET'].dropna().unique())
        ptype = st.selectbox("Type", meta_df['PROJECT_TYPE'].dropna().unique())
        estimate = st.number_input("Estimate ($)", min_value=0, value=5000000)
        size = st.number_input("Size (Sq Ft)", min_value=0, value=25000)
        submit = st.form_submit_button("Generate")

    if submit:
        with st.spinner("Finding matches..."):
            new_p = {"REGION_NAME": region, "CORE_MARKET": market, "PROJECT_TYPE": ptype, "TOTAL_CONTROL_ESTIMATE": estimate, "BUILDING_SIZE": size}
            sims = find_similar_projects(new_p, meta_df, top_k=3)
            st.session_state.similar_data = sims
            ids = [p["id"] for p in sims]
            context = get_schedule_context(ids, schedule_df)
            gen = generate_schedule(new_p, context)
            
            st.session_state.current_schedule = gen
            st.session_state.initial_markdown = clean_ui_text(gen)
            st.session_state.history = [gen]
            st.session_state.messages = []
            st.rerun()

    if st.session_state.current_schedule:
        st.sidebar.divider()
        st.sidebar.subheader("⛈️ Weather Simulation")
        delay_days = st.sidebar.slider("Delay (Days)", 1, 30, 7)
        if st.sidebar.button("Simulate Impact"):
            with st.spinner("Processing weather delay..."):
                instr = f"SIMULATE WEATHER DELAY: Apply a {delay_days} day delay to all outdoor tasks and ripple dependencies."
                res = refine_schedule(st.session_state.current_schedule, instr)
                st.session_state.messages.append({"role": "user", "content": f"Simulated {delay_days}d delay."})
                st.session_state.messages.append({"role": "assistant", "content": clean_ui_text(res)})
                st.session_state.current_schedule = res
                st.session_state.history.append(res)
                st.rerun()

# --- Main Logic ---
if st.session_state.current_schedule:
    # 🧪 Brute Force Header Seeker for Charts
    csv_raw = ""
    match = re.search(r'<CSV_START>(.*?)(?:<CSV_END>|$)', st.session_state.current_schedule, re.DOTALL)
    content = match.group(1).strip() if match else st.session_state.current_schedule

    df_plot = pd.DataFrame()
    if "Task,Phase,Start_Day" in content:
        try:
            h_idx = content.find("Task,Phase,Start_Day")
            df_plot = pd.read_csv(io.StringIO(content[h_idx:]), on_bad_lines='skip')
            df_plot.columns = [c.strip() for c in df_plot.columns]
            for col in ['Start_Day', 'Duration', 'Cost', 'Labor']:
                if col in df_plot.columns:
                    df_plot[col] = pd.to_numeric(df_plot[col].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce').fillna(0)
        except: pass

    # --- Section: Metrics ---
    if not df_plot.empty:
        st.subheader("📊 Executive Overview")
        m1, m2, m3, m4 = st.columns(4)
        total_days = int(df_plot['Start_Day'].max() + df_plot['Duration'].max()) if 'Start_Day' in df_plot.columns else 0
        m1.metric("Duration", f"{total_days} Days")
        m2.metric("Total Cost", f"${df_plot['Cost'].sum():,.0f}")
        m3.metric("Peak Labor Phase", df_plot.groupby('Phase')['Labor'].sum().idxmax() if 'Phase' in df_plot.columns else "N/A")
        m4.metric("Risk Level", "Medium" if total_days > 365 else "Low")
        st.divider()

    # --- Section: Similarity ---
    if st.session_state.similar_data:
        st.subheader("🔍 Similarity Detection Logs")
        cols = st.columns(3)
        for i, p in enumerate(st.session_state.similar_data):
            with cols[i]:
                st.write(f"**Project ID:** `{p['id']}`")
                st.write(f"Match Score: {p['score']}%")
                st.progress(p['score'] / 100.0)
        st.divider()

    # --- Charts ---
    if not df_plot.empty and 'Task' in df_plot.columns:
        cmap = {'Pre-Construction': '#4dabf7', 'Substructure': '#51cf66', 'Superstructure': '#fcc419', 'MEP/Finishes': '#ff922b', 'Closeout': '#ff6b6b'}
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📅 Live Schedule")
            show_crit = st.toggle("Highlight Critical Path")
            fig = go.Figure()
            for _, r in df_plot.iterrows():
                is_crit = str(r.get('Critical', 'No')).lower() == 'yes'
                line = dict(color='red', width=2) if (show_crit and is_crit) else dict(color='white', width=0.5)
                fig.add_trace(go.Bar(name=r.get('Phase'), y=[r.get('Task')], x=[r.get('Duration')], base=r.get('Start_Day', 0), orientation='h', marker=dict(color=cmap.get(r.get('Phase'), '#adb5bd'), line=line), showlegend=False))
            fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0), yaxis=dict(autorange="reversed"), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("💰 Financial Allocation")
            if 'Phase' in df_plot.columns:
                fig_p = px.pie(df_plot.groupby('Phase')['Cost'].sum().reset_index(), values='Cost', names='Phase', hole=.4, color='Phase', color_discrete_map=cmap)
                fig_p.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
                st.plotly_chart(fig_p, use_container_width=True)
        st.divider()

    # --- Details ---
    st.subheader("📝 Project Details")
    st.markdown(st.session_state.initial_markdown)
    st.divider()

    # --- Assistant ---
    st.subheader("🤖 Assistant")
    for m in st.session_state.messages:
        role = "user-msg" if m["role"] == "user" else "ai-msg"
        st.markdown(f'<div class="chat-bubble {role}"><b>{"👤 You" if m["role"] == "user" else "🤖 Assistant"}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)

    user_q = st.chat_input("Ask for modifications...")
    if user_q:
        with st.spinner("Processing..."):
            res = refine_schedule(st.session_state.current_schedule, user_q)
            st.session_state.messages.append({"role": "user", "content": user_q})
            st.session_state.messages.append({"role": "assistant", "content": clean_ui_text(res)})
            st.session_state.current_schedule = res
            st.session_state.history.append(res)
            st.rerun()

    if st.button("⏪ Undo"):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()
            if len(st.session_state.messages) >= 2: st.session_state.messages = st.session_state.messages[:-2]
            st.session_state.current_schedule = st.session_state.history[-1]
            st.rerun()

    st.download_button("⬇️ Export Report", st.session_state.current_schedule, "report.md")