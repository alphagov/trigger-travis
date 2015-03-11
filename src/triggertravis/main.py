import os
import urllib2
import json

TRAVIS_TOKEN = os.environ['TRAVIS_TOKEN']
TRAVIS_ENDPOINT = os.getenv('TRAVIS_ENDPOINT', 'https://api.travis-ci.org/')

from flask import Flask, abort, jsonify

app = Flask(__name__)


def api_call(resource, data=None):
    url = TRAVIS_ENDPOINT + resource
    if data:
        data = json.dumps(data)
        
    req = urllib2.Request(url, data)
    req.add_header('Authorization', 'token ' + TRAVIS_TOKEN)
    
    if data:
        req.add_header('Content-Type', 'application/json; charset=UTF-8')
    
    p = urllib2.urlopen(req)
    return json.loads(p.read())


@app.route('/trigger/<path:repository>', methods=['GET'])
def travis_ping(repository):
    builds = api_call('repos/{}/builds'.format(repository))
    if len(builds) == 0:
        return abort(404)
        
    # find the most recent master
    last_build_id = None
    for build in builds:
        if build['branch'] == 'master':
            last_build_id = build['id']
    
    if last_build_id:
        result = api_call('requests', { 'build_id': last_build_id })['flash'][0]
    
        if 'notice' in result:
            return jsonify({'success' : True, 'build' : last_build_id, 'message' : result['notice']})
        elif 'error' in result:
            return jsonify({'success' : False, 'build' : last_build_id, 'message' : result['error']})
        else:
            abort(500)
    else:
        abort(404)
    
    