CREATE DATABASE ClothingStore;
USE ClothingStore;

CREATE TABLE Store (
    ClothingID INT PRIMARY KEY,
    Price INT NOT NULL
);

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    State VARCHAR(50) NOT NULL,
    Age INT NOT NULL,
    GoldCustomer BOOLEAN DEFAULT FALSE
);

CREATE TABLE CustomerTransactions (
    CustomerTransactionID INT PRIMARY KEY,
    CustomerID INT,
    ClothingID INT,
    Amount INT NOT NULL,
    TotalCost INT NOT NULL,
    Date DATETIME NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID) ON DELETE CASCADE
);

CREATE TABLE StoreTransactions (
    StoreTransactionID INT PRIMARY KEY,
    ClothingID INT,
    Amount INT NOT NULL,
    TotalCost INT NOT NULL,
    Date DATETIME NOT NULL,
    FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID) ON DELETE CASCADE
);

CREATE TABLE Warehouse (
    ClothingID INT PRIMARY KEY,
    Cost INT NOT NULL,
    FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID)
);

CREATE TABLE Clothes (
    ClothingID INT PRIMARY KEY,
    Color VARCHAR(30) NOT NULL,
    Brand VARCHAR(50) NOT NULL,
    Style VARCHAR(50) NOT NULL,
    FOREIGN KEY (ClothingID) REFERENCES Store(ClothingID)
);

CREATE VIEW GoldCustomers AS
SELECT CustomerID, State, Age
FROM Customer
WHERE GoldCustomer = TRUE;

