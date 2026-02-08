from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # check a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    email = "test_student@mergington.edu"

    # Ensure not already signed up
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    if email in participants:
        # remove to ensure clean state
        resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
        assert resp.status_code == 200

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Signed up")

    # Confirm participant present
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Unregistered")

    # Confirm removed
    resp = client.get(f"/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants
