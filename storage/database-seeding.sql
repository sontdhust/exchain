DROP USER IF EXISTS 'trader';
DROP USER IF EXISTS 'watcher';
GRANT ALL ON `exchain`.* TO 'trader'@'localhost' IDENTIFIED BY 'asperitas';
GRANT REPLICATION SLAVE, REPLICATION CLIENT, SELECT ON *.* TO 'watcher'@'%' IDENTIFIED BY 'asperitas';
FLUSH PRIVILEGES;

USE `exchain`;

INSERT INTO `users` (`name`) VALUES ('trader');

INSERT INTO `tickers` (`exchange`, `pair`, `symbol`, `priority`) VALUES
    ('bitflyer', 'btcfxjpy', 'FX_BTC_JPY', 1);

INSERT INTO `assets` (`user_id`, `ticker_id`, `priority`, `size`) VALUES
    (1, 1, 1, 0);
