import requests

# Step 1: Obtain the token
token_url = 'http://localhost:8000/api/token/'
login_data = {
    'username': 'Neelesh',  # Replace with your username
    'password': 'password123'   # Replace with your password
}

response = requests.post(token_url, data=login_data)
if response.status_code == 200:
    token = response.json().get('access')
    print(f"Access Token: {token}")
else:
    print("Failed to obtain token:", response.json())
    exit(1)

# Step 2: Use the token to upload a file
upload_url = 'http://localhost:8000/api/upload/'
file_path = 'path/to/your/file.pdf'  # Replace with the actual path to your file

headers = {
    'Authorization': f'Bearer {token}',
}

files = {'file': open(file_path, 'rb')}
upload_response = requests.post(upload_url, headers=headers, files=files)

if upload_response.status_code == 201:
    print("File uploaded successfully:", upload_response.json())
else:
    print("Failed to upload file:", upload_response.json())
