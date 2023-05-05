import requests

# Set up the request data
token = "<your_access_token>"
url = "https://api.linkedin.com/v2/oauth/token/introspect"
data = {
    "client_id": "<your_client_id>",
    "client_secret": "<your_client_secret>",
    "token": token
}

# Make the request and print the response
response = requests.post(url, data=data)
print(response.json())
