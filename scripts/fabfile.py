from fabric.api import *
import time, json

app_name = 'AuthAPI'
uwsgi_apps_enabled = '/etc/uwsgi/apps-enabled'
uwsgi_touch_path = '/var/run/uwsgi'

num_keep_releases = 5

file_list = [   '../AuthAPI/controllers/*.py',
                '../AuthAPI/decorators/*.py',
                '../AuthAPI/models/*.py',
                '../AuthAPI/services/*.py',
                '../AuthAPI/responses/*.py',
                '../AuthAPI/views/*.py',
                '../AuthAPI/*.py',
                '../conf/uwsgi.ini',
                '../requirements.txt'   ]

def staging():
    f = open('../conf/fab_env_staging.json', 'r')
    env_stuff = json.load(f)
    f.close()
    env.hosts = env_stuff['hosts']
    env.user = env_stuff['user']
    env.key_filename = env_stuff['key']
    env.app_path = '/var/www/SERVER_URL'
    env.base_url = 'SERVER_URL'

def pack():
    filelist = ' '.join(file_list)
    local('tar czf ../dist/{}.tar.gz {}'.format(app_name, filelist))

def deploy():
    # new source distribution
    pack()

    # upload it to server
    run('mkdir -p {}/tmp'.format(env.app_path))
    put('../dist/{}.tar.gz'.format(app_name), '{}/tmp'.format(env.app_path))

    # extract it to folder
    timestamp = time.strftime("%Y%m%d%H%M%S")
    deploy_path = '{}/releases/{}'.format(env.app_path, timestamp)
    run('mkdir -p {}'.format(deploy_path))

    with cd('{}'.format(env.app_path)):
        run('tar xzf tmp/{}.tar.gz -C {}'.format(app_name, deploy_path))
        run('ln -nfs {} current'.format(deploy_path))

    with cd('{}/current'.format(env.app_path)):
        run('virtualenv venv; source venv/bin/activate; pip install -r requirements.txt')
        run('echo "chdir = {}/current" >> conf/uwsgi.ini'.format(env.app_path))
        run('echo "logto = /var/log/uwsgi/{}.log" >> conf/uwsgi.ini'.format(env.base_url))
        run('echo "virtualenv = {}/current/venv" >> conf/uwsgi.ini'.format(env.app_path))
        run('ln -nsf {}/current/conf/uwsgi.ini {}/{}.ini'.format(env.app_path, uwsgi_apps_enabled, app_name))

    # touch uwsgi to make it reload
        run('touch {}'.format(uwsgi_touch_path))

    # cleanup
    with cd('{}/releases'.format(env.app_path)):
        run('rm -r `ls -r | tail -n +{}`;true'.format(num_keep_releases + 1))
