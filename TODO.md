## TO DO LIST FOR CLOSE CALL DATABASE


fix this issue when we have opus


Redirecting to Strava oauth

127.0.0.1 - - [12/Jul/2025:21:23:41 +0000] "GET /get-strava-login HTTP/1.1" 302 0 "https://closecalldatabase.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36" 2332
Strava Token: cb059070859ea94bf6af96d2a43c09620251a21d
Trying to complete Token Exchange
Token Exchange Completed. Strava sent athlete data.
HERE COMES THE OAUTH_RESP
{'token_type': 'Bearer', 'expires_at': 1752377027, 'expires_in': 21600, 'refresh_token': 'cc5c86daa16ad2215b8536bb5a15eeeae966bab3', 'access_token': '2929d6ece3c31e8f65cf02e5e510a06fdd5896f5', 'athlete': {'id': 122173998, 'username': 'zakjensen', 'resource_state': 2, 'firstname': 'Zak', 'lastname': 'J', 'bio': '', 'city': 'Vancouver', 'state': 'Washington', 'country': 'United States', 'sex': 'M', 'premium': True, 'summit': True, 'created_at': '2023-08-01T23:04:22Z', 'updated_at': '2025-06-19T00:21:41Z', 'badge_type_id': 1, 'weight': 63.9565, 'profile_medium': 'https://dgalywyr863hv.cloudfront.net/pictures/athletes/122173998/28078855/3/medium.jpg', 'profile': 'https://dgalywyr863hv.cloudfront.net/pictures/athletes/122173998/28078855/3/large.jpg', 'friend': None, 'follower': None}}
ERROR Internal Server Error: /strava-registration
Traceback (most recent call last):
  File "/home/eae/code/closecall/core/views.py", line 515, in strava_registration
    user = User.objects.get(username=created_username)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/eae/code/closecall/.venv/lib/python3.12/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/eae/code/closecall/.venv/lib/python3.12/site-packages/django/db/models/query.py", line 649, in get
    raise self.model.DoesNotExist(
django.contrib.auth.models.User.DoesNotExist: User matching query does not exist.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/eae/code/closecall/.venv/lib/python3.12/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/home/eae/code/closecall/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/eae/code/closecall/core/views.py", line 522, in strava_registration
    email = oauth_resp['athlete']['email']
            ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'email'
127.0.0.1 - - [12/Jul/2025:21:23:47 +0000] "GET /strava-registration?state=&code=cb059070859ea94bf6af96d2a43c09620251a21d&scope=read HTTP/1.1" 500 5155 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36" 332758

I think that the strava API used to return the email but it no longer does.







<hr>

### Done

- NAV BAR, Dark Blue on Black for the Close Call Database menu item. FIX!

fixed Strava oauth error (untested)