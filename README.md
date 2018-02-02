# exchain
Automated cryptocurrencies trading tool

### 1. Environment
```
exchain# apt-get update -y
exchain# apt-get install -y vim python python-pip mariadb-server python-mysql.connector tzdata
exchain# service mysql start
exchain# mysql_secure_installation
exchain# dpkg-reconfigure tzdata
```

### 2. Configure
```
exchain# cp ./storage/config.json.example ./storage/config.json
exchain# cp ./storage/database.sql.example ./storage/database.sql
exchain# vi ./storage/config.json
exchain# vi ./storage/database.sql
```

### 3. Import data
```
exchain# mysql -uroot < ./storage/database.sql
```

### 4. Run
```
exchain# mkdir tmp
exchain# python exchain > ./tmp/exchain.log 2>&1 &
```
