from api_mock import API_GATEWAY

def approve_redemption(account_id, reward_id, user_id):
    balance_res = API_GATEWAY.GET(f"/loyalty/balance/{account_id}")
    if balance_res.status != 200:
        return {"error": "Balance unavailable"}

    reward_res = API_GATEWAY.GET(f"/rewards/{reward_id}")
    if reward_res.status != 200:
        return {"error": "Reward unavailable"}

    balance = balance_res.data["balance"]
    cost = reward_res.data["cost"]

    if balance < cost:
        return {"error": "Insufficient Points"}

    payload = {
        "account_id": account_id,
        "reward_id": reward_id,
        "user_id": user_id
    }

    confirmation = API_GATEWAY.POST("/loyalty/redeem", payload)
    return confirmation.data if confirmation.status == 200 else {"error": confirmation.error}

