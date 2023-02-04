/*
 Navicat MySQL Data Transfer

 Source Server         : @ArchNAS
 Source Server Type    : MariaDB
 Source Server Version : 100904 (10.9.4-MariaDB)
 Source Host           : 127.0.0.1:3306
 Source Schema         : web_monitor

 Target Server Type    : MariaDB
 Target Server Version : 100904 (10.9.4-MariaDB)
 File Encoding         : 65001

 Date: 04/02/2023 11:51:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for websites
-- ----------------------------
DROP TABLE IF EXISTS `websites`;
CREATE TABLE `websites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `last_try_failed` tinyint(1) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;
