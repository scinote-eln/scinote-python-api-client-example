# Setting up API access for SciNote running on local infrastructure

## Procedure
- Identify the scinote docker container
- Run Rails Console
- Create Doorkeeper application

## Identify scinote docker container
From Linux terminal run the following command
```
docker ps
```
You should get a list of running docker containers.
Find the one with image called
```
scinote_web_production
```
To the left hand side you should see the ID of the container. Copy it, we will need it in the next step. 

(For this example we will assume the id is 6009a11b217f)

## Run rails console
From terminal run the following command
```
docker exec -ti 6009a11b217f rails c
```
!Replace '6009a11b217f' with the id of your actual docker container. 

There might be a few lines of output, but at the end you should see the rails console prompt:

```
irb(main):001:0>
```

## Create Doorkeeper Application
First let's prepare all of the data we need. You can copy the following line by line.

```ruby
uid = SecureRandom.uuid
secret = SecureRandom.uuid
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
name = 'API'
```
**Important:** 
The first two lines will generate the unique strings and assign them to the variables. Please note them down (or copy them) as they will need to be provided to the potential api clients

Now let's create the application. (you can paste the following line by line)
```ruby
app = Doorkeeper::Application.new
app.uid = uid
app.secret = secret
app.redirect_uri = redirect_uri
app.name = name
app.save!
```

You should be informed that application was successfully saved and now you can close the rails console pressing CTRL+D.

## Thats it :)
As mentioned, you should now have uid and secret needed to obtain access tokens for your API client. 