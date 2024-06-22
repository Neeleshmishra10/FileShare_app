import requests

token_url = 'http://localhost:8000/api/token/'
upload_url = 'http://127.0.0.1:8000/api/upload/file/'

#  user credentials
credentials = {
    'username': 'neelesh',
    'password': 'password123'
}

#  token
token_response = requests.post(token_url, data=credentials)
token_data = token_response.json()
access_token = token_data.get('access')

if not access_token:
    print("Error obtaining token:", token_data)
    exit()

print(f"Access Token: {access_token}")

# headers including the token
headers = {
    'Authorization': f'Bearer {access_token}',
}


file_path = 'http://127.0.0.1:8000/api/upload/file.txt/'  

with open(file_path, 'rb') as file:
    files = {'file': file}
    upload_response = requests.post(upload_url, headers=headers, files=files)
    print(upload_response.json())
