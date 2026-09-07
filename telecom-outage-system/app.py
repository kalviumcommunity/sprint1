import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Network Impact Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background-color: #040d1a;
    color: #e8f0ff;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Exo 2', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: #071221;
    border-right: 1px solid rgba(30, 144, 255, 0.15);
}

[data-testid="stSidebar"] * {
    color: #dce9ff;
}

.main-title {
    font-size: 2.3rem;
    font-weight: 700;
    color: #f5f9ff;
    margin-bottom: 0;
}

.subtitle {
    color: #7e91ad;
    margin-top: 5px;
    margin-bottom: 20px;
}

.status-online {
    color: #00d084;
    font-size: 0.9rem;
}

div[data-testid="stMetric"] {
    background: rgba(12, 30, 52, 0.85);
    border: 1px solid rgba(55, 140, 255, 0.18);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 0 25px rgba(0, 90, 180, 0.08);
}

div[data-testid="stMetricLabel"] {
    color: #91a4c0;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
}

.priority-card {
    background: linear-gradient(
        135deg,
        rgba(12, 31, 55, 0.95),
        rgba(8, 20, 38, 0.95)
    );
    border: 1px solid rgba(56, 139, 253, 0.18);
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 12px;
}

.critical-card {
    border-left: 4px solid #ff3b5c;
}

.high-card {
    border-left: 4px solid #ff8a3d;
}

.medium-card {
    border-left: 4px solid #ffd43b;
}

.low-card {
    border-left: 4px solid #00d084;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
}

.card-text {
    color: #91a4c0;
    font-size: 0.85rem;
}

.score-critical {
    color: #ff3b5c;
    font-weight: 700;
    font-size: 1.2rem;
}

.score-high {
    color: #ff8a3d;
    font-weight: 700;
    font-size: 1.2rem;
}

.score-medium {
    color: #ffd43b;
    font-weight: 700;
    font-size: 1.2rem;
}

.score-low {
    color: #00d084;
    font-weight: 700;
    font-size: 1.2rem;
}

.alert-box {
    background: rgba(255, 59, 92, 0.08);
    border: 1px solid rgba(255, 59, 92, 0.25);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

div.stButton > button {
    background: linear-gradient(90deg, #087cff, #00a8ff);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1rem;
    font-weight: 600;
}

div.stButton > button:hover {
    box-shadow: 0 0 18px rgba(0, 140, 255, 0.5);
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================

outages = [
    {
        "Priority": "CRITICAL",
        "Outage ID": "OUT-2048",
        "Region": "Bengaluru South",
        "Network": "5G Core",
        "Affected Customers": 42500,
        "Complaints": 1248,
        "Usage Impact": 78,
        "Revenue Risk": "₹18.4L",
        "Duration": "37 min",
        "Impact Score": 94,
        "Status": "Active"
    },
    {
        "Priority": "CRITICAL",
        "Outage ID": "OUT-2071",
        "Region": "Mumbai West",
        "Network": "4G LTE",
        "Affected Customers": 38200,
        "Complaints": 980,
        "Usage Impact": 74,
        "Revenue Risk": "₹15.2L",
        "Duration": "52 min",
        "Impact Score": 91,
        "Status": "Investigating"
    },
    {
        "Priority": "HIGH",
        "Outage ID": "OUT-2056",
        "Region": "Chennai Central",
        "Network": "Fiber",
        "Affected Customers": 24500,
        "Complaints": 870,
        "Usage Impact": 62,
        "Revenue Risk": "₹9.8L",
        "Duration": "1h 14m",
        "Impact Score": 82,
        "Status": "Active"
    },
    {
        "Priority": "HIGH",
        "Outage ID": "OUT-2090",
        "Region": "Pune",
        "Network": "5G",
        "Affected Customers": 18800,
        "Complaints": 620,
        "Usage Impact": 58,
        "Revenue Risk": "₹7.2L",
        "Duration": "45 min",
        "Impact Score": 76,
        "Status": "Investigating"
    },
    {
        "Priority": "MEDIUM",
        "Outage ID": "OUT-2114",
        "Region": "Hyderabad",
        "Network": "4G",
        "Affected Customers": 12400,
        "Complaints": 540,
        "Usage Impact": 41,
        "Revenue Risk": "₹4.6L",
        "Duration": "28 min",
        "Impact Score": 71,
        "Status": "Active"
    },
    {
        "Priority": "LOW",
        "Outage ID": "OUT-2132",
        "Region": "Kolkata",
        "Network": "Fiber",
        "Affected Customers": 3200,
        "Complaints": 80,
        "Usage Impact": 12,
        "Revenue Risk": "₹0.8L",
        "Duration": "16 min",
        "Impact Score": 32,
        "Status": "Resolved"
    }
]

df = pd.DataFrame(outages)

regional_data = pd.DataFrame({
    "Region": ["Bengaluru", "Mumbai", "Chennai", "Hyderabad", "Pune", "Kolkata"],
    "Active Outages": [4, 5, 3, 2, 3, 1],
    "Customers Affected": [52000, 64000, 31000, 19000, 22000, 7000],
    "Complaints": [1420, 1850, 870, 540, 620, 180],
    "Impact Score": [94, 91, 82, 71, 76, 43]
})

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# 📡 NetPulse")
st.sidebar.caption("Network Impact Intelligence")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "OPERATIONS",
    [
        "Dashboard",
        "Live Outages",
        "Impact Analysis",
        "Customer Complaints",
        "Regional Analytics",
        "Priority Queue",
        "Reports",
        "Settings"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🟢 System Online")
st.sidebar.caption("Last updated: Just now")

# ============================================================
# TOP BAR
# ============================================================

top1, top2, top3 = st.columns([4, 2, 2])

with top1:
    st.markdown(
        '<p class="status-online">● All Systems Operational</p>',
        unsafe_allow_html=True
    )

with top2:
    st.text_input(
        "Search",
        placeholder="Search outage, region or ticket...",
        label_visibility="collapsed"
    )

with top3:
    st.markdown("🔔  **3 Alerts**  👤 **Amol**")

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Network Operations Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Identify which network outage needs attention first.</div>',
        unsafe_allow_html=True
    )

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🚨 Active Outages", "27", "↑ 4 today")
    c2.metric("🔴 Critical", "6", "Requires attention")
    c3.metric("👥 Customers Affected", "128,450", "↑ 12%")
    c4.metric("🌍 Regions Impacted", "14", "Across India")
    c5.metric("⏱ Avg Resolution", "42 min", "↓ 8 min")

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:

        st.subheader("🚨 Highest Operational Impact")
        st.caption("Incidents ranked by real-time operational impact score")

        top_outages = df.sort_values(
            "Impact Score",
            ascending=False
        ).head(4)

        for index, row in top_outages.iterrows():

            severity = row["Priority"].lower()

            st.markdown(
                f"""
                <div class="priority-card {severity}-card">
                    <div class="card-title">
                        {row["Outage ID"]} — {row["Region"]}
                    </div>

                    <div class="card-text">
                        {row["Network"]} •
                        {row["Affected Customers"]:,} affected customers •
                        {row["Complaints"]:,} complaints
                    </div>

                    <div class="card-text">
                        Usage Impact: {row["Usage Impact"]}% •
                        Revenue Risk: {row["Revenue Risk"]} •
                        Duration: {row["Duration"]}
                    </div>

                    <div class="score-{severity}">
                        Impact Score: {row["Impact Score"]}/100
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"View Incident {row['Outage ID']}",
                key=f"view_{row['Outage ID']}"
            ):
                st.session_state["selected_outage"] = row["Outage ID"]
                st.success(f"Selected {row['Outage ID']}")

    with right:

        st.subheader("🔔 Live Alerts")

        alerts = [
            ("🔴", "Critical outage detected", "Bengaluru South", "2 min ago"),
            ("🟠", "Complaint spike detected", "Chennai Central", "8 min ago"),
            ("🟡", "Traffic anomaly detected", "Hyderabad", "14 min ago"),
            ("🟢", "Outage resolved", "Mumbai West", "21 min ago")
        ]

        for icon, title, region, time in alerts:
            st.markdown(
                f"""
                <div class="alert-box">
                    <b>{icon} {title}</b><br>
                    <span class="card-text">{region} • {time}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎯 Operational Impact Score")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=94,
                title={"text": "OUT-2048 Priority Score"},
                number={"suffix": " / 100"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#ff3b5c"},
                    "steps": [
                        {"range": [0, 50], "color": "#123047"},
                        {"range": [50, 75], "color": "#1b4057"},
                        {"range": [75, 100], "color": "#2b2330"}
                    ]
                }
            )
        )

        gauge.update_layout(
            height=320,
            paper_bgcolor="#071221",
            font_color="white"
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    with col2:

        st.subheader("📊 Impact Score Factors")

        factors = pd.DataFrame({
            "Factor": [
                "Customer Impact",
                "Network Severity",
                "Usage / Traffic",
                "Complaint Volume",
                "Revenue Risk"
            ],
            "Weight": [35, 25, 20, 10, 10]
        })

        fig = px.bar(
            factors,
            x="Weight",
            y="Factor",
            orientation="h",
            text="Weight",
            color="Weight"
        )

        fig.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        fig.update_layout(
            height=320,
            paper_bgcolor="#071221",
            plot_bgcolor="#071221",
            font_color="white",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("🗺 Live Network Impact Map")

    map_data = pd.DataFrame({
        "City": [
            "Bengaluru",
            "Chennai",
            "Hyderabad",
            "Mumbai",
            "Delhi",
            "Pune",
            "Kolkata"
        ],
        "lat": [
            12.9716,
            13.0827,
            17.3850,
            19.0760,
            28.6139,
            18.5204,
            22.5726
        ],
        "lon": [
            77.5946,
            80.2707,
            78.4867,
            72.8777,
            77.1025,
            73.8567,
            88.3639
        ],
        "Impact": [94, 82, 71, 91, 65, 76, 43]
    })

    fig_map = px.scatter_geo(
        map_data,
        lat="lat",
        lon="lon",
        size="Impact",
        color="Impact",
        hover_name="City",
        projection="natural earth",
        scope="asia"
    )

    fig_map.update_geos(
        center={"lat": 20, "lon": 78},
        projection_scale=4,
        bgcolor="#071221",
        landcolor="#0c2033",
        showland=True,
        showocean=True,
        oceancolor="#040d1a"
    )

    fig_map.update_layout(
        height=500,
        paper_bgcolor="#071221",
        font_color="white",
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

# ============================================================
# LIVE OUTAGES
# ============================================================

elif page == "Live Outages":

    st.title("🚨 Live Network Outages")
    st.caption("Real-time incident monitoring")

    filter_priority = st.multiselect(
        "Filter by priority",
        df["Priority"].unique(),
        default=df["Priority"].unique()
    )

    filtered = df[
        df["Priority"].isin(filter_priority)
    ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# IMPACT ANALYSIS
# ============================================================

elif page == "Impact Analysis":

    st.title("🎯 Operational Impact Analysis")

    score_df = df.sort_values(
        "Impact Score",
        ascending=False
    )

    fig = px.bar(
        score_df,
        x="Outage ID",
        y="Impact Score",
        color="Priority",
        hover_data=[
            "Affected Customers",
            "Complaints",
            "Usage Impact"
        ]
    )

    fig.update_layout(
        paper_bgcolor="#071221",
        plot_bgcolor="#071221",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("""
    ### How the Priority Score Works

    - **35%** Customer Impact
    - **25%** Network Severity
    - **20%** Usage and Traffic Impact
    - **10%** Customer Complaint Volume
    - **10%** Estimated Revenue Risk
    """)

# ============================================================
# CUSTOMER COMPLAINTS
# ============================================================

elif page == "Customer Complaints":

    st.title("📞 Customer Complaint Intelligence")

    st.metric(
        "Total Complaints",
        f"{df['Complaints'].sum():,}"
    )

    hours = list(range(24))

    complaints_df = pd.DataFrame({
        "Hour": hours,
        "Complaints": [
            random.randint(100, 900)
            for _ in hours
        ]
    })

    fig = px.area(
        complaints_df,
        x="Hour",
        y="Complaints",
        title="Complaint Volume — Last 24 Hours"
    )

    fig.update_layout(
        paper_bgcolor="#071221",
        plot_bgcolor="#071221",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Top Complaint Categories")

    categories = pd.DataFrame({
        "Category": [
            "No Network",
            "Slow Internet",
            "Call Drops",
            "5G Not Available",
            "Intermittent Connectivity"
        ],
        "Count": [1240, 980, 740, 620, 410]
    })

    st.dataframe(
        categories,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# REGIONAL ANALYTICS
# ============================================================

elif page == "Regional Analytics":

    st.title("🌍 Regional Network Health")

    st.dataframe(
        regional_data,
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        regional_data,
        x="Region",
        y="Impact Score",
        text="Impact Score",
        title="Operational Impact by Region"
    )

    fig.update_layout(
        paper_bgcolor="#071221",
        plot_bgcolor="#071221",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# PRIORITY QUEUE
# ============================================================

elif page == "Priority Queue":

    st.title("🥇 Priority Queue")
    st.caption("All incidents ranked by operational impact")

    priority_df = df.sort_values(
        "Impact Score",
        ascending=False
    ).reset_index(drop=True)

    st.dataframe(
        priority_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Select Incident")

    incident = st.selectbox(
        "Choose an outage",
        priority_df["Outage ID"]
    )

    selected = priority_df[
        priority_df["Outage ID"] == incident
    ].iloc[0]

    st.markdown("---")

    st.subheader(
        f"{selected['Outage ID']} — {selected['Region']}"
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Impact Score",
        f"{selected['Impact Score']}/100"
    )

    b.metric(
        "Customers",
        f"{selected['Affected Customers']:,}"
    )

    c.metric(
        "Complaints",
        f"{selected['Complaints']:,}"
    )

    d.metric(
        "Usage Impact",
        f"{selected['Usage Impact']}%"
    )

    st.markdown("### 🚨 Recommended Action")

    if selected["Impact Score"] >= 80:
        st.error(
            "Immediate escalation recommended. "
            "High customer impact and high operational risk."
        )
    else:
        st.warning(
            "Monitor closely and assign a network engineer."
        )

    b1, b2, b3, b4 = st.columns(4)

    if b1.button("🚨 Escalate Incident"):
        st.success("Incident escalated successfully.")

    if b2.button("👨‍💻 Assign Network Team"):
        st.success("Network team assigned.")

    if b3.button("🔍 Mark Investigating"):
        st.success("Status updated to Investigating.")

    if b4.button("✓ Resolve Incident"):
        st.success("Incident marked as Resolved.")

# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("📄 Network Operations Reports")

    r1, r2, r3 = st.columns(3)

    r1.metric("Daily Outages", "27")
    r2.metric("Revenue Risk", "₹56.2L")
    r3.metric("Avg Resolution Time", "42 min")

    st.markdown("### Available Reports")

    report_types = [
        "📊 Daily Outage Summary",
        "🌍 Regional Impact Report",
        "📞 Customer Complaint Trends",
        "⏱ Resolution Time Analysis",
        "🚨 Most Affected Regions",
        "💰 Revenue Impact Report"
    ]

    cols = st.columns(3)

    for i, report in enumerate(report_types):
        cols[i % 3].info(report)

    if st.button("Generate Report"):
        st.success(
            "Report generated successfully!"
        )

# ============================================================
# SETTINGS
# ============================================================

elif page == "Settings":

    st.title("⚙️ System Settings")

    st.subheader("Alert Thresholds")

    critical_threshold = st.slider(
        "Critical Impact Score",
        70,
        100,
        85
    )

    high_threshold = st.slider(
        "High Priority Score",
        50,
        90,
        70
    )

    st.subheader("Notifications")

    email_alerts = st.toggle(
        "Email Notifications",
        True
    )

    sms_alerts = st.toggle(
        "SMS Alerts",
        True
    )

    st.subheader("Data Refresh")

    refresh_rate = st.selectbox(
        "Dashboard Refresh Interval",
        ["30 seconds", "1 minute", "5 minutes"]
    )

    if st.button("Save Settings"):
        st.success("Settings saved successfully!")