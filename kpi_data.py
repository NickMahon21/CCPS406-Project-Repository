from api_mock import API_GATEWAY

#Mock statistics to represent what could be with live data
def get_kpi_summary():
    tickets = API_GATEWAY.tickets
    rewards = API_GATEWAY.rewards

    return {
        "open_tickets": len([t for t in tickets.values() if t["status"] == "open"]),
        "total_rewards": len(rewards),
        "feedback_count": 4,  # static example
        "avg_response_time": 12.4  # mocked KPI
    }
