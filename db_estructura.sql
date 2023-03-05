CREATE SCHEMA `transito` DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci;

USE `transito`;
--
-- Table structure for table `oficial`
--

DROP TABLE IF EXISTS `oficial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oficial` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) COLLATE utf8_spanish_ci DEFAULT NULL,
  `usuario_app` varchar(60) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_app_UNIQUE` (`usuario_app`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `persona`
--

DROP TABLE IF EXISTS `persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) COLLATE utf8_spanish_ci DEFAULT NULL,
  `correo` varchar(45) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehiculo`
--

DROP TABLE IF EXISTS `vehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehiculo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `placa_patente` varchar(45) COLLATE utf8_spanish_ci DEFAULT NULL,
  `marca` varchar(60) COLLATE utf8_spanish_ci DEFAULT NULL,
  `color` varchar(60) COLLATE utf8_spanish_ci DEFAULT NULL,
  `id_persona` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `placa_patente_UNIQUE` (`placa_patente`),
  KEY `id_persona_vehiculo_idx` (`id_persona`),
  CONSTRAINT `id_persona_vehiculo` FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;



DROP TABLE IF EXISTS `infraccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `infraccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comentarios` varchar(200) COLLATE utf8_spanish_ci DEFAULT NULL,
  `fecha_creacion` timestamp(2) NULL DEFAULT NULL,
  `id_oficial` int DEFAULT NULL,
  `id_vehiculo` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_infracion_id_oficial_idx` (`id_oficial`),
  KEY `fk_infracion_id_vehiculo_idx` (`id_vehiculo`),
  CONSTRAINT `fk_infracion_id_oficial` FOREIGN KEY (`id_oficial`) REFERENCES `oficial` (`id`),
  CONSTRAINT `fk_infracion_id_vehiculo` FOREIGN KEY (`id_vehiculo`) REFERENCES `vehiculo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;