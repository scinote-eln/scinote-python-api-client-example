# Basic python client for obtaining access to the SciNote API

## Requirements
- Python 3 with standard lib
- Computer with the access to the SciNote
- SciNote username and password
- SciNote API ID and secret

## Procedure
- Update the settings.json file
- Obtain the authorization code url
- Open the url, sign in, authorize the app
- Copy the authorization code to settings.yml
- Obtain the access and refresh tokens
- Run the example

### Updating the settings.json
Open the settings.json file, it should look a bit like this:
```javascript
{
    "server_url": "",
    "api_uid": "",
    "api_secret": "",
    "api_redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "authorization_code": ""
}
```
Fill in the missing values.
If you're unsure what your server url, api_uid or api_secret are, please contact our support team at support@scinote.net

If you are running local installation of SciNote, you can find the information about setting up the access in ```setting_up_api_access_local_instance.md``` file in this folder. 

You can (and should) leave the 'authorization_code' empty for now. 

### Obtaining the authorization code url
From command prompt run the command
```
python3 get_auth_code.py
```
The command should output an url. Click (or ctrl + click) on it.\* Your browser should open and lead to to SciNote login page.\**
After a successful login, you will be prompted to Authorize the application, which you need to confirm.
After confirmation you will be presented with authorization code. 

Copy that code and paste it into appropriate field in  settings.json. 

```javascript
{
  "server_url": "https://your-instance.scinote.net",
  "api_uid": "xxx",
  "api_secret": "xxx",
  "api_redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
  "authorization_code": "PASTE THE CODE HERE"
}
```
\* you might need to copy the code and paste it into browser
\** if you are already logged into SciNote you will skip the logging-in step


### Obtain access and refresh tokens
From the terminal run:
```
python3 get_auth_tokens.py
```

Hopefully you should see the response
```
Successfully acquired tokens and written them into settings file, you can start testing API using examples
```

You can now check settings.json, you should be able to see some additional values there. 
```javascript
{
  ...
  ...
  "access_token": "xxxxxx",
  "refresh_token": "xxxxx",
  "access_token_created_at": 1616778780,
  "access_token_expires_in": 7200
}
```
Congratulations you are now able to test your api access. 

### Running the example
Our example fetches the list of existing projects in the team with id 1 and outputs their names.

In terminal run following command:

```
python3 example_list_projects.py
```

You should be now able to see the project names listed as an output of the command. 

### Refreshing the access token
Access token will expire in 2 hours. After that, you will need to get a new token. 

The example how the token is refreshed can be found in example_list_projects.py (lines 15-55)

# WARNING

This code should serve as an example and should not be used in production environment. 

The settings.json file should be cleared out once you've completed the testing and secrets and tokens should be stored in safe, encrypted storage (i.e. database, secrets manager etc.) 

You should treat the tokens in confidential manner, similar as you do with your usernames and passwords. 