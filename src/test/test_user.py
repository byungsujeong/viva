from database.repository import UserRepository
from database.orm import User

from service.userService import UserService


def test_user_sign_up_success(client, mocker,):
    hash_password = mocker.patch.object(
        UserService,
        "hash_password",
        return_value="hashed"
    )
    user_create = mocker.patch.object(
        User,
        "create",
        return_value=User(id=None, email="user1@viva.com", password="hashed", username="user1", is_active=None)
    )
    mocker.patch.object(
        UserRepository,
        "create_user",
        return_value=User(id=1, email="user1@viva.com", password="hashed", username="user1", is_active=True)
    )

    body = {
        "eamil": "user1@viva.com",
        "password": "1q2w3e4rA!",
        "username": "user1",
    }

    response = client.post("/users/sign-up", json=body)
    
    hash_password.assert_called_once_with(
        password="1q2w3e4rA!"
    )
    user_create.assert_called_once_with(
        email="user1@viva.com",
        hashed_password="hashed",
        username="user1",
    )
    assert response.status_code == 201
    assert response.json() == {
        "id":1, "email": "user1@viva.com", "password": "hashed", "username": "user1"
    }  