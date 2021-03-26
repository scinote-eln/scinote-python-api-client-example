from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib import error
from settings import settings
import json
import time

# Firstly check if tokens are set
if not settings['access_token']:
    puts("access token is not set")
    quit()

# Check if access token has expired and get a new one if it has
# This code if an example how to handle the expired tokens and should be used thoroughout the client app
if (settings['access_token_created_at'] + settings['access_token_expires_in'] < int(time.time())):
    print("Access token has expired, fetching a new one using refresh token")
    
    url = settings['server_url'] + "/oauth/token"
    post_fields = {'grant_type': 'refresh_token',
                    'client_id': settings['api_uid'],
                    'client_secret': settings['api_secret'],
                    'redirect_uri': settings['api_redirect_uri'],
                    'refresh_token': settings['refresh_token']
    }     

    payload = json.dumps(post_fields).encode('utf-8')

    request = Request(url)
    request.add_header('Content-Type', 'application/json; charset=utf-8')
    request.add_header('Content-Length', len(payload))
    request.add_header('Accept', 'application/json')
    try:
        response = urlopen(request, payload)
    except error.HTTPError:
        print("HTTP request failed when refreshing a token")
        quit()

    try:
        json_response = json.loads(response.read().decode())
    except:
        print("Parsing response to json failed when refreshing a token")
        quit()
    
    print("Successfully got new token pair")
    print("Writing new tokens to the settings file")
    settings['access_token'] = json_response['access_token']
    settings['refresh_token'] = json_response['refresh_token']
    settings['access_token_created_at'] = json_response['created_at']
    settings['access_token_expires_in'] = json_response['expires_in']

    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=2)


# Finally the API part, access the projects
# Mind that url is defined to catch projects from teams with id 1
# You can change this if you wish
api_url = settings['server_url'] + "/api/v1/teams/1/projects"
api_request = Request(api_url)
api_request.add_header('Authorization', 'Bearer ' + settings['access_token'])
try:
    api_response = urlopen(api_request)
except:
    print("HTTP request failed when fetching projects")
    quit()

try:
    json_api_response = json.loads(api_response.read().decode())
except:
    print("Parsing response into json failed when fetching projects")
    quit()

print("Listing projects")
print("-------------------")
for project in json_api_response['data']:
    print(project['attributes']['name'])
print("-------------------")