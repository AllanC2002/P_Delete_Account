import pytest
from unittest.mock import patch, MagicMock
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True
    with app.test_client() as client:
        yield client

@patch("services.functions.conection_accounts")
@patch("services.functions.conection_userprofile")
@patch("main.jwt.decode") # Mock jwt.decode
def test_delete_account_success(mock_jwt_decode, mock_con_userprofile, mock_con_accounts, client):
    # Simulate JWT decoding
    mock_jwt_decode.return_value = {"user_id": 123}

    # Simulate database connection for accounts
    mock_session_acc = MagicMock()
    mock_con_accounts.return_value = mock_session_acc

    fake_user = MagicMock()
    mock_session_acc.query().filter_by().first.return_value = fake_user

    # Simulate database connection for user profile
    mock_session_profile = MagicMock()
    mock_con_userprofile.return_value = mock_session_profile

    fake_profile = MagicMock()
    mock_session_profile.query().filter_by().first.return_value = fake_profile

    # Execute the DELETE request
    response = client.delete(
        "/delete-account",
        headers={"Authorization": "Bearer test.jwt.token"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User 123 successfully deleted logically"
