#!/usr/bin/env python

import urllib2, json



class Travis:
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    def _api_call(self, resource, data=None):
        url = self.endpoint + resource
        if data:
            data = json.dumps(data)

        req = urllib2.Request(url, data)
        req.add_header('Authorization', 'token ' + self.token)

        if data:
            req.add_header('Content-Type', 'application/json; charset=UTF-8')

        p = urllib2.urlopen(req)
        return json.loads(p.read())


    def get_builds(self, repository, branch = None):
        builds = self._api_call('/repos/{}/builds'.format(repository))
        if branch:
            return filter(lambda build : build['branch'] == branch, builds)
        else:
            return builds


    def build(self, build_id):
        return self._api_call('requests', { 'build_id': build_id })['flash'][0]
