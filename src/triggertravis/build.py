#!/usr/bin/env python

import os, json

from github import GitHub
from heroku import Heroku
from travis import Travis


github = GitHub(os.getenv('GITHUB_KEY'))
heroku = Heroku(os.getenv('HEROKU_KEY'))
travis = Travis(os.getenv('TRAVIS_ENDPOINT', 'https://api.travis-ci.org/'), os.getenv('TRAVIS_KEY'))

APPS = json.loads(os.getenv('APPS'))
E2E_OWNER = os.getenv('E2E_OWNER')
E2E_REPO = os.getenv('E2E_REPO')


def deploy_and_test(repo_owner, repo_name, branch, commit_id):
    repo_path = repo_owner + '/' + repo_name
    if repo_path in APPS:
        app_name = APPS[repo_path]
        url = github.get_source_tarball(repo_owner, repo_name, commit_id)
        print "Deploying {}/{} at {} to Heroku app {} from {}".format(repo_owner, repo_name, commit_id, app_name, url)
        (deployed, message) = heroku.deploy_and_wait(app_name, url, commit_id)
        if deployed:
            print "Deployed"
            running_build = None
            while True:
                root = github.get_sha(E2E_OWNER, E2E_REPO, 'master')
                print "E2E master is at {}".format(root)
            
                builds = filter(
                  lambda build: (build['commit'] == root) and (build['event_type'] == 'push'), 
                  travis.get_builds('{}/{}'.format(E2E_OWNER, E2E_REPO))
                )
            
                if len(builds) > 0:
                    latest_build = builds[0]
                    if latest_build['finished_at'] is None:
                        print "Waiting for build {}".format(latest_build['id'])
                    else:
                        # try and re-run
                        result = travis.build(latest_build['id'])
                        if 'error' in result:
                            print "Could not start build {}: {}".format(latest_build['id'], result['error'])
                        else:
                            running_build = latest_build
                            break

                time.sleep(5)
    
            print "Started build {}".format(running_build['id'])
        else:
            print "Deploy failed: {}".format(message)
    else:
        print "Unknown app: {}".format(repo_path)