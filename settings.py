import json
import urllib.parse

try:
    with open('settings.json') as json_file:
        settings = json.load(json_file)
except:
    print("Couldn't load settings file, please check settings.json is present in current folder")
    quit()

auth_code_url = (
    settings['server_url'] +
    "/oauth/authorize?client_id=" +
    settings['api_uid'] + 
    "&redirect_uri=" +
    urllib.parse.quote(settings['api_redirect_uri']) +
    "&response_type=code"
)
