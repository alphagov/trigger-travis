#!/usr/bin/python

import json
import urllib

with open("travis_hook_payload.json") as txt:
    payload = json.loads(txt.read())

data = urllib.urlencode({ "payload": json.dumps(payload) })
result = urllib.urlopen("https://gds-pay-builder.herokuapp.com/travishook", data).read()
print result