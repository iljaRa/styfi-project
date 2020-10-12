#!/bin/bash

#~ First, DOWNLOAD all the repositories including data and the searchengine
```
mkdir git_repos;
cd git_repos;
git clone https://github.com/iljaRa/styfi-project.git
cd styfi-project/
tar xzf dataset_hm.tar.gz 
cd 
mkdir software_misc
```

#~ Second, INSTALL all the necessary packages and libraries
```
cd installs;
./install_styfi.sh
```

Now, you can TEST the connectivity with FileCounter.war
for that, make sure to upload FileCounter.war from your local computer to the server directory ~/software_misc/
```
sudo service tomcat7 start
cd /var/lib/webapps
sudo cp ~/software_misc/FileCounter.war .
sudo service tomcat7 restart
```

You can test it by accessing http://<HOST-IP-ADDRESS>:8080/FileCounter/FileCounter
as a repsonse, you should see sth like: "This site has been accessed 1 times."

#~ Finally, SETUP MySQL database:
Start mysql
```
sudo service mysql start
sudo mysql -u root -p
```
Create the database as well as a new user, and manage permissions
```
mysql> create database fashion_hm;
mysql> use fashion_hm;
mysql> CREATE USER 'styfi'@'localhost' IDENTIFIED BY 'styfi';
mysql> GRANT ALL PRIVILEGES ON * . * TO 'styfi'@'localhost';
mysql> quit
```

Then, add infos from the scraped html files to the database
```
cd ~/git_repos/styfi-project
tar xzf infos.tar.gz 
python3 add_info_to_db.py 1
```

```
cd /var/lib/tomcat7/webapps
cp ~/software_misc/bash_script.sh .
sudo chmod +x bash_script.sh
```

Adjust the directory of the searchengine inside the bash_script.sh on line 3: `cd ~/git_repos/cv-sift-search/;` 


#~ Now, upload StyFiServer.war from software_misc/
```
cd /var/lib/tomcat7/webapps
sudo rm -r StyFiServer*
sudo cp ~/software_misc/StyFiServer.war .
sudo service tomcat7 restart
sudo cp bash_script.sh StyFiServer
sudo chmod +x StyFiServer/bash_script.sh
```
