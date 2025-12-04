from api_mock import API_GATEWAY

#Temporary data assignment while API calls are not functional
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

def adjust_points(account_id, user_id, amount, reason):
    # 1. Retrieve current balance
    balance_res = API_GATEWAY.GET(f"/loyalty/balance/{account_id}")
    if balance_res.status != 200:
        return {"error": "Balance unavailable"}

    current_balance = balance_res.data["balance"]

    # 2. Adjust points (positive or negative)
    new_balance = current_balance + amount

    # Prevent negative point totals
    if new_balance < 0:
        return {"error": "Adjustment would result in negative balance"}

    # 3. Apply adjustment
    API_GATEWAY.loyalty_balance[account_id] = new_balance

    # 4. Build adjustment record (mock)
    adjustment_record = {
        "account_id": account_id,
        "user_id": user_id,
        "amount": amount,
        "new_balance": new_balance,
        "reason": reason
    }

    return adjustment_record
