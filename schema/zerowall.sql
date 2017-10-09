DROP DATABASE IF EXISTS `zerowall`;

CREATE DATABASE `zerowall` DEFAULT CHARACTER SET utf8 collate utf8_general_ci;

use `zerowall`;

CREATE TABLE `income` (
    `uid` VARCHAR(32) NOT NULL,
    `ip` VARCHAR(64) NOT NULL, -- 1.1.1.1/24
    `allow` BOOLEAN NOT NULL,
    `comment` VARCHAR(200) NULL
);

CREATE TABLE `http` (
    `uid` VARCHAR(32) NOT NULL,
    `key` VARCHAR(64) NOT NULL, 
    `value` VARCHAR(64) NOT NULL, 
    `type` VARCHAR(10) NOT NULL, -- regex/cotain/equal
    `allow` BOOLEAN NOT NULL,
);

-- e.g.: key http verb, value get, type equal, allow true
-- e.g.: key http header ua, value sqlmap, type cotain, allow false

CREATE TABLE `log` (
    `uid` VARCHAR(32) NOT NULL,
    `srcip` VARCHAR(32) NOT NULL,
    `url` VARCHAR(32) NOT NULL,
    `full` VARCHAR(1000) NULL, -- depend on log level
    `resp` TEXT NULL, -- depend on log level
    `time` TIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE `setting` (
    `logfull` BOOLEAN NOT NULL DEFAULT 0,
    `logresp` BOOLEAN NOT NULL DEFAULT 0 
);

INSERT INTO `setting` VALUES(0, 0);