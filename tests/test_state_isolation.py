def test_state_isolation_mutates_activity_in_this_test_only(client):
    # Arrange
    activity = "Art Club"
    email = "isolated.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    participants = client.get("/activities").json()[activity]["participants"]

    # Assert
    assert response.status_code == 200
    assert email in participants


def test_state_isolation_starts_clean_for_next_test(client):
    # Arrange
    activity = "Art Club"
    email = "isolated.student@mergington.edu"

    # Act
    participants = client.get("/activities").json()[activity]["participants"]

    # Assert
    assert email not in participants