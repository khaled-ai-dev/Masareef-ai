import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Masareef | AI Financial Intelligence", page_icon="💠", layout="wide", initial_sidebar_state="collapsed")

FastAPI_URL = "http://127.0.0.1:8000"
Ollama_URL = "http://127.0.0.1:11434/api/generate"
n8n_Webhook_URL = "http://localhost:5678/webhook/61497b9d-7604-4e26-8619-b9ac32857a14"


with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:2.2rem;">💠</div>
        <div style="font-size:1.1rem; font-weight:700; color:#fff; letter-spacing:1px;">MASAREEF AI</div>
        <div style="font-size:0.65rem; color:#7b61ff; letter-spacing:2px; text-transform:uppercase; margin-top:2px;">v1.0 · Cairo, EG</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.08); margin:10px 0 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.75rem; color:#9a9db3; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px;">⚙️ System Status</div>', unsafe_allow_html=True)
    try:
        requests.get(f"{FastAPI_URL}/", timeout=3)
        st.success("FastAPI Backend")
    except Exception:
        st.error("FastAPI Backend")
    try:
        requests.get("http://127.0.0.1:11434", timeout=3)
        st.success("Ollama (Local AI)")
    except Exception:
        st.error("Ollama (Local AI)")
    st.info("n8n Agent Workflow")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem; color:#5a5d70; line-height:1.6;">
        Built with a 3-layer categorization engine: dictionary lookup → keyword rules → local AI fallback (Llama 3.2 via Ollama), fully offline and free to run.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

            html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

            .stApp {
            background-color: #05060d;
            background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(123,97,255,0.25), transparent),
            radial-gradient(ellipse 60% 50% at 100% 20%, rgba(0,245,196,0.15), transparent),
            radial-gradient(ellipse 60% 50% at 0% 100%, rgba(255,95,162,0.12), transparent),
            linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
            background-size: auto, auto, auto, 42px 42px, 42px 42px;
            animation: aurora-drift 18s ease-in-out infinite alternate;
            color: #e8e8f0;
            }
            @keyframes aurora-drift {
            0%   { background-position: 0% 0%, 100% 0%, 0% 100%, 0 0, 0 0; }
            100% { background-position: 5% 5%, 95% 8%, 5% 95%, 0 0, 0 0; }
            }

            #MainMenu, footer { visibility: hidden; }
            header 
            {
            background: transparent !important;
            }

            /* Hero header */
            .hero-container {
            text-align: center;
            padding: 30px 0 10px 0;
            }
            .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #00f5c4, #7b61ff, #ff5fa2);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 6s linear infinite;
            margin-bottom: 0;
            }
            @keyframes shine {
            to { background-position: 200% center; }
            }
            .hero-subtitle {
            color: #8b8fa3;
            font-size: 0.95rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: -8px;
            }

            /* Glass card */
            .glass-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 22px 24px;
            margin-bottom: 18px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
            }
            .section-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            }

            /* Glowing KPI metric cards */
            .KPI_Card {
            background: linear-gradient(145deg, rgba(123,97,255,0.12), rgba(0,245,196,0.06));
            border: 1px solid rgba(123,97,255,0.25);
            border-radius: 16px;
            padding: 18px 20px;
            text-align: left;
            transition: all 0.25s ease;
            box-shadow: 0 0 0 rgba(123,97,255,0);
            }
            .KPI_Card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(123,97,255,0.35);
            border: 1px solid rgba(123,97,255,0.6);
            }
            .KPI_Icon { font-size: 1.6rem; margin-bottom: 6px; }
            .KPI-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            font-family: 'JetBrains Mono', monospace;
            }
            .KPI-Label {
            font-size: 0.78rem;
            color: #9a9db3;
            text-transform: uppercase;
            letter-spacing: 1px;
            }

            /* Buttons */
            div.stButton > button {
            background: linear-gradient(90deg, #7b61ff, #00c9a7);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(123,97,255,0.3);
            }
            div.stButton > button:hover {
            box-shadow: 0 6px 22px rgba(123,97,255,0.55);
            transform: translateY(-2px);
            }

            /* Text area / inputs */
            .stTextArea textarea {
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            color: #e8e8f0 !important;
            }

            /* Tabs */
            ..stTabs [data-baseweb="tab-list"] {
                gap: 28px;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                padding-bottom: 0;
            }
            .stTabs [data-baseweb="tab"] {
                background: transparent;
                border-radius: 10px 10px 0 0;
                padding: 12px 4px;
                color: #6b6e82;
                font-weight: 600;
                font-size: 0.95rem;
                transition: all 0.2s ease;
                border: none;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: #c8cad8;
            }
            .stTabs [aria-selected="true"] {
                background: transparent !important;
                color: #ffffff !important;
                box-shadow: inset 0 -2px 0 #7b61ff;
            }
            .stTabs [data-baseweb="tab-highlight"] {
                background-color: transparent;
            }

            /* AI report box */
            .ai-report-box {
            background: linear-gradient(145deg, rgba(0,245,196,0.06), rgba(123,97,255,0.06));
            border-left: 3px solid #00f5c4;
            border-radius: 14px;
            padding: 22px 26px;
            line-height: 1.7;
            color: #d8dae8;
            white-space: pre-wrap;
            }

            .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            }
            .badge-dict { background: rgba(0,245,196,0.15); color: #00f5c4; }
            .badge-keyword { background: rgba(123,97,255,0.15); color: #a78bff; }
            .badge-ai { background: rgba(255,95,162,0.15); color: #ff5fa2; }


            div[class*="st-key-donut_box"] {
            background: linear-gradient(135deg, rgba(255,95,162,0.08), rgba(123,97,255,0.05));
            border-left: 3px solid #ff5fa2;
            border-radius: 18px;
            padding: 22px 24px;
            }

            div[class*="st-key-bar_box"] {
            background: linear-gradient(135deg, rgba(0,245,196,0.08), rgba(123,97,255,0.05));
            border-left: 3px solid #00f5c4;
            border-radius: 18px;
            padding: 22px 24px;
            }

            </style>
            
            """, unsafe_allow_html=True)


st.markdown("""
            <div class= "hero-container">
            <div class="hero-title">💠 Masareef AI</div>
            <div class = "hero-subtitle">Egyptian Bank SMS Intelligence Agent</div>
            
            """, unsafe_allow_html=True)


def KPI_Card(icon, value, label):
    return f"""
    <div class="KPI-Card">
    <div class="KPI-Icon">{icon}</div>
    <div class="KPI-Value">{value}</div>
    <div class="KPI-Label">{label}</div>
    </div> """

def Source_Badge(source):
    mapping = {
        "dictionary": ("badge-dict", "📖 Dictionary Match"),
        "dictionary_partial": ("badge-dict", "📖 Dictionary (Partial)"),
        "keyword": ("badge-keyword", "🔑 Keyword Rule"),
        "ai_cache": ("badge-ai", "🤖 AI (Cached)"),
        "ai_agent": ("badge-ai", "🤖 AI (Live)"),
    }
    css_class, label = mapping.get(source, ("badge-keyword", source or "Unknown"))
    return f'<span class="badge {css_class}">{label}</span>'


def Fetch_Summary():
    try:
        request = requests.get(f"{FastAPI_URL}/spending-summary", timeout=15)
        request.raise_for_status()
        return request.json()
    except Exception:
        return None
    

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📩 Process Transaction", "🤖 AI Insights"])

with tab1:
    Summary = Fetch_Summary()

    if Summary:
        cat_df = pd.DataFrame(Summary.get("Summary_By_Category", []))
        recent_df = pd.DataFrame(Summary.get("Recent_Transactions", []))

        if not cat_df.empty:
            cat_totals = cat_df.groupby("category", as_index=False)["total_amount"].sum().sort_values("total_amount", ascending=False)
        else:
            cat_totals = cat_df.copy()

        total_spent = cat_df["total_amount"].sum() if not cat_df.empty else 0
        total_txns = cat_df["count"].sum() if not cat_df.empty else 0
        top_category = cat_df.sort_values("total_amount", ascending=False).iloc[0]["category"] if not cat_df.empty else "N/A"
        num_categories = cat_df["category"].nunique() if not cat_df.empty else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(KPI_Card("💰", f"{total_spent:,.0f} EGP", "Total Amount"), unsafe_allow_html=True)
        k2.markdown(KPI_Card("🧾", f"{total_txns}", "Transactions"), unsafe_allow_html=True)
        k3.markdown(KPI_Card("🏆", top_category, "Top Category"), unsafe_allow_html=True)
        k4.markdown(KPI_Card("🗂️", f"{num_categories}", "Categories Active"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)


        def Get_Quick_Stats(cat_df, recent_df):
            if cat_df.empty or recent_df.empty:
                return None
            top_merchant = recent_df["merchant"].mode()[0] if not recent_df.empty else "N/A"
            busiest_cat = cat_df.sort_values("count", ascending=False).iloc[0]
            avg_txn = busiest_cat["total_amount"] / busiest_cat["count"]
            return top_merchant, avg_txn, busiest_cat

        stats = Get_Quick_Stats(cat_df, recent_df)

        box_left, box_right = st.columns(2)
        with box_left:
            if stats:
                top_merchant, avg_txn, _ = stats
                st.markdown(f"""<div class="glass-card" style="background:linear-gradient(135deg, rgba(255,95,162,0.08), rgba(123,97,255,0.05)); border-left:3px solid #ff5fa2;">
                                <div style="font-size:0.75rem; color:#ff5fa2; letter-spacing:1.5px; text-transform:uppercase; font-weight:600;">🏆 Top Merchant</div>
                                <div style="font-size:1.6rem; font-weight:700; color:#fff; margin-top:6px;">{top_merchant}</div>
                                <div style="font-size:0.8rem; color:#9a9db3; margin-top:4px;">Most frequent transaction source</div>
                            </div>
                            """, unsafe_allow_html=True)
        with box_right:
            if stats:
                _, avg_txn, busiest_cat = stats
                st.markdown(f"""<div class="glass-card" style="background:linear-gradient(135deg, rgba(0,245,196,0.08), rgba(123,97,255,0.05)); border-left:3px solid #00f5c4;">
                                <div style="font-size:0.75rem; color:#00f5c4; letter-spacing:1.5px; text-transform:uppercase; font-weight:600;">💡 Quick Insight</div>
                                <div style="font-size:1.6rem; font-weight:700; color:#fff; margin-top:6px;">{avg_txn:,.0f} EGP avg</div>
                                <div style="font-size:0.8rem; color:#9a9db3; margin-top:4px;">Across {int(busiest_cat['count'])} {busiest_cat['category']} transactions</div>
                            </div>
                            """, unsafe_allow_html=True)


        col_left, col_right = st.columns(2)

        with col_left:
            with st.container(key="donut_box"):
                st.markdown('<div class="section-title">🍩 Spending by Category</div>', unsafe_allow_html=True)
                if not cat_df.empty:
                    fig_donut = go.Figure(data=[go.Pie(labels=cat_df["category"], values=cat_df["total_amount"], hole=0.62,
                                                       marker=dict(colors=px.colors.sequential.Tealgrn_r, line=dict(color="#0a0e1a", width=2)),
                                                       textfont=dict(color="white", size=12))])
                    fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                            showlegend=True, legend=dict(font=dict(color="#c8cad8")),
                                            margin=dict(t=10, b=10, l=10, r=10), height=320)
                    st.plotly_chart(fig_donut, use_container_width=True)
                else:
                    st.info("No data yet! Process a transaction first.")

        with col_right:
            with st.container(key="bar_box"):
                st.markdown('<div class="section-title">📊 Category Totals</div>', unsafe_allow_html=True)
                if not cat_df.empty:
                    fig_bar = go.Figure(go.Bar(x=cat_totals["total_amount"], y=cat_totals["category"], orientation="h",
                                               marker=dict(color=cat_totals["total_amount"], colorscale="Tealgrn", line=dict(width=0)),
                                               text=cat_totals["total_amount"].apply(lambda x: f"{x:,.0f} EGP"), textposition="outside",
                                               textfont=dict(color="#e8e8f0", size=12), constraintext="none", cliponaxis=False))
                    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                          font=dict(color="#c8cad8"), margin=dict(t=10, b=10, l=10, r=10), height=320,
                                          xaxis=dict(showgrid=False, title="Amount (EGP)", range=[0, cat_totals["total_amount"].max() * 1.25]), yaxis=dict(showgrid=False))
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No data yet.")

        st.markdown("""<div class="glass-card" style="background:linear-gradient(135deg, rgba(0,245,196,0.08), rgba(123,97,255,0.05)); border-left:3px solid #00f5c4;">""", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🕓 Recent Transactions</div>', unsafe_allow_html=True)

        if not recent_df.empty:
            icons = {"Shopping": "🛍️", "Dining": "🍽️", "Bills": "💡", "Transport": "🚗",
                     "Groceries": "🛒", "Entertainment": "🎬", "Transfer": "💸",
                     "Salary Credit": "💰", "ATM Withdrawal": "🏧"}
            cat_colors = {"Shopping": "#00f5c4", "Dining": "#7b61ff", "Bills": "#ff5fa2",
                          "Transport": "#4fd1c5", "Groceries": "#00f5c4", "Entertainment": "#a78bff",
                          "Transfer": "#ff5fa2", "Salary Credit": "#4ade80", "ATM Withdrawal": "#fbbf24"}

            rows_html = ""
            for i, row in recent_df.iterrows():
                icon = icons.get(row["category"], "📌")
                color = cat_colors.get(row["category"], "#9a9db3")
                type_colors = {"Purchase": "#7b61ff", "Transfer": "#00f5c4", "Salary Credit": "#4ade80", "ATM Withdrawal": "#fbbf24"}
                type_color = type_colors.get(row.get("transaction_type", ""), "#9a9db3")
                rows_html += f"""<tr style="background:linear-gradient(90deg, {color}14, transparent 40%); border-left:3px solid {color};">
                                    <td style="padding:14px 16px; color:#fff; font-weight:600;">{row['merchant']}</td>
                                    <td style="padding:14px 16px;">
                                        <span style="background:{color}22; color:{color}; padding:4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600;">
                                            {icon} {row['category']}
                                        </span>
                                    </td>
                                    <td style="padding:14px 16px;">
                                        <span style="background:{type_color}22; color:{type_color}; padding: 4px 12px; border-radius:20px; font-size:0.78rem; font-weight:600; margin-left:6px;">
                                            {row.get('transaction_type', '')}
                                        </span>
                                    </td>
                                    <td style="padding:14px 16px; text-align:right; color:{color}; font-family:'JetBrains Mono'; font-weight:700;">
                                        {row['amount']:,.2f} EGP
                                    </td>
                                    <td style="padding:14px 16px; text-align:right; color:#7a7d90; font-size:0.85rem;">{row['date']}</td>
                                </tr>"""

            table_html = f"""
            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.1);">
                    <th style="text-align:left; padding:10px 16px; color:#7a7d90; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Merchant</th>
                    <th style="text-align:left; padding:10px 16px; color:#7a7d90; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Category</th>
                    <th style="text-align:left; padding:10px 16px; color:#7a7d90; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Type</th>
                    <th style="text-align:right; padding:10px 16px; color:#7a7d90; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Amount</th>
                    <th style="text-align:right; padding:10px 16px; color:#7a7d90; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Date</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>"""
            st.markdown(table_html, unsafe_allow_html=True)
        
        else:
            st.info("No transactions yet.")
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("⚠️ Can't reach FastAPI. Make sure it's running on port 8000.")

    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

# ------------------------------------------------------------
# TAB 2 — PROCESS TRANSACTION
# ------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">📩 Paste a Bank SMS</div>', unsafe_allow_html=True)
    sms_input = st.text_area("Paste bank SMS", height=130, placeholder="From HSBC: 13JUL26 CARREFOUR Purchase from 482-193***-756 EGP 450.00- Your available balance is EGP 3,200.00", label_visibility="collapsed")

    if st.button("⚡ Process Transaction"):
        if not sms_input.strip():
            st.warning("Paste an SMS first.")
        else:
            with st.spinner("Extracting, classifying, categorizing..."):
                try:
                    request = requests.post(f"{FastAPI_URL}/process-transaction", json={"sms": sms_input}, timeout=30)
                    request.raise_for_status()
                    st.session_state["last_txn"] = request.json()
                except Exception as e:
                    st.error(f"Error: {e}")

    if "last_txn" in st.session_state:
        d = st.session_state["last_txn"]
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(KPI_Card("🏪", d.get("Merchant", "N/A"), "Merchant"), unsafe_allow_html=True)
        c2.markdown(KPI_Card("💵", f"{d.get('Amount', 'N/A')} EGP", "Amount"), unsafe_allow_html=True)
        c3.markdown(KPI_Card("🗂️", d.get("Category", "N/A"), "Category"), unsafe_allow_html=True)
        c4.markdown(KPI_Card("🔁", d.get("Transaction_Type", "N/A"), "Type"), unsafe_allow_html=True)
        st.markdown(Source_Badge(d.get("Category_Source", "")), unsafe_allow_html=True)

# ------------------------------------------------------------
# TAB 3 — AI INSIGHTS
# ------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">🤖 AI-Generated Weekly Report</div>', unsafe_allow_html=True)
    st.caption("Triggers your live n8n agent — pulls real spending data, reasons with a local AI model, and emails you the report.")

    if st.button("🚀 Trigger Weekly Report Workflow"):
        with st.spinner("Running n8n workflow — fetching data, reasoning, sending email..."):
            try:
                resp = requests.post(n8n_Webhook_URL, timeout=90)
                resp.raise_for_status()
                st.success("✅ Workflow triggered — check your inbox for the report!")
            except Exception as e:
                st.error(f"Couldn't reach n8n: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; color:#4a4d5e; font-size:0.75rem; margin-top:30px;'>Masareef AI · {datetime.now().strftime('%Y')}</p>", unsafe_allow_html=True)