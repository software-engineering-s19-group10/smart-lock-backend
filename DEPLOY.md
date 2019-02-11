To deploy to production (make sure you have Heroku installed first)  
```
heroku login
git add .
git commit -m "Your commit message here"
git push heroku master
```

You might run into an error with the function in `settings.py` to set Django's SECRET_KEY.
If that happens, run `heroku config:set DISABLE_COLLECTSTATIC=1` to fix the issue.
