# SETUP FOR VAGRANT DEV BOX BUZZHIRE
PROJNAME=buzzhire
echo 'export DJANGO_CONFIGURATION="VagrantDev"' >> /home/vagrant/.profile
DJANGO_CONFIGURATION="VagrantDev"
source /home/vagrant/.profile

# GENERAL SETUP
sudo apt-get update
sudo apt-get -y install vim
sudo apt-get -y install curl
sudo apt-get -y install redis-server

#PYTHON / DJANGO
sudo apt-get -y install python-pip
sudo apt-get -y install python-dev

# POSTGRES & DEPENDENCIES
sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev
sudo apt-get -y install libgdal1
sudo apt-get -y install libffi-dev
sudo apt-get -y install libgeos-dev

# POSTGIS TUTORIAL
# https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS20Ubuntu1204
sudo apt-get -y install python-software-properties
sudo apt-add-repository -y ppa:ubuntugis/ppa
sudo apt-get -y update
sudo apt-get -y install postgis
sudo apt-get -y install postgresql-9.1-postgis-2.0 # Added 2.0 at the end

sudo /etc/init.d/postgresql restart

# DB SETUP 
# sudo su postgres -c "createuser -d -R -P $PROJNAME"
# Hardcoded to buzzhire for now

sudo su postgres -c "cd /vagrant/; ./dbcreator.sh"
sudo /etc/init.d/postgresql restart

# PIP REQUIREMENTS
cd /vagrant
sudo pip install -r requirements.pip

# SECRET FILE SETUP
touch /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_HOST = 'localhost'" >> /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_NAME = '$PROJNAME'" >> /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_USER = '$PROJNAME'" >> /vagrant/settings/secret.py
echo "DEFAULT_DATABASE_PASSWORD = '$PROJNAME'" >> /vagrant/settings/secret.py
echo "SECRET_KEY = 'Km)lid2fmzVy0^wJUfi60mAP5NeVK'" >> /vagrant/settings/secret.py
echo "EMAIL_HOST_PASSWORD = 'asdf'" >> /vagrant/settings/secret.py
echo "AWS_SECRET_ACCESS_KEY = 'xxx'" >> /vagrant/settings/secret.py
echo "BRAINTREE_PRIVATE_KEY = 'yyy'" >> /vagrant/settings/secret.py

mkdir -p /vagrant/logs/

cd /vagrant; ./manage.py runserver 0.0.0.0:8000 &
echo "DONE"
