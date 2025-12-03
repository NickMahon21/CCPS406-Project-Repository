import random

class MockResponse:
    def __init__(self, status, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error

class MockAPI:
    def __init__(self):
        self.users = {
            1: {"user_id": 1, "name": "Alice", "role_id": 2},
            2: {"user_id": 2, "name": "Bob", "role_id": 1},
        }

        self.rewards = {
            10: {"reward_id": 10, "name": "Gift Card", "cost": 100},
            20: {"reward_id": 20, "name": "Coffee Coupon", "cost": 20},
        }

        self.loyalty_balance = {
            1001: 200  # account_id → points
        }

        self.tickets = {
            501: {"ticket_id": 501, "status": "open", "agent_id": None}
        }

    # -----------------------------
    # GET Requests
    # -----------------------------
    def GET(self, endpoint):
        if endpoint.startswith("/user-management/user/"):
            user_id = int(endpoint.split("/")[-1])
            return self._get_user(user_id)

        if endpoint.startswith("/loyalty/balance/"):
            account = int(endpoint.split("/")[-1])
            return self._get_balance(account)

        if endpoint.startswith("/rewards/"):
            reward = int(endpoint.split("/")[-1])
            return self._get_reward(reward)

        return MockResponse(400, error="Invalid GET endpoint")

    # Internal GET handlers
    def _get_user(self, user_id):
        return MockResponse(200, self.users[user_id]) if user_id in self.users else MockResponse(404, error="User not found")

    def _get_balance(self, account):
        return MockResponse(200, {"balance": self.loyalty_balance[account]}) if account in self.loyalty_balance else MockResponse(404, error="Account not found")

    def _get_reward(self, reward):
        return MockResponse(200, self.rewards[reward]) if reward in self.rewards else MockResponse(404, error="Reward not found")

    # -----------------------------
    # POST Requests
    # -----------------------------
    def POST(self, endpoint, payload):
        if endpoint == "/user-management/assign-role":
            return self._assign_role(payload)

        if endpoint == "/loyalty/redeem":
            return self._redeem_points(payload)

        return MockResponse(400, error="Invalid POST endpoint")

    def _assign_role(self, payload):
        user_id = payload["user_id"]
        role = payload["role_id"]

        if user_id not in self.users:
            return MockResponse(404, error="User not found")

        self.users[user_id]["role_id"] = role
        return MockResponse(200, self.users[user_id])

    def _redeem_points(self, payload):
        account = payload["account_id"]
        reward = payload["reward_id"]

        cost = self.rewards[reward]["cost"]
        self.loyalty_balance[account] -= cost
        return MockResponse(200, {"transaction_id": random.randint(10000, 99999)})

    # -----------------------------
    # PATCH Requests
    # -----------------------------
    def PATCH(self, endpoint, payload):
        if endpoint == "/support/ticket/assign":
            return self._assign_ticket(payload)

        if endpoint == "/support/ticket/status":
            return self._update_ticket(payload)

        return MockResponse(400, error="Invalid PATCH endpoint")

    def _assign_ticket(self, payload):
        ticket = payload["ticket_id"]
        agent = payload["agent_id"]

        if ticket not in self.tickets:
            return MockResponse(404, error="Ticket not found")

        self.tickets[ticket]["agent_id"] = agent
        return MockResponse(200, self.tickets[ticket])

    def _update_ticket(self, payload):
        ticket = payload["ticket_id"]
        status = payload["status"]

        if ticket not in self.tickets:
            return MockResponse(404, error="Ticket not found")

        self.tickets[ticket]["status"] = status
        return MockResponse(200, self.tickets[ticket])


# Global API instance shared by all modules
API_GATEWAY = MockAPI()

