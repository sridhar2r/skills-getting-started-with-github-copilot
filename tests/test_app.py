from fastapi.testclient import TestClient
import urllib.parse

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Some known activities should exist
    assert "Chess Club" in data


def test_signup_and_delete_flow():
    activity_name = "Chess Club"
    email = "teststudent@example.com"

    # Ensure clean state
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Signup
    encoded_activity = urllib.parse.quote(activity_name, safe="")
    signup_res = client.post(f"/activities/{encoded_activity}/signup?email={urllib.parse.quote(email, safe='')}")
    assert signup_res.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Signup twice should fail
    dup_res = client.post(f"/activities/{encoded_activity}/signup?email={urllib.parse.quote(email, safe='')}")
    assert dup_res.status_code == 400

    # Delete the participant
    delete_res = client.delete(f"/activities/{encoded_activity}/participants?email={urllib.parse.quote(email, safe='')}")
    assert delete_res.status_code == 200
    assert email not in activities[activity_name]["participants"]

    # Deleting again should return 404
    delete_again = client.delete(f"/activities/{encoded_activity}/participants?email={urllib.parse.quote(email, safe='')}")
    assert delete_again.status_code == 404
