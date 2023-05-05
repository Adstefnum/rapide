import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your client ID, secret, and callback URL here
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CALLBACK_URL = os.getenv('CALLBACK_URL')

# Set the API base URL
BASE_URL = 'https://api.linkedin.com/v2'

# Set the requested scopes
SCOPES = ['r_liteprofile', 'r_emailaddress', 'w_member_social']

# Set the redirect URL for user authorization
authorization_url = f'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK_URL}&state=foobar&scope={"+".join(SCOPES)}'

# Redirect the user to the authorization URL
print(f'Please go to this URL to authorize your application: {authorization_url}')

# After the user authorizes your application, your callback URL will receive an authorization code that you can use to obtain an access token.

# Set the authorization code here
authorization_code = input('Please enter the authorization code: ')

# Exchange the authorization code for an access token
access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
access_token_params = {'grant_type': 'authorization_code',
                       'code': authorization_code,
                       'redirect_uri': CALLBACK_URL,
                       'client_id': CLIENT_ID,
                       'client_secret': CLIENT_SECRET}
response = requests.post(access_token_url, data=access_token_params)
if response.ok:
    access_token = response.json()['access_token']
    print(f'Successfully obtained access token: {access_token}')
else:
    print(f'Error obtaining access token: {response.status_code} {response.text}')

# Use the access token to retrieve your connections
headers = {'Authorization': f'Bearer {access_token}',
           'Connection': 'Keep-Alive'}
connections_url = 'https://api.linkedin.com/v2/connections?q=viewer&start=0&count=50'
response = requests.get(connections_url, headers=headers)
if response.ok:
    print(response.json())
    connections = response.json()['elements']
    print(f'Successfully retrieved {len(connections)} connections')
else:
    print(f'Error retrieving connections: {response.status_code} {response.text}')

# Filter the connections by those you have not messaged before
connections = response.json()["elements"]
unmessaged_connections = []
for connection in connections:
    messaging_url = f"https://api.linkedin.com/v2/communications?actionCategory=MESSAGE&recipients=List({connection['id']})"
    response = requests.get(messaging_url, headers=headers)
    if response.status_code != 200:
        print("Error getting messaging history:", response.status_code, response.text)
        exit()
    messaging_history = response.json()["elements"]
    if not messaging_history:
        unmessaged_connections.append(connection)

# Send a message to each unmessaged connection
# message = {
#     "subject": "Hello!",
#     "body": "Hey there, I hope you are doing well."
# }
# for connection in unmessaged_connections:
#     messaging_url = f"https://api.linkedin.com/v2/communications?actionCategory=MESSAGE&recipients=List({connection['id']})"
#     response = requests.post(messaging_url, headers=headers, json=message)
#     if response.status_code != 201:
#         print("Error sending message to", connection["firstName"], connection["lastName"], ":", response.status_code, response.text)
#     else:
#         print("Message sent to", connection["firstName"], connection["lastName"])


