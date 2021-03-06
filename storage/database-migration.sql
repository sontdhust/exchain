SET time_zone = '+09:00';
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';
SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `exchain`;
CREATE DATABASE IF NOT EXISTS `exchain` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;

USE `exchain`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `api` text COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '{"slack_webhook_url":"","bitflyer_api_key":"","bitflyer_api_secret":""}',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `tickers`;
CREATE TABLE `tickers` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `exchange` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `pair` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `symbol` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `priority` double(15, 5) NOT NULL COMMENT 'A higher value indicates a higher priority. `0` is ignored.',
    `side` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'close' COMMENT 'Either `buy`, `sell`, `hold`, `close`',
    `price` double(15, 5) NOT NULL DEFAULT '0.00000',
    `updated_at` timestamp NULL DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `assets`;
CREATE TABLE `assets` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `user_id` int(10) unsigned NOT NULL,
    `ticker_id` int(10) unsigned NOT NULL,
    `priority` double(15, 5) NOT NULL DEFAULT '0.00000' COMMENT 'A higher value indicates a higher priority. `0` is ignored.',
    `size` double(15, 5) NOT NULL,
    `updated_at` timestamp NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `assets_user_id_ticker_id_unique` (`user_id`, `ticker_id`),
    KEY `assets_user_id_foreign` (`user_id`),
    KEY `assets_ticker_id_foreign` (`ticker_id`),
    CONSTRAINT `assets_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
    CONSTRAINT `assets_ticker_id_foreign` FOREIGN KEY (`ticker_id`) REFERENCES `tickers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `trades`;
CREATE TABLE `trades` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `asset_id` int(10) unsigned NOT NULL,
    `side` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `price` double(15, 5) NOT NULL COMMENT 'Ticker price',
    `amount` double(15, 5) NOT NULL,
    `type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Either `market`, `limit`, `stop`...',
    `executed` tinyint(1) NOT NULL DEFAULT '0',
    `created_at` timestamp NULL DEFAULT NULL,
    `updated_at` timestamp NULL DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `trades_asset_id_foreign` (`asset_id`),
    CONSTRAINT `trades_asset_id_foreign` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
