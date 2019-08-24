# exchain
Automated cryptocurrencies trading tool

- Parameters:
  - **path**: */home/dare/Workspace*
  - **interval**: *1*

### 0. Preparation
<pre>
host$ cd <b>path</b>
host$ git clone https://github.com/sontdhust/exchain
host$ docker run -dit --name exchain --expose=3306 -v <b>path</b>/exchain:<i>/root/exchain</i> ubuntu
host$ docker exec -it exchain bash
</pre>

### 1. Environment
```
exchain# cd ~/exchain
exchain# apt-get update -y
exchain# apt-get install -y vim python python-pip mariadb-server tzdata cron git
exchain# service mysql start
exchain# mysql_secure_installation
exchain# vi /etc/mysql/mariadb.conf.d/50-server.cnf
```
> #bind-address = 127.0.0.1

```
exchain# service mysql restart --server-id=1 --log-bin --binlog-format=row --binlog-do-db=exchain
exchain# dpkg-reconfigure tzdata
exchain# pip install mysql-connector==2.1.6 requests
```

### 2. Import data
```
exchain# mysql -uroot < ./storage/database-migration.sql
exchain# mysql -uroot < ./storage/database-seeding.sql
```

### 3. Run
```
exchain# crontab -e
```
> */<b>interval</b> * * * * python <i>/root/exchain</i>/exchain

```
exchain# service cron start
```
