# Simple OpenID Connect Provider

## General info
This project is simple OpenID Connect Provider application.
This application implement simple flow of OpenID protocol from scratch.

## Warnig
Don't use this project in production

## Setup
To run this project and install requirements packages use requirements.txt and upgrade database
and rename .env.example to .env and changes settings
```
(env) $ pip install -r /path/to/requirements.txt
(env) $ flask db upgrade
```

#### Authentication & Authorization Request Sample
```
http://127.0.0.1:5000/api/v1/oidc/authorize?response_type=code
                       &client_id=SSOAdminPanel
                       &redirect_uri=https://YOUR_APP/callback
                       &scope=profile
                       &state=EZ87XrGqV2wZ
                       &code_challenge=ab370b82bac00258ff596fe738336b2874c983ee5dd89d6297ce2a8e359e1b9e
                       &code_challenge_method=SHA256

Callback:
https://YOUR_APP/callback?code=f8c8cff2ad914e14a78982a12b01a4b9&state=EZ87XrGqV2wZ
```                    
#### Token Request Sample
```
http://127.0.0.1:5000/api/v1/oidc/token

Body:
{
    "grant_type" : "authorization_code",
    "client_id":"SSOAdminPanel",
    "client_secret": "test_secret",
    "code_verifier" : "8GNYVYHnYOyrm6Dc9zVP",
    "code": "f8c8cff2ad914e14a78982a12b01a4b9",
    "redirect_uri":"https://YOUR_APP/callback"
}

Response:
{
    "status": 200,
    "message": "Token successfully created.",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciO...",
        "expires_in": 3600
    }
}
```
