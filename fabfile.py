from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import sudo
from fabric.api import settings
from fabric.api import task

env.use_ssh_config = True
env.user = "vagrant"
env.hosts = ["127.0.0.1:2222"]

result = local('vagrant ssh-config | grep IdentityFile', capture=True)
env.key_filename = result.split()[1]
print result

HOME_DIR = "/home/vagrant/"
VIRTUAL_ENV_DIR = HOME_DIR + "envs/"

def test():
    run_tests = "source /api/envs/marker-vagrant-env/bin/activate && python /api/marker/manage.py test /api/marker"
    local("vagrant ssh default -c '%s'" % run_tests)

@task
def checker():
    run('whoami')

@task
def deploy(dry_run="false"):
#    test()
    prepare()
    sync_files(dry_run)
    install_deps()
    setup_virtualenv()
    setup_apache()

    local("curl 127.0.0.1:8080/hc/status/")


def prepare():
    with settings(warn_only=True):
        if run("test -d api").failed:
            print "No directory. Making..."
            run("mkdir api")
        else:
            print "Directory exists"

@task
def sync_files(dry="true"):
    base_command = "rsync -avz "
    ssh_vagrant = "-e 'ssh -p 2222' "
    base_command += ssh_vagrant
    dry_run = " --dry-run "
    if dry == "true": # Have to use strings because fabric passes in all args as strings
        base_command += dry_run

    exclusions = [".git", ".vagrant", "**.pyc", "Vagrantfile", "*provision*", "*script*", "TAGS", ".gitignore", "fabfile*"]
    source = "./"
    dest = "vagrant@127.0.0.1:/home/vagrant/api"
    base_command += " ".join(map(lambda x: '--exclude "%s"' % x, exclusions)) + " " + source + " " + dest
    local(base_command)

def install_deps():
    install_packages()
    install_wsgi()
    install_geos()
    install_proj4()

def update_package_manager():
    sudo("apt-get update")

def install_packages():
    update_package_manager()
    package_list = ["apache2","python-dev","apache2-dev","python-pip","emacs24","libpq-dev","postgresql","postgresql-contrib","postgis","postgis-doc","postgresql-9.3-postgis-2.1"]
    packages_for_pillow = ["libjpeg8-dev","zlib1g-dev","libffi-dev"]

    package_list.extend(packages_for_pillow)

    base_command = "apt-get install -y "
    base_command += " ".join(package_list)

    sudo(base_command)

def install_wsgi():
    with cd(HOME_DIR):
        wsgi_url = "https://github.com/GrahamDumpleton/mod_wsgi/archive/4.4.21.tar.gz"
        get_url(wsgi_url)
        run("tar xvfz 4.4.21.tar.gz")
        with cd("mod_wsgi-4.4.21/"):
            run("./configure")
            run("make")
            sudo("make install")

        sudo('echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so" | sudo tee -a /etc/apache2/apache2.conf')

def install_geos():
    with cd(HOME_DIR):
        geos_url = "http://download.osgeo.org/geos/geos-3.4.2.tar.bz2"
        get_url(geos_url)
        run("tar xjf geos-3.4.2.tar.bz2")
        with cd("geos-3.4.2"):
            run("./configure")
            run("make")
            sudo("make install")

def install_proj4():
    with cd(HOME_DIR):
        proj4_url = "http://download.osgeo.org/proj/proj-4.9.1.tar.gz"
        datumgrid_url = "http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz"
        get_url(proj4_url)
        get_url(datumgrid_url)
        run("tar xzf proj-4.9.1.tar.gz")
        with cd("proj-4.9.1/nad"):
            run("tar xzf " + HOME_DIR + "proj-datumgrid-1.5.tar.gz")

        sudo("echo '/usr/local/lib' >> /etc/ld.so.conf.d/local-lib.conf") # Add /usr/local/lib to dynamic linker run-time bindings for PROJ.4
        with cd(HOME_DIR + "/proj-4.9.1"):
            run("./configure")
            run("make")
            sudo("make install")

@task
def setup_virtualenv():
    with settings(warn_only=True):
        if run("test -d %s" % VIRTUAL_ENV_DIR).failed:
            run("mkdir %s" % VIRTUAL_ENV_DIR)

    sudo("pip install virtualenv")

    marker_virtual_env_path = VIRTUAL_ENV_DIR + "marker"
    run("virtualenv " + marker_virtual_env_path)
    run("source %s/bin/activate" % marker_virtual_env_path)
    with cd(HOME_DIR + "api/"):
        sudo("pip install -r requirements.txt")

@task
def setup_apache():
    sudo("cp /home/vagrant/api/vm_fixtures/000-default.conf /etc/apache2/sites-available/marker.conf")
    sudo("a2ensite marker")
    sudo("a2dissite 000-default.conf")
    sudo("service apache2 restart")

def get_url(url):
    run("wget '{}'".format(url))
