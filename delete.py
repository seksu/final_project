import requests
s = requests.Session()
s.post('http://161.246.5.160:8000/login/', json = { "email" : "admin@admin.com",
                                                    "password" : "testadmin" })
response = s.get('http://161.246.5.160:8000/delete/searching_detail/')
print(response.content)
