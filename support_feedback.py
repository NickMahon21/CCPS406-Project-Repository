from api_mock import API_GATEWAY

def assign_ticket(ticket_id, agent_id):
    payload = {"ticket_id": ticket_id, "agent_id": agent_id}
    response = API_GATEWAY.PATCH("/support/ticket/assign", payload)
    return response.data if response.status == 200 else {"error": response.error}

def update_ticket_status(ticket_id, status):
    payload = {"ticket_id": ticket_id, "status": status}
    response = API_GATEWAY.PATCH("/support/ticket/status", payload)
    return response.data if response.status == 200 else {"error": response.error}

