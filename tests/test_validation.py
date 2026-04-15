from src.app import activities


def test_signup_duplicate_keeps_participant_count_unchanged(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity]["participants"])

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
    assert final_count == initial_count


def test_unregister_returns_consistent_error_contract(client):
    # Arrange
    activity = "Art Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert "detail" in payload
    assert payload["detail"] == "Participant not found in this activity"


def test_signup_full_activity_returns_400(client):
    # Arrange
    activity = "Art Club"
    max_participants = activities[activity]["max_participants"]
    activities[activity]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]
    email = "overflow.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_full_activity_keeps_participants_unchanged(client):
    # Arrange
    activity = "Art Club"
    max_participants = activities[activity]["max_participants"]
    activities[activity]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]
    email = "overflow.student@mergington.edu"
    initial_count = len(activities[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    final_count = len(activities[activity]["participants"])

    # Assert
    assert response.status_code == 400
    assert final_count == initial_count