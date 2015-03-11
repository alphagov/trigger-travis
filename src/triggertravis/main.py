import os
import urllib2
import json

TRAVIS_TOKEN = os.environ['TRAVIS_TOKEN']
TRAVIS_ENDPOINT = os.getenv('TRAVIS_ENDPOINT', 'https://api.travis-ci.org/')

from flask import Flask, abort, jsonify

app = Flask(__name__)


def api_call(url, token=None, data=None):
    if data:
        data = json.dumps(data)
    req = urllib2.Request(url, data)
    if data:
        req.add_header('Content-Type', 'application/json; charset=UTF-8')
    if token:
        req.add_header('Authorization', 'token ' + token)
    p = urllib2.urlopen(req)
    return json.loads(p.read())


@app.route('/trigger/<path:repository>', methods=['GET'])
def travis_ping(repository):
    builds = api_call('https://api.travis-ci.com/repos/{}/builds'.format(repository), TRAVIS_TOKEN)
    if len(builds) == 0:
        return abort(404)

    last_build_id = builds[0]['id']
    return jsonify({'status' : api_call('https://api.travis-ci.com/requests', TRAVIS_TOKEN, { 'build_id': last_build_id })['result']})
