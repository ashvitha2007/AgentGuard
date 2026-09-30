import requests

BACKEND_URL = "http://localhost:8000"

def check_agent_action(action_type, description, target=None, data_classification="public"):
    response = requests.post(
        f"{BACKEND_URL}/api/actions/evaluate",
        headers={"Authorization": "Bearer YOUR_TOKEN"},
        json={
            "action_type": action_type,
            "description": description,
            "target": target,
            "data_classification": data_classification,
            "data_source": "agent",
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("Replace YOUR_TOKEN with a login token before running this client.")
