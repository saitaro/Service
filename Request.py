import requests

r = requests.post(
    'http://127.0.0.1:8000/register/', 
    json={
        'username': 'Boyyo',
        # 'password': 'nelson',
    }
)

print(r)
print(r.text)
 
