import requests

data = {
    'username': 'Chevy',
    # 'password': 'pass1234',
}

r = requests.post(
    'http://127.0.0.1:8000/register/', 
    params=data, 
    headers={
        'X-CSRFToken':
        'dUqV1iuSqgobFbkW8IWBsRrKSyBeb3eowwtABEvLho4irD78NGj26myE4xQD0ham'
    }
)

print(r)
print(r.text)


