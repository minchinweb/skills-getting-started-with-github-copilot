from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu"],
            },
        }
    )


def test_get_activities_returns_seed_data():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_student_to_activity():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unknown_activity_signup_returns_404():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_student_from_activity():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_student_returns_404():
    # Arrange
    reset_activities()
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
