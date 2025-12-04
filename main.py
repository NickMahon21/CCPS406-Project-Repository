import streamlit as st
import streamlit.components.v1 as components

from user_management import assign_role, get_user_profile
from rewards_management import approve_redemption, adjust_points
from support_feedback import assign_ticket, update_ticket_status, resolve_feedback, get_all_feedback, respond_to_feedback
from kpi_data import get_kpi_summary
from datetime import datetime, timedelta

# -----------------------------------------------------------
# PAGE CONFIG & CSS STYLES
# -----------------------------------------------------------
st.set_page_config(
    page_title="BizPoints Admin Dashboard",
    layout="wide"
)

# CSS for cleaner UI
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
    ["Dashboard Overview", "User Management", "Rewards Management", "Support Tickets & Feedback", "Content Management"]
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
elif page == "Rewards Management":
    st.markdown('<div class="section-header">Rewards & Redemption Management</div>', unsafe_allow_html=True)

    # ------------------------------
    # POINT REDEMPTION SECTION
    # ------------------------------
    st.subheader("💰 Reward Adjustments & Redemptions")

    with st.expander("🎁 Approve Redemption Request"):
        account = st.number_input("Account ID", value=1001)
        reward = st.number_input("Reward ID", value=20)
        user = st.number_input("User Redeeming (User ID)", value=1)
        if st.button("Approve Redemption"):
            st.json(approve_redemption(account, reward, user))

    # ------------------------------
    # POINT ADJUSTMENT SECTION
    # ------------------------------
    with st.expander("➕➖ Point Adjustments"):
        account_adj = st.number_input("Account ID (Adjustment)", value=1001)
        user_adj = st.number_input("Admin User ID", value=1)
        amount_adj = st.number_input("Adjustment Amount (+ or -)", value=0)
        reason_adj = st.text_input("Adjustment Reason", value="Manual adjustment")
        if st.button("Submit Adjustment"):
            st.json(adjust_points(account_adj, user_adj, amount_adj, reason_adj))

    # ------------------------------
    # REWARDS CATALOGUE MANAGEMENT
    # ------------------------------
    st.subheader("📘 Rewards Catalogue Management")

    # Initialize session state for catalogue
    if "rewards_catalogue" not in st.session_state:
        st.session_state.rewards_catalogue = {
            1: {"name": "Free Coffee", "cost": 80},
            2: {"name": "Gift Card $10", "cost": 250},
            3: {"name": "Company Mug", "cost": 150}
        }

    # Display catalogue
    with st.expander("📦 View Rewards Catalogue"):
        for reward_id, info in st.session_state.rewards_catalogue.items():
            st.write(f"**ID:** {reward_id} | **Reward:** {info['name']} | **Cost:** {info['cost']} points")

    # Add new reward
    with st.expander("➕ Add Reward"):
        new_name = st.text_input("Reward Name")
        new_cost = st.number_input("Reward Cost (points)", min_value=1)

        if st.button("Add Reward"):
            new_id = max(st.session_state.rewards_catalogue.keys()) + 1
            st.session_state.rewards_catalogue[new_id] = {"name": new_name, "cost": new_cost}
            st.success("Reward added successfully.")

    # Update or delete rewards
    with st.expander("✏️ Update / Delete Reward"):
        reward_ids = list(st.session_state.rewards_catalogue.keys())
        selected_reward = st.selectbox("Select Reward ID", reward_ids)

        updated_name = st.text_input(
            "Updated Name", 
            value=st.session_state.rewards_catalogue[selected_reward]["name"]
        )
        updated_cost = st.number_input(
            "Updated Cost", 
            value=st.session_state.rewards_catalogue[selected_reward]["cost"]
        )

        if st.button("Update Reward"):
            st.session_state.rewards_catalogue[selected_reward]["name"] = updated_name
            st.session_state.rewards_catalogue[selected_reward]["cost"] = updated_cost
            st.success("Reward updated successfully.")

        if st.button("Delete Reward"):
            del st.session_state.rewards_catalogue[selected_reward]
            st.success("Reward deleted successfully.")



# -----------------------------------------------------------
# SUPPORT AND  FEEDBACK                
# -----------------------------------------------------------
elif page == "Support Tickets & Feedback":
    st.markdown('<div class="section-header">Support & Feedback Management</div>', unsafe_allow_html=True)

    # ------------------------------------------
    # SUPPORT TICKETS
    # ------------------------------------------
    st.subheader("🎫 Support Ticket Actions")

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

    # ------------------------------------------
    # FEEDBACK HANDLING SECTION
    # ------------------------------------------
    st.subheader("📝 Client Feedback")

    # Display all feedback
    with st.expander("📄 View All Feedback"):
        feedback_list = get_all_feedback()

        for fb in feedback_list:
            st.write(f"**Feedback ID:** {fb['feedback_id']}")
            st.write(f"**Client ID:** {fb['client_id']}")
            st.write(f"**Text:** {fb['text']}")
            st.write(f"**Status:** {fb['status']}")
            st.write(f"**Response:** {fb['response']}")
            st.markdown("---")

    # Respond to feedback
    with st.expander("✉️ Respond to Feedback"):
        fb_id = st.number_input("Feedback ID", value=301)
        response_text = st.text_area("Response Message")
        if st.button("Submit Response"):
            st.json(respond_to_feedback(fb_id, response_text))

    # Mark feedback as resolved
    with st.expander("✔️ Mark Feedback as Resolved"):
        fb_id_res = st.number_input("Feedback ID to Resolve", value=302)
        if st.button("Mark Resolved"):
            st.json(resolve_feedback(fb_id_res))

# -----------------------------------------------------------
# CONTENT MANAGEMENT — EVENTS & TRAINING CALENDAR
# -----------------------------------------------------------
elif page == "Content Management":
    st.markdown('<div class="section-header">Training & Event Calendar</div>', unsafe_allow_html=True)

    st.subheader("📚 Training Material Management")

    # Initialize training storage
    if "training_materials" not in st.session_state:
        st.session_state.training_materials = {}

    # Upload section
    with st.expander("📤 Upload Training Material"):
        uploaded_file = st.file_uploader("Upload PDF, DOCX, or PPTX", type=["pdf", "docx", "pptx"])

        material_name = st.text_input("Material Title")

        if st.button("Upload Material"):
            if uploaded_file and material_name:
                st.session_state.training_materials[material_name] = uploaded_file.getvalue()
                st.success("Material uploaded successfully!")
            else:
                st.error("Please provide a title and upload a file.")

    # View & manage materials
    with st.expander("📁 View / Manage Uploaded Materials"):
        if st.session_state.training_materials:
            selected_material = st.selectbox("Select Material", list(st.session_state.training_materials.keys()))

            if st.button("Download Material"):
                st.download_button(
                    label="Download File",
                    data=st.session_state.training_materials[selected_material],
                    file_name=selected_material,
                )

            if st.button("Delete Material"):
                del st.session_state.training_materials[selected_material]
                st.success("Material deleted successfully.")
        else:
            st.info("No training materials uploaded yet.")

    
    # Initialize session state for calendar events
    if "calendar_events" not in st.session_state:
        st.session_state.calendar_events = []

    # ------------------------------
    # ADD NEW EVENT / TRAINING
    # ------------------------------
    st.subheader("➕ Add Event / Training")

    title = st.text_input("Title")
    event_type = st.selectbox("Type", ["Event", "Training"])
    date = st.date_input("Date")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")

    if st.button("Add Entry"):
        start_dt = datetime.combine(date, start_time)
        end_dt = datetime.combine(date, end_time)

        color = "#FF4B4B" if event_type == "Event" else "#9B59B6"  # red or purple

        st.session_state.calendar_events.append({
            "title": f"{event_type}: {title}",
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "color": color,
        })
        st.success(f"{event_type} added successfully!")

    # ------------------------------
    # DELETE EVENT / TRAINING
    # ------------------------------
    st.subheader("🗑 Delete Entry")

    if st.session_state.calendar_events:
        event_titles = [e["title"] for e in st.session_state.calendar_events]
        delete_choice = st.selectbox("Select Entry to Delete", event_titles)

        if st.button("Delete Entry"):
            st.session_state.calendar_events = [
                e for e in st.session_state.calendar_events if e["title"] != delete_choice
            ]
            st.success("Entry deleted successfully!")
    else:
        st.info("No events or trainings available to delete.")

    # ------------------------------
    # RENDER CALENDAR
    # ------------------------------
    calendar_options = {
        "initialView": "timeGridWeek",
        "editable": False,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "timeGridWeek,timeGridDay",
        },
        "slotMinTime": "08:00:00",
        "slotMaxTime": "20:00:00",
    }

    # Convert Python list → JS array
    import json
    events_json = json.dumps(st.session_state.calendar_events)

    calendar_html = f"""
    <div id='calendar'></div>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css'>
    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js'></script>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {{
                initialView: '{calendar_options["initialView"]}',
                editable: {str(calendar_options["editable"]).lower()},
                selectable: {str(calendar_options["selectable"]).lower()},
                headerToolbar: {{
                    left: '{calendar_options["headerToolbar"]["left"]}',
                    center: '{calendar_options["headerToolbar"]["center"]}',
                    right: '{calendar_options["headerToolbar"]["right"]}',
                }},
                slotMinTime: '{calendar_options["slotMinTime"]}',
                slotMaxTime: '{calendar_options["slotMaxTime"]}',
                events: {events_json}
            }});
            calendar.render();
        }});
    </script>
    """

    components.html(calendar_html, height=700, scrolling=True)
