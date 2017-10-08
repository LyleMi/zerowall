DROP DATABASE IF EXISTS `zerowall`;

CREATE DATABASE `zerowall` DEFAULT CHARACTER SET utf8 collate utf8_general_ci;

use `zerowall`;

CREATE TABLE `income` (
    -- `id` INT AUTO_INCREMENT,
    `uid` VARCHAR(32) NOT NULL,
    `ip` VARCHAR(64) NOT NULL, -- 1.1.1.1/24
    `port` VARCHAR(64) NOT NULL, -- '' / '24-89'
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

-- ex: key http verb, value get, type equal, allow true
-- ex: key http header ua, value sqlmap, type cotain, allow false

CREATE TABLE `log` (
    `uid` VARCHAR(32) NOT NULL,
    `src` VARCHAR(32) NOT NULL,
    `url` VARCHAR(32) NOT NULL,
    `full` VARCHAR(1000) NULL,
    `time` TIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE `setting` (
    `loglevel` INT NOT NULL DEFAULT 1; -- VERBOSE/DEBUG/...
);

INSERT INTO `setting` VALUES(1);