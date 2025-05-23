-- Criação do banco de dados
CREATE DATABASE water_station;
USE water_station;

-- =================================================================
-- TABELAS BASE DO SISTEMA
-- =================================================================

-- Tabela Authorization Level
CREATE TABLE AuthorizationLevel (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL UNIQUE
);

-- Tabela Region
CREATE TABLE Region (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Description VARCHAR(255) NOT NULL
);

-- Tabela Users
CREATE TABLE Users (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL, -- Lembre-se de armazenar como hash
    AuthLevelID BIGINT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Status VARCHAR(50) DEFAULT 'ACTIVE',
    FOREIGN KEY (AuthLevelID) REFERENCES AuthorizationLevel(ID)
);

-- Tabela Address
CREATE TABLE Address (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Street VARCHAR(255),
    Number VARCHAR(255),
    Neighborhood VARCHAR(255),
    State VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    Cep VARCHAR(255) NOT NULL,
    Coordinates VARCHAR(255), -- Coordenadas do endereço do usuário (opcional)
    UserID BIGINT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(ID) ON DELETE CASCADE
);

-- Tabela User Region (relação N:M)
CREATE TABLE UserRegion (
    UserID BIGINT NOT NULL,
    RegionID BIGINT NOT NULL,
    AssignedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (UserID, RegionID),
    FOREIGN KEY (UserID) REFERENCES Users(ID) ON DELETE CASCADE,
    FOREIGN KEY (RegionID) REFERENCES Region(ID) ON DELETE CASCADE
);

-- Tabela Plant
CREATE TABLE Plant (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(255) NOT NULL,
    Name VARCHAR(255),
    AddressID BIGINT NOT NULL,
    RegionID BIGINT NOT NULL,
    Status VARCHAR(50) DEFAULT 'ACTIVE',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AddressID) REFERENCES Address(ID),
    FOREIGN KEY (RegionID) REFERENCES Region(ID),
    CONSTRAINT UQ_Plant_AddressID UNIQUE (AddressID)
);

-- =================================================================
-- SISTEMA DE COMPONENTES HÍDRICOS
-- =================================================================

-- Tabela para categorizar tipos de componentes
CREATE TABLE ComponentType (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL UNIQUE,
    TableName VARCHAR(255) NOT NULL, -- Ex: 'Reservoir', 'Dissanilizer'
    Description VARCHAR(500),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Reservoir
CREATE TABLE Reservoir (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Capacity INT NOT NULL,
    Type VARCHAR(255) NOT NULL,
    PlantID BIGINT NOT NULL,
    ComponentTypeID BIGINT NOT NULL,
    Coordinates VARCHAR(255) NOT NULL,
    Status VARCHAR(50) DEFAULT 'ACTIVE',
    InstallationDate DATE,
    LastMaintenanceDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PlantID) REFERENCES Plant(ID) ON DELETE CASCADE,
    FOREIGN KEY (ComponentTypeID) REFERENCES ComponentType(ID)
);

-- Tabela Dissanilizer
CREATE TABLE Dissanilizer (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    MaxAlkalinity INT NOT NULL,
    PlantID BIGINT NOT NULL,
    ComponentTypeID BIGINT NOT NULL,
    Coordinates VARCHAR(255) NOT NULL,
    Status VARCHAR(50) DEFAULT 'ACTIVE',
    InstallationDate DATE,
    LastMaintenanceDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PlantID) REFERENCES Plant(ID) ON DELETE CASCADE,
    FOREIGN KEY (ComponentTypeID) REFERENCES ComponentType(ID)
);

-- Tabela Water Well
CREATE TABLE WaterWell (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    MaxFlow INT NOT NULL,
    Depth DECIMAL(10,2),
    PlantID BIGINT NOT NULL,
    ComponentTypeID BIGINT NOT NULL,
    Coordinates VARCHAR(255) NOT NULL,
    Status VARCHAR(50) DEFAULT 'ACTIVE',
    InstallationDate DATE,
    LastMaintenanceDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PlantID) REFERENCES Plant(ID) ON DELETE CASCADE,
    FOREIGN KEY (ComponentTypeID) REFERENCES ComponentType(ID)
);

-- =================================================================
-- SISTEMA DE SENSORES
-- =================================================================

-- Tabela Sensor
CREATE TABLE Sensor (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(255) NOT NULL, -- Tipo de leitura do sensor (Nível, Vazão, pH)
    Name VARCHAR(255),
    Model VARCHAR(255),
    SerialNumber VARCHAR(255) UNIQUE, -- Número de série deve ser único
    Status VARCHAR(50) DEFAULT 'ACTIVE',
    InstallationDate DATE,
    CalibrationDate DATE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela intermediária para relacionamento polimórfico Sensor-Componente
CREATE TABLE SensorComponent (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    SensorID BIGINT NOT NULL,
    ComponentTypeID BIGINT NOT NULL,
    ComponentID BIGINT NOT NULL, -- ID do componente na sua respectiva tabela (Reservoir.ID, etc.)
    AssignedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (SensorID) REFERENCES Sensor(ID) ON DELETE CASCADE,
    FOREIGN KEY (ComponentTypeID) REFERENCES ComponentType(ID),
    UNIQUE (SensorID) -- Garante que um sensor só pode estar associado a um componente
);

-- Tabela Read (leituras dos sensores)
CREATE TABLE SensorRead (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    SensorID BIGINT NOT NULL,
    Datetime DATETIME NOT NULL,
    Value DECIMAL(10,2) NOT NULL,
    Unit VARCHAR(50),
    Status VARCHAR(50) DEFAULT 'VALID', -- Ex: VALID, INVALID, ESTIMATED
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (SensorID) REFERENCES Sensor(ID) ON DELETE CASCADE,
    INDEX idx_sensor_datetime (SensorID, Datetime),
    INDEX idx_datetime (Datetime)
);

-- =================================================================
-- INSERÇÃO DE DADOS INICIAIS
-- =================================================================

-- Tipos de componentes iniciais
INSERT INTO ComponentType (ID, Name, TableName, Description) VALUES 
(1, 'RESERVOIR', 'Reservoir', 'Reservatórios de armazenamento de água'),
(2, 'DISSANILIZER', 'Dissanilizer', 'Sistemas de dessalinização'),
(3, 'WATER_WELL', 'WaterWell', 'Poços de água subterrânea');

-- Níveis de autorização iniciais
INSERT INTO AuthorizationLevel (ID, Name) VALUES
(1, 'ADMIN'),
(2, 'MANAGER'),
(3, 'OPERATOR'),
(4, 'VIEWER');

-- Usuário Admin (Senha 'admin_pass')
INSERT INTO Users (Name, Email, Password, AuthLevelID, Status) 
VALUES (
    'Administrador Principal',
    'admin@waterstation.com',
    'hashed_admin_pass',
    (SELECT ID FROM AuthorizationLevel WHERE Name = 'Admin'), -- Buscando AuthLevelID pelo nome
    'ACTIVE'
);

-- Cadastro de regiões iniciais
INSERT INTO Region (Name, Description) VALUES ('Norte', 'Região Norte da área de cobertura');
INSERT INTO Region (Name, Description) VALUES ('Sul', 'Região Sul da área de cobertura');
INSERT INTO Region (Name, Description) VALUES ('Leste', 'Região Leste da área de cobertura');
INSERT INTO Region (Name, Description) VALUES ('Oeste', 'Região Oeste da área de cobertura');
INSERT INTO Region (Name, Description) VALUES ('Centro', 'Região Centro da área de cobertura');