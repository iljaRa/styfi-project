# Style Finder app (StyFi)
Full backend solution for an app that matches a potential T-Shirt from an input image to images from a database (images and information scraped from hm.com). 

## Installation
This installation concerns the Computer Vision tools, MySQL and JAVA based server on a remote machine, e.g. EC2 by AWS

The following instructions assume that you are deploying the app on a new (virtual) Ubuntu 16.04 machine.

Disclaimer: An update with more recent software versions and Ubuntu 20.04 will follow soon.

If you are trying out the code on your local machine, we recommend creating a new virtual environment (venv) for the purpose of the setup.

First, DOWNLOAD all the repositories including data and the searchengine
```
cd ~/
mkdir git_repos;
cd git_repos;
git clone https://github.com/iljaRa/styfi-project.git
cd styfi-project/
tar xzf dataset_hm.tar.gz 
cd 
mkdir software_misc
```

Second, INSTALL all the necessary packages and libraries
```
cd installs;
./install_styfi.sh
```
After confirming the password, use it to login to mysql and choose the appropriate responses for the rest of the installation.

Now, you can TEST the connectivity with FileCounter.war
for that, make sure to upload FileCounter.war from the downloaded git repository to the root, like this:
```
sudo service tomcat7 start
cd /var/lib/tomcat7/webapps/
sudo cp ~/git_repos/styfi-project/styfi-server/FileCounter.war .
sudo service tomcat7 restart
```

Now you can test it by accessing http://<HOST-IP-ADDRESS>:8080/FileCounter/FileCounter
as a repsonse, you should see sth like: "This site has been accessed 1 times."
If it didn't work, follow the guide below step by step: 
https://www.digitalocean.com/community/tutorials/how-to-install-apache-tomcat-8-on-ubuntu-16-04


Third, SETUP MySQL database:
```
sudo service mysql start
sudo mysql -u root -p
```

Create the database as well as a new user, and manage permissions - paste the following into the mysql console:
```
mysql>  create database fashion_hm;
use fashion_hm;
CREATE USER 'styfi'@'localhost' IDENTIFIED BY 'styfi';
GRANT ALL PRIVILEGES ON * . * TO 'styfi'@'localhost';
quit
```
Then, add infos from the scraped html files to the database
```
python3 add_info_to_db.py 1
```

```
cd /var/lib/tomcat7/webapps
cp ~/git_repos/styfi-project/styfi-server/bash_script.sh .
sudo chmod +x bash_script.sh
```
Set the necessary permissions for `git_repos/`
```
cd
sudo chgrp -R tomcat7 git_repos/
sudo chmod -R g+w git_repos/
```

Adjust the directory of the searchengine inside the bash_script.sh on line 3: `cd ~/git_repos/cv-sift-search/;` 


Now, upload `StyFiServer.war` (if there already is one, then delete it [PLEASE BE CAREFUL]):
```
cd /var/lib/tomcat7/webapps
# The line below deletes the existing StyFiServer.war, do think twice
sudo rm -r StyFiServer*
sudo cp ~/git_repos/styfi-project/styfi-server/StyFiServer.war .
sudo service tomcat7 restart
sudo cp bash_script.sh StyFiServer/
sudo chmod +x StyFiServer/bash_script.sh
```

Finally, you can test if the setup worked by accessing http://<HOST-IP-ADDRESS>:8080/StyFiServer/ImageUpload
as a repsonse, you should see some information about the T-Shirt, including a URL of the found item (that should match your query)

## Setting up the server
To set up `StyfiServer` and create `StyfiServer.war`, use the JAVA classes inside `styfi-project/styfi-server`.

## Getting data
To scrape fashion data from hm.com, use the code inside `styfi-project/hm_fashion_scraper`. Note that as the website design changes very often, you might have to adjust the code appropriately.

Also, very important, check hm.com/robots.txt to see whether hm.com allows to scrape the information. At the time of writing this text, it is allowed because hm.com/robots.txt returns:
```
User-agent: *
Disallow:
```

Note that it is generally recommended to use the API of the store to scrape data. However, we wrote our own scraper because it is more educative and fun, and gives us more flexibility.
