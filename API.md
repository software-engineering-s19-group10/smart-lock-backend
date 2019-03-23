# API Endpoints:
## General Notes
+ These endpoints are going to be relative paths, so you'll have to add them to a base URL to access them.
+ If you're running the server locally, use `http://localhost:3000/` as the base URL.
+ If you're trying to access the production database, use `http://boiling-reef-89836.herokuapp.com/` as the base URL.
+ Some URLs can take in numbers (to get values or change values). These will be represented by <num> in URLs.

## Authentication/Authorization
+ There is a token-based authentication system built into the API that protects from unregistered users getting information.
+ Each token is a random hash of characters that is generated when a user is created   .
+ To get the token for a user, send a `POST` request to `lock_owners/api/authenticate/` with data `{username: <username>, password: <password>}` (fill in username and password yourself)
+ The request will either return the token in the form `Token <token>` or it will return an error message.
+ To use the token with an API endpoint that requires authentication, you have to add an HTTP header to the message. 
The HTTP header will be formatted `Authorization: Token <token>`.
+ If you don't supply authentication, the API request will fail, so make sure you always authenticate before any other requests. You can also save the token in a variable somewhere so you just have to authenticate at the very beginning and that's it.


## Endpoint URLs
`lock_owners/api/users/`
+ Requires authentication
+ `GET` request - gets a list of all users. Try printing out the users to see their format.
+ `POST` request - adds a user with the data fields passed in with the request. Data should be in the same format as one of the entries from the `GET` request at the URL.
  
`lock_owners/api/users/<num>/`
+ Requires authentication
+ `GET` request - gets a user with user id == num.
+ `PATCH` request - updates the user with id == num, with the data passed in with the request.
+ `DELETE` request - deletes the given user.

  
`lock_owners/api/locks/`
+ Works like the users endpoint
  
  
`lock_owners/api/locks/<num>/`
+ Works like the users endpoint

`lock_owners/api/permissions/`
+ Works like the users endpoint
  
  
`lock_owners/api/permissions/<num>/`
+ Works like the users endpoint

`lock_owners/api/srn`
+ `GET` request - gets a list of all stranger reports in database. 

Here is an example of the returned value: 

``` json
[
{"latitude":65.0,"longitude":-144.123,"stranger_report_time":"2019-03-20T16:42:37Z","lock":1},
{"latitude":65.0,"longitude":-144.123,"stranger_report_time":"2019-03-20T16:42:37Z","lock":1}
] 
```

+ `POST` request - adds a stranger report with the data fields passed in with the request. Data should be in the same format as one of the entries from the `GET` request at the URL.
That means pass in latitude and longitude. For stranger report time, pass in time in ISO 8601 format. If you are using python,
just use the datetime module. For "lock", pass in id.
  

`lock_owners/api/sms`
To send texts, use the following url path for whatever url we use:

```
http://example.com/lock_owners/api/sms/?content=hi%20%how%20are%20you&dest=18001231231
```

For the parameters, as you can see pass in content which will be the body of the text. Pass in dest to be the
number we send the message to. The phone number should have the country code in front. So, if you are sending
a number like 973-123-1232, write it like 19731231232.

For the demo, i will have to add your number to a list of recognized numbers.

`lock_owners/api/mms`

You can send MMS messages but you have to give a url for an image to send. The parameters to give are the same as in sms but there's an extra parameter which is "img_url" which takes the URL of the image. 
