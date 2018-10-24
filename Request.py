import requests

data = {
    'username': 'Bond',
    # 'email': 'james@mi6.uk',
    # 'password': 'germanyfirst123',
    # 'groups': ['agents', 'crew'],
    # 'date_joined':'',
    # 'email_user':'',
    # 'first_name':'',
    # 'id':'',
    # 'is_active':'',
    # 'is_anonymous':'',
    # 'is_authenticated':'',
    # 'is_staff':'',
    # 'is_superuser':'',
    # 'last_login':'',
    # 'last_name':'',
    # 'logentry_set':'',
    # 'master':'',
    # 'natural_key':'',
    # 'orders':'',
    # 'pk':'',
    # 'serializable_value':'',
    # 'user_permissions':'',
}


r = requests.post(
    'http://127.0.0.1:8000/regi/', 
    params=data, 
    # headers={
    #     'X-CSRFToken':
    #     'dUqV1iuSqgobFbkW8IWBsRrKSyBeb3eowwtABEvLho4irD78NGj26myE4xQD0ham'
    # }
)

print(r)
print(r.text)


