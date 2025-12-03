import streamlit as st

from user_management import assign_role, get_user_profile
from rewards_management import approve_redemption
from support_feedback import assign_ticket, update_ticket_status
from kpi import get_kpi_summary

st.set_page_config(page_title="BizPoints Admin Dashboard")

st.title("BizPoints Admin Dashboard")
st.write("CCPS406 – Assignment 3 Deployment")

tab1, tab2, tab3, tab4 = st.tabs(["User Management", "Rewards", "Support", "KPIs"])

# ------------------------------------------
# USER MANAGEMENT
# ------------------------------------------
with tab1:
    st.subheader("Manage Users")

    user_id = st.number_input("User ID", value=1)
    role_id = st.number_input("Role ID", value=1)

    if st.button("Assign Role"):
        st.json(assign_role(user_id, role_id))

    if st.button("Get User Profile"):
        st.json(get_user_profile(user_id))

# ------------------------------------------
# REWARDS
# ------------------------------------------
with tab2:
    st.subheader("Rewards Management")

    account = st.number_input("Account ID", value=1001)
    reward = st.number_input("Reward ID", value=20)
    user = st.number_input("User Redeeming", value=1)

    if st.button("Approve Redemption"):
        st.json(approve_redemption(account, reward, user))

# ------------------------------------------
# SUPPORT
# ------------------------------------------
with tab3:
    st.subheader("Support Ticket Management")

    ticket = st.number_input("Ticket ID", value=501)
    agent = st.number_input("Agent ID", value=77)
    status = st.text_input("New Status", value="closed")

    if st.button("Assign Agent"):
        st.json(assign_ticket(ticket, agent))

    if st.button("Update Ticket Status"):
        st.json(update_ticket_status(ticket, status))

# ------------------------------------------
# KPIS
# ------------------------------------------
with tab4:
    st.subheader("KPI Overview")

    if st.button("Load KPIs"):
        st.json(get_kpi_summary())

