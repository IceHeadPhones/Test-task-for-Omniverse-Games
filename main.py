import requests

credentials = {"username": "example_user", "password": "example_password"}
credentials_invalid = {"login": "example_usertt", "password": "example_passwordddd"}
user_ids = ["3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-4562-b3fc-2c963f66afa7"]
user_ids_invalid = ["3fa85f64-5717-4562-b3fc-2c963f66afgbfbbfga6", "3fa85f64-5717-4562-b3fc-2c963f66afa7"]
user_ids3 = ["3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-4562-b3fc-2c963f66afa7", "3fa85f64-5717-4562-b3fc-2c963f66afa8"]

def test_authentication_start_battle_end_battle():
    """
    Позитивный тестовый сценарий всех эндпоинтов
    """
    response = requests.post(url="https://testers-task.omniversegames.ru/login", json=credentials)
    assert response.status_code == 200
    jwt_token = response.json()['access_token']

    data = {"users": user_ids}
    response = requests.post(url="https://testers-task.omniversegames.ru/battle/start",
                             headers={"Authorization": 'Bearer ' + jwt_token}, json=data)
    assert response.status_code == 200
    battle_id = response.json()['battle_id']

    payload = {
        "battle_id": battle_id,
        "results": {
            user_ids[0]: {"is_won": True},
            user_ids[1]: {"is_won": False}
        }
    }
    response = requests.post(url="https://testers-task.omniversegames.ru/battle/end", json=payload,
                             headers={"Authorization": 'Bearer ' + jwt_token})
    assert response.status_code == 200


def test_authentication():
    """
    Негативный тестовый сценарий
    для некорректной авторизации
    """
    response = requests.post(url="https://testers-task.omniversegames.ru/login", json=credentials_invalid)
    assert response.status_code == 422


def test_start_with_invalid_user_count():
    """
    Негативный тестовый сценарий
    для начала боя с некорретным количеством ID юзера
    """
    response = requests.post(url="https://testers-task.omniversegames.ru/login", json=credentials)
    assert response.status_code == 200
    data = {"users": [user_ids[0]]}
    jwt_token = response.json()['access_token']
    response = requests.post(url="https://testers-task.omniversegames.ru/battle/start",
                             headers={"Authorization": "Bearer " + jwt_token}, json=data)
    assert response.status_code == 400
    print("response.text", response.text)


def test_end_battle_with_no_id():
    """
    Негативный тестовый сценарий
    для завершения боя с отсутствием ID боя
    """
    response = requests.post(url="https://testers-task.omniversegames.ru/login", json=credentials)
    assert response.status_code == 200
    data = {"users": user_ids}
    jwt_token = response.json()['access_token']
    response = requests.post(url="https://testers-task.omniversegames.ru/battle/start",
                             headers={"Authorization": "Bearer " + jwt_token}, json=data)
    assert response.status_code == 200

    payload = {
        "results": {
            user_ids[0]: {"is_won": True},
            user_ids[1]: {"is_won": False}
        }
    }

    response = requests.post(url="https://testers-task.omniversegames.ru/battle/end", json=payload,
                             headers={"Authorization": 'Bearer ' + jwt_token})
    assert response.status_code == 422


def test_start_battle_with_invalid_uuid4():
    """
    Негативный тестовый сценарий
    для начала боя с некорретным ID юзера
    """
    response = requests.post(url="https://testers-task.omniversegames.ru/login", json=credentials)
    assert response.status_code == 200
    data = {"users": user_ids_invalid}
    jwt_token = response.json()['access_token']
    response = requests.post(url="https://testers-task.omniversegames.ru/battle/start",
                             headers={"Authorization": "Bearer " + jwt_token}, json=data)
    assert response.status_code == 422


def test_start_battle_with_3_users():
    """
    Негативный тестовый сценарий
    для начала боя с 3-мя юзерами
    """
    response = requests.post(url="https://testers-task.omniversegames.ru/login", json=credentials)
    assert response.status_code == 200
    jwt_token = response.json()['access_token']

    data = {"users": user_ids3}
    response = requests.post(url="https://testers-task.omniversegames.ru/battle/start",
                             headers={"Authorization": 'Bearer ' + jwt_token}, json=data)
    assert response.status_code == 400