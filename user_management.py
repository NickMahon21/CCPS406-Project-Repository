from api_mock import API_GATEWAY

def assign_role(user_id, role_id):
    payload = {"user_id": user_id, "role_id": role_id}
    response = API_GATEWAY.POST("/user-management/assign-role", payload)
    return response.data if response.status == 200 else {"error": response.error}

def get_user_profile(user_id):
    response = API_GATEWAY.GET(f"/user-management/user/{user_id}")
    return response.data if response.status == 200 else {"error": response.error}
