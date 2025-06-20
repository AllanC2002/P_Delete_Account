import requests

BASE_URL = "http://localhost:8081"

# 1. Login para obtener token
login_data = {
    "User_mail": "alla@coorreea",
    "password": "1234"
}

resp_login = requests.post(f"http://localhost:8080/login", json=login_data)

if resp_login.status_code != 200:
    print("Error al hacer login:", resp_login.status_code, resp_login.json())
    exit()

token = resp_login.json().get("token")
print("Token JWT:", token)

# 2. Usar token para eliminar cuenta
headers = {
    "Authorization": f"Bearer {token}"
}

resp_delete = requests.delete(f"{BASE_URL}/delete-account", headers=headers)

print("Respuesta al eliminar cuenta:", resp_delete.status_code, resp_delete.json())
