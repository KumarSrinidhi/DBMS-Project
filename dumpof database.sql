CREATE DATABASE  IF NOT EXISTS `real_estatemanagement_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `real_estatemanagement_system`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: real_estatemanagement_system
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `agent`
--

DROP TABLE IF EXISTS `agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agent` (
  `agentId` int NOT NULL,
  `userId` int NOT NULL,
  `licenseNumber` varchar(20) NOT NULL,
  `experienceYears` int NOT NULL,
  `brokerageName` varchar(50) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`agentId`),
  UNIQUE KEY `userId` (`userId`),
  UNIQUE KEY `licenseNumber` (`licenseNumber`),
  CONSTRAINT `agent_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
  CONSTRAINT `agent_chk_1` CHECK ((`experienceYears` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent`
--

LOCK TABLES `agent` WRITE;
/*!40000 ALTER TABLE `agent` DISABLE KEYS */;
INSERT INTO `agent` VALUES (201,2,'MH-REA-2024-123',8,'Metro Brokers',1),(202,5,'HR-REA-4567-456',12,'NCR Properties Ltd.',1),(203,11,'TS-REA-7890-789',5,'Hyderabad Realty',1);
/*!40000 ALTER TABLE `agent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `amenities`
--

DROP TABLE IF EXISTS `amenities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenities` (
  `amenityId` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text,
  PRIMARY KEY (`amenityId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenities`
--

LOCK TABLES `amenities` WRITE;
/*!40000 ALTER TABLE `amenities` DISABLE KEYS */;
INSERT INTO `amenities` VALUES (1,'Swimming Pool','Olympic-sized pool with lifeguard'),(2,'Clubhouse','5000 sqft with banquet facilities'),(3,'EV Charging','Fast charging stations'),(4,'24/7 Security','CCTV and biometric access'),(5,'Gym','Fully equipped fitness center'),(6,'Childrens Play Area','Safe play area for kids'),(7,'Landscaped Garden','Beautifully maintained gardens'),(8,'Power Backup','Full power backup for common areas');
/*!40000 ALTER TABLE `amenities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apscheduler_jobs`
--

DROP TABLE IF EXISTS `apscheduler_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apscheduler_jobs` (
  `id` varchar(191) NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apscheduler_jobs`
--

LOCK TABLES `apscheduler_jobs` WRITE;
/*!40000 ALTER TABLE `apscheduler_jobs` DISABLE KEYS */;
INSERT INTO `apscheduler_jobs` VALUES ('check_saved_searches',1746742616.928598,_binary '���\0\0\0\0\0\0}�(�version�K�id��check_saved_searches��func��scheduler:check_saved_searches��trigger��apscheduler.triggers.interval��IntervalTrigger���)��}�(hK�timezone��builtins��getattr����zoneinfo��ZoneInfo����	_unpickle���R��\rAsia/Calcutta�K��R��\nstart_date��datetime��datetime���C\n\�	.8+V�h��R��end_date�N�interval�h\Z�	timedelta���K\0MK\0��R��jitter�Nub�executor��default��args�)�kwargs�}��name�h�misfire_grace_time�K�coalesce���\rmax_instances�K�\rnext_run_time�hC\n\�	.8+V�h��R�u.'),('daily_maintenance',1746826200,_binary '��\0\0\0\0\0\0}�(�version�K�id��daily_maintenance��func��maintenance:run_maintenance��trigger��apscheduler.triggers.cron��CronTrigger���)��}�(hK�timezone��builtins��getattr����zoneinfo��ZoneInfo����	_unpickle���R��\rAsia/Calcutta�K��R��\nstart_date�N�end_date�N�fields�]�(� apscheduler.triggers.cron.fields��	BaseField���)��}�(�name��year��\nis_default���expressions�]��%apscheduler.triggers.cron.expressions��\rAllExpression���)��}��step�Nsbaubh�\nMonthField���)��}�(h\"�month�h$�h%]�h))��}�h,Nsbaubh�DayOfMonthField���)��}�(h\"�day�h$�h%]�h))��}�h,Nsbaubh�	WeekField���)��}�(h\"�week�h$�h%]�h))��}�h,Nsbaubh�DayOfWeekField���)��}�(h\"�day_of_week�h$�h%]�h))��}�h,Nsbaubh)��}�(h\"�hour�h$�h%]�h\'�RangeExpression���)��}�(h,N�first�K�last�Kubaubh)��}�(h\"�minute�h$�h%]�hR)��}�(h,NhUK\0hVK\0ubaubh)��}�(h\"�second�h$�h%]�hR)��}�(h,NhUK\0hVK\0ubaube�jitter�Nub�executor��default��args�)�kwargs�}�h\"�run_maintenance��misfire_grace_time�K�coalesce���\rmax_instances�K�\rnext_run_time��datetime��datetime���C\n\�\n\0\0\0\0\0�h��R�u.');
/*!40000 ALTER TABLE `apscheduler_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buyer`
--

DROP TABLE IF EXISTS `buyer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buyer` (
  `buyerId` int NOT NULL,
  `userId` int NOT NULL,
  `minBudget` decimal(12,2) DEFAULT NULL,
  `maxBudget` decimal(12,2) DEFAULT NULL,
  `preferredLocations` text,
  PRIMARY KEY (`buyerId`),
  UNIQUE KEY `userId` (`userId`),
  CONSTRAINT `buyer_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
  CONSTRAINT `buyer_chk_1` CHECK ((`minBudget` >= 0)),
  CONSTRAINT `buyer_chk_2` CHECK ((`maxBudget` >= `minBudget`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buyer`
--

LOCK TABLES `buyer` WRITE;
/*!40000 ALTER TABLE `buyer` DISABLE KEYS */;
INSERT INTO `buyer` VALUES (301,3,5000000.00,150000000.00,'Mumbai,Bangalore'),(302,9,10000000.00,100000000.00,'Gurgaon,Noida,Hyderabad');
/*!40000 ALTER TABLE `buyer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commercialproperty`
--

DROP TABLE IF EXISTS `commercialproperty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commercialproperty` (
  `propertyId` int NOT NULL,
  `businessType` varchar(30) NOT NULL,
  `floor` int NOT NULL,
  `parkingSlots` int NOT NULL,
  PRIMARY KEY (`propertyId`),
  CONSTRAINT `commercialproperty_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `commercialproperty_chk_1` CHECK ((`parkingSlots` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commercialproperty`
--

LOCK TABLES `commercialproperty` WRITE;
/*!40000 ALTER TABLE `commercialproperty` DISABLE KEYS */;
INSERT INTO `commercialproperty` VALUES (5002,'IT Office',15,50),(5004,'Co-working',5,20),(5006,'Retail',2,150),(5007,'Tech Park',10,100),(5010,'Showroom',1,10);
/*!40000 ALTER TABLE `commercialproperty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contactmessages`
--

DROP TABLE IF EXISTS `contactmessages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactmessages` (
  `messageId` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `message` text NOT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('New','Read','Responded') DEFAULT 'New',
  PRIMARY KEY (`messageId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactmessages`
--

LOCK TABLES `contactmessages` WRITE;
/*!40000 ALTER TABLE `contactmessages` DISABLE KEYS */;
/*!40000 ALTER TABLE `contactmessages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `userId` int NOT NULL,
  `propertyId` int NOT NULL,
  `addedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`userId`,`propertyId`),
  KEY `propertyId` (`propertyId`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (3,5003,'2023-09-20 11:45:00'),(3,5008,'2023-10-05 09:15:00'),(6,5002,'2023-11-15 12:00:00'),(9,5005,'2023-07-10 14:20:00'),(9,5007,'2023-08-25 16:30:00');
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `indianidentity`
--

DROP TABLE IF EXISTS `indianidentity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `indianidentity` (
  `identityId` int NOT NULL,
  `userId` int NOT NULL,
  `aadhaarNumber` char(12) DEFAULT NULL,
  `panNumber` char(10) DEFAULT NULL,
  PRIMARY KEY (`identityId`),
  UNIQUE KEY `aadhaarNumber` (`aadhaarNumber`),
  UNIQUE KEY `panNumber` (`panNumber`),
  KEY `userId` (`userId`),
  CONSTRAINT `indianidentity_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
  CONSTRAINT `indianidentity_chk_1` CHECK ((length(`aadhaarNumber`) = 12)),
  CONSTRAINT `indianidentity_chk_2` CHECK ((length(`panNumber`) = 10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indianidentity`
--

LOCK TABLES `indianidentity` WRITE;
/*!40000 ALTER TABLE `indianidentity` DISABLE KEYS */;
INSERT INTO `indianidentity` VALUES (101,2,'123412341234','ABCTY1234D'),(102,4,'567856785678','XYZZY5678X'),(103,3,'901290129012','PQRST9012U'),(104,9,'345634563456','NCRTY3456M'),(105,10,'789078907890','HYDER7890A'),(106,5,'234523452345','MHREA5678X'),(107,6,'678967896789','TENAN9012U'),(108,7,'012301230123','LEGAL3456M'),(109,8,'456745674567','TAXCO7890A'),(110,1,'890189018901','ADMIN1234D');
/*!40000 ALTER TABLE `indianidentity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `indianlocation`
--

DROP TABLE IF EXISTS `indianlocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `indianlocation` (
  `locationId` int NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `pincode` char(6) DEFAULT NULL,
  `reraZone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`locationId`),
  UNIQUE KEY `city` (`city`,`state`,`pincode`),
  CONSTRAINT `indianlocation_chk_1` CHECK ((length(`pincode`) = 6))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `indianlocation`
--

LOCK TABLES `indianlocation` WRITE;
/*!40000 ALTER TABLE `indianlocation` DISABLE KEYS */;
INSERT INTO `indianlocation` VALUES (1001,'Mumbai','Maharashtra','400001','MahaRERA Zone 1'),(1002,'Bangalore','Karnataka','560001','Karnataka RERA'),(1003,'Gurgaon','Haryana','122001','HRERA Gurugram'),(1004,'Hyderabad','Telangana','500001','TSRERA Hyderabad'),(1005,'Pune','Maharashtra','411001','MahaRERA Zone 2'),(1006,'Noida','Uttar Pradesh','201301','UP RERA NCR'),(1007,'Chennai','Tamil Nadu','600001','TNRERA Chennai'),(1008,'Kolkata','West Bengal','700001','West Bengal RERA');
/*!40000 ALTER TABLE `indianlocation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listing`
--

DROP TABLE IF EXISTS `listing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listing` (
  `listingId` int NOT NULL,
  `propertyId` int NOT NULL,
  `agentId` int DEFAULT NULL,
  `listPrice` decimal(12,2) NOT NULL,
  `bookingAmount` decimal(12,2) DEFAULT NULL,
  `maintenanceCharges` decimal(12,2) DEFAULT NULL,
  `availableFrom` date NOT NULL,
  `isActive` tinyint(1) DEFAULT '1',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`listingId`),
  KEY `propertyId` (`propertyId`),
  KEY `agentId` (`agentId`),
  CONSTRAINT `listing_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `listing_ibfk_2` FOREIGN KEY (`agentId`) REFERENCES `agent` (`agentId`),
  CONSTRAINT `listing_chk_1` CHECK ((`listPrice` > 0)),
  CONSTRAINT `listing_chk_2` CHECK ((`bookingAmount` >= 0)),
  CONSTRAINT `listing_chk_3` CHECK ((`maintenanceCharges` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing`
--

LOCK TABLES `listing` WRITE;
/*!40000 ALTER TABLE `listing` DISABLE KEYS */;
INSERT INTO `listing` VALUES (3002,5005,202,55000000.00,1000000.00,NULL,'2023-07-15',1,'2025-04-29 04:52:52'),(3003,5007,203,70000000.00,NULL,50000.00,'2023-08-01',1,'2025-04-29 04:52:52'),(3004,5003,201,100000000.00,750000.00,20000.00,'2023-09-01',1,'2025-04-29 04:52:52'),(3005,5009,202,27500000.00,250000.00,NULL,'2023-10-01',1,'2025-04-29 04:52:52');
/*!40000 ALTER TABLE `listing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance`
--

DROP TABLE IF EXISTS `maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance` (
  `requestId` int NOT NULL AUTO_INCREMENT,
  `propertyId` int NOT NULL,
  `raisedBy` int NOT NULL,
  `issueType` varchar(30) NOT NULL,
  `description` text,
  `status` varchar(20) DEFAULT 'Pending',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `resolvedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`requestId`),
  KEY `propertyId` (`propertyId`),
  KEY `raisedBy` (`raisedBy`),
  CONSTRAINT `maintenance_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `maintenance_ibfk_2` FOREIGN KEY (`raisedBy`) REFERENCES `users` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance`
--

LOCK TABLES `maintenance` WRITE;
/*!40000 ALTER TABLE `maintenance` DISABLE KEYS */;
INSERT INTO `maintenance` VALUES (2,5004,6,'Electrical','AC not working in main hall','Resolved','2025-04-29 04:52:52',NULL),(3,5008,4,'Structural','Crack in living room wall','Pending','2025-04-29 04:52:52',NULL),(4,5003,9,'Pest Control','Termite infestation noticed','Completed','2025-04-29 04:52:52',NULL),(5,5007,10,'HVAC','Central AC system not cooling properly','In Progress','2025-04-29 04:52:52',NULL);
/*!40000 ALTER TABLE `maintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nearbyamenities`
--

DROP TABLE IF EXISTS `nearbyamenities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nearbyamenities` (
  `amenityId` int NOT NULL AUTO_INCREMENT,
  `propertyId` int NOT NULL,
  `category` enum('Education','Healthcare','Shopping','Transportation') NOT NULL,
  `name` varchar(100) NOT NULL,
  `distance` float NOT NULL,
  PRIMARY KEY (`amenityId`),
  KEY `propertyId` (`propertyId`),
  CONSTRAINT `nearbyamenities_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nearbyamenities`
--

LOCK TABLES `nearbyamenities` WRITE;
/*!40000 ALTER TABLE `nearbyamenities` DISABLE KEYS */;
/*!40000 ALTER TABLE `nearbyamenities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notificationId` int NOT NULL AUTO_INCREMENT,
  `userId` int NOT NULL,
  `message` text NOT NULL,
  `type` varchar(50) NOT NULL,
  `relatedId` int DEFAULT NULL,
  `isRead` tinyint(1) DEFAULT NULL,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `title` varchar(100) NOT NULL DEFAULT 'Notification',
  PRIMARY KEY (`notificationId`),
  KEY `idx_notifications_user_date` (`userId`,`createdAt` DESC),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performancemetrics`
--

DROP TABLE IF EXISTS `performancemetrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `performancemetrics` (
  `metricId` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `avgResponseTime` decimal(10,2) DEFAULT NULL,
  `searchesPerMinute` int DEFAULT NULL,
  `errorsPerMinute` int DEFAULT NULL,
  `activeUsers` int DEFAULT NULL,
  `cpuUsage` decimal(5,2) DEFAULT NULL,
  `memoryUsage` decimal(5,2) DEFAULT NULL,
  `alertSent` tinyint(1) DEFAULT '0',
  `alertType` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`metricId`),
  KEY `idx_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performancemetrics`
--

LOCK TABLES `performancemetrics` WRITE;
/*!40000 ALTER TABLE `performancemetrics` DISABLE KEYS */;
/*!40000 ALTER TABLE `performancemetrics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property` (
  `propertyId` int NOT NULL AUTO_INCREMENT,
  `address` text NOT NULL,
  `ownerId` int NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `carpetArea` int NOT NULL,
  `typeId` int NOT NULL,
  `locationId` int NOT NULL,
  `reraRegistered` tinyint(1) DEFAULT '0',
  `isActive` tinyint(1) DEFAULT '1',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `furnishingType` enum('Unfurnished','Semi-Furnished','Fully Furnished') DEFAULT 'Unfurnished',
  `propertyAge` varchar(20) DEFAULT 'New',
  `ownershipType` enum('Freehold','Leasehold') DEFAULT 'Freehold',
  `listingType` enum('Buy','Sell','Rent','New Projects') DEFAULT 'Sell',
  `propertyCategory` enum('Residential','Commercial','Agricultural') DEFAULT 'Residential',
  `maintenanceCharge` decimal(12,2) DEFAULT NULL,
  `totalFloors` int DEFAULT NULL,
  `floorNumber` int DEFAULT NULL,
  `waterSupply` enum('24/7','Fixed Time','Borewell','Municipal') DEFAULT '24/7',
  `facing` enum('North','South','East','West','North-East','North-West','South-East','South-West') DEFAULT NULL,
  `overlooking` varchar(100) DEFAULT NULL,
  `powerBackup` enum('None','Partial','Full') DEFAULT 'None',
  `description` text,
  `isFeatured` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`propertyId`),
  KEY `typeId` (`typeId`),
  KEY `locationId` (`locationId`),
  KEY `ownerId` (`ownerId`),
  CONSTRAINT `property_ibfk_1` FOREIGN KEY (`typeId`) REFERENCES `propertytype` (`typeId`),
  CONSTRAINT `property_ibfk_2` FOREIGN KEY (`locationId`) REFERENCES `indianlocation` (`locationId`),
  CONSTRAINT `property_ibfk_3` FOREIGN KEY (`ownerId`) REFERENCES `users` (`userId`),
  CONSTRAINT `property_chk_1` CHECK ((`price` > 0)),
  CONSTRAINT `property_chk_2` CHECK ((`carpetArea` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=5014 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property`
--

LOCK TABLES `property` WRITE;
/*!40000 ALTER TABLE `property` DISABLE KEYS */;
INSERT INTO `property` VALUES (5001,'Sea View Apartment, Worli',4,125000000.00,1800,1,1001,1,1,'2025-05-02 02:19:23',NULL,NULL,'Unfurnished','New','Freehold','Sell','Residential',NULL,NULL,NULL,'24/7',NULL,NULL,'None',NULL,0),(5002,'test3',10,80000000.00,54126,1,1001,0,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Buy','Residential',41265.00,NULL,NULL,'24/7','North','','None','',0),(5003,'Tech Villa, Whitefield',4,97500000.00,4500,2,1002,1,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Sell','Residential',NULL,NULL,NULL,'24/7',NULL,NULL,'None',NULL,0),(5004,'Startup Office, Koramangala',10,32000000.00,5454,1,1001,0,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Buy','Residential',NULL,NULL,NULL,'24/7','North','','None','',0),(5005,'Farmhouse, Sohna Road',9,50000000.00,10000,3,1003,1,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Sell','Residential',NULL,NULL,NULL,'24/7',NULL,NULL,'None',NULL,0),(5006,'Retail Space, DLF Mall',4,120000000.00,3000,5,1006,1,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Sell','Residential',NULL,NULL,NULL,'24/7',NULL,NULL,'None',NULL,0),(5007,'HITEC City Office Tower',10,67000000.00,5698566,1,1004,0,1,'2025-04-29 04:52:52',17.404,78.4668,'Unfurnished','New','Freehold','Buy','Residential',NULL,NULL,NULL,'24/7','North','','None','',0),(5008,'Banjara Hills Villa',4,180000000.00,8000,2,1004,1,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Sell','Residential',NULL,NULL,NULL,'24/7',NULL,NULL,'None',NULL,0),(5009,'Residential Plot, Wakad',9,25000000.00,5000,7,1005,1,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Sell','Residential',NULL,NULL,NULL,'24/7',NULL,NULL,'None',NULL,0),(5010,'Commercial Showroom, Hinjewadi',10,45000000.00,654123654,1,1001,0,1,'2025-04-29 04:52:52',NULL,NULL,'Unfurnished','New','Freehold','Buy','Residential',NULL,NULL,NULL,'24/7','North','','None','',0),(5012,'feghfjklfsdghjkl;ghfjkl;\'',10,23456789.00,5786,4,1002,1,1,'2025-06-04 22:36:46',12.9356,77.519,'Unfurnished','5-10 years','Leasehold','New Projects','Commercial',345678.00,34,4,'24/7','North-West','','None','',0),(5013,'dfghjkl;\'',10,23456789.00,456,1,1001,0,1,'2025-06-05 08:19:13',NULL,NULL,'Unfurnished','New','Freehold','Buy','Residential',NULL,NULL,NULL,'24/7','North','','Full','dsfghjkl;',0);
/*!40000 ALTER TABLE `property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertyamenities`
--

DROP TABLE IF EXISTS `propertyamenities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertyamenities` (
  `propertyId` int NOT NULL,
  `amenityId` int NOT NULL,
  PRIMARY KEY (`propertyId`,`amenityId`),
  KEY `amenityId` (`amenityId`),
  CONSTRAINT `propertyamenities_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `propertyamenities_ibfk_2` FOREIGN KEY (`amenityId`) REFERENCES `amenities` (`amenityId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertyamenities`
--

LOCK TABLES `propertyamenities` WRITE;
/*!40000 ALTER TABLE `propertyamenities` DISABLE KEYS */;
INSERT INTO `propertyamenities` VALUES (5003,1),(5008,1),(5012,1),(5013,1),(5003,2),(5008,2),(5012,2),(5013,2),(5003,3),(5005,3),(5008,3),(5012,3),(5008,4),(5012,4),(5008,5),(5012,5),(5012,6),(5013,6),(5003,7),(5005,7),(5008,7),(5012,7),(5003,8),(5005,8),(5008,8),(5012,8);
/*!40000 ALTER TABLE `propertyamenities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertyconfiguration`
--

DROP TABLE IF EXISTS `propertyconfiguration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertyconfiguration` (
  `configId` int NOT NULL,
  `typeId` int NOT NULL,
  `configName` varchar(30) NOT NULL,
  PRIMARY KEY (`configId`),
  KEY `typeId` (`typeId`),
  CONSTRAINT `propertyconfiguration_ibfk_1` FOREIGN KEY (`typeId`) REFERENCES `propertytype` (`typeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertyconfiguration`
--

LOCK TABLES `propertyconfiguration` WRITE;
/*!40000 ALTER TABLE `propertyconfiguration` DISABLE KEYS */;
INSERT INTO `propertyconfiguration` VALUES (101,1,'1BHK'),(102,1,'2BHK'),(103,1,'3BHK'),(104,2,'3BHK'),(105,2,'4BHK'),(106,2,'5BHK'),(107,4,'Small Office'),(108,4,'Medium Office'),(109,4,'Large Office'),(110,5,'Small Shop'),(111,5,'Medium Shop'),(112,5,'Large Shop');
/*!40000 ALTER TABLE `propertyconfiguration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertydocuments`
--

DROP TABLE IF EXISTS `propertydocuments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertydocuments` (
  `docId` int NOT NULL,
  `propertyId` int NOT NULL,
  `docType` varchar(30) NOT NULL,
  `docNumber` varchar(50) NOT NULL,
  `issueDate` date NOT NULL,
  `issuingAuthority` varchar(50) NOT NULL,
  `filePath` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`docId`),
  KEY `propertyId` (`propertyId`),
  CONSTRAINT `propertydocuments_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertydocuments`
--

LOCK TABLES `propertydocuments` WRITE;
/*!40000 ALTER TABLE `propertydocuments` DISABLE KEYS */;
INSERT INTO `propertydocuments` VALUES (402,5005,'GPA','GPA/HR/456/2023','2023-03-20','Gurgaon SDM','/docs/5005/gpa.pdf'),(403,5007,'Khata','TS/KHATA/789','2023-05-01','GHMC Hyderabad','/docs/5007/khata.pdf'),(404,5003,'Sale Deed','SD/KA/2023/567','2023-02-10','Bangalore Registrar','/docs/5003/sale_deed.pdf'),(405,5009,'Title Deed','TD/MH/2023/890','2023-04-05','Pune Registrar','/docs/5009/title_deed.pdf');
/*!40000 ALTER TABLE `propertydocuments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertyimages`
--

DROP TABLE IF EXISTS `propertyimages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertyimages` (
  `imageId` int NOT NULL AUTO_INCREMENT,
  `propertyId` int NOT NULL,
  `imageURL` varchar(255) NOT NULL,
  `isPrimary` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`imageId`),
  KEY `propertyId` (`propertyId`),
  CONSTRAINT `propertyimages_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertyimages`
--

LOCK TABLES `propertyimages` WRITE;
/*!40000 ALTER TABLE `propertyimages` DISABLE KEYS */;
INSERT INTO `propertyimages` VALUES (4,5003,'/static/images/properties/5003/1.jpg',1),(5,5003,'/static/images/properties/5003/2.jpg',0),(6,5005,'/static/images/properties/5005/1.jpg',1),(7,5007,'/static/images/properties/5007/1.jpg',1),(8,5008,'/static/images/properties/5008/1.jpg',1),(9,5009,'/static/images/properties/5009/1.jpg',1),(10,5010,'/static/images/properties/5010/1.jpg',1),(11,5002,'/static/images/properties/5002/1.jpg',1),(12,5004,'/static/images/properties/5004/1.jpg',1),(13,5001,'/static/images/properties/5001/1.jpg',1),(14,5001,'/static/images/properties/5001/2.jpg',0),(15,5001,'/static/images/properties/5001/3.jpg',0),(16,5001,'/static/images/properties/5001/4.jpg',0),(17,5001,'/static/images/properties/5001/gym3.png',0),(18,5001,'/static/images/properties/5001/parking.png',0),(19,5001,'/static/images/properties/5001/security4.png',0),(20,5001,'/static/images/properties/5001/swimming-pool2.png',0),(21,5002,'/static/images/properties/5002/2.jpg',0),(22,5002,'/static/images/properties/5002/3.jpg',0),(23,5002,'/static/images/properties/5002/4.jpg',0),(24,5003,'/static/images/properties/5003/2.jpg',0),(25,5003,'/static/images/properties/5003/3.jpg',0),(26,5003,'/static/images/properties/5003/4.jpg',0),(27,5003,'/static/images/properties/5003/5.jpg',0),(28,5003,'/static/images/properties/5003/6.jpg',0),(29,5003,'/static/images/properties/5003/7.jpg',0),(30,5003,'/static/images/properties/5003/8.jpg',0),(31,5003,'/static/images/properties/5003/9.jpg',0),(32,5004,'/static/images/properties/5004/2.jpg',0),(33,5004,'/static/images/properties/5004/3.jpg',0),(34,5004,'/static/images/properties/5004/4.jpg',0),(35,5004,'/static/images/properties/5004/5.jpg',0),(36,5004,'/static/images/properties/5004/6.jpg',0),(37,5004,'/static/images/properties/5004/7.jpg',0),(38,5004,'/static/images/properties/5004/8.jpg',0),(39,5005,'/static/images/properties/5005/2.jpg',0),(40,5005,'/static/images/properties/5005/3.jpg',0),(41,5005,'/static/images/properties/5005/4.jpg',0),(42,5005,'/static/images/properties/5005/5.jpg',0),(43,5006,'/static/images/properties/5006/1.jpg',1),(44,5006,'/static/images/properties/5006/2.jpg',0),(45,5007,'/static/images/properties/5007/2.jpg',0),(46,5007,'/static/images/properties/5007/3.jpg',0),(47,5007,'/static/images/properties/5007/4.jpg',0),(48,5007,'/static/images/properties/5007/5.jpg',0),(49,5007,'/static/images/properties/5007/6.jpg',0),(50,5007,'/static/images/properties/5007/7.jpg',0),(51,5008,'/static/images/properties/5008/2.jpg',0),(52,5008,'/static/images/properties/5008/3.jpg',0),(53,5008,'/static/images/properties/5008/4.jpg',0),(54,5008,'/static/images/properties/5008/5.jpg',0),(55,5008,'/static/images/properties/5008/6.jpg',0),(56,5010,'/static/images/properties/5010/2.jpg',0),(57,5010,'/static/images/properties/5010/3.jpg',0);
/*!40000 ALTER TABLE `propertyimages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertytax`
--

DROP TABLE IF EXISTS `propertytax`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertytax` (
  `taxId` int NOT NULL,
  `propertyId` int NOT NULL,
  `financialYear` varchar(9) NOT NULL,
  `taxAmount` decimal(12,2) NOT NULL,
  `dueDate` date NOT NULL,
  `paid` tinyint(1) DEFAULT '0',
  `paymentDate` date DEFAULT NULL,
  PRIMARY KEY (`taxId`),
  KEY `propertyId` (`propertyId`),
  CONSTRAINT `propertytax_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `propertytax_chk_1` CHECK ((`taxAmount` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertytax`
--

LOCK TABLES `propertytax` WRITE;
/*!40000 ALTER TABLE `propertytax` DISABLE KEYS */;
INSERT INTO `propertytax` VALUES (8002,5005,'2023-24',150000.00,'2023-12-31',0,NULL),(8003,5007,'2023-24',420000.00,'2024-03-31',1,'2024-03-15'),(8004,5003,'2023-24',195000.00,'2023-12-31',1,'2023-12-20'),(8005,5008,'2023-24',350000.00,'2023-12-31',1,'2023-12-10');
/*!40000 ALTER TABLE `propertytax` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertytype`
--

DROP TABLE IF EXISTS `propertytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertytype` (
  `typeId` int NOT NULL,
  `typeName` varchar(30) NOT NULL,
  PRIMARY KEY (`typeId`),
  UNIQUE KEY `typeName` (`typeName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertytype`
--

LOCK TABLES `propertytype` WRITE;
/*!40000 ALTER TABLE `propertytype` DISABLE KEYS */;
INSERT INTO `propertytype` VALUES (1,'Apartment'),(4,'Commercial Office'),(3,'Farm House'),(6,'Industrial Warehouse'),(7,'Plot'),(5,'Retail Shop'),(2,'Villa');
/*!40000 ALTER TABLE `propertytype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rentalagreement`
--

DROP TABLE IF EXISTS `rentalagreement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rentalagreement` (
  `agreementId` int NOT NULL,
  `propertyId` int NOT NULL,
  `ownerId` int NOT NULL,
  `tenantId` int NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `monthlyRent` decimal(12,2) NOT NULL,
  `securityDeposit` decimal(12,2) NOT NULL,
  `maintenanceIncluded` tinyint(1) DEFAULT '0',
  `status` varchar(20) DEFAULT 'Active',
  PRIMARY KEY (`agreementId`),
  KEY `propertyId` (`propertyId`),
  KEY `ownerId` (`ownerId`),
  KEY `tenantId` (`tenantId`),
  CONSTRAINT `rentalagreement_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `rentalagreement_ibfk_2` FOREIGN KEY (`ownerId`) REFERENCES `users` (`userId`),
  CONSTRAINT `rentalagreement_ibfk_3` FOREIGN KEY (`tenantId`) REFERENCES `users` (`userId`),
  CONSTRAINT `rentalagreement_chk_1` CHECK ((`endDate` > `startDate`)),
  CONSTRAINT `rentalagreement_chk_2` CHECK ((`monthlyRent` > 0)),
  CONSTRAINT `rentalagreement_chk_3` CHECK ((`securityDeposit` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rentalagreement`
--

LOCK TABLES `rentalagreement` WRITE;
/*!40000 ALTER TABLE `rentalagreement` DISABLE KEYS */;
INSERT INTO `rentalagreement` VALUES (7001,5004,10,6,'2023-11-01','2024-10-31',450000.00,2000000.00,1,'Active'),(7002,5002,4,9,'2023-12-01','2024-11-30',1200000.00,5000000.00,0,'Active'),(7003,5006,4,3,'2024-01-15','2024-12-14',750000.00,3000000.00,1,'Active');
/*!40000 ALTER TABLE `rentalagreement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `residentialproperty`
--

DROP TABLE IF EXISTS `residentialproperty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `residentialproperty` (
  `propertyId` int NOT NULL,
  `bedrooms` int NOT NULL,
  `bathrooms` int NOT NULL,
  `floor` int NOT NULL,
  `totalFloors` int NOT NULL,
  `vaastuCompliant` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`propertyId`),
  CONSTRAINT `residentialproperty_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `residentialproperty_chk_1` CHECK ((`bedrooms` > 0)),
  CONSTRAINT `residentialproperty_chk_2` CHECK ((`bathrooms` > 0)),
  CONSTRAINT `residentialproperty_chk_3` CHECK ((`totalFloors` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `residentialproperty`
--

LOCK TABLES `residentialproperty` WRITE;
/*!40000 ALTER TABLE `residentialproperty` DISABLE KEYS */;
INSERT INTO `residentialproperty` VALUES (5003,4,4,1,3,1),(5008,5,5,2,3,0);
/*!40000 ALTER TABLE `residentialproperty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `savedsearch`
--

DROP TABLE IF EXISTS `savedsearch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `savedsearch` (
  `searchId` int NOT NULL AUTO_INCREMENT,
  `userId` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `criteria` json NOT NULL,
  `notifyEmail` tinyint(1) DEFAULT NULL,
  `notifySMS` tinyint(1) DEFAULT NULL,
  `frequency` enum('Daily','Weekly','Monthly') DEFAULT NULL,
  `lastNotified` datetime DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  PRIMARY KEY (`searchId`),
  KEY `userId` (`userId`),
  CONSTRAINT `savedsearch_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `savedsearch`
--

LOCK TABLES `savedsearch` WRITE;
/*!40000 ALTER TABLE `savedsearch` DISABLE KEYS */;
/*!40000 ALTER TABLE `savedsearch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `searchanalytics`
--

DROP TABLE IF EXISTS `searchanalytics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `searchanalytics` (
  `searchId` int NOT NULL AUTO_INCREMENT,
  `userId` int DEFAULT NULL,
  `searchTimestamp` datetime NOT NULL,
  `city` varchar(30) DEFAULT NULL,
  `propertyType` varchar(30) DEFAULT NULL,
  `minPrice` decimal(12,2) DEFAULT NULL,
  `maxPrice` decimal(12,2) DEFAULT NULL,
  `minArea` int DEFAULT NULL,
  `maxArea` int DEFAULT NULL,
  `bedrooms` int DEFAULT NULL,
  `bathrooms` int DEFAULT NULL,
  `furnishingType` varchar(20) DEFAULT NULL,
  `propertyAge` varchar(20) DEFAULT NULL,
  `ownershipType` varchar(20) DEFAULT NULL,
  `listingType` varchar(20) DEFAULT NULL,
  `ipAddress` varchar(45) DEFAULT NULL,
  `userAgent` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`searchId`),
  KEY `userId` (`userId`),
  CONSTRAINT `searchanalytics_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `searchanalytics`
--

LOCK TABLES `searchanalytics` WRITE;
/*!40000 ALTER TABLE `searchanalytics` DISABLE KEYS */;
/*!40000 ALTER TABLE `searchanalytics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `transactionId` int NOT NULL,
  `propertyId` int NOT NULL,
  `buyerId` int NOT NULL,
  `sellerId` int NOT NULL,
  `agentId` int DEFAULT NULL,
  `transactionDate` date NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `stampDuty` decimal(12,2) NOT NULL,
  `registrationCharges` decimal(12,2) NOT NULL,
  `paymentMethod` varchar(20) NOT NULL,
  `status` varchar(20) DEFAULT 'Completed',
  PRIMARY KEY (`transactionId`),
  KEY `propertyId` (`propertyId`),
  KEY `buyerId` (`buyerId`),
  KEY `sellerId` (`sellerId`),
  KEY `agentId` (`agentId`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`buyerId`) REFERENCES `users` (`userId`),
  CONSTRAINT `transaction_ibfk_3` FOREIGN KEY (`sellerId`) REFERENCES `users` (`userId`),
  CONSTRAINT `transaction_ibfk_4` FOREIGN KEY (`agentId`) REFERENCES `agent` (`agentId`),
  CONSTRAINT `transaction_chk_1` CHECK ((`amount` > 0)),
  CONSTRAINT `transaction_chk_2` CHECK ((`stampDuty` >= 0)),
  CONSTRAINT `transaction_chk_3` CHECK ((`registrationCharges` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES (6002,5007,9,10,203,'2023-10-15',68500000.00,320000.00,120000.00,'Cheque','Completed'),(6003,5005,3,9,202,'2024-01-20',52500000.00,275000.00,95000.00,'UPI','Completed'),(6004,5003,9,4,201,'2024-02-10',95000000.00,475000.00,142500.00,'RTGS','Completed');
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdocuments`
--

DROP TABLE IF EXISTS `userdocuments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdocuments` (
  `doc_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `doc_type` varchar(50) DEFAULT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `original_filename` varchar(255) DEFAULT NULL,
  `file_size` int DEFAULT NULL,
  `mime_type` varchar(100) DEFAULT NULL,
  `upload_date` datetime DEFAULT NULL,
  `verified_by` int DEFAULT NULL,
  `verification_date` datetime DEFAULT NULL,
  `rejection_reason` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`doc_id`),
  KEY `user_id` (`user_id`),
  KEY `fk_verified_by` (`verified_by`),
  CONSTRAINT `fk_verified_by` FOREIGN KEY (`verified_by`) REFERENCES `users` (`userId`) ON DELETE SET NULL,
  CONSTRAINT `userdocuments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdocuments`
--

LOCK TABLES `userdocuments` WRITE;
/*!40000 ALTER TABLE `userdocuments` DISABLE KEYS */;
INSERT INTO `userdocuments` VALUES (1,1,'identity','static\\documents\\user_1_identity_20250605054934_Screenshot_2025-06-05_052440.png','2025-06-05 05:49:34',0,'Screenshot 2025-06-05 052440.png',62967,'image/png','2025-06-05 05:49:35',1,'2025-06-05 00:52:31','Hello ');
/*!40000 ALTER TABLE `userdocuments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userrole`
--

DROP TABLE IF EXISTS `userrole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userrole` (
  `roleId` int NOT NULL AUTO_INCREMENT,
  `roleName` varchar(50) NOT NULL,
  PRIMARY KEY (`roleId`),
  UNIQUE KEY `roleName` (`roleName`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userrole`
--

LOCK TABLES `userrole` WRITE;
/*!40000 ALTER TABLE `userrole` DISABLE KEYS */;
INSERT INTO `userrole` VALUES (1,'Admin'),(2,'Agent'),(3,'Buyer'),(6,'Legal Officer'),(8,'Property Manager'),(4,'Seller'),(7,'Tax Consultant'),(5,'Tenant'),(10,'test');
/*!40000 ALTER TABLE `userrole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` char(10) DEFAULT NULL,
  `roleId` int NOT NULL,
  `isActive` tinyint(1) DEFAULT '1',
  `isBanned` tinyint(1) DEFAULT '0',
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `email_notifications` tinyint(1) DEFAULT '1',
  `sms_notifications` tinyint(1) DEFAULT '0',
  `marketing_emails` tinyint(1) DEFAULT '1',
  `loginAttempts` int DEFAULT '0',
  `lastLoginAttempt` datetime DEFAULT NULL,
  `lastPasswordChange` datetime DEFAULT NULL,
  `passwordResetToken` varchar(100) DEFAULT NULL,
  `passwordResetExpires` datetime DEFAULT NULL,
  `lastLogin` datetime DEFAULT NULL,
  `lastLoginIP` varchar(45) DEFAULT NULL,
  `twoFactorEnabled` tinyint(1) DEFAULT '0',
  `twoFactorSecret` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `passwordResetToken` (`passwordResetToken`),
  KEY `roleId` (`roleId`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`roleId`) REFERENCES `userrole` (`roleId`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin_mumbai','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','admin@realestate.com','9820123456',1,1,0,'2025-04-29 04:52:52','2025-06-05 06:12:07',1,0,1,0,'2025-06-05 00:42:07',NULL,NULL,NULL,'2025-06-05 00:42:07','127.0.0.1',0,NULL),(2,'rahul','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','rahul@metrobrokers.com','9876543210',2,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(3,'priya_buyer','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','priya.sharma@email.com','8888877777',3,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(4,'singh_properties','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','singh.properties@email.com','7777766666',4,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(5,'mehta_brokers','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','mehta@ncrproperties.com','9999955555',2,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(6,'kumar_tenant','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','kumar.tenant@email.com','8888888888',5,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(7,'legal_ravi','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','ravi@legal.com','7777777777',6,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(8,'tax_consult','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','tax@consultant.com','6666666666',7,1,0,'2025-04-29 04:52:52','2025-06-05 06:07:53',1,0,1,0,'2025-06-05 00:37:53',NULL,NULL,NULL,'2025-06-05 00:37:54','127.0.0.1',0,NULL),(9,'ncr_investor','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','investor@ncr.com','9876509876',3,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL),(10,'hyderabad_prop','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','owner@hyderabadprop.com','9876543211',4,1,0,'2025-04-29 04:52:52','2025-06-05 08:55:03',1,0,1,0,'2025-06-05 03:25:03',NULL,NULL,NULL,'2025-06-05 03:25:03','127.0.0.1',0,NULL),(11,'property_mgr','pbkdf2:sha256:260000$oapfm5wtdyR1O6xk$055aa909e47ba8c2e3ca3116200e580c086f69b9a314093d23094398a8bfdb05','manager@realestate.com','9876543212',8,1,0,'2025-04-29 04:52:52','2025-05-23 03:37:10',1,0,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valuation`
--

DROP TABLE IF EXISTS `valuation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valuation` (
  `valuationId` int NOT NULL,
  `propertyId` int NOT NULL,
  `valuationDate` date NOT NULL,
  `marketValue` decimal(12,2) NOT NULL,
  `rentalValue` decimal(12,2) DEFAULT NULL,
  `conductedBy` varchar(50) NOT NULL,
  PRIMARY KEY (`valuationId`),
  KEY `propertyId` (`propertyId`),
  CONSTRAINT `valuation_ibfk_1` FOREIGN KEY (`propertyId`) REFERENCES `property` (`propertyId`),
  CONSTRAINT `valuation_chk_1` CHECK ((`marketValue` > 0)),
  CONSTRAINT `valuation_chk_2` CHECK ((`rentalValue` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valuation`
--

LOCK TABLES `valuation` WRITE;
/*!40000 ALTER TABLE `valuation` DISABLE KEYS */;
INSERT INTO `valuation` VALUES (10002,5007,'2023-06-20',65000000.00,420000.00,'CBRE Hyderabad'),(10003,5003,'2023-03-10',95000000.00,350000.00,'Knight Frank'),(10004,5008,'2023-07-05',175000000.00,550000.00,'Colliers International'),(10005,5005,'2023-05-15',48000000.00,150000.00,'ANAROCK');
/*!40000 ALTER TABLE `valuation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-05 12:16:18
