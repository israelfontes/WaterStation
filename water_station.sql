-- Criação do banco de dados
CREATE DATABASE water_station;
USE water_station;

-- Tabela Authorization Level
CREATE TABLE AuthorizationLevel (
    ID BIGINT NOT NULL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Tabela Address
CREATE TABLE Address (
    ID BIGINT NOT NULL PRIMARY KEY,
    Street VARCHAR(255),
    Number VARCHAR(255),
    Neighborhood VARCHAR(255),
    State VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    Cep VARCHAR(255) NOT NULL,
    Coordinated VARCHAR(255)
);

-- Tabela Region
CREATE TABLE Region (
    ID BIGINT NOT NULL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description VARCHAR(255) NOT NULL
);

-- Tabela User
CREATE TABLE User (
    ID BIGINT NOT NULL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    AddressID BIGINT NOT NULL,
    AuthLevelID BIGINT NOT NULL,
    FOREIGN KEY (AddressID) REFERENCES Address(ID),
    FOREIGN KEY (AuthLevelID) REFERENCES AuthorizationLevel(ID)
);

-- Tabela User Region (relação N:M)
CREATE TABLE UserRegion (
    UserID BIGINT NOT NULL,
    RegionID BIGINT NOT NULL,
    PRIMARY KEY (UserID, RegionID),
    FOREIGN KEY (UserID) REFERENCES User(ID),
    FOREIGN KEY (RegionID) REFERENCES Region(ID)
);

-- Tabela Sensor
CREATE TABLE Sensor (
    ID BIGINT NOT NULL PRIMARY KEY,
    Type VARCHAR(255) NOT NULL,
    MacAddress VARCHAR(255) NOT NULL,
    MeasurementUnit VARCHAR(255) NOT NULL,
    LocationID BIGINT,
	
	ReservoirID BIGINT NULL,
    DissanilizerID BIGINT NULL,
    WaterWellID BIGINT NULL,
	
	FOREIGN KEY (ReservoirID) REFERENCES Reservoir(ID),
    FOREIGN KEY (DissanilizerID) REFERENCES Dissanilizer(ID),
    FOREIGN KEY (WaterWellID) REFERENCES WaterWell(ID)
	
	CHECK (
        (ReservoirID IS NOT NULL AND DissanilizerID IS NULL AND WaterWellID IS NULL) OR
        (ReservoirID IS NULL AND DissanilizerID IS NOT NULL AND WaterWellID IS NULL) OR
        (ReservoirID IS NULL AND DissanilizerID IS NULL AND WaterWellID IS NOT NULL)
    )
);

-- Tabela Reservoir
CREATE TABLE Reservoir (
    ID BIGINT NOT NULL PRIMARY KEY,
    Capacity INT NOT NULL,
    Type VARCHAR(255) NOT NULL,
    SensorID BIGINT NOT NULL,
    FOREIGN KEY (SensorID) REFERENCES Sensor(ID)
);

-- Tabela Dissanilizer
CREATE TABLE Dissanilizer (
    ID BIGINT NOT NULL PRIMARY KEY,
    MaxAlkalinity INT NOT NULL,
    SensorID BIGINT NOT NULL,
    FOREIGN KEY (SensorID) REFERENCES Sensor(ID)
);

-- Tabela Water Well
CREATE TABLE WaterWell (
    ID BIGINT NOT NULL PRIMARY KEY,
    MaxFlow INT NOT NULL,
    SensorID BIGINT NOT NULL,
    FOREIGN KEY (SensorID) REFERENCES Sensor(ID)
);

-- Tabela Plant
CREATE TABLE Plant (
    ID BIGINT NOT NULL PRIMARY KEY,
    Type VARCHAR(255) NOT NULL,
    AddressID BIGINT NOT NULL,
    RegionID BIGINT NOT NULL,
    ReservoirID BIGINT,
    DissanilizerID BIGINT,
    WaterWellID BIGINT,
    FOREIGN KEY (RegionID) REFERENCES Region(ID),
    FOREIGN KEY (ReservoirID) REFERENCES Reservoir(ID),
    FOREIGN KEY (DissanilizerID) REFERENCES Dissanilizer(ID),
    FOREIGN KEY (WaterWellID) REFERENCES WaterWell(ID)
);

-- Tabela Read (leituras dos sensores)
CREATE TABLE SensorRead (
    ID BIGINT NOT NULL PRIMARY KEY,
    SensorID BIGINT NOT NULL,
    Datetime VARCHAR(255) NOT NULL,
    Value VARCHAR(255) NOT NULL,
    FOREIGN KEY (SensorID) REFERENCES Sensor(ID)
);