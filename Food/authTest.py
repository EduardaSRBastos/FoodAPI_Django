import requests

def make_food_list_request():
    url = 'http://localhost:8000/food/'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1Njk2NTc1LCJpYXQiOjE2ODU2OTYyNzUsImp0aSI6ImJhMTFiYTQ3ZGYyZTQ2ZjFhN2FmOWRkNmY1YTk3NmE4IiwidXNlcl9pZCI6NCwidXNlcm5hbWUiOiJhZG1pbjUifQ.vlkD8iHp0Ikeh7_s5FlPWEiQRaHT51NQAQ-9RIunEyI'
    }

    response = requests.get(url, headers=headers)
    print(response.json())

# Call the function to make the API request
make_food_list_request()