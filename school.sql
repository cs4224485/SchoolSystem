-- MySQL dump 10.14  Distrib 5.5.60-MariaDB, for Linux (x86_64)
--
-- Host: 172.16.123.203    Database: schooladmin
-- ------------------------------------------------------
-- Server version	5.5.60-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `schooladmin`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `schooladmin` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `schooladmin`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add allergy',7,'add_allergy'),(26,'Can change allergy',7,'change_allergy'),(27,'Can delete allergy',7,'delete_allergy'),(28,'Can view allergy',7,'view_allergy'),(29,'Can add country',8,'add_country'),(30,'Can change country',8,'change_country'),(31,'Can delete country',8,'delete_country'),(32,'Can view country',8,'view_country'),(33,'Can add family info',9,'add_familyinfo'),(34,'Can change family info',9,'change_familyinfo'),(35,'Can delete family info',9,'delete_familyinfo'),(36,'Can view family info',9,'view_familyinfo'),(37,'Can add family member',10,'add_familymember'),(38,'Can change family member',10,'change_familymember'),(39,'Can delete family member',10,'delete_familymember'),(40,'Can view family member',10,'view_familymember'),(41,'Can add family status',11,'add_familystatus'),(42,'Can change family status',11,'change_familystatus'),(43,'Can delete family status',11,'delete_familystatus'),(44,'Can view family status',11,'view_familystatus'),(45,'Can add graduate institutions',12,'add_graduateinstitutions'),(46,'Can change graduate institutions',12,'change_graduateinstitutions'),(47,'Can delete graduate institutions',12,'delete_graduateinstitutions'),(48,'Can view graduate institutions',12,'view_graduateinstitutions'),(49,'Can add health info',13,'add_healthinfo'),(50,'Can change health info',13,'change_healthinfo'),(51,'Can delete health info',13,'delete_healthinfo'),(52,'Can view health info',13,'view_healthinfo'),(53,'Can add home address',14,'add_homeaddress'),(54,'Can change home address',14,'change_homeaddress'),(55,'Can delete home address',14,'delete_homeaddress'),(56,'Can view home address',14,'view_homeaddress'),(57,'Can add inherited disease',15,'add_inheriteddisease'),(58,'Can change inherited disease',15,'change_inheriteddisease'),(59,'Can delete inherited disease',15,'delete_inheriteddisease'),(60,'Can view inherited disease',15,'view_inheriteddisease'),(61,'Can add student info',16,'add_studentinfo'),(62,'Can change student info',16,'change_studentinfo'),(63,'Can delete student info',16,'delete_studentinfo'),(64,'Can view student info',16,'view_studentinfo'),(65,'Can add student inner info',17,'add_studentinnerinfo'),(66,'Can change student inner info',17,'change_studentinnerinfo'),(67,'Can delete student inner info',17,'delete_studentinnerinfo'),(68,'Can view student inner info',17,'view_studentinnerinfo'),(69,'Can add student parents',18,'add_studentparents'),(70,'Can change student parents',18,'change_studentparents'),(71,'Can delete student parents',18,'delete_studentparents'),(72,'Can view student parents',18,'view_studentparents'),(73,'Can add student privacy',19,'add_studentprivacy'),(74,'Can change student privacy',19,'change_studentprivacy'),(75,'Can delete student privacy',19,'delete_studentprivacy'),(76,'Can view student privacy',19,'view_studentprivacy'),(77,'Can add student to parents',20,'add_studenttoparents'),(78,'Can change student to parents',20,'change_studenttoparents'),(79,'Can delete student to parents',20,'delete_studenttoparents'),(80,'Can view student to parents',20,'view_studenttoparents'),(81,'Can add wechat open id',21,'add_wechatopenid'),(82,'Can change wechat open id',21,'change_wechatopenid'),(83,'Can delete wechat open id',21,'delete_wechatopenid'),(84,'Can view wechat open id',21,'view_wechatopenid'),(85,'Can add competent organization',22,'add_competentorganization'),(86,'Can change competent organization',22,'change_competentorganization'),(87,'Can delete competent organization',22,'delete_competentorganization'),(88,'Can view competent organization',22,'view_competentorganization'),(89,'Can add school history',23,'add_schoolhistory'),(90,'Can change school history',23,'change_schoolhistory'),(91,'Can delete school history',23,'delete_schoolhistory'),(92,'Can view school history',23,'view_schoolhistory'),(93,'Can add major',24,'add_major'),(94,'Can change major',24,'change_major'),(95,'Can delete major',24,'delete_major'),(96,'Can view major',24,'view_major'),(97,'Can add school boundary',25,'add_schoolboundary'),(98,'Can change school boundary',25,'change_schoolboundary'),(99,'Can delete school boundary',25,'delete_schoolboundary'),(100,'Can view school boundary',25,'view_schoolboundary'),(101,'Can add system',26,'add_system'),(102,'Can change system',26,'change_system'),(103,'Can delete system',26,'delete_system'),(104,'Can view system',26,'view_system'),(105,'Can add school to title',27,'add_schooltotitle'),(106,'Can change school to title',27,'change_schooltotitle'),(107,'Can delete school to title',27,'delete_schooltotitle'),(108,'Can view school to title',27,'view_schooltotitle'),(109,'Can add group',28,'add_group'),(110,'Can change group',28,'change_group'),(111,'Can delete group',28,'delete_group'),(112,'Can view group',28,'view_group'),(113,'Can add school honor',29,'add_schoolhonor'),(114,'Can change school honor',29,'change_schoolhonor'),(115,'Can delete school honor',29,'delete_schoolhonor'),(116,'Can view school honor',29,'view_schoolhonor'),(117,'Can add school to honor',30,'add_schooltohonor'),(118,'Can change school to honor',30,'change_schooltohonor'),(119,'Can delete school to honor',30,'delete_schooltohonor'),(120,'Can view school to honor',30,'view_schooltohonor'),(121,'Can add school title',31,'add_schooltitle'),(122,'Can change school title',31,'change_schooltitle'),(123,'Can delete school title',31,'delete_schooltitle'),(124,'Can view school title',31,'view_schooltitle'),(125,'Can add school info',32,'add_schoolinfo'),(126,'Can change school info',32,'change_schoolinfo'),(127,'Can delete school info',32,'delete_schoolinfo'),(128,'Can view school info',32,'view_schoolinfo'),(129,'Can add community',33,'add_community'),(130,'Can change community',33,'change_community'),(131,'Can delete community',33,'delete_community'),(132,'Can view community',33,'view_community'),(133,'Can add assessment',34,'add_assessment'),(134,'Can change assessment',34,'change_assessment'),(135,'Can delete assessment',34,'delete_assessment'),(136,'Can view assessment',34,'view_assessment'),(137,'Can add score line',35,'add_scoreline'),(138,'Can change score line',35,'change_scoreline'),(139,'Can delete score line',35,'delete_scoreline'),(140,'Can view score line',35,'view_scoreline'),(141,'Can add choice field',36,'add_choicefield'),(142,'Can change choice field',36,'change_choicefield'),(143,'Can delete choice field',36,'delete_choicefield'),(144,'Can view choice field',36,'view_choicefield'),(145,'Can add field type',37,'add_fieldtype'),(146,'Can change field type',37,'change_fieldtype'),(147,'Can delete field type',37,'delete_fieldtype'),(148,'Can view field type',37,'view_fieldtype'),(149,'Can add school settings',38,'add_schoolsettings'),(150,'Can change school settings',38,'change_schoolsettings'),(151,'Can delete school settings',38,'delete_schoolsettings'),(152,'Can view school settings',38,'view_schoolsettings'),(153,'Can add setting to field',39,'add_settingtofield'),(154,'Can change setting to field',39,'change_settingtofield'),(155,'Can delete setting to field',39,'delete_settingtofield'),(156,'Can view setting to field',39,'view_settingtofield'),(157,'Can add scope of filling',40,'add_scopeoffilling'),(158,'Can change scope of filling',40,'change_scopeoffilling'),(159,'Can delete scope of filling',40,'delete_scopeoffilling'),(160,'Can view scope of filling',40,'view_scopeoffilling'),(161,'Can add stu class',41,'add_stuclass'),(162,'Can change stu class',41,'change_stuclass'),(163,'Can delete stu class',41,'delete_stuclass'),(164,'Can view stu class',41,'view_stuclass'),(165,'Can add country',42,'add_country'),(166,'Can change country',42,'change_country'),(167,'Can delete country',42,'delete_country'),(168,'Can view country',42,'view_country');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$120000$RQlWQbWMD4GH$0MTrlrT+DZoYUw5V7KFTkFk1g4eNHSuvVCFumZaPskM=','2018-10-10 09:09:29.981756',1,'harry','','','',1,1,'2018-09-25 09:42:57.847993');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-09-25 09:43:21.199407','1','青霉素',1,'[{\"added\": {}}]',7,1),(2,'2018-09-25 09:43:27.855271','1','花粉',2,'[{\"changed\": {\"fields\": [\"title\"]}}]',7,1),(3,'2018-09-25 09:43:32.840373','1','牛奶',2,'[{\"changed\": {\"fields\": [\"title\"]}}]',7,1),(4,'2018-09-25 09:43:40.964487','1','海鲜',2,'[{\"changed\": {\"fields\": [\"title\"]}}]',7,1),(5,'2018-09-25 09:43:44.981414','1','橘子',2,'[{\"changed\": {\"fields\": [\"title\"]}}]',7,1),(6,'2018-09-25 09:43:57.951983','1','中国',1,'[{\"added\": {}}]',8,1),(7,'2018-09-25 09:44:13.570405','1','美国',2,'[{\"changed\": {\"fields\": [\"country_name\", \"english_name\", \"img\"]}}]',8,1),(8,'2018-09-25 09:44:25.585968','2','青霉素',1,'[{\"added\": {}}]',7,1),(9,'2018-09-25 09:44:28.165327','3','花粉',1,'[{\"added\": {}}]',7,1),(10,'2018-09-25 09:44:30.066386','4','牛奶',1,'[{\"added\": {}}]',7,1),(11,'2018-09-25 09:44:32.490613','5','海鲜',1,'[{\"added\": {}}]',7,1),(12,'2018-09-25 09:44:52.056844','2','中国',1,'[{\"added\": {}}]',8,1),(13,'2018-09-25 09:45:14.052938','1','三目国际学校',1,'[{\"added\": {}}]',12,1),(14,'2018-09-25 09:45:20.802344','2','三目小学西安校区',1,'[{\"added\": {}}]',12,1),(15,'2018-09-25 09:45:29.002564','3','三目小学北京校区',1,'[{\"added\": {}}]',12,1),(16,'2018-09-25 09:45:38.981271','4','乐城国际学校',1,'[{\"added\": {}}]',12,1),(17,'2018-09-25 09:45:46.767275','5','三目小学',1,'[{\"added\": {}}]',12,1),(18,'2018-09-25 09:45:58.616368','1','高血压',1,'[{\"added\": {}}]',15,1),(19,'2018-09-25 09:46:03.615808','2','心脏病',1,'[{\"added\": {}}]',15,1),(20,'2018-09-25 09:47:08.503087','2','中国',3,'',8,1),(21,'2018-09-25 09:47:08.505115','1','美国',3,'',8,1),(22,'2018-09-25 09:47:27.043855','3','中国',1,'[{\"added\": {}}]',8,1),(23,'2018-09-25 09:47:34.604948','4','美国',1,'[{\"added\": {}}]',8,1),(24,'2018-09-25 10:10:00.488386','1','张三',3,'',19,1),(25,'2018-09-25 10:19:51.947699','15','张三',3,'',19,1),(26,'2018-09-25 10:22:02.006774','17','张三',3,'',19,1),(27,'2018-09-25 10:27:48.346872','21','StudentInnerInfo object (21)',3,'',17,1),(28,'2018-09-25 10:27:48.348801','20','StudentInnerInfo object (20)',3,'',17,1),(29,'2018-09-25 10:27:48.350220','18','StudentInnerInfo object (18)',3,'',17,1),(30,'2018-09-25 10:27:48.351760','17','StudentInnerInfo object (17)',3,'',17,1),(31,'2018-09-25 10:27:48.353339','15','StudentInnerInfo object (15)',3,'',17,1),(32,'2018-09-25 10:27:48.354678','14','StudentInnerInfo object (14)',3,'',17,1),(33,'2018-09-25 10:27:48.356098','1','StudentInnerInfo object (1)',3,'',17,1),(34,'2018-09-26 01:43:57.828054','21','张三',3,'',16,1),(35,'2018-09-26 01:49:59.857891','22','StudentInnerInfo object (22)',3,'',17,1),(36,'2018-09-26 01:50:27.183244','22','王三',3,'',16,1),(37,'2018-09-26 01:50:57.035364','23','王三',3,'',16,1),(38,'2018-09-26 08:26:51.455003','5','韩国',1,'[{\"added\": {}}]',8,1),(39,'2018-09-27 06:11:07.644085','1','再婚',1,'[{\"added\": {}}]',11,1),(40,'2018-09-27 06:11:11.720859','2','离异',1,'[{\"added\": {}}]',11,1),(41,'2018-09-27 06:11:14.653621','3','留守',1,'[{\"added\": {}}]',11,1),(42,'2018-09-27 06:11:17.834203','4','领养',1,'[{\"added\": {}}]',11,1),(43,'2018-09-27 06:11:22.820465','5','单亲',1,'[{\"added\": {}}]',11,1),(44,'2018-09-27 06:11:25.219568','6','其他',1,'[{\"added\": {}}]',11,1),(45,'2018-09-27 07:36:29.726028','3','李四家庭信息',3,'',9,1),(46,'2018-09-27 07:36:29.728037','2','李四家庭信息',3,'',9,1),(47,'2018-09-27 07:36:29.729472','1','王宇家庭信息',3,'',9,1),(48,'2018-09-27 07:36:36.373951','2','王二',3,'',18,1),(49,'2018-09-27 07:36:36.398367','1','王二',3,'',18,1),(50,'2018-09-27 07:37:09.395013','30','李四',3,'',19,1),(51,'2018-09-27 07:37:09.396756','29','王宇',3,'',19,1),(52,'2018-09-27 07:37:09.398177','28','张三',3,'',19,1),(53,'2018-09-27 07:37:09.399585','27','王一',3,'',19,1),(54,'2018-09-27 07:37:09.400948','26','王二',3,'',19,1),(55,'2018-09-27 07:37:09.402276','25','张三',3,'',19,1),(56,'2018-09-27 07:37:09.403712','24','张三',3,'',19,1),(57,'2018-09-27 07:37:19.495154','30','StudentInnerInfo object (30)',3,'',17,1),(58,'2018-09-27 07:37:19.497122','29','StudentInnerInfo object (29)',3,'',17,1),(59,'2018-09-27 07:37:19.498679','28','StudentInnerInfo object (28)',3,'',17,1),(60,'2018-09-27 07:37:19.500187','27','StudentInnerInfo object (27)',3,'',17,1),(61,'2018-09-27 07:37:19.501611','26','StudentInnerInfo object (26)',3,'',17,1),(62,'2018-09-27 07:37:19.502978','25','StudentInnerInfo object (25)',3,'',17,1),(63,'2018-09-27 07:37:19.504340','24','StudentInnerInfo object (24)',3,'',17,1),(64,'2018-09-27 10:55:12.187966','37','王一',3,'',19,1),(65,'2018-09-27 10:55:25.065086','37','StudentInfo object (37)',3,'',16,1),(66,'2018-09-27 10:56:50.960721','36','StudentInfo object (36)',3,'',16,1),(67,'2018-09-27 11:06:31.439306','29','王宇',3,'',16,1),(68,'2018-09-27 11:06:39.328836','1','张三',3,'',16,1),(69,'2018-09-27 11:06:45.102875','15','张三',3,'',16,1),(70,'2018-09-27 11:07:02.223672','28','张八',3,'',16,1),(71,'2018-09-27 11:07:02.225612','27','王一',3,'',16,1),(72,'2018-09-27 11:07:02.227081','26','王二',3,'',16,1),(73,'2018-09-27 11:07:02.228458','25','张三',3,'',16,1),(74,'2018-09-27 11:07:02.229825','24','张三',3,'',16,1),(75,'2018-09-27 11:07:02.231108','20','张三',3,'',16,1),(76,'2018-09-27 11:07:02.232423','18','张三',3,'',16,1),(77,'2018-09-27 11:07:02.233802','17','张三',3,'',16,1),(78,'2018-09-27 11:07:32.236767','35','StudentInnerInfo object (35)',3,'',17,1),(79,'2018-09-28 06:03:48.154026','38','张八',3,'',16,1),(80,'2018-09-28 06:03:48.156331','35','蒋XX',3,'',16,1),(81,'2018-09-28 06:03:48.158168','34','王一',3,'',16,1),(82,'2018-09-28 06:03:48.159937','33','王无',3,'',16,1),(83,'2018-09-28 06:03:48.161566','32','张八',3,'',16,1),(84,'2018-09-28 06:03:48.163322','31','王武',3,'',16,1),(85,'2018-09-28 06:03:48.164875','30','李四',3,'',16,1),(86,'2018-09-28 06:37:31.171523','40','王二',3,'',16,1),(87,'2018-09-28 07:36:51.479957','44','宋婷',3,'',16,1),(88,'2018-09-29 02:01:37.684173','39','张八',3,'',16,1),(89,'2018-10-09 07:28:56.811426','56','打发打发',3,'',38,1),(90,'2018-10-09 07:28:56.814326','55','打发打发',3,'',38,1),(91,'2018-10-09 07:28:56.815764','54','打发打发',3,'',38,1),(92,'2018-10-09 07:28:56.817203','53','适当放大',3,'',38,1),(93,'2018-10-09 07:28:56.818640','52','适当放大',3,'',38,1),(94,'2018-10-09 07:28:56.820059','51','适当放大',3,'',38,1),(95,'2018-10-09 07:28:56.821521','50','适当放大',3,'',38,1),(96,'2018-10-09 07:28:56.823204','49','适当放大',3,'',38,1),(97,'2018-10-09 07:28:56.824900','48','适当放大',3,'',38,1),(98,'2018-10-09 07:28:56.826297','47','适当放大',3,'',38,1),(99,'2018-10-09 07:28:56.827691','46','适当放大',3,'',38,1),(100,'2018-10-09 07:28:56.829445','45','适当放大',3,'',38,1),(101,'2018-10-09 07:28:56.830886','44','是的发放',3,'',38,1),(102,'2018-10-09 07:28:56.832417','43','大概是法国',3,'',38,1),(103,'2018-10-09 07:28:56.833959','42','大概是法国',3,'',38,1),(104,'2018-10-09 07:28:56.835343','41','的说法',3,'',38,1),(105,'2018-10-09 07:28:56.837108','40','学生调查',3,'',38,1),(106,'2018-10-09 07:28:56.838484','39','学生调查',3,'',38,1),(107,'2018-10-09 07:28:56.840700','38','海鲜',3,'',38,1),(108,'2018-10-09 07:28:56.842111','37','海鲜',3,'',38,1),(109,'2018-10-09 07:28:56.843533','36','海鲜',3,'',38,1),(110,'2018-10-09 07:28:56.845037','35','士大夫撒旦发',3,'',38,1),(111,'2018-10-09 07:28:56.846412','34','士大夫撒旦发',3,'',38,1),(112,'2018-10-09 07:28:56.847834','33','士大夫',3,'',38,1),(113,'2018-10-09 07:28:56.849209','32','青霉素',3,'',38,1),(114,'2018-10-09 07:28:56.850619','31','学生2',3,'',38,1),(115,'2018-10-09 07:28:56.852126','30','学生2',3,'',38,1),(116,'2018-10-09 07:28:56.853517','29','学生2',3,'',38,1),(117,'2018-10-09 07:28:56.854979','28','学生2',3,'',38,1),(118,'2018-10-09 07:28:56.856421','27','学生2',3,'',38,1),(119,'2018-10-09 07:28:56.857881','26','学生2',3,'',38,1),(120,'2018-10-09 07:28:56.859238','25','学生2',3,'',38,1),(121,'2018-10-09 07:28:56.860647','24','学生2',3,'',38,1),(122,'2018-10-09 07:28:56.862081','23','学生2',3,'',38,1),(123,'2018-10-09 07:28:56.863455','22','学生2',3,'',38,1),(124,'2018-10-09 07:28:56.864865','21','学生2',3,'',38,1),(125,'2018-10-09 07:28:56.866249','20','学生2',3,'',38,1),(126,'2018-10-09 07:28:56.867780','19','学生2',3,'',38,1),(127,'2018-10-09 07:28:56.869189','18','学生2',3,'',38,1),(128,'2018-10-09 07:28:56.870681','17','学生2',3,'',38,1),(129,'2018-10-09 07:28:56.872875','16','学生2',3,'',38,1),(130,'2018-10-09 07:28:56.874252','15','学生2',3,'',38,1),(131,'2018-10-09 07:28:56.875634','14','学生',3,'',38,1),(132,'2018-10-09 07:28:56.877048','13','学生',3,'',38,1),(133,'2018-10-09 07:28:56.878414','12','学生',3,'',38,1),(134,'2018-10-09 07:28:56.879969','11','学生',3,'',38,1),(135,'2018-10-09 07:28:56.881382','10','学生',3,'',38,1),(136,'2018-10-09 07:28:56.882807','9','学生',3,'',38,1),(137,'2018-10-09 07:28:56.884196','8','牛奶',3,'',38,1),(138,'2018-10-09 07:28:56.885604','7','sdf ',3,'',38,1),(139,'2018-10-09 07:28:56.887129','6','海鲜',3,'',38,1),(140,'2018-10-09 07:28:56.888572','5','花粉',3,'',38,1),(141,'2018-10-09 07:28:56.890030','4','青霉素',3,'',38,1),(142,'2018-10-09 07:28:56.891398','3','花粉',3,'',38,1),(143,'2018-10-09 07:28:56.892839','2','心脏病',3,'',38,1),(144,'2018-10-09 07:28:56.894243','1','海鲜',3,'',38,1),(145,'2018-10-09 08:02:44.069614','1','ScopeOfFilling object (1)',1,'[{\"added\": {}}]',40,1),(146,'2018-10-09 08:02:46.637355','2','ScopeOfFilling object (2)',1,'[{\"added\": {}}]',40,1),(147,'2018-10-09 08:02:50.050958','3','ScopeOfFilling object (3)',1,'[{\"added\": {}}]',40,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(34,'school','assessment'),(36,'school','choicefield'),(33,'school','community'),(22,'school','competentorganization'),(42,'school','country'),(37,'school','fieldtype'),(28,'school','group'),(24,'school','major'),(25,'school','schoolboundary'),(23,'school','schoolhistory'),(29,'school','schoolhonor'),(32,'school','schoolinfo'),(38,'school','schoolsettings'),(31,'school','schooltitle'),(30,'school','schooltohonor'),(27,'school','schooltotitle'),(40,'school','scopeoffilling'),(35,'school','scoreline'),(39,'school','settingtofield'),(26,'school','system'),(6,'sessions','session'),(7,'students','allergy'),(8,'students','country'),(9,'students','familyinfo'),(10,'students','familymember'),(11,'students','familystatus'),(12,'students','graduateinstitutions'),(13,'students','healthinfo'),(14,'students','homeaddress'),(15,'students','inheriteddisease'),(41,'students','stuclass'),(16,'students','studentinfo'),(17,'students','studentinnerinfo'),(18,'students','studentparents'),(19,'students','studentprivacy'),(20,'students','studenttoparents'),(21,'students','wechatopenid');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6tr7qg5187xhh5exmrrzd7ggqzh6bzha','MjBkNmFmZDhmNTdjM2ZhNjM2OGViNTUzNzg0NWNlY2MzOGZmZWJiMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOWFjNjA3ZDRlZGUyMTVjNWRjMmQ2NDIzZjJhN2ZlNmY5MDZmNGUzIn0=','2018-10-24 09:09:29.984042'),('didv9nz13hhs2oenenxe4nauwl4ffqnc','MjBkNmFmZDhmNTdjM2ZhNjM2OGViNTUzNzg0NWNlY2MzOGZmZWJiMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOWFjNjA3ZDRlZGUyMTVjNWRjMmQ2NDIzZjJhN2ZlNmY5MDZmNGUzIn0=','2018-10-09 09:43:12.292739');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_assessment`
--

DROP TABLE IF EXISTS `school_assessment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_assessment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_assessment`
--

LOCK TABLES `school_assessment` WRITE;
/*!40000 ALTER TABLE `school_assessment` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_assessment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_choicefield`
--

DROP TABLE IF EXISTS `school_choicefield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_choicefield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fieldName` varchar(32) NOT NULL,
  `field_english` varchar(32) NOT NULL,
  `field_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_choicefield_field_type_id_9aab7bc7_fk_school_fieldtype_id` (`field_type_id`),
  CONSTRAINT `school_choicefield_field_type_id_9aab7bc7_fk_school_fieldtype_id` FOREIGN KEY (`field_type_id`) REFERENCES `school_fieldtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_choicefield`
--

LOCK TABLES `school_choicefield` WRITE;
/*!40000 ALTER TABLE `school_choicefield` DISABLE KEYS */;
INSERT INTO `school_choicefield` VALUES (1,'性别','gender',1),(2,'国籍','country',1),(3,'民族','nation',1),(4,'生日','birthday',1),(5,'照片','photo',1),(6,'邮箱','email',1),(7,'届别','period',1),(8,'毕业园校','graduate_institutions',1),(9,'户籍','resident',1),(10,'姓名','full_name',1),(11,'身份证','id_card',1),(12,'班级','school_class',1),(13,'所在学校','school',1),(14,'身高','height',2),(15,'体重','weight',2),(16,'视力','vision',2),(17,'视力状况','vision_status',2),(18,'残疾状况','disability',2),(19,'血型','blood_type',2),(20,'过敏源','allergy',2),(21,'遗传病','InheritedDisease',2),(22,'居住条件','living_condition',3),(23,'居住类型','living_type',3),(24,'家庭语言','language',3),(25,'家庭状况','family_status',3),(26,'家长姓名','name',4),(27,'家长生日','parents_birthday',4),(28,'家长电话','telephone',4),(29,'学历','education',4),(30,'工作单位','company',4),(31,'职务','job',4),(32,'家长微信','parents_wechat',4);
/*!40000 ALTER TABLE `school_choicefield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_community`
--

DROP TABLE IF EXISTS `school_community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_community` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_community`
--

LOCK TABLES `school_community` WRITE;
/*!40000 ALTER TABLE `school_community` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_community` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_competentorganization`
--

DROP TABLE IF EXISTS `school_competentorganization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_competentorganization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_competentorganization`
--

LOCK TABLES `school_competentorganization` WRITE;
/*!40000 ALTER TABLE `school_competentorganization` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_competentorganization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_fieldtype`
--

DROP TABLE IF EXISTS `school_fieldtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_fieldtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_fieldtype`
--

LOCK TABLES `school_fieldtype` WRITE;
/*!40000 ALTER TABLE `school_fieldtype` DISABLE KEYS */;
INSERT INTO `school_fieldtype` VALUES (1,1),(2,2),(3,3),(4,4);
/*!40000 ALTER TABLE `school_fieldtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_group`
--

DROP TABLE IF EXISTS `school_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_group`
--

LOCK TABLES `school_group` WRITE;
/*!40000 ALTER TABLE `school_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_major`
--

DROP TABLE IF EXISTS `school_major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_major` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(16) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_major`
--

LOCK TABLES `school_major` WRITE;
/*!40000 ALTER TABLE `school_major` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolboundary`
--

DROP TABLE IF EXISTS `school_schoolboundary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolboundary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Year` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_schoolboundary_school_id_563eafbd_fk_school_schoolinfo_id` (`school_id`),
  CONSTRAINT `school_schoolboundary_school_id_563eafbd_fk_school_schoolinfo_id` FOREIGN KEY (`school_id`) REFERENCES `school_schoolinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolboundary`
--

LOCK TABLES `school_schoolboundary` WRITE;
/*!40000 ALTER TABLE `school_schoolboundary` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schoolboundary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolhistory`
--

DROP TABLE IF EXISTS `school_schoolhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` int(11) NOT NULL,
  `start_time` date NOT NULL,
  `end_time` date NOT NULL,
  `old_name` varchar(64) NOT NULL,
  `new_name` varchar(64) NOT NULL,
  `school_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_schoolhistory_school_id_dd4a70d3_fk_school_schoolinfo_id` (`school_id`),
  CONSTRAINT `school_schoolhistory_school_id_dd4a70d3_fk_school_schoolinfo_id` FOREIGN KEY (`school_id`) REFERENCES `school_schoolinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolhistory`
--

LOCK TABLES `school_schoolhistory` WRITE;
/*!40000 ALTER TABLE `school_schoolhistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schoolhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolhonor`
--

DROP TABLE IF EXISTS `school_schoolhonor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolhonor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  `assessment_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_schoolhonor_assessment_id_cce7428b_fk_school_as` (`assessment_id`),
  CONSTRAINT `school_schoolhonor_assessment_id_cce7428b_fk_school_as` FOREIGN KEY (`assessment_id`) REFERENCES `school_assessment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolhonor`
--

LOCK TABLES `school_schoolhonor` WRITE;
/*!40000 ALTER TABLE `school_schoolhonor` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schoolhonor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolinfo`
--

DROP TABLE IF EXISTS `school_schoolinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `school_name` varchar(64) NOT NULL,
  `English_name` varchar(64) DEFAULT NULL,
  `abbreviation` varchar(16) DEFAULT NULL,
  `internal_id` varchar(255) NOT NULL,
  `school_code` varchar(64) DEFAULT NULL,
  `local_school_name` varchar(64) DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `pattern` varchar(100) DEFAULT NULL,
  `website` varchar(128) DEFAULT NULL,
  `school_type` int(11) NOT NULL,
  `school_layer` int(11) NOT NULL,
  `create_time` date DEFAULT NULL,
  `province` varchar(32) NOT NULL,
  `city` varchar(32) NOT NULL,
  `region` varchar(32) NOT NULL,
  `street` varchar(32) DEFAULT NULL,
  `address` varchar(128) NOT NULL,
  `campus_district` varchar(32) DEFAULT NULL,
  `campus_english_name` varchar(32) DEFAULT NULL,
  `community_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `system_id` int(11) DEFAULT NULL,
  `country` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `internal_id` (`internal_id`),
  KEY `school_schoolinfo_group_id_1d773119_fk_school_group_id` (`group_id`),
  KEY `school_schoolinfo_school_name_cbbb724e` (`school_name`),
  KEY `school_schoolinfo_system_id_a13b0f05_fk_school_system_id` (`system_id`),
  KEY `school_schoolinfo_community_id_8529e9e1_fk_school_community_id` (`community_id`),
  CONSTRAINT `school_schoolinfo_community_id_8529e9e1_fk_school_community_id` FOREIGN KEY (`community_id`) REFERENCES `school_community` (`id`),
  CONSTRAINT `school_schoolinfo_group_id_1d773119_fk_school_group_id` FOREIGN KEY (`group_id`) REFERENCES `school_group` (`id`),
  CONSTRAINT `school_schoolinfo_system_id_a13b0f05_fk_school_system_id` FOREIGN KEY (`system_id`) REFERENCES `school_system` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolinfo`
--

LOCK TABLES `school_schoolinfo` WRITE;
/*!40000 ALTER TABLE `school_schoolinfo` DISABLE KEYS */;
INSERT INTO `school_schoolinfo` VALUES (1,'XXXX小学',NULL,NULL,'',NULL,NULL,'','',NULL,1,2,NULL,'陕西省','西安市','雁塔区',NULL,'XXXXX路',NULL,NULL,NULL,NULL,NULL,'1'),(3,'3606学校',NULL,NULL,'2e8e33d7-3b3e-497b-8229-6da3a8f3a6be',NULL,NULL,'','',NULL,2,1,NULL,'陕西','西安','高新',NULL,'科技路500号',NULL,NULL,NULL,NULL,NULL,'1'),(4,'盐道街小学','ChengDu Yandaojie Primary School',NULL,'7be61359-c05b-47b3-81bf-59f3a6f5e2ef',NULL,NULL,'','',NULL,1,2,NULL,'四川省','成都市','锦江区',NULL,'盐道街2号',NULL,NULL,NULL,NULL,NULL,'1'),(5,'盐道街小学','ChengDu Yandaojie Primary School（East）',NULL,'20463166-4861-4777-b1e3-a9980a88eb3c',NULL,NULL,'','',NULL,1,2,NULL,'四川省','成都市','锦江区',NULL,'莲花南路10号','东区',NULL,NULL,NULL,NULL,'1'),(9,'吉林省第二实验学校','The Second Experimental School Of Jilin Province',NULL,'8d58d633-c4ff-4de6-a289-bbf2aa470525',NULL,NULL,'','',NULL,1,4,NULL,'吉林省','长春市','朝阳区',NULL,'南湖新村中街421号','南湖校区',NULL,NULL,NULL,NULL,'1'),(11,'吉林省第二实验学校','The Second Experimental Gaoxin School Of Jilin Province',NULL,'1c48411c-f3de-4d2a-8f53-4f16575c9cb9',NULL,NULL,'','',NULL,1,4,NULL,'吉林省','长春市','朝阳区',NULL,'华光街1001号','高新校区',NULL,NULL,NULL,NULL,'1'),(13,'武汉大学附属中学','Wuhan University Middle School',NULL,'1d8fbe66-1ec4-4196-8a1e-30f39d6d66e1',NULL,NULL,'','',NULL,1,3,NULL,'湖北省','武汉市','洪山区',NULL,'八一路29号',NULL,NULL,NULL,NULL,NULL,'1');
/*!40000 ALTER TABLE `school_schoolinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolinfo_competent_organization`
--

DROP TABLE IF EXISTS `school_schoolinfo_competent_organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolinfo_competent_organization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `schoolinfo_id` int(11) NOT NULL,
  `competentorganization_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `school_schoolinfo_compet_schoolinfo_id_competento_b0e8fb78_uniq` (`schoolinfo_id`,`competentorganization_id`),
  KEY `school_schoolinfo_co_competentorganizatio_7071a98d_fk_school_co` (`competentorganization_id`),
  CONSTRAINT `school_schoolinfo_co_competentorganizatio_7071a98d_fk_school_co` FOREIGN KEY (`competentorganization_id`) REFERENCES `school_competentorganization` (`id`),
  CONSTRAINT `school_schoolinfo_co_schoolinfo_id_667f2118_fk_school_sc` FOREIGN KEY (`schoolinfo_id`) REFERENCES `school_schoolinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolinfo_competent_organization`
--

LOCK TABLES `school_schoolinfo_competent_organization` WRITE;
/*!40000 ALTER TABLE `school_schoolinfo_competent_organization` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schoolinfo_competent_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolinfo_major`
--

DROP TABLE IF EXISTS `school_schoolinfo_major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolinfo_major` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `schoolinfo_id` int(11) NOT NULL,
  `major_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `school_schoolinfo_major_schoolinfo_id_major_id_b42b645c_uniq` (`schoolinfo_id`,`major_id`),
  KEY `school_schoolinfo_major_major_id_85b3f9ee_fk_school_major_id` (`major_id`),
  CONSTRAINT `school_schoolinfo_major_major_id_85b3f9ee_fk_school_major_id` FOREIGN KEY (`major_id`) REFERENCES `school_major` (`id`),
  CONSTRAINT `school_schoolinfo_ma_schoolinfo_id_e7746c03_fk_school_sc` FOREIGN KEY (`schoolinfo_id`) REFERENCES `school_schoolinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolinfo_major`
--

LOCK TABLES `school_schoolinfo_major` WRITE;
/*!40000 ALTER TABLE `school_schoolinfo_major` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schoolinfo_major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolsettings`
--

DROP TABLE IF EXISTS `school_schoolsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolsettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stat_time` date NOT NULL,
  `end_time` date NOT NULL,
  `title` varchar(64) NOT NULL,
  `Qrcode` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolsettings`
--

LOCK TABLES `school_schoolsettings` WRITE;
/*!40000 ALTER TABLE `school_schoolsettings` DISABLE KEYS */;
INSERT INTO `school_schoolsettings` VALUES (57,'2018-10-10','2018-10-12','学生问卷调查','fe881c0f-24fc-4190-8386-2f80add47d98.png'),(58,'2018-10-10','2018-10-12','学生问卷调查2','44783847-9dfe-4653-bc93-25124e83469d.png'),(59,'2018-10-10','2018-10-12','学生问卷调查3','838756a1-0177-4be4-8666-82fec6f8fef0.png'),(60,'2018-10-10','2018-10-18','学生调查表','c417d84c-19a5-47a4-a208-12627ec7f72d.png'),(61,'2018-10-10','2018-10-11','学生问卷','e423764f-36e1-4b11-af11-f1145a9cac7e.png'),(62,'2018-10-10','2018-10-11','学生调查XXX','5848cec8-e46d-4471-85e7-e3f7770a3a98.png'),(63,'2018-10-10','2018-10-11','学生调查XXX','eef5f6d0-be7c-4fdd-81f3-b264235504e8.png'),(64,'2018-10-10','2018-10-11','学生调查XXX','98998d46-99ad-4145-b933-8c3bfbd945f0.png'),(65,'2018-10-10','2018-10-11','学生调查XXX','936b454d-d13a-4f2e-ad7c-56d525cfaf1a.png'),(66,'2018-10-10','2018-10-11','学生调查XXX','11df6fc7-536a-4ccc-b2ca-ae3d46a00b85.png'),(67,'2018-10-10','2018-10-11','学生调查XXX','a569a72c-52bc-482f-926f-f6e2c1c0f0af.png'),(68,'2018-10-10','2018-10-17','学生表单','28528fff-0440-435d-a7e1-9bea3af963bf.png'),(69,'2018-10-21','2018-10-26','cxvcbvv','e6745f95-0b44-41b2-ab38-8d6ff2f83a0a.png'),(70,'2018-10-10','2018-10-18','学生信息表','64f2ea5a-baa2-4c0d-9776-ab3d04f3e5fe.png'),(71,'2018-10-10','2018-10-12','学生入学','ebec91c4-febd-441a-8d53-3c661527842d.png'),(72,'2018-10-10','2018-10-12','学生入学','72ed3edf-27c6-41f8-aa7c-596905ab98df.png'),(73,'2018-10-11','2018-10-13','sdsfsf','ad437638-0af8-40bf-8ee0-82a57007847a.png'),(74,'2018-10-11','2018-10-12','sdfsdf','0f1198b9-35c8-4d4b-a391-33c0d86fbaf1.png'),(75,'2018-10-10','2018-10-12','是第三方','ee3ede52-910f-4c69-91e3-1bafaff1694f.png'),(76,'2018-10-17','2018-10-12','沙发沙发','f611aa35-3bc6-447f-8295-0a2687a4aaeb.png'),(77,'2018-10-10','2018-10-19','撒大苏打','5d526d29-14d8-4ddd-bf6f-c3f4da683f3e.png'),(78,'2018-10-10','2018-10-19','撒发生','a5960c3e-2332-4dfc-a1a9-7a8af11ae623.png'),(79,'2018-10-10','2018-10-12','打发士大夫','85b08085-10b2-45d9-b4db-747bde119677.png'),(80,'2018-10-10','2018-10-12','胜多负少','47172624-bb88-4429-8924-83210d4f088e.png'),(81,'2018-10-17','2018-10-19','的风格的','1eeb0a0e-89ed-43f1-8366-8de1ffe6e8b1.png'),(82,'2018-10-17','2018-10-18','的风格','1dc0eeb8-6a2b-49e5-baaa-cf8fe7fb4bf5.png'),(83,'2018-10-17','2018-10-18','士大夫十分','741b9736-ca3d-41b3-a899-4a1b60619720.png'),(84,'2018-10-11','2018-10-25','学生调查最新','6cf8e773-a800-495b-b936-46f38041ab42.png'),(85,'2018-10-11','2018-10-19','学校学生调查表','419a6d5a-4770-46c8-8577-ecc626a2ab24.png'),(86,'2018-10-11','2018-10-12','士大夫十分','cfe8e4eb-3621-4f03-bf4f-7d9fa94d781e.png');
/*!40000 ALTER TABLE `school_schoolsettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolsettings_fill_range`
--

DROP TABLE IF EXISTS `school_schoolsettings_fill_range`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolsettings_fill_range` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `schoolsettings_id` int(11) NOT NULL,
  `scopeoffilling_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `school_schoolsettings_fi_schoolsettings_id_scopeo_3c713438_uniq` (`schoolsettings_id`,`scopeoffilling_id`),
  KEY `school_schoolsetting_scopeoffilling_id_92915ddc_fk_school_sc` (`scopeoffilling_id`),
  CONSTRAINT `school_schoolsetting_scopeoffilling_id_92915ddc_fk_school_sc` FOREIGN KEY (`scopeoffilling_id`) REFERENCES `school_scopeoffilling` (`id`),
  CONSTRAINT `school_schoolsetting_schoolsettings_id_7e768818_fk_school_sc` FOREIGN KEY (`schoolsettings_id`) REFERENCES `school_schoolsettings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolsettings_fill_range`
--

LOCK TABLES `school_schoolsettings_fill_range` WRITE;
/*!40000 ALTER TABLE `school_schoolsettings_fill_range` DISABLE KEYS */;
INSERT INTO `school_schoolsettings_fill_range` VALUES (1,68,1),(2,68,2),(4,69,1),(3,69,2),(5,70,1),(6,71,1),(7,72,1),(9,73,1),(8,73,2),(10,73,3),(12,74,1),(11,74,2),(13,75,1),(14,82,2),(15,83,2),(17,84,2),(16,84,3),(19,85,1),(18,85,2),(21,86,2),(20,86,3);
/*!40000 ALTER TABLE `school_schoolsettings_fill_range` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schoolsettings_school_range`
--

DROP TABLE IF EXISTS `school_schoolsettings_school_range`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schoolsettings_school_range` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `schoolsettings_id` int(11) NOT NULL,
  `schoolinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `school_schoolsettings_sc_schoolsettings_id_school_d30d66de_uniq` (`schoolsettings_id`,`schoolinfo_id`),
  KEY `school_schoolsetting_schoolinfo_id_ce703b0e_fk_school_sc` (`schoolinfo_id`),
  CONSTRAINT `school_schoolsetting_schoolsettings_id_f035275f_fk_school_sc` FOREIGN KEY (`schoolsettings_id`) REFERENCES `school_schoolsettings` (`id`),
  CONSTRAINT `school_schoolsetting_schoolinfo_id_ce703b0e_fk_school_sc` FOREIGN KEY (`schoolinfo_id`) REFERENCES `school_schoolinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schoolsettings_school_range`
--

LOCK TABLES `school_schoolsettings_school_range` WRITE;
/*!40000 ALTER TABLE `school_schoolsettings_school_range` DISABLE KEYS */;
INSERT INTO `school_schoolsettings_school_range` VALUES (47,57,3),(48,58,3),(49,59,3),(50,60,1),(51,60,3),(52,61,1),(53,61,3),(54,62,1),(57,63,1),(60,64,1),(63,65,1),(66,66,1),(69,67,1),(72,68,1),(73,68,3),(74,69,3),(75,70,1),(76,71,1),(77,72,3),(78,73,3),(79,74,1),(80,75,1),(87,82,4),(88,82,5),(89,83,4),(90,83,5),(92,84,4),(93,84,9),(91,84,11),(97,85,4),(96,85,5),(94,85,9),(95,85,11),(98,86,4),(99,86,5);
/*!40000 ALTER TABLE `school_schoolsettings_school_range` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schooltitle`
--

DROP TABLE IF EXISTS `school_schooltitle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schooltitle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schooltitle`
--

LOCK TABLES `school_schooltitle` WRITE;
/*!40000 ALTER TABLE `school_schooltitle` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schooltitle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schooltohonor`
--

DROP TABLE IF EXISTS `school_schooltohonor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schooltohonor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` date NOT NULL,
  `honor_id` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_schooltohonor_honor_id_8b55e60f_fk_school_schoolhonor_id` (`honor_id`),
  KEY `school_schooltohonor_school_id_1cb4d598_fk_school_schoolinfo_id` (`school_id`),
  CONSTRAINT `school_schooltohonor_school_id_1cb4d598_fk_school_schoolinfo_id` FOREIGN KEY (`school_id`) REFERENCES `school_schoolinfo` (`id`),
  CONSTRAINT `school_schooltohonor_honor_id_8b55e60f_fk_school_schoolhonor_id` FOREIGN KEY (`honor_id`) REFERENCES `school_schoolhonor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schooltohonor`
--

LOCK TABLES `school_schooltohonor` WRITE;
/*!40000 ALTER TABLE `school_schooltohonor` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schooltohonor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_schooltotitle`
--

DROP TABLE IF EXISTS `school_schooltotitle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_schooltotitle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` date NOT NULL,
  `school_id` int(11) NOT NULL,
  `title_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_schooltotitle_school_id_248c958f_fk_school_schoolinfo_id` (`school_id`),
  KEY `school_schooltotitle_title_id_3d56ab61_fk_school_schooltitle_id` (`title_id`),
  CONSTRAINT `school_schooltotitle_title_id_3d56ab61_fk_school_schooltitle_id` FOREIGN KEY (`title_id`) REFERENCES `school_schooltitle` (`id`),
  CONSTRAINT `school_schooltotitle_school_id_248c958f_fk_school_schoolinfo_id` FOREIGN KEY (`school_id`) REFERENCES `school_schoolinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_schooltotitle`
--

LOCK TABLES `school_schooltotitle` WRITE;
/*!40000 ALTER TABLE `school_schooltotitle` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_schooltotitle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_scopeoffilling`
--

DROP TABLE IF EXISTS `school_scopeoffilling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_scopeoffilling` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_scopeoffilling`
--

LOCK TABLES `school_scopeoffilling` WRITE;
/*!40000 ALTER TABLE `school_scopeoffilling` DISABLE KEYS */;
INSERT INTO `school_scopeoffilling` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `school_scopeoffilling` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_scoreline`
--

DROP TABLE IF EXISTS `school_scoreline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_scoreline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `line` int(11) NOT NULL,
  `Year` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_scoreline_school_id_3d8dc9ff_fk_school_schoolinfo_id` (`school_id`),
  CONSTRAINT `school_scoreline_school_id_3d8dc9ff_fk_school_schoolinfo_id` FOREIGN KEY (`school_id`) REFERENCES `school_schoolinfo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_scoreline`
--

LOCK TABLES `school_scoreline` WRITE;
/*!40000 ALTER TABLE `school_scoreline` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_scoreline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_settingtofield`
--

DROP TABLE IF EXISTS `school_settingtofield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_settingtofield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order` int(11) NOT NULL,
  `fields_id` int(11) NOT NULL,
  `setting_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_settingtofiel_fields_id_5436c2cc_fk_school_ch` (`fields_id`),
  KEY `school_settingtofiel_setting_id_b7dec672_fk_school_sc` (`setting_id`),
  CONSTRAINT `school_settingtofiel_setting_id_b7dec672_fk_school_sc` FOREIGN KEY (`setting_id`) REFERENCES `school_schoolsettings` (`id`),
  CONSTRAINT `school_settingtofiel_fields_id_5436c2cc_fk_school_ch` FOREIGN KEY (`fields_id`) REFERENCES `school_choicefield` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=358 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_settingtofield`
--

LOCK TABLES `school_settingtofield` WRITE;
/*!40000 ALTER TABLE `school_settingtofield` DISABLE KEYS */;
INSERT INTO `school_settingtofield` VALUES (186,1,8,57),(187,2,7,57),(188,3,4,57),(189,4,16,57),(190,5,19,57),(191,6,23,57),(192,7,24,57),(193,8,28,57),(194,9,31,57),(195,1,8,58),(196,2,7,58),(197,3,4,58),(198,4,16,58),(199,5,19,58),(200,6,23,58),(201,7,24,58),(202,8,28,58),(203,9,31,58),(204,1,8,59),(205,2,7,59),(206,3,4,59),(207,4,16,59),(208,5,19,59),(209,6,23,59),(210,7,24,59),(211,8,28,59),(212,9,31,59),(213,1,3,60),(214,2,12,60),(215,3,16,60),(216,4,20,60),(217,5,23,60),(218,6,24,60),(219,7,28,60),(220,8,32,60),(221,1,8,61),(222,2,11,61),(223,3,2,61),(224,4,17,61),(225,5,16,61),(226,6,19,61),(227,7,23,61),(228,8,25,61),(229,9,31,61),(230,10,28,61),(231,1,8,68),(232,2,7,68),(233,3,11,68),(234,4,16,68),(235,5,20,68),(236,6,23,68),(237,7,27,68),(238,8,31,68),(239,1,2,69),(240,2,8,69),(241,3,19,69),(242,4,24,69),(243,5,31,69),(244,1,2,70),(245,2,11,70),(246,3,8,70),(247,4,3,70),(248,5,9,70),(249,6,5,70),(250,7,20,70),(251,8,17,70),(252,9,23,70),(253,10,24,70),(254,11,27,70),(255,12,31,70),(256,1,8,71),(257,2,2,71),(258,3,11,71),(259,4,16,71),(260,5,20,71),(261,6,23,71),(262,7,24,71),(263,8,27,71),(264,9,31,71),(265,1,3,72),(266,2,11,72),(267,3,12,72),(268,4,19,72),(269,5,20,72),(270,6,23,72),(271,7,27,72),(272,8,31,72),(273,1,3,73),(274,2,16,73),(275,3,20,73),(276,4,23,73),(277,5,27,73),(278,6,31,73),(279,1,7,74),(280,2,11,74),(281,3,16,74),(282,4,20,74),(283,5,23,74),(284,6,24,74),(285,7,27,74),(286,8,31,74),(287,1,8,75),(288,2,16,75),(289,3,20,75),(290,4,23,75),(291,5,24,75),(292,6,27,75),(293,1,8,82),(294,2,11,82),(295,3,15,82),(296,4,19,82),(297,5,23,82),(298,6,27,82),(299,7,31,82),(300,1,2,83),(301,2,8,83),(302,3,12,83),(303,4,16,83),(304,5,23,83),(305,6,25,83),(306,7,27,83),(307,8,31,83),(308,1,2,84),(309,2,10,84),(310,3,7,84),(311,4,11,84),(312,5,12,84),(313,6,3,84),(314,7,8,84),(315,8,5,84),(316,9,19,84),(317,10,20,84),(318,11,23,84),(319,12,24,84),(320,13,27,84),(321,14,32,84),(322,1,2,85),(323,2,10,85),(324,3,13,85),(325,4,12,85),(326,5,7,85),(327,6,5,85),(328,7,11,85),(329,8,3,85),(330,9,9,85),(331,10,14,85),(332,11,15,85),(333,12,16,85),(334,13,17,85),(335,14,18,85),(336,15,19,85),(337,16,20,85),(338,17,21,85),(339,18,22,85),(340,19,23,85),(341,20,24,85),(342,21,25,85),(343,22,26,85),(344,23,27,85),(345,24,28,85),(346,25,29,85),(347,26,30,85),(348,27,31,85),(349,28,32,85),(350,1,2,86),(351,2,10,86),(352,3,8,86),(353,4,20,86),(354,5,21,86),(355,6,23,86),(356,7,25,86),(357,8,27,86);
/*!40000 ALTER TABLE `school_settingtofield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school_system`
--

DROP TABLE IF EXISTS `school_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school_system` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school_system`
--

LOCK TABLES `school_system` WRITE;
/*!40000 ALTER TABLE `school_system` DISABLE KEYS */;
/*!40000 ALTER TABLE `school_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_allergy`
--

DROP TABLE IF EXISTS `students_allergy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_allergy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_allergy`
--

LOCK TABLES `students_allergy` WRITE;
/*!40000 ALTER TABLE `students_allergy` DISABLE KEYS */;
INSERT INTO `students_allergy` VALUES (1,'橘子'),(2,'青霉素'),(3,'花粉'),(4,'牛奶'),(5,'海鲜');
/*!40000 ALTER TABLE `students_allergy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_country`
--

DROP TABLE IF EXISTS `students_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_name` varchar(32) NOT NULL,
  `english_name` varchar(32) NOT NULL,
  `img` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_country`
--

LOCK TABLES `students_country` WRITE;
/*!40000 ALTER TABLE `students_country` DISABLE KEYS */;
INSERT INTO `students_country` VALUES (1,'中国','China','country_img/p0_B3WOGAF.png'),(4,'美国','USA','country_img/p0_IXzmbZk.png'),(5,'韩国','Korea','country_img/u1385895653614807634fm58bpow1280bpoh853.jpg');
/*!40000 ALTER TABLE `students_country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_familyinfo`
--

DROP TABLE IF EXISTS `students_familyinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_familyinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `living_type` int(11) DEFAULT NULL,
  `language` int(11) NOT NULL,
  `create_time` date NOT NULL,
  `student_id` int(11) NOT NULL,
  `living_condition` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `students_familyinfo_student_id_4b7a8af6_fk_students_` (`student_id`),
  CONSTRAINT `students_familyinfo_student_id_4b7a8af6_fk_students_` FOREIGN KEY (`student_id`) REFERENCES `students_studentprivacy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_familyinfo`
--

LOCK TABLES `students_familyinfo` WRITE;
/*!40000 ALTER TABLE `students_familyinfo` DISABLE KEYS */;
INSERT INTO `students_familyinfo` VALUES (7,2,2,'2018-09-28',43,2),(8,1,1,'2018-09-28',45,2),(9,1,1,'2018-09-29',46,1);
/*!40000 ALTER TABLE `students_familyinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_familyinfo_family_status`
--

DROP TABLE IF EXISTS `students_familyinfo_family_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_familyinfo_family_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `familyinfo_id` int(11) NOT NULL,
  `familystatus_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `students_familyinfo_fami_familyinfo_id_familystat_818012c0_uniq` (`familyinfo_id`,`familystatus_id`),
  KEY `students_familyinfo__familystatus_id_35453fff_fk_students_` (`familystatus_id`),
  CONSTRAINT `students_familyinfo__familystatus_id_35453fff_fk_students_` FOREIGN KEY (`familystatus_id`) REFERENCES `students_familystatus` (`id`),
  CONSTRAINT `students_familyinfo__familyinfo_id_8a974713_fk_students_` FOREIGN KEY (`familyinfo_id`) REFERENCES `students_familyinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_familyinfo_family_status`
--

LOCK TABLES `students_familyinfo_family_status` WRITE;
/*!40000 ALTER TABLE `students_familyinfo_family_status` DISABLE KEYS */;
INSERT INTO `students_familyinfo_family_status` VALUES (14,7,1),(15,7,2),(16,8,1),(17,8,2),(18,9,1),(19,9,2);
/*!40000 ALTER TABLE `students_familyinfo_family_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_familymember`
--

DROP TABLE IF EXISTS `students_familymember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_familymember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `relations` varchar(16) NOT NULL,
  `Is_living` tinyint(1) NOT NULL,
  `handle_shuttle` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_familymember`
--

LOCK TABLES `students_familymember` WRITE;
/*!40000 ALTER TABLE `students_familymember` DISABLE KEYS */;
/*!40000 ALTER TABLE `students_familymember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_familystatus`
--

DROP TABLE IF EXISTS `students_familystatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_familystatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_familystatus`
--

LOCK TABLES `students_familystatus` WRITE;
/*!40000 ALTER TABLE `students_familystatus` DISABLE KEYS */;
INSERT INTO `students_familystatus` VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6);
/*!40000 ALTER TABLE `students_familystatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_graduateinstitutions`
--

DROP TABLE IF EXISTS `students_graduateinstitutions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_graduateinstitutions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_graduateinstitutions`
--

LOCK TABLES `students_graduateinstitutions` WRITE;
/*!40000 ALTER TABLE `students_graduateinstitutions` DISABLE KEYS */;
INSERT INTO `students_graduateinstitutions` VALUES (1,'三目国际学校'),(2,'三目小学西安校区'),(3,'三目小学北京校区'),(4,'乐城国际学校'),(5,'三目小学');
/*!40000 ALTER TABLE `students_graduateinstitutions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_healthinfo`
--

DROP TABLE IF EXISTS `students_healthinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_healthinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `height` int(11) DEFAULT NULL,
  `weight` decimal(4,2) DEFAULT NULL,
  `vision_left` decimal(3,2) DEFAULT NULL,
  `vision_right` decimal(3,2) DEFAULT NULL,
  `vision_status` int(11) DEFAULT NULL,
  `disability` int(11) NOT NULL,
  `record_date` date NOT NULL,
  `blood_type` int(11) NOT NULL,
  `InheritedDisease_id` int(11) DEFAULT NULL,
  `allergy_id` int(11) DEFAULT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `students_healthinfo_InheritedDisease_id_d35c5af5_fk_students_` (`InheritedDisease_id`),
  KEY `students_healthinfo_allergy_id_cf2d6a8f_fk_students_allergy_id` (`allergy_id`),
  KEY `students_healthinfo_student_id_128ca10e_fk_students_` (`student_id`),
  CONSTRAINT `students_healthinfo_allergy_id_cf2d6a8f_fk_students_allergy_id` FOREIGN KEY (`allergy_id`) REFERENCES `students_allergy` (`id`),
  CONSTRAINT `students_healthinfo_InheritedDisease_id_d35c5af5_fk_students_` FOREIGN KEY (`InheritedDisease_id`) REFERENCES `students_inheriteddisease` (`id`),
  CONSTRAINT `students_healthinfo_student_id_128ca10e_fk_students_` FOREIGN KEY (`student_id`) REFERENCES `students_studentinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_healthinfo`
--

LOCK TABLES `students_healthinfo` WRITE;
/*!40000 ALTER TABLE `students_healthinfo` DISABLE KEYS */;
INSERT INTO `students_healthinfo` VALUES (7,150,34.50,4.50,5.50,2,2,'2018-09-28',1,NULL,NULL,43),(8,174,55.50,2.30,5.30,2,1,'2018-09-28',3,NULL,5,45),(9,180,45.50,5.10,5.10,3,1,'2018-09-29',2,NULL,1,46),(10,180,45.50,5.10,5.10,3,1,'2018-09-29',2,NULL,1,46);
/*!40000 ALTER TABLE `students_healthinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_homeaddress`
--

DROP TABLE IF EXISTS `students_homeaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_homeaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `province` varchar(16) NOT NULL,
  `city` varchar(16) NOT NULL,
  `region` varchar(16) NOT NULL,
  `address` varchar(128) NOT NULL,
  `record_time` date NOT NULL,
  `family_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `students_homeaddress_family_id_3c7179f4_fk_students_` (`family_id`),
  CONSTRAINT `students_homeaddress_family_id_3c7179f4_fk_students_` FOREIGN KEY (`family_id`) REFERENCES `students_familyinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_homeaddress`
--

LOCK TABLES `students_homeaddress` WRITE;
/*!40000 ALTER TABLE `students_homeaddress` DISABLE KEYS */;
INSERT INTO `students_homeaddress` VALUES (7,'天津市','天津市','河西区','S士大夫','2018-09-28',7),(8,'辽宁省','沈阳市','沈河区','对对对','2018-09-28',8),(9,'北京市','北京市','东城区','那你扭扭捏捏','2018-09-29',9);
/*!40000 ALTER TABLE `students_homeaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_inheriteddisease`
--

DROP TABLE IF EXISTS `students_inheriteddisease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_inheriteddisease` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_inheriteddisease`
--

LOCK TABLES `students_inheriteddisease` WRITE;
/*!40000 ALTER TABLE `students_inheriteddisease` DISABLE KEYS */;
INSERT INTO `students_inheriteddisease` VALUES (1,'高血压'),(2,'心脏病');
/*!40000 ALTER TABLE `students_inheriteddisease` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_stuclass`
--

DROP TABLE IF EXISTS `students_stuclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_stuclass` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_stuclass`
--

LOCK TABLES `students_stuclass` WRITE;
/*!40000 ALTER TABLE `students_stuclass` DISABLE KEYS */;
/*!40000 ALTER TABLE `students_stuclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_studentinfo`
--

DROP TABLE IF EXISTS `students_studentinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_studentinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` int(11) NOT NULL,
  `nation` varchar(32) DEFAULT NULL,
  `residence_province` varchar(16) DEFAULT NULL,
  `residence_city` varchar(16) DEFAULT NULL,
  `residence_region` varchar(16) DEFAULT NULL,
  `birthday` date NOT NULL,
  `age` int(11) NOT NULL,
  `day_age` int(11) NOT NULL,
  `constellation` int(11) NOT NULL,
  `chinese_zodiac` int(11) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `QQ` int(11) DEFAULT NULL,
  `wechat` varchar(32) DEFAULT NULL,
  `create_time` date NOT NULL,
  `country_id` int(11) NOT NULL,
  `graduate_institutions_id` int(11) DEFAULT NULL,
  `period` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  `stu_class_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `QQ` (`QQ`),
  KEY `students_studentinfo_country_id_e49c1ab8_fk_students_country_id` (`country_id`),
  KEY `students_studentinfo_graduate_institution_24309002_fk_students_` (`graduate_institutions_id`),
  KEY `students_studentinfo_school_id_bf7f0e8b_fk_school_schoolinfo_id` (`school_id`),
  CONSTRAINT `students_studentinfo_school_id_bf7f0e8b_fk_school_schoolinfo_id` FOREIGN KEY (`school_id`) REFERENCES `school_schoolinfo` (`id`),
  CONSTRAINT `students_studentinfo_country_id_e49c1ab8_fk_students_country_id` FOREIGN KEY (`country_id`) REFERENCES `students_country` (`id`),
  CONSTRAINT `students_studentinfo_graduate_institution_24309002_fk_students_` FOREIGN KEY (`graduate_institutions_id`) REFERENCES `students_graduateinstitutions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_studentinfo`
--

LOCK TABLES `students_studentinfo` WRITE;
/*!40000 ALTER TABLE `students_studentinfo` DISABLE KEYS */;
INSERT INTO `students_studentinfo` VALUES (41,'子','王',1,'维吾尔族','北京市','北京市','东城区','2005-09-28',13,4748,10,2,'student/photo/img-1a7c655ec00643fe1d1bfb1772ff61f2.jpg',NULL,NULL,NULL,'2018-09-28',1,1,1,1,1),(42,'宋','小',2,'汉族','天津市','天津市','河西区','2018-09-28',0,0,10,3,'student/photo/u1385895653614807634fm58bpow1280bpoh853_CysNp3r.jpg',NULL,NULL,NULL,'2018-09-28',1,2,1,1,1),(43,'一','宋',2,'汉族','天津市','天津市','南开区','2003-09-28',15,5479,10,12,'student/photo/TIM图片20180913160950_CevcXFQ.jpg',NULL,NULL,NULL,'2018-09-28',1,5,1,1,1),(45,'一','吕',1,'汉族','河北省','邢台市','长安区','1994-09-28',24,8766,10,3,'student/photo/wx_camera_1538108988871.jpg',NULL,NULL,NULL,'2018-09-28',1,2,1,1,1),(46,'爽','蔡',1,'汉族','河北省','石家庄市','长安区','2001-05-29',17,6332,6,10,'student/photo/img-b53e7e554d5cd2221ae5f0d91fb726d5.jpg',NULL,NULL,NULL,'2018-09-29',1,1,1,1,1);
/*!40000 ALTER TABLE `students_studentinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_studentinnerinfo`
--

DROP TABLE IF EXISTS `students_studentinnerinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_studentinnerinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interior_student_id` varchar(255) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `interior_student_id` (`interior_student_id`),
  UNIQUE KEY `student_id` (`student_id`),
  CONSTRAINT `students_studentinne_student_id_54320d17_fk_students_` FOREIGN KEY (`student_id`) REFERENCES `students_studentinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_studentinnerinfo`
--

LOCK TABLES `students_studentinnerinfo` WRITE;
/*!40000 ALTER TABLE `students_studentinnerinfo` DISABLE KEYS */;
INSERT INTO `students_studentinnerinfo` VALUES (41,'sid:906a69b7-6465-42a4-a86e-1f42c858f984',41),(42,'sid:af50ad18-ccbf-40b3-a70a-e109103e09f0',42),(43,'sid:108361fc-3085-444b-8bd9-023cb22ec424',43),(45,'sid:cb19b0df-65fa-48fe-a5da-b49943b9f74e',45),(46,'sid:15a0fd35-a19a-4d54-97fd-5c3ad302991a',46);
/*!40000 ALTER TABLE `students_studentinnerinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_studentparents`
--

DROP TABLE IF EXISTS `students_studentparents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_studentparents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `birthday` date NOT NULL,
  `telephone` varchar(32) NOT NULL,
  `education` int(11) NOT NULL,
  `company` varchar(64) NOT NULL,
  `job` varchar(32) NOT NULL,
  `wechat` varchar(32) DEFAULT NULL,
  `wechat_open_id_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `students_studentpare_wechat_open_id_id_7b7bbcdb_fk_students_` (`wechat_open_id_id`),
  CONSTRAINT `students_studentpare_wechat_open_id_id_7b7bbcdb_fk_students_` FOREIGN KEY (`wechat_open_id_id`) REFERENCES `students_wechatopenid` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_studentparents`
--

LOCK TABLES `students_studentparents` WRITE;
/*!40000 ALTER TABLE `students_studentparents` DISABLE KEYS */;
INSERT INTO `students_studentparents` VALUES (3,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(4,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(5,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(6,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(7,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(8,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(9,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(10,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(11,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(12,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(13,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(14,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(15,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(16,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(17,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(18,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(19,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(20,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(21,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(22,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(23,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL),(24,'1','f','2018-09-28','135456151',4,'1','1','1',NULL),(25,'2','拂去','2018-09-28','156781',1,'3213214','34235','4',NULL),(26,'高','杨','2018-09-28','17629202424',2,'西安市','市场','602098657',NULL),(27,'1王','二','1964-10-30','1232232323',3,'XXX有限公司','IT','1',NULL);
/*!40000 ALTER TABLE `students_studentparents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_studentprivacy`
--

DROP TABLE IF EXISTS `students_studentprivacy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_studentprivacy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(256) NOT NULL,
  `id_card` varchar(32) DEFAULT NULL,
  `student_code` int(11) DEFAULT NULL,
  `telephone` varchar(32) DEFAULT NULL,
  `student_detail_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_detail_id` (`student_detail_id`),
  UNIQUE KEY `id_card` (`id_card`),
  KEY `students_studentprivacy_full_name_b0af98c4` (`full_name`(255)),
  CONSTRAINT `students_studentpriv_student_detail_id_0636dcea_fk_students_` FOREIGN KEY (`student_detail_id`) REFERENCES `students_studentinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_studentprivacy`
--

LOCK TABLES `students_studentprivacy` WRITE;
/*!40000 ALTER TABLE `students_studentprivacy` DISABLE KEYS */;
INSERT INTO `students_studentprivacy` VALUES (41,'王子','142602199604131511',NULL,NULL,41),(42,'小宋','142602199304131528',NULL,NULL,42),(43,'宋一','350301198906180060',NULL,NULL,43),(45,'吕一','360102199510210720',NULL,NULL,45),(46,'蔡爽','14260219930413151X',NULL,NULL,46);
/*!40000 ALTER TABLE `students_studentprivacy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_studenttoparents`
--

DROP TABLE IF EXISTS `students_studenttoparents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_studenttoparents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `relation` int(11) NOT NULL,
  `is_main_contact` tinyint(1) NOT NULL,
  `parents_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `students_studenttopa_parents_id_c4bad7ab_fk_students_` (`parents_id`),
  KEY `students_studenttopa_student_id_a4c29d42_fk_students_` (`student_id`),
  CONSTRAINT `students_studenttopa_student_id_a4c29d42_fk_students_` FOREIGN KEY (`student_id`) REFERENCES `students_studentprivacy` (`id`),
  CONSTRAINT `students_studenttopa_parents_id_c4bad7ab_fk_students_` FOREIGN KEY (`parents_id`) REFERENCES `students_studentparents` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_studenttoparents`
--

LOCK TABLES `students_studenttoparents` WRITE;
/*!40000 ALTER TABLE `students_studenttoparents` DISABLE KEYS */;
/*!40000 ALTER TABLE `students_studenttoparents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_wechatopenid`
--

DROP TABLE IF EXISTS `students_wechatopenid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students_wechatopenid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_wechatopenid`
--

LOCK TABLES `students_wechatopenid` WRITE;
/*!40000 ALTER TABLE `students_wechatopenid` DISABLE KEYS */;
/*!40000 ALTER TABLE `students_wechatopenid` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-11 13:55:57
