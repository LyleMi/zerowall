DROP DATABASE IF EXISTS `zerowall`;

CREATE DATABASE `zerowall` DEFAULT CHARACTER SET utf8 collate utf8_general_ci;

use `zerowall`;

CREATE TABLE `http` (
    `uid` VARCHAR(32) NOT NULL,
    `ip` VARCHAR(64) NOT NULL,
    `port` INT NOT NULL,
    `protocol` VARCHAR(10) NOT NULL
);

