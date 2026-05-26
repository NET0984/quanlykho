-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: quanlykhovatlieu
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add category',6,'add_category'),(22,'Can change category',6,'change_category'),(23,'Can delete category',6,'delete_category'),(24,'Can view category',6,'view_category'),(25,'Can add product',7,'add_product'),(26,'Can change product',7,'change_product'),(27,'Can delete product',7,'delete_product'),(28,'Can view product',7,'view_product'),(29,'Can add product unit',8,'add_productunit'),(30,'Can change product unit',8,'change_productunit'),(31,'Can delete product unit',8,'delete_productunit'),(32,'Can view product unit',8,'view_productunit'),(33,'Can add user',9,'add_user'),(34,'Can change user',9,'change_user'),(35,'Can delete user',9,'delete_user'),(36,'Can view user',9,'view_user'),(37,'Can add warehouse transaction',16,'add_warehousetransaction'),(38,'Can change warehouse transaction',16,'change_warehousetransaction'),(39,'Can delete warehouse transaction',16,'delete_warehousetransaction'),(40,'Can view warehouse transaction',16,'view_warehousetransaction'),(41,'Can add inventory',12,'add_inventory'),(42,'Can change inventory',12,'change_inventory'),(43,'Can delete inventory',12,'delete_inventory'),(44,'Can view inventory',12,'view_inventory'),(45,'Can add sales order',13,'add_salesorder'),(46,'Can change sales order',13,'change_salesorder'),(47,'Can delete sales order',13,'delete_salesorder'),(48,'Can view sales order',13,'view_salesorder'),(49,'Can add warehouse',15,'add_warehouse'),(50,'Can change warehouse',15,'change_warehouse'),(51,'Can delete warehouse',15,'delete_warehouse'),(52,'Can view warehouse',15,'view_warehouse'),(53,'Can add system log',14,'add_systemlog'),(54,'Can change system log',14,'change_systemlog'),(55,'Can delete system log',14,'delete_systemlog'),(56,'Can view system log',14,'view_systemlog'),(57,'Can add export log',11,'add_exportlog'),(58,'Can change export log',11,'change_exportlog'),(59,'Can delete export log',11,'delete_exportlog'),(60,'Can view export log',11,'view_exportlog'),(61,'Can add customer debt',10,'add_customerdebt'),(62,'Can change customer debt',10,'change_customerdebt'),(63,'Can delete customer debt',10,'delete_customerdebt'),(64,'Can view customer debt',10,'view_customerdebt'),(65,'Can add Blacklisted Token',17,'add_blacklistedtoken'),(66,'Can change Blacklisted Token',17,'change_blacklistedtoken'),(67,'Can delete Blacklisted Token',17,'delete_blacklistedtoken'),(68,'Can view Blacklisted Token',17,'view_blacklistedtoken'),(69,'Can add Outstanding Token',18,'add_outstandingtoken'),(70,'Can change Outstanding Token',18,'change_outstandingtoken'),(71,'Can delete Outstanding Token',18,'delete_outstandingtoken'),(72,'Can view Outstanding Token',18,'view_outstandingtoken'),(73,'Can add sales order',20,'add_salesorder'),(74,'Can change sales order',20,'change_salesorder'),(75,'Can delete sales order',20,'delete_salesorder'),(76,'Can view sales order',20,'view_salesorder'),(77,'Can add customer debt',19,'add_customerdebt'),(78,'Can change customer debt',19,'change_customerdebt'),(79,'Can delete customer debt',19,'delete_customerdebt'),(80,'Can view customer debt',19,'view_customerdebt'),(81,'Can add sales order item',21,'add_salesorderitem'),(82,'Can change sales order item',21,'change_salesorderitem'),(83,'Can delete sales order item',21,'delete_salesorderitem'),(84,'Can view sales order item',21,'view_salesorderitem'),(85,'Can add import receipt',24,'add_importreceipt'),(86,'Can change import receipt',24,'change_importreceipt'),(87,'Can delete import receipt',24,'delete_importreceipt'),(88,'Can view import receipt',24,'view_importreceipt'),(89,'Can add import receipt item',25,'add_importreceiptitem'),(90,'Can change import receipt item',25,'change_importreceiptitem'),(91,'Can delete import receipt item',25,'delete_importreceiptitem'),(92,'Can view import receipt item',25,'view_importreceiptitem'),(93,'Can add product stock',26,'add_productstock'),(94,'Can change product stock',26,'change_productstock'),(95,'Can delete product stock',26,'delete_productstock'),(96,'Can view product stock',26,'view_productstock'),(97,'Can add export receipt',22,'add_exportreceipt'),(98,'Can change export receipt',22,'change_exportreceipt'),(99,'Can delete export receipt',22,'delete_exportreceipt'),(100,'Can view export receipt',22,'view_exportreceipt'),(101,'Can add export receipt item',23,'add_exportreceiptitem'),(102,'Can change export receipt item',23,'change_exportreceiptitem'),(103,'Can delete export receipt item',23,'delete_exportreceiptitem'),(104,'Can view export receipt item',23,'view_exportreceiptitem'),(105,'Can add Phiên kiểm kê',27,'add_inventoryaudit'),(106,'Can change Phiên kiểm kê',27,'change_inventoryaudit'),(107,'Can delete Phiên kiểm kê',27,'delete_inventoryaudit'),(108,'Can view Phiên kiểm kê',27,'view_inventoryaudit'),(109,'Can add Dòng kiểm kê',28,'add_inventoryaudititem'),(110,'Can change Dòng kiểm kê',28,'change_inventoryaudititem'),(111,'Can delete Dòng kiểm kê',28,'delete_inventoryaudititem'),(112,'Can view Dòng kiểm kê',28,'view_inventoryaudititem'),(113,'Can add Phiếu hao hụt',29,'add_inventoryloss'),(114,'Can change Phiếu hao hụt',29,'change_inventoryloss'),(115,'Can delete Phiếu hao hụt',29,'delete_inventoryloss'),(116,'Can view Phiếu hao hụt',29,'view_inventoryloss'),(117,'Can add Nhật ký xuất báo cáo',30,'add_reportexportlog'),(118,'Can change Nhật ký xuất báo cáo',30,'change_reportexportlog'),(119,'Can delete Nhật ký xuất báo cáo',30,'delete_reportexportlog'),(120,'Can view Nhật ký xuất báo cáo',30,'view_reportexportlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` char(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES ('02000000000000000000000000000003','Cát & Sỏi'),('02000000000000000000000000000010','Đinh vít & Bu lông'),('02000000000000000000000000000002','Gạch & Đá'),('02000000000000000000000000000008','Gỗ & Ván ép'),('02000000000000000000000000000005','Ống nhựa & Phụ kiện'),('02000000000000000000000000000004','Sắt thép xây dựng'),('02000000000000000000000000000006','Sơn & Chống thấm'),('02000000000000000000000000000007','Tấm lợp & Mái'),('02000000000000000000000000000009','Vật liệu cách nhiệt'),('02000000000000000000000000000001','Xi măng & Vữa');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-04-08 08:15:54.243409','01000000-0000-0000-0000-000000000009','ketoan01',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',9,'01000000000000000000000000000002'),(2,'2026-04-08 08:22:59.487135','01000000-0000-0000-0000-000000000009','ketoan01',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',9,'01000000000000000000000000000002');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(9,'authentication','user'),(4,'contenttypes','contenttype'),(27,'inventory','inventoryaudit'),(28,'inventory','inventoryaudititem'),(29,'inventory','inventoryloss'),(19,'order','customerdebt'),(20,'order','salesorder'),(21,'order','salesorderitem'),(6,'product','category'),(10,'product','customerdebt'),(11,'product','exportlog'),(12,'product','inventory'),(7,'product','product'),(8,'product','productunit'),(13,'product','salesorder'),(14,'product','systemlog'),(15,'product','warehouse'),(16,'product','warehousetransaction'),(30,'reports','reportexportlog'),(5,'sessions','session'),(17,'token_blacklist','blacklistedtoken'),(18,'token_blacklist','outstandingtoken'),(22,'warehouse','exportreceipt'),(23,'warehouse','exportreceiptitem'),(24,'warehouse','importreceipt'),(25,'warehouse','importreceiptitem'),(26,'warehouse','productstock');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-23 07:39:45.101094'),(2,'contenttypes','0002_remove_content_type_name','2026-03-23 07:39:45.246313'),(3,'auth','0001_initial','2026-03-23 07:39:45.866918'),(4,'auth','0002_alter_permission_name_max_length','2026-03-23 07:39:45.965114'),(5,'auth','0003_alter_user_email_max_length','2026-03-23 07:39:45.974471'),(6,'auth','0004_alter_user_username_opts','2026-03-23 07:39:45.981492'),(7,'auth','0005_alter_user_last_login_null','2026-03-23 07:39:45.988828'),(8,'auth','0006_require_contenttypes_0002','2026-03-23 07:39:45.993822'),(9,'auth','0007_alter_validators_add_error_messages','2026-03-23 07:39:46.000798'),(10,'auth','0008_alter_user_username_max_length','2026-03-23 07:39:46.007906'),(11,'auth','0009_alter_user_last_name_max_length','2026-03-23 07:39:46.015109'),(12,'auth','0010_alter_group_name_max_length','2026-03-23 07:39:46.030855'),(13,'auth','0011_update_proxy_permissions','2026-03-23 07:39:46.037147'),(14,'auth','0012_alter_user_first_name_max_length','2026-03-23 07:39:46.044047'),(15,'authentication','0001_initial','2026-03-23 07:39:46.637343'),(16,'admin','0001_initial','2026-03-23 07:39:46.884249'),(17,'admin','0002_logentry_remove_auto_add','2026-03-23 07:39:46.901772'),(18,'admin','0003_logentry_add_action_flag_choices','2026-03-23 07:39:46.910695'),(19,'product','0001_initial','2026-03-23 07:39:47.237996'),(20,'sessions','0001_initial','2026-03-23 07:39:47.296813'),(21,'product','0002_warehouse_exportlog_salesorder_customerdebt_and_more','2026-03-23 07:51:14.177832'),(22,'product','0002_remove_exportlog_user_and_more','2026-04-06 03:01:33.618459'),(23,'token_blacklist','0001_initial','2026-04-06 03:01:33.923635'),(24,'token_blacklist','0002_outstandingtoken_jti_hex','2026-04-06 03:01:34.012718'),(25,'token_blacklist','0003_auto_20171017_2007','2026-04-06 03:01:34.029049'),(26,'token_blacklist','0004_auto_20171017_2013','2026-04-06 03:01:34.149225'),(27,'token_blacklist','0005_remove_outstandingtoken_jti','2026-04-06 03:01:34.234609'),(28,'token_blacklist','0006_auto_20171017_2113','2026-04-06 03:01:34.269839'),(29,'token_blacklist','0007_auto_20171017_2214','2026-04-06 03:01:34.574716'),(30,'token_blacklist','0008_migrate_to_bigautofield','2026-04-06 03:01:35.006040'),(31,'token_blacklist','0010_fix_migrate_to_bigautofield','2026-04-06 03:01:35.018538'),(32,'token_blacklist','0011_linearizes_history','2026-04-06 03:01:35.024010'),(33,'token_blacklist','0012_alter_outstandingtoken_user','2026-04-06 03:01:35.034786'),(34,'token_blacklist','0013_alter_blacklistedtoken_options_and_more','2026-04-06 03:01:35.047618'),(35,'order','0001_initial','2026-04-14 10:34:45.813381'),(36,'order','0002_remove_warehousetransaction_warehouse_and_more','2026-04-14 10:34:48.266070'),(37,'warehouse','0001_initial','2026-04-14 10:34:49.154576'),(38,'warehouse','0002_exportreceipt_exportreceiptitem','2026-04-14 10:34:49.797587'),(39,'warehouse','0003_add_sales_order_to_export_receipt','2026-04-14 10:34:49.945301'),(40,'warehouse','0004_remove_exportreceipt_sales_order','2026-04-14 10:34:50.095440'),(41,'warehouse','0005_exportreceipt_sales_order_and_more','2026-04-14 10:34:50.258244'),(42,'order','0003_remove_customerdebt','2026-04-19 09:45:41.827302'),(43,'order','0004_salesorder_picked_status','2026-04-20 04:09:24.663797'),(44,'warehouse','0006_exportreceipt_pickup_flow','2026-04-20 04:09:25.001314'),(45,'authentication','0002_alter_user_full_name_alter_user_phone_number','2026-04-29 05:52:25.603498'),(46,'product','0003_alter_category_name_alter_product_base_price_and_more','2026-04-29 05:52:25.630428'),(47,'inventory','0001_initial','2026-04-29 05:52:27.914755'),(48,'inventory','0002_remove_reportexportlog_idx_exportlog_type_date_and_more','2026-04-29 05:52:27.956791'),(49,'reports','0001_initial','2026-04-29 05:52:27.972448'),(50,'order','0005_alter_salesorder_status','2026-05-07 05:59:49.210442'),(51,'warehouse','0007_alter_exportreceipt_status_and_more','2026-05-07 05:59:49.290360');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('apqfxjr8z9xrjdizft12kycli1sl0f2v','.eJxVjjsOwjAQBe_iGlte2xtjSnrOEK29axJAiZRPhbg7iZQC6jczem_V0rp07TrL1PasLipZayk51BE56UBN0lRYNKSKOeIZQgF1-tUylacMu8sPGu6jKeOwTH02O2KOdTa3keV1Pdi_QEdzt9leoAJECWQlbCcKBG6qiwlrDhXRlmgJ2KGvGF0qxAExOy8ZofHeq88Xqo1APw:1w6Rcj:T98F0yC38yKBhdho_cGRyvK0emNbLezPmc__-E7r2bw','2026-04-11 11:14:37.388088'),('dt6h4kqu99q4zdxxo118c574k38hgx9d','.eJxtjMEOwiAQRP-FsxJaQLoevfsNZGG3UjWQlPZk_Hdb7UET5zCXeW8ewuM8JT9XHv1A4ihUo97Z_6lPGiV231rAeOO8unTFfCkyljyNQ5ArIre1ynMhvp829ucgYU2Lba0NEAAcA_bYojIHIjAIELWxjh0pJmRSgNgZbHVk0xGHnskspcXzBTwQP-o:1wAOFH:5OMoyNeAmuYjK8Io-uemWDS2bq4BMup7mQuJhLJnEok','2026-04-22 08:26:43.874791'),('ht6eszx7zi81nff5bordrp5u3arry95o','.eJxVzrkOwjAQBNB_cY0t3wclPd8QrXe9hEOJlKNC_DuJlALqmTeat-hgXfpundvU3UmcRdFaQ7FBpkBFeohFAlKTpnCoKWTj0YjTL6uAzzbslh4w3EaF47BM96r2ijrSWV1Haq_L0f0b6GHuN92qjVEzUs7aViJ00Rl2lRmLzzpp7zVvF0xsprhUEawPBXljhMRNfL7DRkF7:1wHxem:2pqiPq42WU8ts7aq5sGtQpW0xc5DwlGNfTiHtQ_eMb4','2026-05-13 05:40:20.436710'),('lolgodfhx9csz9fjhbu9rxijpwq4z0e3','.eJxtjDsOwjAQRO_iGqz1J3ZCSc8ZIu-uFwdQIuVTIe5OglKAxBTTzHvzVG1a5tIuUx7bjtVJgYFPjn9qj1WHbw0T3XO_uXxL_XXQNPTz2KHeEL2vk74MnB_nnf05KGkqq53RhgBCXNdgkZlccEYcilDja4jgPQjGyoRsGheRkvVVQ7JqTCxZvd4v2D8W:1wKs8z:HLOJHkNQD0HVOGpm4ee1WPtSBTAv1V6xIgWys4ptT1Y','2026-05-21 06:23:33.428203'),('rgi1dl7tnii30eg9t28itmytw1iwtm02','.eJxtjDsOwjAQRO_iGqz1J3ZCSc8ZIu-uFwdQIuVTIe5OglKAxBTTzHvzVG1a5tIuUx7bjtVJgYFPjn9qj1WHbw0T3XO_uXxL_XXQNPTz2KHeEL2vk74MnB_nnf05KGkqq53RhgBCXNdgkZlccEYcilDja4jgPQjGyoRsGheRkvVVQ7JqTCxZvd4v2D8W:1wKroo:8yBXqEyxA_pb1cmk_78ytQHPJPL4VkamH2qsYEIZFNY','2026-05-21 06:02:42.006636');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `export_receipt_items`
--

DROP TABLE IF EXISTS `export_receipt_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `export_receipt_items` (
  `id` char(32) NOT NULL,
  `quantity` decimal(15,2) NOT NULL,
  `unit_price` decimal(19,4) NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `product_id` char(32) NOT NULL,
  `receipt_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `export_receipt_items_product_id_07b55fac_fk_products_id` (`product_id`),
  KEY `export_receipt_items_receipt_id_da1a4967_fk_export_receipts_id` (`receipt_id`),
  CONSTRAINT `export_receipt_items_product_id_07b55fac_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `export_receipt_items_receipt_id_da1a4967_fk_export_receipts_id` FOREIGN KEY (`receipt_id`) REFERENCES `export_receipts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `export_receipt_items`
--

LOCK TABLES `export_receipt_items` WRITE;
/*!40000 ALTER TABLE `export_receipt_items` DISABLE KEYS */;
INSERT INTO `export_receipt_items` VALUES ('18c3d55f7dd4460ebd4c81bfa0fa7c8f',2.00,195000.0000,'Don DH-DEMO-001','03000000000000000000000000000008','f6c03c44865646e8bb3ac72f69434d60'),('1cb5fd84ec4f4c428058351158784fcb',2.00,120000.0000,'Đơn hàng DH-20260420-003','03000000000000000000000000000018','425f5840408f44638c46dbd0b76021c2'),('266c2ab9dfd04ad6bc73a3d3d6825587',3.00,320000.0000,'Don DH-DEMO-017','03000000000000000000000000000019','8b2d09267a9e4515b69d030cadcacf5a'),('2b43e297da08418295ea5659a7867089',1.00,850000.0000,'Don DH-DEMO-012','03000000000000000000000000000015','016738018254438e8b0feecf0b7e4163'),('31210adc3e534771bed6b440e584f65d',2.00,95000.0000,'Don DH-DEMO-010','03000000000000000000000000000014','5d9a520049dc41d4a6982421e1dd0a7f'),('31dedd3c614343c5b6bb389ebfeef54f',2.00,95000.0000,'Don hang DH-20260420-001','03000000000000000000000000000014','1b6b553ab2124448af52f40e565bed06'),('41bcfa9837e042b1ad9c190fc24f18ff',2.00,195000.0000,'Don hang DH-20260420-002','03000000000000000000000000000008','d673fa1d3da441e38f55f54c72b1c2d4'),('4dd45efe58da40a5a840bee7d45a2088',2.00,320000.0000,'','03000000000000000000000000000019','8e61158cc00d4e72b095d5fd16b7d8e3'),('5323d70fd33a41fe811408b9e95070f6',3.00,220000.0000,'Don DH-DEMO-002','03000000000000000000000000000007','4807190bbd334eb0b4c65fb77d16fb83'),('579f948ba1614a58b9aa38c7e291dc60',3.00,185000.0000,'Don DH-DEMO-014','03000000000000000000000000000010','f65cf24707a94224b25b834a3a382323'),('628b7f830b3848e58d145924c15990f8',2.00,120000.0000,'Don DH-DEMO-013','03000000000000000000000000000018','282be10207a14c588dc4158a656d3c56'),('74cecb0cb31f49468eaf15c6d251499c',1.00,185000.0000,'Don DH-DEMO-009','03000000000000000000000000000013','5637231245be4b7d8f7b8aa75aea670b'),('78b4bb13bb5a40b4853b8146a915fe87',10.00,265000.0000,'Don hang DH-20260419-001','03000000000000000000000000000011','71aec8d676f94496861a741a4bbc3374'),('79b797f539e740c797425b0e59ad1eb6',1.00,185000.0000,'Đơn hàng DH-20260429-001','03000000000000000000000000000017','b6560c31037a472d80d069e07377cd6c'),('79ea59273f7f4648983c726db0154807',1.00,265000.0000,'Don DH-DEMO-015','03000000000000000000000000000011','f3d4e3aeacd44087a41785e9f5c86f9f'),('84eeff8900cb4651afefd944ec8a86c2',1.00,55000.0000,'Don DH-DEMO-018','03000000000000000000000000000003','6c4d1bbc6d1b4befb9c615c13dfecf75'),('8b4938332cfc40d093d9a07d198fbc04',2.00,55000.0000,'','03000000000000000000000000000003','b05948242cf54be693f0672b3e355be2'),('937d1731517843a9bf5807b54eeec740',2.00,900.0000,'Don DH-DEMO-007','03000000000000000000000000000005','56b3d8576da04ddda90046a84018299c'),('b3e2bfe68f534672ac97e06c6037ac3c',1.00,1200.0000,'Don DH-DEMO-006','03000000000000000000000000000004','5f83031d4d1c4c41a5b0346b6b6a6600'),('b63ac7f0e7b94713b79d3f9e321eedb3',2.00,185000.0000,'Don DH-DEMO-016','03000000000000000000000000000017','08a6baf8705844aeaec69266f60ef96b'),('c55dd18927ee47178d2b1a137bc4c7ec',20.00,320000.0000,'','03000000000000000000000000000019','0b96ac468f0847ce9a2bf637bb10443e'),('ca8cc10d0a6d412e913d427d556059bd',1.00,120000.0000,'','03000000000000000000000000000018','6ed4580737cc456f835d7f773f62d385'),('d9b0eafdbed146f6b4439a1f2a1bc914',3.00,320000.0000,'Don DH-DEMO-008','03000000000000000000000000000012','95aa8439a04140e5b6cbe95cf487ec98'),('ebe76bd5eda749589673ac2ffd846832',3.00,260000.0000,'Don DH-DEMO-011','03000000000000000000000000000009','9e2c1664cf2f439f8b624eed2dbc4f9b'),('efc6e4d2d1cb4c8b845f05d53854a8ee',1.00,92000.0000,'','03000000000000000000000000000002','9b3f8dae8b4047b7a70e24252711ae07');
/*!40000 ALTER TABLE `export_receipt_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `export_receipts`
--

DROP TABLE IF EXISTS `export_receipts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `export_receipts` (
  `id` char(32) NOT NULL,
  `receipt_code` varchar(30) NOT NULL,
  `status` varchar(10) NOT NULL,
  `note` longtext,
  `rejection_note` longtext,
  `created_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `created_by_id` char(32) NOT NULL,
  `reviewed_by_id` char(32) DEFAULT NULL,
  `sales_order_id` char(32) DEFAULT NULL,
  `picked_at` datetime(6) DEFAULT NULL,
  `pickup_photo` varchar(100) DEFAULT NULL,
  `picked_by_id` char(32) DEFAULT NULL,
  `stock_deducted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `receipt_code` (`receipt_code`),
  KEY `export_receipts_created_by_id_12bba5bb_fk_users_id` (`created_by_id`),
  KEY `export_receipts_reviewed_by_id_0ef33c0d_fk_users_id` (`reviewed_by_id`),
  KEY `export_receipts_sales_order_id_dfad21cd_fk_sales_orders_id` (`sales_order_id`),
  KEY `export_receipts_picked_by_id_d0b830d5_fk_users_id` (`picked_by_id`),
  CONSTRAINT `export_receipts_created_by_id_12bba5bb_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `export_receipts_picked_by_id_d0b830d5_fk_users_id` FOREIGN KEY (`picked_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `export_receipts_reviewed_by_id_0ef33c0d_fk_users_id` FOREIGN KEY (`reviewed_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `export_receipts_sales_order_id_dfad21cd_fk_sales_orders_id` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `export_receipts`
--

LOCK TABLES `export_receipts` WRITE;
/*!40000 ALTER TABLE `export_receipts` DISABLE KEYS */;
INSERT INTO `export_receipts` VALUES ('016738018254438e8b0feecf0b7e4163','EX-20260416-007','APPROVED','Xuat hang cho don DH-DEMO-012','','2026-04-16 07:51:20.436049','2026-04-16 07:53:47.673822','b3e155ca4a5543408138c00727e48ab5','9000a92575d94a69acde19f5b75814c1','44349456382f40578cbf36e6b00b838f',NULL,NULL,NULL,0),('08a6baf8705844aeaec69266f60ef96b','EX-20260416-011','APPROVED','Xuat hang cho don DH-DEMO-016','','2026-04-16 07:51:20.485524','2026-04-16 07:51:20.490715','a9a24097b5e04dbe8b2f6b2d5728691a','7dd717a8e78447c8b9c2bf1a812267ae','6e0b5a6f4f7a4f5cbc8af9a20fb14e7f',NULL,NULL,NULL,0),('0b96ac468f0847ce9a2bf637bb10443e','EX-20260420-001','APPROVED','','','2026-04-20 04:37:28.834184','2026-04-20 04:37:54.915968','01000000000000000000000000000006','9000a92575d94a69acde19f5b75814c1',NULL,NULL,'',NULL,0),('1b6b553ab2124448af52f40e565bed06','EX-20260420-004','APPROVED','Xuat hang cho don DH-20260420-001 - KH: Nguyen Quang Sang','','2026-04-20 04:50:20.331361','2026-04-29 05:36:25.196901','9000a92575d94a69acde19f5b75814c1','9000a92575d94a69acde19f5b75814c1','8ec1a9446480476c80fc66b849b042c3','2026-04-20 04:50:36.884128','','9000a92575d94a69acde19f5b75814c1',1),('282be10207a14c588dc4158a656d3c56','EX-20260416-008','APPROVED','Xuat hang cho don DH-DEMO-013','','2026-04-16 07:51:20.441511','2026-04-16 07:51:20.446723','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae','69c790f1e5234a9cafe64bad22626cf5',NULL,NULL,NULL,0),('425f5840408f44638c46dbd0b76021c2','EX-20260420-006','APPROVED','Xuất hàng cho đơn DH-20260420-003 - KH: Nguyen Quang Sang','','2026-04-20 05:18:52.416465','2026-04-20 05:19:48.766535','9000a92575d94a69acde19f5b75814c1','9000a92575d94a69acde19f5b75814c1','31fcf04570d942c88de03f014a259c1f','2026-04-20 05:19:25.350305','','9000a92575d94a69acde19f5b75814c1',1),('4807190bbd334eb0b4c65fb77d16fb83','EX-20260416-015','REJECTED','Xuat hang cho don DH-DEMO-002','Tu choi demo','2026-04-16 07:51:20.566132','2026-04-16 07:51:20.568982','a9a24097b5e04dbe8b2f6b2d5728691a','a9a24097b5e04dbe8b2f6b2d5728691a','14438ca3b91944cca9c6a4405df67246',NULL,NULL,NULL,0),('5637231245be4b7d8f7b8aa75aea670b','EX-20260416-004','PREPARING','Xuat hang cho don DH-DEMO-009',NULL,'2026-04-16 07:51:20.411130',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL,'f53eabc726f7416a8577d369d517704a',NULL,NULL,NULL,0),('56b3d8576da04ddda90046a84018299c','EX-20260416-002','PREPARING','Xuat hang cho don DH-DEMO-007',NULL,'2026-04-16 07:51:20.396963',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL,'0ae089a0a0174abb966322eaec4ac8e4',NULL,NULL,NULL,0),('5d9a520049dc41d4a6982421e1dd0a7f','EX-20260416-005','PREPARING','Xuat hang cho don DH-DEMO-010',NULL,'2026-04-16 07:51:20.418073',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL,'4dd5d4ec13cd40b9a5aaede345e3ed0b',NULL,NULL,NULL,0),('5f83031d4d1c4c41a5b0346b6b6a6600','EX-20260416-001','PREPARING','Xuat hang cho don DH-DEMO-006',NULL,'2026-04-16 07:51:20.391151',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL,'3331ca55e4544eb080578342396e4cac',NULL,NULL,NULL,0),('6c4d1bbc6d1b4befb9c615c13dfecf75','EX-20260416-013','APPROVED','Xuat hang cho don DH-DEMO-018','','2026-04-16 07:51:20.528792','2026-04-16 07:51:20.536217','a9a24097b5e04dbe8b2f6b2d5728691a','a9a24097b5e04dbe8b2f6b2d5728691a','e034cd464860410483789601aef06140',NULL,NULL,NULL,0),('6ed4580737cc456f835d7f773f62d385','EX-20260420-003','APPROVED','','','2026-04-20 04:45:40.225589','2026-04-20 04:45:56.396258','01000000000000000000000000000006','9000a92575d94a69acde19f5b75814c1',NULL,NULL,'',NULL,0),('71aec8d676f94496861a741a4bbc3374','EX-20260419-001','APPROVED','Xuat hang cho don DH-20260419-001 - KH: Nguyen Quang Sang','','2026-04-19 09:48:00.389782','2026-04-20 04:16:52.728115','01000000000000000000000000000006','9000a92575d94a69acde19f5b75814c1','975b37cb662c418d8ec841d956555c7d',NULL,'',NULL,0),('8b2d09267a9e4515b69d030cadcacf5a','EX-20260416-012','APPROVED','Xuat hang cho don DH-DEMO-017','','2026-04-16 07:51:20.506857','2026-04-16 07:51:20.516927','a9a24097b5e04dbe8b2f6b2d5728691a','7dd717a8e78447c8b9c2bf1a812267ae','6933b3e4d205400f922fe1d48bb12935',NULL,NULL,NULL,0),('8e61158cc00d4e72b095d5fd16b7d8e3','EX-20260507-001','APPROVED','','','2026-05-07 06:19:34.258476','2026-05-07 06:19:58.358992','9000a92575d94a69acde19f5b75814c1','9000a92575d94a69acde19f5b75814c1',NULL,NULL,'',NULL,0),('95aa8439a04140e5b6cbe95cf487ec98','EX-20260416-003','PREPARING','Xuat hang cho don DH-DEMO-008',NULL,'2026-04-16 07:51:20.404538',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL,'9c6f6eaa73c340159eedea920c1cec88',NULL,NULL,NULL,0),('9b3f8dae8b4047b7a70e24252711ae07','EX-20260420-002','PREPARING','',NULL,'2026-04-20 04:39:06.612467',NULL,'01000000000000000000000000000006',NULL,NULL,NULL,'',NULL,0),('9e2c1664cf2f439f8b624eed2dbc4f9b','EX-20260416-006','PREPARING','Xuat hang cho don DH-DEMO-011',NULL,'2026-04-16 07:51:20.430193',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL,'19f42deea4014e1eb1c57f667b2aa50e',NULL,NULL,NULL,0),('b05948242cf54be693f0672b3e355be2','EX-20260429-001','APPROVED','','','2026-04-29 05:37:02.944583','2026-04-29 05:37:07.764930','9000a92575d94a69acde19f5b75814c1','9000a92575d94a69acde19f5b75814c1',NULL,NULL,'',NULL,0),('b6560c31037a472d80d069e07377cd6c','EX-20260429-002','PREPARING','Xuất hàng cho đơn DH-20260429-001 - KH: Nguyen Quang Sang',NULL,'2026-04-29 05:37:29.611601',NULL,'9000a92575d94a69acde19f5b75814c1',NULL,'842c0aa24547494ea32458caba9c4234',NULL,'',NULL,0),('d673fa1d3da441e38f55f54c72b1c2d4','EX-20260420-005','APPROVED','Xuat hang cho don DH-20260420-002 - KH: Nguyen Quang Sang','','2026-04-20 04:54:33.816432','2026-04-20 04:54:59.076238','9000a92575d94a69acde19f5b75814c1','9000a92575d94a69acde19f5b75814c1','8611d11014fc4a4abb6a22770b594220','2026-04-20 04:54:39.276997','','9000a92575d94a69acde19f5b75814c1',1),('f3d4e3aeacd44087a41785e9f5c86f9f','EX-20260416-010','APPROVED','Xuat hang cho don DH-DEMO-015','','2026-04-16 07:51:20.468766','2026-04-16 07:51:20.473972','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae','27212d52a9b642d2a1042041c2e91026',NULL,NULL,NULL,0),('f65cf24707a94224b25b834a3a382323','EX-20260416-009','APPROVED','Xuat hang cho don DH-DEMO-014','','2026-04-16 07:51:20.454467','2026-04-16 07:51:20.458889','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae','baab578692674588904c49de18320b1e',NULL,NULL,NULL,0),('f6c03c44865646e8bb3ac72f69434d60','EX-20260416-014','REJECTED','Xuat hang cho don DH-DEMO-001','Tu choi demo','2026-04-16 07:51:20.546036','2026-04-16 07:51:20.548986','a9a24097b5e04dbe8b2f6b2d5728691a','a9a24097b5e04dbe8b2f6b2d5728691a','f3cb4d5734ab42e8bb2f7461166110b7',NULL,NULL,NULL,0);
/*!40000 ALTER TABLE `export_receipts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `import_receipt_items`
--

DROP TABLE IF EXISTS `import_receipt_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `import_receipt_items` (
  `id` char(32) NOT NULL,
  `quantity` decimal(15,2) NOT NULL,
  `unit_price` decimal(19,4) NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `product_id` char(32) NOT NULL,
  `receipt_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `import_receipt_items_product_id_fd4bc892_fk_products_id` (`product_id`),
  KEY `import_receipt_items_receipt_id_524a4414_fk_import_receipts_id` (`receipt_id`),
  CONSTRAINT `import_receipt_items_product_id_fd4bc892_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `import_receipt_items_receipt_id_524a4414_fk_import_receipts_id` FOREIGN KEY (`receipt_id`) REFERENCES `import_receipts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `import_receipt_items`
--

LOCK TABLES `import_receipt_items` WRITE;
/*!40000 ALTER TABLE `import_receipt_items` DISABLE KEYS */;
INSERT INTO `import_receipt_items` VALUES ('0f1857c09aa3406784a26e016a4dd689',29.00,95000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000014','691525be478544f59575ea26e6eed58f'),('1507c8cdceb5411c84102764c0717968',28.00,320000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000019','82f43c6b8cac47e1beab1059fadea4ee'),('17a7b685263045018e3923de5aa409ad',8.00,265000.0000,'Dong demo','03000000000000000000000000000011','73810d70b6874d4f8d976241b7da4cdd'),('2503fa16d4c74bb79b0b7b3b11277e7e',22.00,420000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000016','645bcf44acbc4ca9964f68616ddd8833'),('25f4e60575344efcb98377d35fd5bab3',4.00,185000.0000,'Dong demo 2','03000000000000000000000000000010','b294255e0d4848ae92572a1ab7450396'),('26d1bb86fee646cd9b31b40066e8d541',20.00,55000.0000,'','03000000000000000000000000000003','9aa21af6109942efbb556ae6f66a2c90'),('285a9a4c846a492bb252f81607b7b538',28.00,185000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000013','645bcf44acbc4ca9964f68616ddd8833'),('2bfd71d7d9204f06b4c9dc5698ad00f8',26.00,185000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000017','691525be478544f59575ea26e6eed58f'),('2e1c6142aa9643beb953d5b91134c7c2',8.00,900.0000,'Dong demo','03000000000000000000000000000005','462a1829326144be817c7a8a2fbf18bf'),('31c1e9623fbd4e588e25309b5d092462',25.00,1200.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000004','a74f99471ec84aabb5e3710a42913dab'),('3345c78c9ef4467d9af6839f9fb586fe',24.00,265000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000011','645bcf44acbc4ca9964f68616ddd8833'),('361dcf5206cc469f9114b81691d2cf31',24.00,28000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000020','82f43c6b8cac47e1beab1059fadea4ee'),('382e293d31f144c385a34d36da79ccd0',6.00,120000.0000,'Dong demo','03000000000000000000000000000018','b294255e0d4848ae92572a1ab7450396'),('3c51148c188148e9ac6b9a70f057bdb2',21.00,220000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000007','61ae34c11cb94323876e7dba3b88d01f'),('49935f23abb948109d7bd0ad5b022f87',26.00,900.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000005','806bff6384614f239d6e542777d8f3f0'),('535546147ff1477db098b6a861dab80e',6.00,185000.0000,'Dong demo','03000000000000000000000000000013','39f21d64c0ef4eed9c6f0309fa86b8eb'),('5405c7a5c6e74707a20c3ad566246e90',30.00,260000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000009','82f43c6b8cac47e1beab1059fadea4ee'),('5f034b2f888847a58d0309b58f1e2fb1',25.00,185000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000010','61ae34c11cb94323876e7dba3b88d01f'),('6afdd7fdeb424cce8bb0ce2045846f62',20.00,195000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000008','806bff6384614f239d6e542777d8f3f0'),('6c65b94690424b0cbfbd786d4c881094',27.00,55000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000003','a74f99471ec84aabb5e3710a42913dab'),('817987eaa6ae4f29bce832bd105800a1',5.00,320000.0000,'Dong demo','03000000000000000000000000000012','4c87a3b08ba84ec4aa3e25bb6c19880a'),('86e77abe95a1460cb94a9231d6fd754d',7.00,185000.0000,'Dong demo','03000000000000000000000000000010','5c968bc9fa9e42c9a6009542a2870d48'),('8ea4117af3654a398eb80d24bfb9c8c7',3.00,120000.0000,'Dong demo 2','03000000000000000000000000000018','5246ef18e4d740f5837f94d903132b13'),('8eba8c0e764d4a1e80bf8ffa32bfd37d',28.00,95000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000001','61ae34c11cb94323876e7dba3b88d01f'),('9d7a1e5abfe2454ba6cff96a59e30ab1',23.00,120000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000018','806bff6384614f239d6e542777d8f3f0'),('9f74e82662ee46d6bedf6c193de510f8',4.00,320000.0000,'Dong demo 2','03000000000000000000000000000012','462a1829326144be817c7a8a2fbf18bf'),('a169841eb44b43d0972bfa6fb87ed396',3.00,95000.0000,'Dong demo 2','03000000000000000000000000000014','39f21d64c0ef4eed9c6f0309fa86b8eb'),('a2a2babbba6b4e3ebc7ba26fa39ba264',5.00,265000.0000,'Dong demo 2','03000000000000000000000000000011','5c968bc9fa9e42c9a6009542a2870d48'),('b028080b97b940809215ceeb2f2632d6',20.00,850000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000015','a74f99471ec84aabb5e3710a42913dab'),('b39107387e87495abbe430f06b4b9853',5.00,850000.0000,'Dong demo 2','03000000000000000000000000000015','afd2f32c93d3463f9fb6cc6c44527bbe'),('b532c08ccfda4e7c9a9b1503148bf861',7.00,95000.0000,'Dong demo','03000000000000000000000000000014','edcc0d5a987a4424bfc3985f4c699cb1'),('b88e9ceffe844453a2be35661e4b1b66',23.00,280000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000006','691525be478544f59575ea26e6eed58f'),('b9e080d2c1a94290badc2a75f8e88cbc',27.00,92000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000002','806bff6384614f239d6e542777d8f3f0'),('c0d16b5635e8488d80dd525e054da2c2',5.00,185000.0000,'Dong demo 2','03000000000000000000000000000013','4c87a3b08ba84ec4aa3e25bb6c19880a'),('c0dd89faf3f74ec4ba0d9ecf21d179b1',4.00,260000.0000,'Dong demo 2','03000000000000000000000000000009','edcc0d5a987a4424bfc3985f4c699cb1'),('c73cde9d9dcc44e2b412adb4a320ca73',3.00,185000.0000,'Dong demo 2','03000000000000000000000000000017','73810d70b6874d4f8d976241b7da4cdd'),('c752410d187243b5bb47876a12c31558',27.00,320000.0000,'Ton kho muc tieu 20-30','03000000000000000000000000000012','61ae34c11cb94323876e7dba3b88d01f'),('cfa9cb523665405eb90d323a3a94c461',8.00,260000.0000,'Dong demo','03000000000000000000000000000009','afd2f32c93d3463f9fb6cc6c44527bbe'),('f4fe3624acaa475092ef84e287c85397',5.00,850000.0000,'Dong demo','03000000000000000000000000000015','5246ef18e4d740f5837f94d903132b13');
/*!40000 ALTER TABLE `import_receipt_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `import_receipts`
--

DROP TABLE IF EXISTS `import_receipts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `import_receipts` (
  `id` char(32) NOT NULL,
  `receipt_code` varchar(30) NOT NULL,
  `status` varchar(10) NOT NULL,
  `note` longtext,
  `rejection_note` longtext,
  `created_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `created_by_id` char(32) NOT NULL,
  `reviewed_by_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `receipt_code` (`receipt_code`),
  KEY `import_receipts_created_by_id_f354946f_fk_users_id` (`created_by_id`),
  KEY `import_receipts_reviewed_by_id_08dff2af_fk_users_id` (`reviewed_by_id`),
  CONSTRAINT `import_receipts_created_by_id_f354946f_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `import_receipts_reviewed_by_id_08dff2af_fk_users_id` FOREIGN KEY (`reviewed_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `import_receipts`
--

LOCK TABLES `import_receipts` WRITE;
/*!40000 ALTER TABLE `import_receipts` DISABLE KEYS */;
INSERT INTO `import_receipts` VALUES ('39f21d64c0ef4eed9c6f0309fa86b8eb','PN-20260416-009','PENDING','Phieu nhap demo 9',NULL,'2026-04-16 07:51:20.358269',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL),('462a1829326144be817c7a8a2fbf18bf','PN-20260416-007','PENDING','Phieu nhap demo 7',NULL,'2026-04-16 07:51:20.346345',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL),('4c87a3b08ba84ec4aa3e25bb6c19880a','PN-20260416-008','PENDING','Phieu nhap demo 8',NULL,'2026-04-16 07:51:20.349911',NULL,'b3e155ca4a5543408138c00727e48ab5',NULL),('5246ef18e4d740f5837f94d903132b13','PN-20260416-012','REJECTED','Phieu nhap demo 12','Tu choi demo','2026-04-16 07:51:20.369140','2026-04-16 07:51:20.370540','a9a24097b5e04dbe8b2f6b2d5728691a','7dd717a8e78447c8b9c2bf1a812267ae'),('5c968bc9fa9e42c9a6009542a2870d48','PN-20260416-014','REJECTED','Phieu nhap demo 14','Tu choi demo','2026-04-16 07:51:20.377629','2026-04-16 07:51:20.380062','a9a24097b5e04dbe8b2f6b2d5728691a','a9a24097b5e04dbe8b2f6b2d5728691a'),('61ae34c11cb94323876e7dba3b88d01f','PN-20260416-002','APPROVED','Phieu nhap demo 2','','2026-04-16 07:51:20.266000','2026-04-16 07:51:20.267441','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae'),('645bcf44acbc4ca9964f68616ddd8833','PN-20260416-003','APPROVED','Phieu nhap demo 3','','2026-04-16 07:51:20.284584','2026-04-16 07:51:20.286233','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae'),('691525be478544f59575ea26e6eed58f','PN-20260416-004','APPROVED','Phieu nhap demo 4','','2026-04-16 07:51:20.300935','2026-04-16 07:51:20.302927','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae'),('73810d70b6874d4f8d976241b7da4cdd','PN-20260416-015','REJECTED','Phieu nhap demo 15','Tu choi demo','2026-04-16 07:51:20.383348','2026-04-16 07:51:20.385227','a9a24097b5e04dbe8b2f6b2d5728691a','a9a24097b5e04dbe8b2f6b2d5728691a'),('806bff6384614f239d6e542777d8f3f0','PN-20260416-001','APPROVED','Phieu nhap demo 1','','2026-04-16 07:51:20.249040','2026-04-16 07:51:20.250927','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae'),('82f43c6b8cac47e1beab1059fadea4ee','PN-20260416-005','APPROVED','Phieu nhap demo 5','','2026-04-16 07:51:20.315878','2026-04-16 07:51:20.317892','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae'),('9aa21af6109942efbb556ae6f66a2c90','PN-20260416-016','APPROVED','','','2026-04-16 07:53:25.652454','2026-04-20 04:38:07.539192','9000a92575d94a69acde19f5b75814c1','9000a92575d94a69acde19f5b75814c1'),('a74f99471ec84aabb5e3710a42913dab','PN-20260416-006','APPROVED','Phieu nhap demo 6','','2026-04-16 07:51:20.329810','2026-04-16 07:51:20.332374','b3e155ca4a5543408138c00727e48ab5','7dd717a8e78447c8b9c2bf1a812267ae'),('afd2f32c93d3463f9fb6cc6c44527bbe','PN-20260416-011','APPROVED','Phieu nhap demo 11','','2026-04-16 07:51:20.365977','2026-04-16 07:52:51.743732','a9a24097b5e04dbe8b2f6b2d5728691a','9000a92575d94a69acde19f5b75814c1'),('b294255e0d4848ae92572a1ab7450396','PN-20260416-013','REJECTED','Phieu nhap demo 13','Tu choi demo','2026-04-16 07:51:20.372917','2026-04-16 07:51:20.374873','a9a24097b5e04dbe8b2f6b2d5728691a','a9a24097b5e04dbe8b2f6b2d5728691a'),('edcc0d5a987a4424bfc3985f4c699cb1','PN-20260416-010','APPROVED','Phieu nhap demo 10','','2026-04-16 07:51:20.362480','2026-04-16 07:53:05.361500','b3e155ca4a5543408138c00727e48ab5','9000a92575d94a69acde19f5b75814c1');
/*!40000 ALTER TABLE `import_receipts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_audit_items`
--

DROP TABLE IF EXISTS `inventory_audit_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_audit_items` (
  `id` char(32) NOT NULL,
  `system_quantity` decimal(15,2) NOT NULL,
  `actual_quantity` decimal(15,2) NOT NULL,
  `note` varchar(500) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `audit_id` char(32) NOT NULL,
  `product_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inventory_audit_items_audit_id_product_id_6115dcc2_uniq` (`audit_id`,`product_id`),
  KEY `idx_audit_item_product` (`product_id`),
  CONSTRAINT `inventory_audit_items_audit_id_9b16595f_fk_inventory_audits_id` FOREIGN KEY (`audit_id`) REFERENCES `inventory_audits` (`id`),
  CONSTRAINT `inventory_audit_items_product_id_6b957246_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `chk_audit_item_actual_qty_non_negative` CHECK ((`actual_quantity` >= 0)),
  CONSTRAINT `chk_audit_item_system_qty_non_negative` CHECK ((`system_quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_audit_items`
--

LOCK TABLES `inventory_audit_items` WRITE;
/*!40000 ALTER TABLE `inventory_audit_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_audit_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_audits`
--

DROP TABLE IF EXISTS `inventory_audits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_audits` (
  `id` char(32) NOT NULL,
  `audit_code` varchar(30) NOT NULL,
  `audit_date` date NOT NULL,
  `note` longtext NOT NULL,
  `status` varchar(10) NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `rejection_note` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` char(32) DEFAULT NULL,
  `created_by_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `audit_code` (`audit_code`),
  KEY `idx_audit_date_status` (`audit_date`,`status`),
  KEY `idx_audit_approved_by` (`approved_by_id`),
  KEY `inventory_audits_created_by_id_16b17d54_fk_users_id` (`created_by_id`),
  KEY `inventory_audits_audit_date_bc853e2a` (`audit_date`),
  KEY `inventory_audits_status_aba5aa6d` (`status`),
  CONSTRAINT `inventory_audits_approved_by_id_0bc12f13_fk_users_id` FOREIGN KEY (`approved_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `inventory_audits_created_by_id_16b17d54_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_audits`
--

LOCK TABLES `inventory_audits` WRITE;
/*!40000 ALTER TABLE `inventory_audits` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_audits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_losses`
--

DROP TABLE IF EXISTS `inventory_losses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_losses` (
  `id` char(32) NOT NULL,
  `loss_code` varchar(30) NOT NULL,
  `loss_quantity` decimal(15,2) NOT NULL,
  `loss_type` varchar(10) NOT NULL,
  `loss_reason` longtext NOT NULL,
  `loss_date` date NOT NULL,
  `unit_cost` decimal(19,4) NOT NULL,
  `status` varchar(10) NOT NULL,
  `rejection_note` longtext,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `audit_item_id` char(32) DEFAULT NULL,
  `created_by_id` char(32) NOT NULL,
  `product_id` char(32) NOT NULL,
  `reviewed_by_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `loss_code` (`loss_code`),
  UNIQUE KEY `audit_item_id` (`audit_item_id`),
  KEY `idx_loss_type_status` (`loss_type`,`status`),
  KEY `idx_loss_date_product` (`loss_date`,`product_id`),
  KEY `idx_loss_product_status` (`product_id`,`status`),
  KEY `inventory_losses_created_by_id_070b0bc6_fk_users_id` (`created_by_id`),
  KEY `inventory_losses_reviewed_by_id_c2adee49_fk_users_id` (`reviewed_by_id`),
  KEY `inventory_losses_loss_type_fe21a2bb` (`loss_type`),
  KEY `inventory_losses_loss_date_518b94d6` (`loss_date`),
  KEY `inventory_losses_status_2a5feaab` (`status`),
  CONSTRAINT `inventory_losses_audit_item_id_0be34b79_fk_inventory` FOREIGN KEY (`audit_item_id`) REFERENCES `inventory_audit_items` (`id`),
  CONSTRAINT `inventory_losses_created_by_id_070b0bc6_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `inventory_losses_product_id_465293e4_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `inventory_losses_reviewed_by_id_c2adee49_fk_users_id` FOREIGN KEY (`reviewed_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `chk_loss_quantity_positive` CHECK ((`loss_quantity` > 0)),
  CONSTRAINT `chk_loss_unit_cost_non_negative` CHECK ((`unit_cost` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_losses`
--

LOCK TABLES `inventory_losses` WRITE;
/*!40000 ALTER TABLE `inventory_losses` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_losses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_stocks`
--

DROP TABLE IF EXISTS `product_stocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_stocks` (
  `id` char(32) NOT NULL,
  `quantity` decimal(15,2) NOT NULL,
  `reserved_quantity` decimal(15,2) NOT NULL DEFAULT '0.00',
  `last_updated` datetime(6) NOT NULL,
  `product_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`),
  CONSTRAINT `product_stocks_product_id_e3e8b865_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_stocks`
--

LOCK TABLES `product_stocks` WRITE;
/*!40000 ALTER TABLE `product_stocks` DISABLE KEYS */;
INSERT INTO `product_stocks` VALUES ('0d6d5995a0d14dbebb511ae7f142732d',18.00,0.00,'2026-04-20 04:54:39.276183','03000000000000000000000000000008'),('30a2371abf7b4d1185a45a0f23ed1318',26.00,0.00,'2026-04-16 07:51:20.258056','03000000000000000000000000000005'),('326c1a92c66a40bea4c6c4955d042d09',34.00,0.00,'2026-04-20 04:50:36.882628','03000000000000000000000000000014'),('412f4de2f1494b14b553e7e6d11e169a',22.00,0.00,'2026-04-16 07:51:20.461946','03000000000000000000000000000010'),('51d6116f747e4834992434e5401311a0',23.00,0.00,'2026-04-16 07:51:20.307066','03000000000000000000000000000006'),('5688ef9dcd824fa09556b137ffe20bd7',28.00,0.00,'2026-04-16 07:51:20.295306','03000000000000000000000000000013'),('66869b20284545a6a5bf1b4d9a45e9e9',24.00,0.00,'2026-04-16 07:53:47.677390','03000000000000000000000000000015'),('7055783c8450453fb266af63d77089d4',24.00,0.00,'2026-04-16 07:51:20.327126','03000000000000000000000000000020'),('79fd3cecafaa43cba78d26becd6e57ed',25.00,0.00,'2026-04-16 07:51:20.340368','03000000000000000000000000000004'),('7d9da2102c0d43cfacd2edbff23ee439',22.00,0.00,'2026-04-16 07:51:20.298500','03000000000000000000000000000016'),('81db3eb36f654ff1b79ff4dab8624d3e',23.00,0.00,'2026-04-16 07:51:20.477417','03000000000000000000000000000011'),('8fdc1143691145fba62680471a51c2aa',28.00,0.00,'2026-04-16 07:51:20.273079','03000000000000000000000000000001'),('a5c27f2135084cae8e95ea393907e415',27.00,0.00,'2026-04-16 07:51:20.255488','03000000000000000000000000000002'),('ab7d302cc8084a128dbf571844eeacfb',21.00,0.00,'2026-04-16 07:51:20.275616','03000000000000000000000000000007'),('acb643b894594300b7bedceabd58d7d6',23.00,0.00,'2026-05-07 06:19:58.362147','03000000000000000000000000000019'),('b8d2b6c5e1bc4522907cf6b32d3f8485',19.00,0.00,'2026-04-20 05:19:25.348910','03000000000000000000000000000018'),('c01e1afd79474d7e9203cc2235120580',42.00,0.00,'2026-04-16 07:53:05.368471','03000000000000000000000000000009'),('c79e985aaad34ae39628803fa89c2b7c',27.00,0.00,'2026-04-16 07:51:20.281830','03000000000000000000000000000012'),('f79e053519e04294a7a5e7d3b26ae1ac',46.00,0.00,'2026-04-20 04:38:07.541583','03000000000000000000000000000003'),('ff66e715178741d8955fa22505396d22',24.00,0.00,'2026-04-16 07:51:20.495749','03000000000000000000000000000017');
/*!40000 ALTER TABLE `product_stocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_units`
--

DROP TABLE IF EXISTS `product_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_units` (
  `id` char(32) NOT NULL,
  `unit_name` varchar(100) NOT NULL,
  `conversion_rate` decimal(19,4) NOT NULL,
  `product_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_units_product_id_4dead36d_fk_products_id` (`product_id`),
  CONSTRAINT `product_units_product_id_4dead36d_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_units`
--

LOCK TABLES `product_units` WRITE;
/*!40000 ALTER TABLE `product_units` DISABLE KEYS */;
INSERT INTO `product_units` VALUES ('04000000000000000000000000000001','Bao',1.0000,'03000000000000000000000000000001'),('04000000000000000000000000000002','Pallet',50.0000,'03000000000000000000000000000001'),('04000000000000000000000000000003','Viên',1.0000,'03000000000000000000000000000004'),('04000000000000000000000000000004','Xe',10000.0000,'03000000000000000000000000000004'),('04000000000000000000000000000005','Khối',1.0000,'03000000000000000000000000000007'),('04000000000000000000000000000006','Tấn',0.6667,'03000000000000000000000000000007'),('04000000000000000000000000000007','Cây',1.0000,'03000000000000000000000000000010'),('04000000000000000000000000000008','Bó',10.0000,'03000000000000000000000000000010'),('04000000000000000000000000000009','Thùng',1.0000,'03000000000000000000000000000015'),('04000000000000000000000000000010','Lít',0.0556,'03000000000000000000000000000015');
/*!40000 ALTER TABLE `product_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` char(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `base_price` decimal(19,4) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `base_unit` varchar(50) NOT NULL,
  `category_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `products_category_id_a7a3a156_fk_categories_id` (`category_id`),
  CONSTRAINT `products_category_id_a7a3a156_fk_categories_id` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('03000000000000000000000000000001','Xi măng Hà Tiên PCB40 50kg',95000.0000,'/media/uploads/san-pham/52da72bb200d479bbc55cc83268f39e1.jpg','Bao','02000000000000000000000000000001'),('03000000000000000000000000000002','Xi măng Bỉm Sơn PCB40 50kg',92000.0000,'/media/uploads/san-pham/e7f52e301cba4125a64d45244e5bc36b.jpg','Bao','02000000000000000000000000000001'),('03000000000000000000000000000003','Vữa xây tô khô trộn sẵn 25kg',55000.0000,'/media/uploads/san-pham/88aa824e54b1474fba3e17f65655d42b.jpg','Bao','02000000000000000000000000000001'),('03000000000000000000000000000004','Gạch đặc 4 lỗ 6x10x22cm',1200.0000,'/media/uploads/san-pham/7027669d47a842658ef455d9b2920f81.jpg','Viên','02000000000000000000000000000002'),('03000000000000000000000000000005','Gạch ống 6 lỗ 8x8x19cm',900.0000,'/media/uploads/san-pham/bcc16c1adf7641fe855e4fb8be4ea58c.jpg','Viên','02000000000000000000000000000002'),('03000000000000000000000000000006','Đá dăm 1x2 xây dựng',280000.0000,'/media/uploads/san-pham/1a0c90a32a3a4233a63c9181df5da29a.jpg','Khối','02000000000000000000000000000002'),('03000000000000000000000000000007','Cát vàng xây dựng (hạt to)',220000.0000,'/media/uploads/san-pham/533333b8e5e54bf7ae471d67ca04d89b.jpg','Khối','02000000000000000000000000000003'),('03000000000000000000000000000008','Cát mịn tô trát',195000.0000,'/media/uploads/san-pham/0465c4a70a3a4b4ebc15559017270682.jpg','Khối','02000000000000000000000000000003'),('03000000000000000000000000000009','Sỏi rửa đổ bê tông 1x2',260000.0000,'/media/uploads/san-pham/c6d14c9187bd4a268fbe8692b7fd5ee4.jpg','Khối','02000000000000000000000000000003'),('03000000000000000000000000000010','Thép cây phi 10 dài 11.7m (Hòa Phát)',185000.0000,'/media/uploads/san-pham/4201a3119b0943eebc8114a67bc3b491.jpg','Cây','02000000000000000000000000000004'),('03000000000000000000000000000011','Thép cây phi 12 dài 11.7m (Hòa Phát)',265000.0000,'/media/uploads/san-pham/c2c2f12271984eebbe243ff8596456da.jpg','Cây','02000000000000000000000000000004'),('03000000000000000000000000000012','Lưới thép hàn phi 4 ô 15x15cm',320000.0000,'/media/uploads/san-pham/2214a0ad804448748cd7e5604291b022.jpg','Tấm','02000000000000000000000000000004'),('03000000000000000000000000000013','Ống nhựa PVC Tiền Phong D114 4m',185000.0000,'/media/uploads/san-pham/44ab157a2352416cb55195a57042df91.jpg','Cây','02000000000000000000000000000005'),('03000000000000000000000000000014','Ống nhựa PVC Tiền Phong D60 4m',95000.0000,'/media/uploads/san-pham/abe3ac4e9c4843c99715db6a29d459b0.jpg','Cây','02000000000000000000000000000005'),('03000000000000000000000000000015','Sơn nước nội thất Dulux 5 Easy 18L',850000.0000,'/media/uploads/san-pham/fab6adec3c4c4126b0c85da1771c32ef.jpg','Thùng','02000000000000000000000000000006'),('03000000000000000000000000000016','Chống thấm Sika Latex 5kg',420000.0000,'/media/uploads/san-pham/97afc434d6104df0968eded1a07021e2.jpg','Thùng','02000000000000000000000000000006'),('03000000000000000000000000000017','Tôn lạnh 0.4mm dài 3m (Hoa Sen)',185000.0000,'/media/uploads/san-pham/62c46e261fd04d3a941475eb693a2efb.jpg','Tấm','02000000000000000000000000000007'),('03000000000000000000000000000018','Tấm Fibro xi măng sóng nhỏ 2.4m',120000.0000,'/media/uploads/san-pham/5e8d1676b80844b6bc190e834dd71074.jpg','Tấm','02000000000000000000000000000007'),('03000000000000000000000000000019','Ván ép 12ly 1220x2440mm',320000.0000,'/media/uploads/san-pham/fbaa7af5478d44b69c5a924a4de427fd.jpg','Tấm','02000000000000000000000000000008'),('03000000000000000000000000000020','Đinh thép 7cm (1kg)',28000.0000,'/media/uploads/san-pham/76754c95813144aa927b5cb48357fbb9.jpg','Kg','02000000000000000000000000000010');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_export_logs`
--

DROP TABLE IF EXISTS `report_export_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_export_logs` (
  `id` char(32) NOT NULL,
  `report_type` varchar(20) NOT NULL,
  `export_format` varchar(5) NOT NULL,
  `exported_at` datetime(6) NOT NULL,
  `filter_params` json NOT NULL,
  `row_count` int NOT NULL,
  `exported_by_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_exportlog_type_date` (`report_type`,`exported_at`),
  KEY `idx_exportlog_user` (`exported_by_id`),
  KEY `report_export_logs_report_type_a9ce09e2` (`report_type`),
  KEY `report_export_logs_exported_at_b401d6a1` (`exported_at`),
  CONSTRAINT `report_export_logs_exported_by_id_bb40d0d2_fk_users_id` FOREIGN KEY (`exported_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_export_logs`
--

LOCK TABLES `report_export_logs` WRITE;
/*!40000 ALTER TABLE `report_export_logs` DISABLE KEYS */;
INSERT INTO `report_export_logs` VALUES ('98761c124d944ca699ae9c2b28b287c6','DISCREPANCY','EXCEL','2026-05-07 06:03:22.917690','{}',20,'9000a92575d94a69acde19f5b75814c1');
/*!40000 ALTER TABLE `report_export_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_order_items`
--

DROP TABLE IF EXISTS `sales_order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_order_items` (
  `id` char(32) NOT NULL,
  `quantity` decimal(15,2) NOT NULL,
  `unit_price` decimal(19,4) NOT NULL,
  `order_id` char(32) NOT NULL,
  `product_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_order_items_order_id_8bd47619_fk_sales_orders_id` (`order_id`),
  KEY `sales_order_items_product_id_ca0aca8c_fk_products_id` (`product_id`),
  CONSTRAINT `sales_order_items_order_id_8bd47619_fk_sales_orders_id` FOREIGN KEY (`order_id`) REFERENCES `sales_orders` (`id`),
  CONSTRAINT `sales_order_items_product_id_ca0aca8c_fk_products_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_order_items`
--

LOCK TABLES `sales_order_items` WRITE;
/*!40000 ALTER TABLE `sales_order_items` DISABLE KEYS */;
INSERT INTO `sales_order_items` VALUES ('06a73895761b4bb0ac74c0f9b2ac38fa',3.00,95000.0000,'67a2395f580741af82ce16e90de5e8c3','03000000000000000000000000000001'),('1627c0b22d39469fab9210a7cdcc0c88',2.00,95000.0000,'4dd5d4ec13cd40b9a5aaede345e3ed0b','03000000000000000000000000000014'),('2d75b40880984ed4857261e4e6e51cc6',1.00,185000.0000,'f53eabc726f7416a8577d369d517704a','03000000000000000000000000000013'),('349a379a29514676a8fdac8cd00019d0',2.00,92000.0000,'2e79280edc0342b78f3ccfba427e826c','03000000000000000000000000000002'),('34de4bd0c8f942dcbb618cae93c42aa8',2.00,900.0000,'0ae089a0a0174abb966322eaec4ac8e4','03000000000000000000000000000005'),('48675bc651f34b29973db464ce34d0c3',1.00,185000.0000,'842c0aa24547494ea32458caba9c4234','03000000000000000000000000000017'),('49be599dd0da48528bea799d0d2f575c',2.00,195000.0000,'8611d11014fc4a4abb6a22770b594220','03000000000000000000000000000008'),('51672ed9717e43739a8624c5abf561f1',2.00,120000.0000,'31fcf04570d942c88de03f014a259c1f','03000000000000000000000000000018'),('573fee31e0ea429d91114c8ce6c40983',2.00,95000.0000,'8ec1a9446480476c80fc66b849b042c3','03000000000000000000000000000014'),('598441501b4f4ed49fb29ece79f1cc6f',1.00,55000.0000,'e034cd464860410483789601aef06140','03000000000000000000000000000003'),('5e290a2160cb4570ae5af5912b9287a3',2.00,185000.0000,'6e0b5a6f4f7a4f5cbc8af9a20fb14e7f','03000000000000000000000000000017'),('641f4311c382492f9d60a957c76da328',3.00,320000.0000,'6933b3e4d205400f922fe1d48bb12935','03000000000000000000000000000019'),('6ab4a80b05da4cd9b4ac6213036b9de9',1.00,1200.0000,'3331ca55e4544eb080578342396e4cac','03000000000000000000000000000004'),('6b85618005e6429ba9b1475bfcd473c7',2.00,195000.0000,'f3cb4d5734ab42e8bb2f7461166110b7','03000000000000000000000000000008'),('6e1006056fe04a8397f1e10f302c8bd9',3.00,260000.0000,'19f42deea4014e1eb1c57f667b2aa50e','03000000000000000000000000000009'),('8884fdf05d734adba0e859dac766fa54',2.00,280000.0000,'8f8f53e3ac674462ad1cfb19ed320752','03000000000000000000000000000006'),('8b7010364a79405c9447aa7bd8a23a94',2.00,120000.0000,'69c790f1e5234a9cafe64bad22626cf5','03000000000000000000000000000018'),('b43987ce336f4253a605826ba557def9',1.00,850000.0000,'44349456382f40578cbf36e6b00b838f','03000000000000000000000000000015'),('b7b66d0ffe054797843bc897dbc8806d',3.00,185000.0000,'baab578692674588904c49de18320b1e','03000000000000000000000000000010'),('c8f2d3b411a140ceb58fe18e1b60d23a',1.00,265000.0000,'27212d52a9b642d2a1042041c2e91026','03000000000000000000000000000011'),('d67209889ee54721b1c4a0662966deb7',10.00,265000.0000,'975b37cb662c418d8ec841d956555c7d','03000000000000000000000000000011'),('db1fdec19f644d259efde2a437f4b2c2',3.00,28000.0000,'90ffd63c63cb4251bf37ef59043b13ab','03000000000000000000000000000020'),('f5e9966c276c4725afb797b08ef6eaa3',1.00,420000.0000,'fd7c1a2bea8b40cbaa4cf07db180656d','03000000000000000000000000000016'),('f65e3be86e4a443cbe6536896351201d',3.00,320000.0000,'9c6f6eaa73c340159eedea920c1cec88','03000000000000000000000000000012'),('f984d9562bf44cd58d5375868428b3d0',3.00,220000.0000,'14438ca3b91944cca9c6a4405df67246','03000000000000000000000000000007');
/*!40000 ALTER TABLE `sales_order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_orders`
--

DROP TABLE IF EXISTS `sales_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_orders` (
  `id` char(32) NOT NULL,
  `order_code` varchar(30) NOT NULL,
  `customer_name` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(15) NOT NULL,
  `created_by_id` char(32) NOT NULL,
  `customer_phone` varchar(20) DEFAULT NULL,
  `note` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_code` (`order_code`),
  KEY `sales_orders_created_by_id_e682ebf4_fk_users_id` (`created_by_id`),
  CONSTRAINT `sales_orders_created_by_id_e682ebf4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_orders`
--

LOCK TABLES `sales_orders` WRITE;
/*!40000 ALTER TABLE `sales_orders` DISABLE KEYS */;
INSERT INTO `sales_orders` VALUES ('0ae089a0a0174abb966322eaec4ac8e4','DH-DEMO-007','Khach hang 07','2026-04-16 07:51:20.229384','WAITING','98fee7f123a14d879f5888689e933bef','0900000007','Don hang demo'),('14438ca3b91944cca9c6a4405df67246','DH-DEMO-002','Khach hang 02','2026-04-16 07:51:20.223973','CONFIRMED','98fee7f123a14d879f5888689e933bef','0900000002','Don hang demo'),('19f42deea4014e1eb1c57f667b2aa50e','DH-DEMO-011','Khach hang 11','2026-04-16 07:51:20.232841','WAITING','98fee7f123a14d879f5888689e933bef','0900000011','Don hang demo'),('27212d52a9b642d2a1042041c2e91026','DH-DEMO-015','Khach hang 15','2026-04-16 07:51:20.237044','DONE','98fee7f123a14d879f5888689e933bef','0900000015','Don hang demo'),('2e79280edc0342b78f3ccfba427e826c','DH-DEMO-019','Khach hang 19','2026-04-16 07:51:20.239840','CANCELLED','98fee7f123a14d879f5888689e933bef','0900000019','Don hang demo'),('31fcf04570d942c88de03f014a259c1f','DH-20260420-003','Nguyen Quang Sang','2026-04-20 05:18:39.977829','DONE','9000a92575d94a69acde19f5b75814c1','',''),('3331ca55e4544eb080578342396e4cac','DH-DEMO-006','Khach hang 06','2026-04-16 07:51:20.227890','WAITING','98fee7f123a14d879f5888689e933bef','0900000006','Don hang demo'),('44349456382f40578cbf36e6b00b838f','DH-DEMO-012','Khach hang 12','2026-04-16 07:51:20.234029','DONE','98fee7f123a14d879f5888689e933bef','0900000012','Don hang demo'),('4dd5d4ec13cd40b9a5aaede345e3ed0b','DH-DEMO-010','Khach hang 10','2026-04-16 07:51:20.232052','WAITING','98fee7f123a14d879f5888689e933bef','0900000010','Don hang demo'),('67a2395f580741af82ce16e90de5e8c3','DH-DEMO-020','Khach hang 20','2026-04-16 07:51:20.241190','CANCELLED','98fee7f123a14d879f5888689e933bef','0900000020','Don hang demo'),('6933b3e4d205400f922fe1d48bb12935','DH-DEMO-017','Khach hang 17','2026-04-16 07:51:20.238631','DONE','98fee7f123a14d879f5888689e933bef','0900000017','Don hang demo'),('69c790f1e5234a9cafe64bad22626cf5','DH-DEMO-013','Khach hang 13','2026-04-16 07:51:20.235318','DONE','98fee7f123a14d879f5888689e933bef','0900000013','Don hang demo'),('6e0b5a6f4f7a4f5cbc8af9a20fb14e7f','DH-DEMO-016','Khach hang 16','2026-04-16 07:51:20.237829','DONE','98fee7f123a14d879f5888689e933bef','0900000016','Don hang demo'),('842c0aa24547494ea32458caba9c4234','DH-20260429-001','Nguyen Quang Sang','2026-04-29 05:37:26.668003','WAITING','9000a92575d94a69acde19f5b75814c1','',''),('8611d11014fc4a4abb6a22770b594220','DH-20260420-002','Nguyen Quang Sang','2026-04-20 04:54:26.436174','DONE','9000a92575d94a69acde19f5b75814c1','',''),('8ec1a9446480476c80fc66b849b042c3','DH-20260420-001','Nguyen Quang Sang','2026-04-20 04:50:14.154062','DONE','9000a92575d94a69acde19f5b75814c1','',''),('8f8f53e3ac674462ad1cfb19ed320752','DH-DEMO-004','Khach hang 04','2026-04-16 07:51:20.225482','CONFIRMED','98fee7f123a14d879f5888689e933bef','0900000004','Don hang demo'),('90ffd63c63cb4251bf37ef59043b13ab','DH-DEMO-005','Khach hang 05','2026-04-16 07:51:20.226369','CONFIRMED','98fee7f123a14d879f5888689e933bef','0900000005','Don hang demo'),('975b37cb662c418d8ec841d956555c7d','DH-20260419-001','Nguyen Quang Sang','2026-04-19 09:47:31.117080','WAITING','01000000000000000000000000000003','',''),('9c6f6eaa73c340159eedea920c1cec88','DH-DEMO-008','Khach hang 08','2026-04-16 07:51:20.230185','WAITING','98fee7f123a14d879f5888689e933bef','0900000008','Don hang demo'),('baab578692674588904c49de18320b1e','DH-DEMO-014','Khach hang 14','2026-04-16 07:51:20.236240','DONE','98fee7f123a14d879f5888689e933bef','0900000014','Don hang demo'),('e034cd464860410483789601aef06140','DH-DEMO-018','Khach hang 18','2026-04-16 07:51:20.239300','DONE','98fee7f123a14d879f5888689e933bef','0900000018','Don hang demo'),('f3cb4d5734ab42e8bb2f7461166110b7','DH-DEMO-001','Khach hang 01','2026-04-16 07:51:20.222726','CONFIRMED','98fee7f123a14d879f5888689e933bef','0900000001','Don hang demo'),('f53eabc726f7416a8577d369d517704a','DH-DEMO-009','Khach hang 09','2026-04-16 07:51:20.231165','WAITING','98fee7f123a14d879f5888689e933bef','0900000009','Don hang demo'),('fd7c1a2bea8b40cbaa4cf07db180656d','DH-DEMO-003','Khach hang 03','2026-04-16 07:51:20.224807','CONFIRMED','98fee7f123a14d879f5888689e933bef','0900000003','Don hang demo');
/*!40000 ALTER TABLE `sales_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` char(32) DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` (`user_id`),
  CONSTRAINT `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_outstandingtoken` VALUES (1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODAzNjUyMSwiaWF0IjoxNzc1NDQ0NTIxLCJqdGkiOiJiMzFiZTE4MjlhNDI0MjIzYjEyNGU0NTJlMDhiODE0NyIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.loY_2mpkpkqMkUo8Bx1J9LpFpnKQlrKNyaA2RkySLZo','2026-04-06 03:02:01.818673','2026-05-06 03:02:01.000000','9000a92575d94a69acde19f5b75814c1','b31be1829a424223b124e452e08b8147'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODAzNzMyNiwiaWF0IjoxNzc1NDQ1MzI2LCJqdGkiOiJkOGY4OTgwNWI0ZDQ0OWEzODJjMWUyYWY0ZjA2MDMwNiIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDIifQ.KcbG8JWYBuqHNbzoz-XI9uFPCEVbBf_05vQko3XC6qw','2026-04-06 03:15:26.700342','2026-05-06 03:15:26.000000','01000000000000000000000000000002','d8f89805b4d449a382c1e2af4f060306'),(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODAzNzMzOCwiaWF0IjoxNzc1NDQ1MzM4LCJqdGkiOiJhYjkyZWIyYjRlNDM0OTc1OTIxN2UxNTRiZTc1OWMwNCIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.-C3y_pnnKhZaup91YPVNnqzEW45m_TT0l01z8om5ibU','2026-04-06 03:15:38.171420','2026-05-06 03:15:38.000000','01000000000000000000000000000006','ab92eb2b4e4349759217e154be759c04'),(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODAzMywiaWF0IjoxNzc1NjM2MDMzLCJqdGkiOiJlMmViYTgzNjczYzg0OTkwYTIwOGI2OTZjYjgzYTgzOSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDIifQ.g77yBXMlICHmpjiy6BZx9PJi1TCai4MX0LnoO6UE3bM','2026-04-08 08:13:53.192510','2026-05-08 08:13:53.000000','01000000000000000000000000000002','e2eba83673c84990a208b696cb83a839'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODA5MSwiaWF0IjoxNzc1NjM2MDkxLCJqdGkiOiJiOWQzNjk5YzhiY2M0MDI1OWIxMDZjYmFmNjBkMGQ5NiIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDIifQ.MWzXOlj0ukHtCRoXPMU73hftOj6XeR5CaNd0r4m1XSQ','2026-04-08 08:14:51.689585','2026-05-08 08:14:51.000000','01000000000000000000000000000002','b9d3699c8bcc40259b106cbaf60d0d96'),(6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODU1OCwiaWF0IjoxNzc1NjM2NTU4LCJqdGkiOiI4YTE3NmI2MjFlMWU0MzMwYjYzZDk4YjY2MThjMjNjNCIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.4htnvQ2wD4u20caVfF3_QSX_ilgPscsOjR1aMwVuG_s','2026-04-08 08:22:38.694598','2026-05-08 08:22:38.000000','01000000000000000000000000000006','8a176b621e1e4330b63d98b6618c23c4'),(7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODU5OCwiaWF0IjoxNzc1NjM2NTk4LCJqdGkiOiI0OTUwNzNiOGY1YmU0ZWYyOTM4MThhYjRiNWRkZDcwZCIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDMifQ.br7Eocpe92zebmfFvUdDOXlQxqkc1vkSe8oOTdSOOxI','2026-04-08 08:23:18.719339','2026-05-08 08:23:18.000000','01000000000000000000000000000003','495073b8f5be4ef293818ab4b5ddd70d'),(8,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODYxMSwiaWF0IjoxNzc1NjM2NjExLCJqdGkiOiIyOTFjYTlkODdmNzM0OTAyOTVmMmY4NTkxOTAwMzI5YyIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDQifQ.rbZsb9wwe8UgHSfICksBpqmRiB9KBFNaVHXbKop9PXg','2026-04-08 08:23:31.036421','2026-05-08 08:23:31.000000','01000000000000000000000000000004','291ca9d87f73490295f2f8591900329c'),(9,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODYyMiwiaWF0IjoxNzc1NjM2NjIyLCJqdGkiOiJjNjJhZDk5YmVkY2Q0MDE3ODQ0NDc4ZWIyMThhMzJjNSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDUifQ.W9hvlG0nR2cyXxkjzY50gfL5JKyqiL-oNYRle-yHlJo','2026-04-08 08:23:42.320343','2026-05-08 08:23:42.000000','01000000000000000000000000000005','c62ad99bedcd4017844478eb218a32c5'),(10,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODY0OSwiaWF0IjoxNzc1NjM2NjQ5LCJqdGkiOiI0ZmZlM2VlNmNkOTU0OWQ2YjZlODUxZmNlNWIwZjk0OSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.lD-i6r3CHS4-3gJvj67FU_WtUxKyrsNnMqs0HEXdMwk','2026-04-08 08:24:09.927339','2026-05-08 08:24:09.000000','01000000000000000000000000000006','4ffe3ee6cd9549d6b6e851fce5b0f949'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODY1OCwiaWF0IjoxNzc1NjM2NjU4LCJqdGkiOiI2Y2U1YmY1MTIwMDE0NzMwYTAxNzA3NjE4ZGQxZTkzMiIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDcifQ.c-FQ3Nqr2iP_Q7UWxPwJBAEkAr2y3pLkxXpjJ0RAOww','2026-04-08 08:24:18.897129','2026-05-08 08:24:18.000000','01000000000000000000000000000007','6ce5bf5120014730a01707618dd1e932'),(12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODY2NiwiaWF0IjoxNzc1NjM2NjY2LCJqdGkiOiJjMDZmYTJlZGVmNjE0NjM4OTA2YjAyZjVkNGU4NTliZSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDgifQ.lKDZNnpTtwPeck5EVP5kUUC4q5-APZAK3nEXySBX7gw','2026-04-08 08:24:26.390588','2026-05-08 08:24:26.000000','01000000000000000000000000000008','c06fa2edef614638906b02f5d4e859be'),(13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODc5NCwiaWF0IjoxNzc1NjM2Nzk0LCJqdGkiOiI4N2RmMTg4MTA2MGY0YTk1YjM2MDQxOTViZGE1NDZkYSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDkifQ.KbubVr7YuX0rC8D_OAah1gd__RxOW4rCegBqHW-hF8A','2026-04-08 08:26:34.947476','2026-05-08 08:26:34.000000','01000000000000000000000000000009','87df1881060f4a95b3604195bda546da'),(14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIyODgwMywiaWF0IjoxNzc1NjM2ODAzLCJqdGkiOiI0ODgzZDIzY2RhYTM0YTMzYTJjMzU3YmM5MDQ2OWQzYSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMTAifQ.3H77PhSLeG1bA2BLOv0tHoNlwFUVk8D3usrHADJrJ6E','2026-04-08 08:26:43.804368','2026-05-08 08:26:43.000000','01000000000000000000000000000010','4883d23cdaa34a33a2c357bc90469d3a'),(15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODc1NTA4MiwiaWF0IjoxNzc2MTYzMDgyLCJqdGkiOiIyYjhiNDQ1NThkNDU0OTMxYTVkNmYzYjFiMDg0ZTMwMyIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.yNQVwOy65oriGMpEwpf2wHvUwwcS-v6mtzNQNml2ayM','2026-04-14 10:38:02.725932','2026-05-14 10:38:02.000000','9000a92575d94a69acde19f5b75814c1','2b8b44558d454931a5d6f3b1b084e303'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTE4NDAzMSwiaWF0IjoxNzc2NTkyMDMxLCJqdGkiOiIwYWNjMmFjMDhkNDE0NWYzYmZlYmVhNjQ5MjhmYWE4YyIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDMifQ.7XHRYfM0jEYiKKk_H9I53SFXKJbFXpxVQJcpCxisIxs','2026-04-19 09:47:11.029503','2026-05-19 09:47:11.000000','01000000000000000000000000000003','0acc2ac08d4145f3bfebea64928faa8c'),(17,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTE4NDA3MCwiaWF0IjoxNzc2NTkyMDcwLCJqdGkiOiIyMzAwMDNkNGVmOTU0YWE3ODMzZDNhNTJjYjAwMGRjMyIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.5NTsnOm8ePG0_s1krn-fRBoI4gT2kQYawbW7UYap7OM','2026-04-19 09:47:50.142560','2026-05-19 09:47:50.000000','01000000000000000000000000000006','230003d4ef954aa7833d3a52cb000dc3'),(18,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MDQxMSwiaWF0IjoxNzc2NjU4NDExLCJqdGkiOiJhOGNiNTQyYTQyNWI0Y2JlYmI5ZWRlNjk3MWI2NWYyNiIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.ZCosG1QR-UbBPeXY6-2u5BkMr4366BbmGMoeD0iBzSU','2026-04-20 04:13:31.974969','2026-05-20 04:13:31.000000','9000a92575d94a69acde19f5b75814c1','a8cb542a425b4cbebb9ede6971b65f26'),(19,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MDYzMiwiaWF0IjoxNzc2NjU4NjMyLCJqdGkiOiJmYTcwYTE2N2MxMjk0Y2JlYWNjMjg3ODVkOTg5ZGRhYSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.BHyKbcbpbbGSphgH-0OMgnmuCDe41M7mDaUW_gSp33g','2026-04-20 04:17:12.918698','2026-05-20 04:17:12.000000','01000000000000000000000000000006','fa70a167c1294cbeacc28785d989ddaa'),(20,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MDY1OCwiaWF0IjoxNzc2NjU4NjU4LCJqdGkiOiIxMDAxMGZhNTAyNzI0YjE3YTIzNGEzMTYzODQyYTU3NCIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.dN13XVpd3oeLhxbIiT-27eb7Q81OumxZowmQN-Tqm5c','2026-04-20 04:17:38.583242','2026-05-20 04:17:38.000000','9000a92575d94a69acde19f5b75814c1','10010fa502724b17a234a3163842a574'),(21,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MTY0MSwiaWF0IjoxNzc2NjU5NjQxLCJqdGkiOiJhMDc1ZDNiNDQwYjM0MWEzODE5NjllNjM0OGU3ODk0OCIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.QuBXnJO4zZxxrtdV2IPViAf7hk6w9D5d_ouWKWaJldc','2026-04-20 04:34:01.356444','2026-05-20 04:34:01.000000','01000000000000000000000000000006','a075d3b440b341a381969e6348e78948'),(22,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MTczOSwiaWF0IjoxNzc2NjU5NzM5LCJqdGkiOiJlNmIwNDQ4YmE3NDE0NTIzYTM5MWZkMjQ5Mjc5YzU1NyIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.2BVHe6E-WvN39W7zPA6CgsN0BeMOR7vqzSfNUvH-dZA','2026-04-20 04:35:39.293039','2026-05-20 04:35:39.000000','01000000000000000000000000000006','e6b0448ba7414523a391fd249279c557'),(23,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MTg2MiwiaWF0IjoxNzc2NjU5ODYyLCJqdGkiOiI0OTc2MDhlMjA3Y2E0M2UyYWY0NDIwYWY0MDUyMTQ0MyIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.FrpeRTNbCBAhYNmZpGf5elUzXnuPQy5EbN0mgDe1lx8','2026-04-20 04:37:42.639258','2026-05-20 04:37:42.000000','9000a92575d94a69acde19f5b75814c1','497608e207ca43e2af4420af40521443'),(24,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MTkxNCwiaWF0IjoxNzc2NjU5OTE0LCJqdGkiOiI3ZjhkMzVhMDBiZTU0OWE2YTVjYjdmOWVhM2YzNWE0NiIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.Gar-zxGcMRg2-xOlNkC-1XRy9EhMKtcZg7ir4zBi6lQ','2026-04-20 04:38:34.003836','2026-05-20 04:38:34.000000','01000000000000000000000000000006','7f8d35a00be549a6a5cb7f9ea3f35a46'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MjE3MywiaWF0IjoxNzc2NjYwMTczLCJqdGkiOiJmMTQ5MTNhODMyMWI0ODFmOGQxMTJiNTMxMzRiNDQ2NCIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDMifQ.81fSTtQ5Bia2XULavvPCC7j0L1VMUfpMZQwOuRbzswk','2026-04-20 04:42:53.851016','2026-05-20 04:42:53.000000','01000000000000000000000000000003','f14913a8321b481f8d112b53134b4464'),(26,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MjE5OSwiaWF0IjoxNzc2NjYwMTk5LCJqdGkiOiIxODk3NjQ5ZDRlYWM0ZDcwYWZjMjk2YTI0YWMxNWFmMSIsInVzZXJfaWQiOiIwMTAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDYifQ.IAnVBGpveUAbW-4PGvWmNfXLQ5O9__2oGmx4jD1K1Sc','2026-04-20 04:43:19.357224','2026-05-20 04:43:19.000000','01000000000000000000000000000006','1897649d4eac4d70afc296a24ac15af1'),(27,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTI1MjM0NywiaWF0IjoxNzc2NjYwMzQ3LCJqdGkiOiJiYTllZTI5YTQyOWU0YzdhYmRjZjliYjMwZTQ5YTMwMSIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.ok4RqiMoRGqrCVYkKjr0_bELOkfiMXyfbKdQlB89BWE','2026-04-20 04:45:47.336887','2026-05-20 04:45:47.000000','9000a92575d94a69acde19f5b75814c1','ba9ee29a429e4c7abdcf9bb30e49a301'),(28,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTQ0NTg1OCwiaWF0IjoxNzc2ODUzODU4LCJqdGkiOiJiODBlODU3OWFiYmU0YzI1OTE2MDI0YThhNTNmNjk0OSIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.rKfmtqcV2wbRKygUWTi1Eic2ovjbJnv7DhJKv6-gAEc','2026-04-22 10:30:58.227206','2026-05-22 10:30:58.000000','9000a92575d94a69acde19f5b75814c1','b80e8579abbe4c25916024a8a53f6949'),(29,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTQ0NTkzOCwiaWF0IjoxNzc2ODUzOTM4LCJqdGkiOiIzZjQwYWY5NDJiN2E0N2JhOGYyNjY1NWU4MmRkODBkOSIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.YtnR2GDGg4n-EYGHOo2Jsbm3Vpe3NT2Q9hpZWwL8nK8','2026-04-22 10:32:18.029916','2026-05-22 10:32:18.000000','9000a92575d94a69acde19f5b75814c1','3f40af942b7a47ba8f26655e82dd80d9'),(30,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3OTQ0NjAyMywiaWF0IjoxNzc2ODU0MDIzLCJqdGkiOiIzZDA0MWJkMjVhNDM0M2FjYjNmZjZhNWJlOTU0MWI0OCIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.aAXi-PsdGEGQOqnyQWTQ2XZblW7q5FFwjtOK7871reE','2026-04-22 10:33:43.584876','2026-05-22 10:33:43.000000','9000a92575d94a69acde19f5b75814c1','3d041bd25a4343acb3ff6a5be9541b48'),(31,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDAzMzIyMCwiaWF0IjoxNzc3NDQxMjIwLCJqdGkiOiIyYWFmMzViYjE5YTE0YWY5OWE5NzU3MjU0ODkxNDMxMiIsInVzZXJfaWQiOiI5MDAwYTkyNS03NWQ5LTRhNjktYWNkZS0xOWY1Yjc1ODE0YzEifQ.wxpjY5B2kXWZYyGmwtXu_J8zr3EOl4sQfaDg5cMTwlA','2026-04-29 05:40:20.394473','2026-05-29 05:40:20.000000','9000a92575d94a69acde19f5b75814c1','2aaf35bb19a14af99a97572548914312');
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `id` char(32) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` longtext,
  `role` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('pbkdf2_sha256$1200000$9u8MwuLVoJrS1zj2QKQ5CL$ohjkR597ClPlHvyAqJW8wMfSNdbMAYnBdglTiKsCd5A=','2026-05-07 06:23:33.420567',1,'admin02','Hùng','Trần','admin02@vlxd.vn',1,1,'2024-01-02 08:00:00.000000','01000000000000000000000000000002','Trần Văn Hùng','0901000002','45 Nguyễn Huệ, Q1, TP.HCM','ADMIN'),('pbkdf2_sha256$1200000$2LF0VtcwORedFl6Snm6dHC$cCN8dA24y4+O9qjhBlLHRIwz9huMCbLdnvq7rsHnm/g=','2026-04-20 04:42:53.912390',0,'sale01','Lan','Phạm','sale01@vlxd.vn',0,1,'2024-01-05 08:00:00.000000','01000000000000000000000000000003','Phạm Thị Lan','0902000001','78 Trần Hưng Đạo, Q5, TP.HCM','SALE'),('pbkdf2_sha256$1200000$8u7u81wH2F8IWU0xq25PDJ$2NCSa490b+W3pFyh8gzzCxxCwEpIVtpHtxPLTMxz50U=','2026-04-08 08:23:31.097083',0,'sale02','Hoa','Lê','sale02@vlxd.vn',0,1,'2024-01-06 08:00:00.000000','01000000000000000000000000000004','Lê Thị Hoa','0902000002','23 Đinh Tiên Hoàng, Q1, TP.HCM','SALE'),('pbkdf2_sha256$1200000$W0oJlI10twTfo13G1PJrzF$qcbfUykm0OCA2nahl6ltZ0rPOXUmW34evbxRpBq/2eM=','2026-04-08 08:23:42.379561',0,'sale03','Tuấn','Đỗ','sale03@vlxd.vn',0,1,'2024-01-07 08:00:00.000000','01000000000000000000000000000005','Đỗ Văn Tuấn','0902000003','56 Lý Thường Kiệt, Q10, TP.HCM','SALE'),('pbkdf2_sha256$1200000$53nkEzUNqnGdqy5SHQl3QB$7vaQQEMNl7QLB0eoCJH5TqBfXi7SwLfssfwTHDIwhtA=','2026-04-20 04:43:19.422985',0,'kho01','Nam','Hoàng','kho01@vlxd.vn',0,1,'2024-01-10 08:00:00.000000','01000000000000000000000000000006','Hoàng Văn Nam','0903000001','11 Điện Biên Phủ, Bình Thạnh, TP.HCM','KHO'),('pbkdf2_sha256$1200000$kxmEJvSKxUbeyNDjYy7efU$k8/bI3JaqlHgsaK63Kr4c6ng5l9sOzR6R5BzCkF79ms=','2026-04-08 08:24:18.962386',0,'kho02','Dũng','Ngô','kho02@vlxd.vn',0,1,'2024-01-11 08:00:00.000000','01000000000000000000000000000007','Ngô Văn Dũng','0903000002','22 Hoàng Văn Thụ, Phú Nhuận, TP.HCM','KHO'),('pbkdf2_sha256$1200000$TCS6yOUNwiPhqMTOzcpF7M$hohmEplH/q0xyfzC0eZmu45x6Ym7HYNl7Z+xV0nAYHA=','2026-04-08 08:24:26.455073',0,'kho03','Hiền','Đinh','kho03@vlxd.vn',0,1,'2024-01-12 08:00:00.000000','01000000000000000000000000000008','Đinh Thị Hiền','0903000003','67 Lê Văn Sỹ, Q3, TP.HCM','KHO'),('pbkdf2_sha256$1200000$aMo8r37ELqYvRyCBwZ9ZS4$5KAZbtS2U7XIwehcga4IcBBxzS3kFdkajer8nmoHg2E=','2026-04-08 08:26:35.006789',0,'ketoan01','Thu','Phan','ketoan01@vlxd.vn',0,1,'2024-01-15 08:00:00.000000','01000000000000000000000000000009','Phan Thị Thu','0904000001','44 Nguyễn Đình Chiểu, Q3, TP.HCM','KE_TOAN'),('pbkdf2_sha256$1200000$gIceKEkYYQNfU2WW8kpyJT$PxfOk2uD9OUv9rqFw20d3FSyxeE8YfY9v6L4AiFpkmA=','2026-04-08 08:26:43.866574',0,'ketoan02','Hằng','Vũ','ketoan02@vlxd.vn',0,1,'2024-01-16 08:00:00.000000','01000000000000000000000000000010','Vũ Thị Hằng','0904000002','77 Bà Huyện Thanh Quan, Q3, TP.HCM','KE_TOAN'),('',NULL,0,'ketoan_demo','','','ketoan_demo@example.com',0,1,'2026-04-14 10:48:55.323540','7dd717a8e78447c8b9c2bf1a812267ae','Kế toán Demo',NULL,NULL,'KE_TOAN'),('pbkdf2_sha256$1200000$9u8MwuLVoJrS1zj2QKQ5CL$ohjkR597ClPlHvyAqJW8wMfSNdbMAYnBdglTiKsCd5A=','2026-04-29 05:40:20.430668',1,'admin','','','',1,1,'2026-03-23 08:16:05.150846','9000a92575d94a69acde19f5b75814c1','',NULL,NULL,''),('',NULL,0,'sale_demo','','','sale_demo@example.com',0,1,'2026-04-14 10:48:55.306522','98fee7f123a14d879f5888689e933bef','Nhân viên Sale Demo',NULL,NULL,'SALE'),('',NULL,1,'admin_demo','','','admin_demo@example.com',1,1,'2026-04-14 10:48:55.302254','a9a24097b5e04dbe8b2f6b2d5728691a','Admin Demo',NULL,NULL,'ADMIN'),('',NULL,0,'kho_demo','','','kho_demo@example.com',0,1,'2026-04-14 10:48:55.314832','b3e155ca4a5543408138c00727e48ab5','Thủ kho Demo',NULL,NULL,'KHO');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` char(32) NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

LOCK TABLES `users_groups` WRITE;
/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` char(32) NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

LOCK TABLES `users_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
INSERT INTO `users_user_permissions` VALUES (8,'01000000000000000000000000000003',24),(10,'01000000000000000000000000000003',28),(9,'01000000000000000000000000000003',32),(11,'01000000000000000000000000000004',24),(13,'01000000000000000000000000000004',28),(12,'01000000000000000000000000000004',32),(14,'01000000000000000000000000000005',24),(16,'01000000000000000000000000000005',28),(15,'01000000000000000000000000000005',32),(2,'01000000000000000000000000000006',24),(3,'01000000000000000000000000000006',25),(4,'01000000000000000000000000000006',26),(5,'01000000000000000000000000000006',28),(6,'01000000000000000000000000000006',29),(1,'01000000000000000000000000000006',32),(18,'01000000000000000000000000000007',24),(19,'01000000000000000000000000000007',25),(20,'01000000000000000000000000000007',26),(21,'01000000000000000000000000000007',28),(22,'01000000000000000000000000000007',29),(17,'01000000000000000000000000000007',32),(24,'01000000000000000000000000000008',24),(25,'01000000000000000000000000000008',25),(26,'01000000000000000000000000000008',26),(27,'01000000000000000000000000000008',28),(28,'01000000000000000000000000000008',29),(23,'01000000000000000000000000000008',32),(30,'01000000000000000000000000000009',28),(31,'01000000000000000000000000000010',28),(41,'7dd717a8e78447c8b9c2bf1a812267ae',24),(43,'7dd717a8e78447c8b9c2bf1a812267ae',28),(42,'7dd717a8e78447c8b9c2bf1a812267ae',32),(32,'98fee7f123a14d879f5888689e933bef',24),(34,'98fee7f123a14d879f5888689e933bef',28),(33,'98fee7f123a14d879f5888689e933bef',32),(36,'b3e155ca4a5543408138c00727e48ab5',24),(37,'b3e155ca4a5543408138c00727e48ab5',25),(38,'b3e155ca4a5543408138c00727e48ab5',26),(39,'b3e155ca4a5543408138c00727e48ab5',28),(40,'b3e155ca4a5543408138c00727e48ab5',29),(35,'b3e155ca4a5543408138c00727e48ab5',32);
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'quanlykhovatlieu'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-07  6:26:02
