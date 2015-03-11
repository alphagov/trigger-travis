# payment-provider-testing

## Requirements
* Python

## Developer Configuration
* Set `TRAVIS_TOKEN` env var to your Travis API token
* Set `REPO_NAME` env var to the github repo to build (must already be in Travis CI)
* Set `TRAVIS_ENDPOINT` to `https://api.travis-ci.com/` if using Travis Pro. It is `https://api.travis-ci.org/` by default.

## Developer Set-Up
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Development Server
```
src/dev_server.py
```
