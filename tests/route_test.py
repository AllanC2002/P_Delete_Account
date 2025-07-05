import requests

BASE_URL = "http://3.212.156.160:8081"

login_data = {
    "User_mail": "allancorrea2",
    "password": "1234"
}

resp_login = requests.post(f"http://52.203.72.116:8080/login", json=login_data)

if resp_login.status_code != 200:
    print("Error al hacer login:", resp_login.status_code, resp_login.json())
    exit()

token = resp_login.json().get("token")
print("Token JWT:", token)

headers = {
    "Authorization": f"Bearer {token}"
}

resp_delete = requests.delete(f"{BASE_URL}/delete-account", headers=headers)

print("Response:", resp_delete.status_code, resp_delete.json())
