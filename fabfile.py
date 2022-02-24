###########################################################################
#
# Usage 
# Windows:
# fab doit(path_to_ssh_key) refresh('dev|staging')
# fab doit(path_to_ssh_key) maintenanceon('dev|staging')
# fab doit(path_to_ssh_key) maintenanceoff('dev|staging')
# fab doit(path_to_ssh_key) productionrefresh
# Example: fab doit('c:\users\tom\.ssh\id_rsa.pem') maintenanceon('dev')
# 
# Linux and MAC OS:
# fab doit -k path_to_pub_ssh_key, refresh -s server_prefix
# Example: fab doit -k /home/danilo/.ssh/id_rsa.pub, refresh -s dev
#
# If you use a passphrase then add --prompt-for-passphrase
# 
###########################################################################
from fabric import task, Connection


@task
def doit(ctx, keypath):
    ctx.user = 'django'
    ctx.host = '<servername>'
    ctx.connect_kwargs.key_filename = ''.format(keypath)


@task
def maintenanceon(ctx, server):
    conn = Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs)
    # create ln to maintenance file
    print('maintenance on')
    with conn.cd('/usr/share/nginx/html/'):
        conn.run('sudo ln -sf /home/django/sites/{0}.<servername>/src/project/templates/maintenance.html {0}-maintenance.html'.format(server))


@task
def maintenanceoff(ctx, server):
    conn = Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs)
    # create ln to maintenance file
    print('maintenance off')
    with conn.cd('/usr/share/nginx/html/'):
        conn.run('sudo unlink {}-maintenance.html'.format(server))


@task
def refresh(ctx, server):
    env_command = '. /home/django/sites/{0}.<servername>.com/{0}/bin/activate'.format(server)

    conn = Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs)

    # set to maintenance mode
    with conn.cd('/usr/share/nginx/html/'):
        print('maintenance on')
        conn.run('sudo ln -sf /home/django/sites/{0}.<servername>.com/src/project/templates/maintenance.html {0}-maintenance.html'.format(server))
    # refresh install
    with conn.cd('/home/django/sites/{}.<servername>.com/src/'.format(server)):
        print('git pull')
        conn.run('git pull')
    # check requirements
    with conn.cd('/home/django/sites/{}.<servername>.com/src/requirements/'.format(server)):
        print('pip-sync')
        conn.run(env_command + '&&' + 'pip-sync {}.txt'.format(server))
    # run migrations and collectstatic
    with conn.cd('/home/django/sites/{}.<servername>.com/src/project/'.format(server)):
        print('migrate')
        conn.run(env_command + '&&' + 'python manage.py migrate')
        print('collecstatic')
        conn.run(env_command + '&&' + 'python manage.py collectstatic --no-input')
    # restart server
    print('restart server')
    conn.sudo('systemctl restart {}.service'.format(server), pty=True)

    # maintenance mode off
    with conn.cd('/usr/share/nginx/html/'):
        print('maintenance off)')
        conn.run('sudo unlink {}-maintenance.html'.format(server))


@task
def productionrefresh(ctx):
    env_command = '. /home/django/sites/www.<servername>.com/www/bin/activate'

    conn = Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs)

    # set to maintenance mode
    with conn.cd('/usr/share/nginx/html/'):
        print('Set to maintenance mode')
        conn.run('sudo ln -sf /home/django/sites/www.<servername>.com/src/project/templates/maintenance.html prod-maintenance.html')
    # refresh install
    with conn.cd('/home/django/sites/www.<servername>.com/src/'):
        print('Git pull')
        conn.run('git pull')
    # check requirements
    with conn.cd('/home/django/sites/www.<servername>.com/src/requirements/'):
        print('pip-sync production.txt')
        conn.run(env_command + '&&' + 'pip-sync production.txt')
    # run migrations and collectstatic
    with conn.cd('/home/django/sites/www.<servername>.com/src/project/'):
        print('python manage.py migrate')
        conn.run(env_command + '&&' + 'python manage.py migrate')
        print('python manage.py collectstatic')
        conn.run(env_command + '&&' + 'python manage.py collectstatic --no-input')
    # restart server
    print('restart production service')
    conn.sudo('systemctl restart production.service', pty=True)
    # maintenance mode off
    with conn.cd('/usr/share/nginx/html/'):
        print('maintenance off')
        conn.run('sudo unlink prod-maintenance.html')


@task
def productioncollect(ctx):
    env_command = '. /home/django/sites/www.<servername>.com/www/bin/activate'

    conn = Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs)
    with conn.cd('/home/django/sites/www.<servername>.com/src/project/'):
        conn.run(env_command + '&&' + 'python manage.py collectstatic --no-input')
