import requests
from pprint import pprint
import json
main_link = 'https://api.github.com/users'
user_name = 'Bernatov'
req = requests.get(f'{main_link}/{user_name}/repos')
if req.ok:
    data = json.loads(req.text)
print(f'Список репозиториев пользователя {user_name}:')
for i in data:
    print(i['name'])

with open('Bernatov.json','wb') as file:
    file.write(req.content)



