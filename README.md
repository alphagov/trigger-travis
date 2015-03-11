# trigger-travis

## Requirements
* Python

## Developer Configuration
* Set `PYTHONPATH` env var to "src/"
* Set `TRAVIS_TOKEN` env var to your Travis API token
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

## API

```
http://server/trigger/<repo_name>
```

For example:
```
http://server/trigger/alphagov/example-project
```

Can only build the master at the moment, but support for other branches will be added.
