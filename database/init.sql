CREATE DATABASE IF NOT EXISTS marketplace_rates;
USE marketplace_rates;

CREATE TABLE IF NOT EXISTS marketplace_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    marketplace VARCHAR(100) NOT NULL,
    shipping FLOAT NOT NULL,
    commission FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_brand_marketplace (brand, marketplace),
    INDEX idx_brand (brand),
    INDEX idx_marketplace (marketplace)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
