CREATE TABLE if not exists `quotes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exchange` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `pair` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `price` decimal(35,10) NOT NULL,
  `batch_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `modified_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  KEY (`exchange`),
  KEY (`pair`),
  KEY (`batch_id`),
  KEY (`created_at`),
  KEY (`modified_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE if not exists  `ranks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exchange` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `pair` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `the_rank` int DEFAULT NULL,
  `standard_deviation` decimal(35,10) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `modified_at` datetime(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY (`exchange`,`pair`),
  KEY (`exchange`),
  KEY (`pair`),
  KEY (`created_at`),
  KEY (`modified_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;