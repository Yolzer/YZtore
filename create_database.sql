CREATE DATABASE IF NOT EXISTS YZstore;
USE YZstore;

-- Otorgar permisos al usuario
GRANT ALL PRIVILEGES ON YZstore.* TO 'Yolzer'@'localhost' IDENTIFIED BY 'Yolzer.1234';
FLUSH PRIVILEGES; 