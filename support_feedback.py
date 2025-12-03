from api_mock import API_GATEWAY

# Sample feedback list while KPIs are not functional
feedback_store = {
    301: {"feedback_id": 301, "client_id": 1001, "text": "Points did not update", "status": "open", "response": None},
    302: {"feedback_id": 302, "client_id": 1002, "text": "Reward not delivered", "status": "open", "response": None},
    303: {"feedback_id": 303, "client_id": 1003, "text": "Great service!", "status": "addressed", "response": "Thank you!"}
}

def get_all_feedback():
    return list(feedback_store.values())

def respond_to_feedback(feedback_id, response_text):
    if feedback_id not in feedback_store:
        return {"error": "Feedback not found"}

    feedback_store[feedback_id]["response"] = response_text
    feedback_store[feedback_id]["status"] = "addressed"
    return feedback_store[feedback_id]

def resolve_feedback(feedback_id):
    if feedback_id not in feedback_store:
        return {"error": "Feedback not found"}

    feedback_store[feedback_id]["status"] = "resolved"
    return feedback_store[feedback_id]

# Ticket assignmwnt and review
from api_mock import API_GATEWAY

def assign_ticket(ticket_id, agent_id):
    payload = {"ticket_id": ticket_id, "agent_id": agent_id}
    response = API_GATEWAY.PATCH("/support/ticket/assign", payload)
    return response.data if response.status == 200 else {"error": response.error}

def update_ticket_status(ticket_id, status):
    payload = {"ticket_id": ticket_id, "status": status}
    response = API_GATEWAY.PATCH("/support/ticket/status", payload)
    return response.data if response.status == 200 else {"error": response.error}
