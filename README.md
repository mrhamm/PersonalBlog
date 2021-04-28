

To install dependencies:
$ python3 -m pip install requirements.txt

To run a development server, rune the following from the project main directory
$ python3 run.py
open "localhost:5000" in browser to view site


**ElasticSearch Settings**
If you wish to test the search engine functionality - start a local elasticsearch
service on port 9200.  If you've never done this, we refer to
https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html


**Docker File**
The docker file is currently configured to start a 3 node cluster on port 9200.  
TO USE AN IMAGE YOU MUST CHANGE THE VALUE OF THE ELASTICSEARCH_URL IN THE .env FILE TO BE "http:es01:9200" 
Run the following:
$ sudo docker build -t blog:test .
$ sudo docker-compose up
Open localhost:5000 to see the server

**Database** 
This version only uses a SQLite database - this will get deleted from any container once the container is stopped.  
In the event that you intend to use the dockerized version for deployment, you will need to configure a different database type.

For small applications, the SQLite database should suffice.

**Administrative Permissions**
The database can be managed at the /admin route.  This route requires you login as an admin at /logintoedit

Default Admin Username: Admin
Default Admin Password: password

To change to a different password, enter the ascii representation of the SHA256 hash of your desired password
into the .env file.  

**Email Capabilities**
To enable the "contact me" form.  You should enter your yahoo email address and password into the .env file.  
Alternatively, you can change to a different mail serve.  You may need to configure your email to give 
the app email permissions.  
The SENDER_EMAIL and RECEIVER_EMAIL variables will be the addresses you choose to send and receive the messages