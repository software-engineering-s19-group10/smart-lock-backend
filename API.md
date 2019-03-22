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
