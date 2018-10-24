import requests

r = requests.post(
    'http://127.0.0.1:8000/register/', 
    json={
        'username': 'Boiio',
        # 'password': 'nelson',
    }
)

print(r)
print(r.text)

