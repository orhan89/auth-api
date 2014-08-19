SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `authapi` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `authapi` ;

-- -----------------------------------------------------
-- Table `authapi`.`applications`
-- -----------------------------------------------------
DROP TABLE `applications`;
CREATE TABLE `applications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `suffix` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `authapi`.`applications_key`
-- -----------------------------------------------------
DROP TABLE `applications_key`;
CREATE TABLE IF NOT EXISTS `applications_key` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_id` int(11) NOT NULL REFERENCES applications(id),
  `type` varchar(50) NOT NULL,
  `key` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
  KEY `key` (`key`),
  FOREIGN KEY (`application_id`)
  	  REFERENCES applications(id)
	  ON UPDATE CASCADE
	  ON DELETE CASCADE 
) ENGINE=InnoDB;

