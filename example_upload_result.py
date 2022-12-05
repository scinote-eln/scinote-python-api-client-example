from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
from urllib import error
from settings import settings
import json
import time
import base64

# To upload the result, you need to specify the full path to the task
# so we need to set up some ids
# more info: https://scinote-eln.github.io/scinote-api-v1-docs/#create-result

TEAM_ID = "21"
PROJECT_ID = "606"
EXPERIMENT_ID = "1657"
TASK_ID = "9865"

# Let's set some attributes of the file we want to upload
RESULT_FILE_PATH = "./sample_data/ecoli.jpg"
RESULT_FILE_TYPE = "image/jpg"
RESULT_FILE_NAME = "ecoli_result.jpg"

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


# Read the content of the file and store it into variable as Base64
file_content = open(RESULT_FILE_PATH, "rb").read()
b64_file_content = base64.b64encode(file_content).decode('ascii')

# Finally the API part

# Firstly let's build the payload for the POST REQUEST

payload = {
  'data': {
    'type': 'results',
    'attributes':{
      'name': "Ecoli result image"
    }
  },
  'included': [
      {
        'type': 'result_files',
        'attributes': {
          'file_name': RESULT_FILE_NAME,
          'file_type': RESULT_FILE_TYPE,
          'file_data': b64_file_content
        }
      }
    ]
  }


# In the second step we'll build headers
bearer_token_string = 'Bearer ' + settings['access_token']
headers = {
  'Content-Type': 'application/vnd.api+json',
  'Authorization': bearer_token_string
}

# And finally let's fire the POST request
api_url = settings['server_url'] + "/api/v1/teams/" + TEAM_ID + "/projects/" + PROJECT_ID + "/experiments/" + EXPERIMENT_ID + "/tasks/" + TASK_ID + "/results"
api_request = requests.post(url = api_url, headers = headers, data = json.dumps(payload))

print(api_request.text)