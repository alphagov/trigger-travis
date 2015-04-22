#!/usr/bin/env python

import os, json, redis

from flask import Flask, request
from rq import Queue

from triggertravis.build import deploy_and_test

app = Flask(__name__)

redis = redis.from_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
queue = Queue(connection=redis)

STATUS_PASSED = 0

@app.route('/travishook', methods=['POST'])
def travis_hook():
    payload_json = request.form['payload']
    print "Travis Hook: {}".format(payload_json)
    payload = json.loads(payload_json)
    
    try:
        status = int (repr(payload['status']))
    except ValueError, e:
        status = None
        
    if (status == STATUS_PASSED) and (payload['branch'] == 'master'):
        queue.enqueue_call(
            func=deploy_and_test,
            args=(
                payload['repository']['owner_name'],
                payload['repository']['name'],
                payload['branch'],
                payload['commit'],
            ),
            timeout=600
        )
        
    return "OK"