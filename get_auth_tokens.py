from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib import error
from settings import settings
import json

url = settings['server_url'] + "/oauth/token"
post_fields = {'grant_type': 'authorization_code',
                'client_id': settings['api_uid'],
                'client_secret': settings['api_secret'],
                'redirect_uri': settings['api_redirect_uri'],
                'code': settings['authorization_code']
}     

payload = json.dumps(post_fields).encode('utf-8')

request = Request(url)
request.add_header('Content-Type', 'application/json; charset=utf-8')
request.add_header('Content-Length', len(payload))
request.add_header('Accept', 'application/json')

try:
    response = urlopen(request, payload)
except error.HTTPError:
    print("HTTP request failed")
    quit()

try:
    json_response = json.loads(response.read().decode())
except:
    print("Parsing response to json failed")
    quit()

if 'json_response' in locals():
    settings['access_token'] = json_response['access_token']
    settings['refresh_token'] = json_response['refresh_token']
    settings['access_token_created_at'] = json_response['created_at']
    settings['access_token_expires_in'] = json_response['expires_in']

    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=2)

    print("Successfully acquired tokens and written them into settings file, you can start testing API using examples")