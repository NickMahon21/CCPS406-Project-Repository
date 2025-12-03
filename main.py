import streamlit as st

from user_management import assign_role, get_user_profile
from rewards_management import approve_redemption
from support_feedback import assign_ticket, update_ticket_status
from kpi_data import get_kpi_summary

# -----------------------------------------------------------
# PAGE CONFIG & CSS STYLES
# -----------------------------------------------------------
st.set_page_config(
    page_title="BizPoints Admin Dashboard",
    layout="wide"
)

# Custom CSS for cleaner UI
st.markdown("""
<style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #4A4A4A;
    }
    .section-header {
        font-size: 24px;
        margin-top: 20px;
        font-weight: 600;
        color: #333333;
    }
    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: #F7F9FC;
        border: 1px solid #EAEAEA;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------
st.sidebar.title("📊 BizPoints Admin")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard Overview", "User Management", "Rewards", "Support Tickets"]
)

# -----------------------------------------------------------
# DASHBOARD HOME PAGE
# -----------------------------------------------------------
if page == "Dashboard Overview":
    st.markdown('<div class="main-title">BizPoints Admin Dashboard</div>', unsafe_allow_html=True)
    st.write("Overview of system metrics and activity")

    kpis = get_kpi_summary()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Open Tickets", kpis["open_tickets"])

    with col2:
        st.metric("Total Rewards", kpis["total_rewards"])

    with col3:
        st.metric("Feedback Count", kpis["feedback_count"])

    with col4:
        st.metric("Avg Response Time (hrs)", kpis["avg_response_time"])

    st.markdown("### Recent Activity")
    st.write("Activity logs or info panels can be added here later.")

# -----------------------------------------------------------
# USER MANAGEMENT PAGE
# -----------------------------------------------------------
elif page == "User Management":
    st.markdown('<div class="section-header">User Management</div>', unsafe_allow_html=True)

    with st.expander("🔧 Assign Role to User"):
        user_id = st.number_input("User ID", value=1)
        role_id = st.number_input("Role ID", value=1)
        if st.button("Assign Role"):
            st.json(assign_role(user_id, role_id))

    with st.expander("🔍 View User Profile"):
        user_id_profile = st.number_input("User ID (Profile)", value=1)
        if st.button("Get User Profile"):
            st.json(get_user_profile(user_id_profile))

# -----------------------------------------------------------
# REWARDS PAGE
# -----------------------------------------------------------
elif page == "Rewards":
    st.markdown('<div class="section-header">Rewards & Redemption Management</div>', unsafe_allow_html=True)

    with st.expander("🎁 Approve Redemption Request"):
        account = st.number_input("Account ID", value=1001)
        reward = st.number_input("Reward ID", value=20)
        user = st.number_input("User Redeeming (User ID)", value=1)
        if st.button("Approve Redemption"):
            st.json(approve_redemption(account, reward, user))

# -----------------------------------------------------------
# SUPPORT PAGE
# -----------------------------------------------------------
elif page == "Support Tickets":
    st.markdown('<div class="section-header">Support Ticket Management</div>', unsafe_allow_html=True)

    with st.expander("📌 Assign Ticket to Agent"):
        ticket = st.number_input("Ticket ID", value=501)
        agent = st.number_input("Agent ID", value=77)
        if st.button("Assign Agent"):
            st.json(assign_ticket(ticket, agent))

    with st.expander("💬 Update Ticket Status"):
        ticket2 = st.number_input("Ticket ID (Status)", value=501)
        status = st.text_input("New Status", value="closed")
        if st.button("Update Status"):
            st.json(update_ticket_status(ticket2, status))
