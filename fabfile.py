from datetime import datetime
from fabric.api import env, local, run, cd, put

env.user = "bdailey"

def restart():
    run('/home/bdailey/webapps/icd10helper/apache2/bin/restart', shell=True, pty=False)

def build_archive(tag):
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    env.datestamp = dt
    local('git archive --format=tar --prefix=%(datestamp)s/ %(tag)s | gzip > %(datestamp)s.tar.gz' % {
        "datestamp": env.datestamp,
        'tag': tag
    })

def deploy_code(tag="HEAD"):
    local('tar czf deploy.tgz *.py requirements.txt templates')
    with cd('/home/bdailey/webapps/icd10helper/lib/python2.7'):
        put('deploy.tgz', 'deploy.tgz')
        run('tar zxf deploy.tgz && rm deploy.tgz')
        # clean up all compiled code.
        run("find . -name '*.pyc' -print0|xargs -0 rm")
    local('rm deploy.tgz')
    restart()

def deploy_static(tag="HEAD"):
    local('cd static && tar czf static.tgz * && mv static.tgz ..')
    with cd('/home/bdailey/webapps/icd10helper_static/'):
        put('static.tgz', 'static.tgz')
        run('tar zxf static.tgz && rm static.tgz')
    local('rm static.tgz')
