import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random

# Set page configuration
st.set_page_config(
    page_title="Smart Sync Guardian - Netflix IAM Monitor",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #E50914;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #564d4d;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f7f7f7;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .risk-high {
        color: #E50914;
        font-weight: bold;
    }
    .risk-medium {
        color: #FFA500;
        font-weight: bold;
    }
    .risk-low {
        color: #2E8B57;
        font-weight: bold;
    }
    .stButton button {
        background-color: #E50914;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=200)
    st.markdown("### Smart Sync Guardian")
    st.markdown("AI-powered IAM Monitoring & Security")
    
    st.markdown("---")
    
    # Filter options
    st.markdown("### Filters")
    business_unit = st.selectbox(
        "Business Unit",
        ["All", "Streaming", "Gaming", "Live Events", "Studio Production", "Content Analytics"]
    )
    
    time_range = st.selectbox(
        "Time Range",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days"]
    )
    
    alert_type = st.multiselect(
        "Alert Types",
        ["Unusual Login Location", "Excessive Permission Changes", "Brute Force Attempts", 
         "Dormant Account Access", "Unusual Access Pattern", "Multiple Failed Logins"],
        default=["Unusual Login Location", "Excessive Permission Changes", "Brute Force Attempts"]
    )
    
    st.markdown("---")
    
    # Demo controls
    st.markdown("### Demo Controls")
    simulate_attack = st.button("Simulate Security Incident")
    
    

# Generate sample data
def generate_data():
    # Current time
    now = datetime.now()
    
    # Create timestamps for the past 24 hours
    timestamps = [now - timedelta(hours=i) for i in range(24)]
    timestamps.reverse()
    
    # Business units and their weights
    business_units = {
        "Streaming": 0.4,
        "Gaming": 0.2,
        "Live Events": 0.15,
        "Studio Production": 0.15,
        "Content Analytics": 0.1
    }
    
    # Event types and their weights
    event_types = {
        "Authentication": 0.5,
        "Authorization": 0.3,
        "Permission Change": 0.1,
        "API Access": 0.1
    }
    
    # Generate base data
    data = []
    for ts in timestamps:
        # Number of events per hour (with some randomness)
        num_events = int(np.random.normal(1000, 200))
        
        for _ in range(num_events):
            # Select business unit based on weights
            bu = np.random.choice(list(business_units.keys()), p=list(business_units.values()))
            
            # Select event type based on weights
            event = np.random.choice(list(event_types.keys()), p=list(event_types.values()))
            
            # Calculate risk score (mostly low, occasionally medium, rarely high)
            risk_score = np.random.choice([1, 2, 3], p=[0.85, 0.12, 0.03])
            
            # Location (mostly US, occasionally international)
            location = np.random.choice(
                ["US-West", "US-East", "US-Central", "Europe", "Asia", "South America"],
                p=[0.4, 0.3, 0.15, 0.07, 0.05, 0.03]
            )
            
            # Success rate (mostly successful)
            success = np.random.choice([True, False], p=[0.95, 0.05])
            
            data.append({
                "timestamp": ts + timedelta(minutes=np.random.randint(0, 60)),
                "business_unit": bu,
                "event_type": event,
                "risk_score": risk_score,
                "location": location,
                "success": success,
                "user_id": f"user_{np.random.randint(1, 1000)}",
                "resource": np.random.choice(["Content API", "User Management", "Billing System", 
                                             "Analytics Dashboard", "Admin Portal", "Content Management"])
            })
    
    return pd.DataFrame(data)

# Generate alerts data
def generate_alerts():
    alert_types = ["Unusual Login Location", "Excessive Permission Changes", "Brute Force Attempts", 
                  "Dormant Account Access", "Unusual Access Pattern", "Multiple Failed Logins"]
    
    business_units = ["Streaming", "Gaming", "Live Events", "Studio Production", "Content Analytics"]
    
    alerts = []
    # Generate 20-30 alerts
    for _ in range(random.randint(20, 30)):
        severity = np.random.choice(["High", "Medium", "Low"], p=[0.2, 0.3, 0.5])
        alert_type = np.random.choice(alert_types)
        timestamp = datetime.now() - timedelta(hours=random.randint(0, 24))
        
        alerts.append({
            "timestamp": timestamp,
            "alert_type": alert_type,
            "severity": severity,
            "business_unit": np.random.choice(business_units),
            "user_id": f"user_{np.random.randint(1, 1000)}",
            "status": np.random.choice(["Open", "In Progress", "Resolved"], p=[0.5, 0.3, 0.2]),
            "details": f"Details about the {alert_type.lower()} alert"
        })
    
    return pd.DataFrame(alerts)

# Main content
df = generate_data()
alerts_df = generate_alerts()

# Header
st.markdown('<div class="main-header">Smart Sync Guardian</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered Identity and Access Management Monitoring for Netflix</div>', unsafe_allow_html=True)

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Total IAM Events (24h)",
        f"{len(df):,}",
        f"{int(len(df)*0.05):+,}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    high_risk = len(df[df["risk_score"] == 3])
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "High Risk Events",
        f"{high_risk}",
        f"{int(high_risk*0.1):+,}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    failed = len(df[df["success"] == False])
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Failed Authentication",
        f"{failed}",
        f"{int(failed*-0.02):+,}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    alerts = len(alerts_df)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Active Alerts",
        f"{alerts}",
        f"{int(alerts*0.15):+,}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Dashboard content
tab1, tab2, tab3 = st.tabs(["Overview", "Alerts", "User Activity"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("IAM Events Over Time")
        
        events_by_time = df.groupby([pd.Grouper(key='timestamp', freq='1H'), 'event_type']).size().unstack().fillna(0)
        
        fig = px.line(events_by_time, x=events_by_time.index, y=events_by_time.columns,
                      color_discrete_sequence=px.colors.qualitative.Plotly,
                      labels={"value": "Events Count", "variable": "Event Type", "timestamp": "Time"})
        
        fig.update_layout(height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
        
        # Events by business unit
        st.subheader("IAM Events by Business Unit")
        
        events_by_bu = df.groupby('business_unit').size()
        
        fig = px.pie(values=events_by_bu.values, names=events_by_bu.index,
                     color_discrete_sequence=px.colors.qualitative.Bold)
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
    
    with col2:
        st.subheader("Risk Assessment")
        
        # Risk distribution
        risk_counts = df['risk_score'].value_counts().sort_index()
        risk_labels = {1: "Low", 2: "Medium", 3: "High"}
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[risk_labels[i] for i in risk_counts.index],
            y=risk_counts.values,
            marker_color=['#2E8B57', '#FFA500', '#E50914']
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Geo distribution
        st.subheader("Geographic Distribution")
        
        geo_counts = df['location'].value_counts()
        
        fig = px.bar(x=geo_counts.index, y=geo_counts.values,
                     labels={"x": "Location", "y": "Events Count"},
                     color_discrete_sequence=['#564d4d'])
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top resources
        st.subheader("Top Accessed Resources")
        resources = df['resource'].value_counts().head(5)
        
        fig = px.bar(x=resources.values, y=resources.index, orientation='h',
                     labels={"x": "Access Count", "y": "Resource"},
                     color_discrete_sequence=['#564d4d'])
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Security Alerts")
    
    # Security alerts table
    filtered_alerts = alerts_df
    
    if business_unit != "All":
        filtered_alerts = filtered_alerts[filtered_alerts["business_unit"] == business_unit]
    
    if alert_type:
        filtered_alerts = filtered_alerts[filtered_alerts["alert_type"].isin(alert_type)]
    
    # Format the display
    display_alerts = filtered_alerts.copy()
    display_alerts["timestamp"] = display_alerts["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    
    # Add color coding for severity
    def color_severity(val):
        if val == "High":
            return "background-color: #ffcccc"
        elif val == "Medium":
            return "background-color: #fff2cc"
        else:
            return "background-color: #ccffcc"
    
    st.dataframe(
        display_alerts.style.applymap(color_severity, subset=["severity"]),
        use_container_width=True,
        height=400
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Alerts by Severity")
        severity_counts = filtered_alerts["severity"].value_counts()
        
        fig = px.pie(names=severity_counts.index, values=severity_counts.values,
                     color=severity_counts.index,
                     color_discrete_map={"High": "#E50914", "Medium": "#FFA500", "Low": "#2E8B57"})
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Alerts by Type")
        type_counts = filtered_alerts["alert_type"].value_counts().head(5)
        
        fig = px.bar(x=type_counts.index, y=type_counts.values,
                     labels={"x": "Alert Type", "y": "Count"},
                     color_discrete_sequence=['#564d4d'])
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("User Activity Analytics")
    
    # Create sample user risk scores
    num_users = 1000
    user_ids = [f"user_{i}" for i in range(1, num_users+1)]
    
    user_data = {
        "user_id": user_ids,
        "risk_score": np.random.normal(30, 15, num_users).clip(0, 100),
        "last_activity": [datetime.now() - timedelta(hours=random.randint(0, 720)) for _ in range(num_users)],
        "auth_failures": np.random.poisson(1, num_users),
        "location_changes": np.random.poisson(0.3, num_users),
        "permission_level": np.random.choice(["Admin", "Power User", "Standard", "Limited"], size=num_users, 
                                            p=[0.05, 0.15, 0.6, 0.2]),
        "business_unit": np.random.choice(list(business_units.keys()), size=num_users, p=list(business_units.values()))
    }
    
    users_df = pd.DataFrame(user_data)
    
    # Add a few high-risk users
    high_risk_indices = np.random.choice(num_users, 20, replace=False)
    users_df.loc[high_risk_indices, "risk_score"] = np.random.uniform(75, 100, 20)
    users_df.loc[high_risk_indices, "auth_failures"] = np.random.poisson(5, 20)
    users_df.loc[high_risk_indices, "location_changes"] = np.random.poisson(2, 20)
    
    # Filter by business unit
    if business_unit != "All":
        users_df = users_df[users_df["business_unit"] == business_unit]
    
    # Highest risk users
    st.subheader("Highest Risk Users")
    high_risk_users = users_df.sort_values("risk_score", ascending=False).head(10)
    high_risk_users["last_activity"] = high_risk_users["last_activity"].dt.strftime("%Y-%m-%d %H:%M")
    
    st.dataframe(high_risk_users[["user_id", "risk_score", "permission_level", "auth_failures", "location_changes", "business_unit", "last_activity"]], 
                use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("User Risk Score Distribution")
        
        fig = px.histogram(users_df, x="risk_score", nbins=20,
                          labels={"risk_score": "Risk Score", "count": "Number of Users"},
                          color_discrete_sequence=['#564d4d'])
        
        fig.update_layout(height=300)
        fig.add_vline(x=75, line_dash="dash", line_color="red")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Users by Permission Level")
        
        perm_counts = users_df["permission_level"].value_counts()
        
        fig = px.pie(names=perm_counts.index, values=perm_counts.values,
                     color_discrete_sequence=px.colors.qualitative.Plotly)
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

# Simulate attack logic
if simulate_attack:
    st.warning("⚠️ Simulating security incident...")
    
    # Create a progress bar
    progress_bar = st.progress(0)
    
    for i in range(101):
        time.sleep(0.02)
        progress_bar.progress(i)
    
    # Show alert
    st.error("🚨 **SECURITY ALERT**: Multiple suspicious login attempts detected for high-privilege account user_752 from unusual location (South America).")
    
    # Show details in an expander
    with st.expander("View Incident Details"):
        st.markdown("""
        ### Security Incident Details
        
        **Timestamp:** {}
        
        **User:** user_752 (Admin)
        
        **Business Unit:** Content Analytics
        
        **Alert Type:** Unusual Login Location + Multiple Failed Logins
        
        **Risk Level:** High
        
        **Location:** São Paulo, Brazil (IP: 187.32.45.108)
        
        **Device:** Unrecognized Windows device
        
        **Failed Attempts:** 6 attempts in 3 minutes
        
        **Access History:** No previous access from this location or device
        
        **Recommended Action:** 
        - Lock account immediately
        - Force password reset
        - Verify with user via secondary channel
        - Review recent activity for potential compromise
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Lock Account", type="primary")
        with col2:
            st.button("Dismiss Alert")
