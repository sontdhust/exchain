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
