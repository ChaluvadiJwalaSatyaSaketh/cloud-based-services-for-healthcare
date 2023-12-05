/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 11.2.0-MariaDB : Database - healthcare_sector
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`healthcare_sector` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;

USE `healthcare_sector`;

/*Table structure for table `book_slot` */

DROP TABLE IF EXISTS `book_slot`;

CREATE TABLE `book_slot` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `dname` varchar(100) DEFAULT NULL,
  `demail` varchar(100) DEFAULT NULL,
  `pname` varchar(100) DEFAULT NULL,
  `pemail` varchar(100) DEFAULT NULL,
  `sym` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'Incomplete',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `book_slot` */

insert  into `book_slot`(`id`,`dname`,`demail`,`pname`,`pemail`,`sym`,`date`,`status`) values (1,'nakku','nakku@gmail.com','preeti','preeti@gmail.com','fever','2023-09-17','Uploaded');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `doctor` */

insert  into `doctor`(`id`,`fname`,`lname`,`email`,`pwd`,`area`,`addr`,`pno`,`status`) values (1,'nakku','star','nakku@gmail.com','1234','kengeri','bangalore','09685745892','Accepted');

/*Table structure for table `features` */

DROP TABLE IF EXISTS `features`;

CREATE TABLE `features` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `disp` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `features` */

insert  into `features`(`id`,`email`,`fname`,`disp`) values (1,'nakku@gmail.com','icu','good bad');

/*Table structure for table `patient` */

DROP TABLE IF EXISTS `patient`;

CREATE TABLE `patient` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `patient` */

insert  into `patient`(`id`,`fname`,`lname`,`email`,`pwd`,`addr`,`pno`,`status`) values (1,'preeti','desai','preeti@gmail.com','1234','bangalore','06589745677','Accepted');

/*Table structure for table `report` */

DROP TABLE IF EXISTS `report`;

CREATE TABLE `report` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `rid` int(10) DEFAULT NULL,
  `pname` varchar(100) DEFAULT NULL,
  `pemail` varchar(100) DEFAULT NULL,
  `dname` varchar(100) DEFAULT NULL,
  `demail` varchar(100) DEFAULT NULL,
  `sym` varchar(100) DEFAULT NULL,
  `disp` varchar(100) DEFAULT NULL,
  `report` longblob DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'Incomplete',
  `action` varchar(100) DEFAULT 'pending',
  `pkey` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `report` */

insert  into `report`(`id`,`rid`,`pname`,`pemail`,`dname`,`demail`,`sym`,`disp`,`report`,`date`,`status`,`action`,`pkey`) values (1,1,'preeti','preeti@gmail.com','nakku','nakku@gmail.com','fever','report','∫&5;Ú‰r3◊Å\r˜z;©˝','2023-09-17','Complated','Close','4a5eb52c');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
