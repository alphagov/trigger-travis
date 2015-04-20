#!/usr/bin/env python

import requests, json, time, datetime



class GitHub:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.api_key)
        }
    
    def get_source_tarball(self, owner, repo, branch_or_commit):
        response = requests.get('https://api.github.com/repos/{0}/{1}/tarball/{2}'.format(owner, repo, branch_or_commit),
            headers=self._headers(),
            allow_redirects=False
        )
        
        if response.status_code == 302:
            return response.headers['Location']
        else:
            return None

    def get_sha(self, owner, repo, branch):
        response = requests.get('https://api.github.com/repos/{0}/{1}/git/refs/heads/{2}'.format(owner, repo, branch),
            headers=self._headers(),
        )
        
        if response.status_code == 404:
            return None
        
        return (json.loads(response.content))['object']['sha']
        
    def create_branch(self, owner, repo, root, branch_name):
        payload = {
          'ref': 'refs/heads/{0}'.format(branch_name),
          'sha': root
        }
        
        response = requests.post('https://api.github.com/repos/{0}/{1}/git/refs'.format(owner, repo),
            headers=self._headers(),
            data=json.dumps(payload)
        )
        
        return (response.status_code == 201)
        
    def touch_file(self, owner, repo, branch, path, commit_message):
        payload = {
            'message' : commit_message,
            'committer': {
                "name": "buildatron",
                "email": "buildatron@gds"
            },
            'content' : 'Lg==',
            'branch' : branch
        }
        
        response = requests.put('https://api.github.com/repos/{0}/{1}/contents/{2}'.format(owner, repo, path),
            headers=self._headers(),
            data=json.dumps(payload)
        )
        
        return (response.status_code == 201)
        
    def create_pull(self, owner, repo, base, branch, title):
        payload = {
          'head': branch,
          'base': base,
          'title': title,
          'body': ""
        }
        
        response = requests.post('https://api.github.com/repos/{0}/{1}/pulls'.format(owner, repo),
            headers=self._headers(),
            data=json.dumps(payload)
        )
        
        return (response.status_code, response.content)
