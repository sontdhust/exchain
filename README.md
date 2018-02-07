# exchain
Automated cryptocurrencies trading tool

- Parameters:
  - **path**: */home/dare/Workspace*

### 0. Preparation
<pre>
host$ cd <b>path</b>
host$ git clone https://github.com/sontdhust/exchain
host$ docker run -dit --name exchain --expose=3306 -v <b>path</b>/exchain:/root/exchain ubuntu
host$ docker exec -it exchain bash
</pre>

### 1. Environment
```
exchain# cd ~/exchain
exchain# apt-get update -y
exchain# apt-get install -y vim python python-pip mariadb-server tzdata git
exchain# service mysql start
exchain# mysql_secure_installation
exchain# vi /etc/mysql/mariadb.conf.d/50-server.cnf
```
> #bind-address = 127.0.0.1

```
exchain# service mysql restart
exchain# dpkg-reconfigure tzdata
exchain# pip install mysql-connector==2.1.6 requests
```

### 2. Configure
```
exchain# cp ./storage/config.json.example ./storage/config.json
exchain# cp ./storage/database-migration.sql.default ./storage/database-migration.sql
exchain# cp ./storage/database-seeding.sql.example ./storage/database-seeding.sql
exchain# vi ./storage/config.json
exchain# vi ./storage/database-seeding.sql
```

### 3. Import data
```
exchain# mysql -uroot < ./storage/database-migration.sql
exchain# mysql -uroot < ./storage/database-seeding.sql
```

### 4. Run
```
exchain# mkdir tmp
exchain# python exchain > ./tmp/exchain.log 2>&1 &
```
