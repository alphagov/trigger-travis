#!/usr/bin/env python

import requests, json, time

class Heroku:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def _headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.api_key),
            'Content-type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3'
        }
    
    def get_build(self, app_name, build_id):
        response = requests.get("https://api.heroku.com/apps/{}/builds/{}".format(app_name, build_id),
            headers=self._headers()
        )
    
        return json.loads(response.content)
    
    def get_builds(self, app_name):
        response = requests.get("https://api.heroku.com/apps/{}/builds".format(app_name),
            headers=self._headers()
        )
    
        return json.loads(response.content)

    def deploy(self, app_name, source_url, version):
        data = {
            "source_blob" : { 
                "url" : source_url, 
                "version" : version
            }
        }
    
        response = requests.post("https://api.heroku.com/apps/{}/builds".format(app_name),
            headers=self._headers(),
            data = json.dumps(data)
        )
    
        return json.loads(response.content)
    
    def deploy_and_wait(self, app_name, url, commit_id):
        result = self.deploy(app_name, url, commit_id)
    
        # wait for the build to complete
        while True:
            status = self.get_build(app_name, result['id'])['status']
            if status == 'pending':
                time.sleep(2)
            else:
                break
    
        return (status == 'succeeded', status)

