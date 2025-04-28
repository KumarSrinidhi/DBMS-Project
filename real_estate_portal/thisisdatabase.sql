CREATE DATABASE Real_EstateManagement_System;
USE Real_EstateManagement_System;

/* Users with authentication  hello */
-- Create User Roles Table
CREATE TABLE UserRole (
    roleId INT PRIMARY KEY AUTO_INCREMENT,
    roleName VARCHAR(50) NOT NULL UNIQUE
);



-- Create Users Table
CREATE TABLE Users (
    userId INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    mobile CHAR(10) UNIQUE,
    roleId INT NOT NULL,
    isActive BOOLEAN DEFAULT TRUE,
    isBanned BOOLEAN DEFAULT FALSE,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (roleId) REFERENCES UserRole(roleId)
);

/* Indian Identity Documents */
CREATE TABLE IndianIdentity (
    identityId INT PRIMARY KEY,
    userId INT NOT NULL,
    aadhaarNumber CHAR(12) UNIQUE,
    panNumber CHAR(10) UNIQUE,
    FOREIGN KEY (userId) REFERENCES Users(userId),
    CHECK (LENGTH(aadhaarNumber) = 12),
    CHECK (LENGTH(panNumber) = 10)
);

/* Property Types */
CREATE TABLE PropertyType (
    typeId INT PRIMARY KEY,
    typeName VARCHAR(30) NOT NULL UNIQUE
);

/* Property Configurations */
CREATE TABLE PropertyConfiguration (
    configId INT PRIMARY KEY,
    typeId INT NOT NULL,
    configName VARCHAR(30) NOT NULL,
    FOREIGN KEY (typeId) REFERENCES PropertyType(typeId)
);

/* Locations with RERA zones */
CREATE TABLE IndianLocation (
    locationId INT PRIMARY KEY,
    city VARCHAR(30) NOT NULL,
    state VARCHAR(30) NOT NULL,
    pincode CHAR(6),
    reraZone VARCHAR(50),
    UNIQUE (city, state, pincode),
    CHECK (LENGTH(pincode) = 6)
);

/* Property with specifics */
CREATE TABLE Property (
    propertyId INT PRIMARY KEY,
    address TEXT NOT NULL,
    ownerId INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    carpetArea INT NOT NULL,
    typeId INT NOT NULL,
    locationId INT NOT NULL,
    reraRegistered BOOLEAN DEFAULT FALSE,
    isActive BOOLEAN DEFAULT TRUE,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (typeId) REFERENCES PropertyType(typeId),
    FOREIGN KEY (locationId) REFERENCES IndianLocation(locationId),
    FOREIGN KEY (ownerId) REFERENCES Users(userId),
    CHECK (price > 0),
    CHECK (carpetArea > 0)
);

ALTER TABLE Property
ADD COLUMN furnishingType ENUM('Unfurnished', 'Semi-Furnished', 'Fully Furnished') DEFAULT 'Unfurnished',
ADD COLUMN propertyAge VARCHAR(20) DEFAULT 'New',
ADD COLUMN ownershipType ENUM('Freehold', 'Leasehold') DEFAULT 'Freehold',
ADD COLUMN listingType ENUM('Buy', 'Sell', 'Rent', 'New Projects') DEFAULT 'Sell',
ADD COLUMN propertyCategory ENUM('Residential', 'Commercial', 'Agricultural') DEFAULT 'Residential';

/* Residential Property Details */
CREATE TABLE ResidentialProperty (
    propertyId INT PRIMARY KEY,
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    floor INT NOT NULL,
    totalFloors INT NOT NULL,
    vaastuCompliant BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    CHECK (bedrooms > 0),
    CHECK (bathrooms > 0),
    CHECK (totalFloors > 0)
);

/* Commercial Property Details */
CREATE TABLE CommercialProperty (
    propertyId INT PRIMARY KEY,
    businessType VARCHAR(30) NOT NULL,
    floor INT NOT NULL,
    parkingSlots INT NOT NULL,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    CHECK (parkingSlots >= 0)
);

/* Real Estate Agent with license */
CREATE TABLE Agent (
    agentId INT PRIMARY KEY,
    userId INT NOT NULL UNIQUE,
    licenseNumber VARCHAR(20) NOT NULL UNIQUE,
    experienceYears INT NOT NULL,
    brokerageName VARCHAR(50),
    isActive BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (userId) REFERENCES Users(userId),
    CHECK (experienceYears >= 0)
);

/* Property Listing with pricing terms */
CREATE TABLE Listing (
    listingId INT PRIMARY KEY,
    propertyId INT NOT NULL,
    agentId INT,
    listPrice DECIMAL(12,2) NOT NULL,
    bookingAmount DECIMAL(12,2),
    maintenanceCharges DECIMAL(12,2),
    availableFrom DATE NOT NULL,
    isActive BOOLEAN DEFAULT TRUE,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    FOREIGN KEY (agentId) REFERENCES Agent(agentId),
    CHECK (listPrice > 0),
    CHECK (bookingAmount >= 0),
    CHECK (maintenanceCharges >= 0)
);

/* Property Documents */
CREATE TABLE PropertyDocuments (
    docId INT PRIMARY KEY,
    propertyId INT NOT NULL,
    docType VARCHAR(30) NOT NULL,
    docNumber VARCHAR(50) NOT NULL,
    issueDate DATE NOT NULL,
    issuingAuthority VARCHAR(50) NOT NULL,
    filePath VARCHAR(255),
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId)
);

/* Property Images */
CREATE TABLE PropertyImages (
    imageId INT PRIMARY KEY AUTO_INCREMENT,
    propertyId INT NOT NULL,
    imageURL VARCHAR(255) NOT NULL,
    isPrimary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId)
);

/* Buyer Preferences */
CREATE TABLE Buyer (
    buyerId INT PRIMARY KEY,
    userId INT NOT NULL UNIQUE,
    minBudget DECIMAL(12,2),
    maxBudget DECIMAL(12,2),
    preferredLocations TEXT,
    FOREIGN KEY (userId) REFERENCES Users(userId),
    CHECK (minBudget >= 0),
    CHECK (maxBudget >= minBudget)
);

/* Property Transaction */
CREATE TABLE Transaction (
    transactionId INT PRIMARY KEY,
    propertyId INT NOT NULL,
    buyerId INT NOT NULL,
    sellerId INT NOT NULL,
    agentId INT,
    transactionDate DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    stampDuty DECIMAL(12,2) NOT NULL,
    registrationCharges DECIMAL(12,2) NOT NULL,
    paymentMethod VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Completed',
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    FOREIGN KEY (buyerId) REFERENCES Users(userId),
    FOREIGN KEY (sellerId) REFERENCES Users(userId),
    FOREIGN KEY (agentId) REFERENCES Agent(agentId),
    CHECK (amount > 0),
    CHECK (stampDuty >= 0),
    CHECK (registrationCharges >= 0)
);

/* Rental Agreement */
CREATE TABLE RentalAgreement (
    agreementId INT PRIMARY KEY,
    propertyId INT NOT NULL,
    ownerId INT NOT NULL,
    tenantId INT NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    monthlyRent DECIMAL(12,2) NOT NULL,
    securityDeposit DECIMAL(12,2) NOT NULL,
    maintenanceIncluded BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    FOREIGN KEY (ownerId) REFERENCES Users(userId),
    FOREIGN KEY (tenantId) REFERENCES Users(userId),
    CHECK (endDate > startDate),
    CHECK (monthlyRent > 0),
    CHECK (securityDeposit >= 0)
);

/* Property Tax */
CREATE TABLE PropertyTax (
    taxId INT PRIMARY KEY,
    propertyId INT NOT NULL,
    financialYear VARCHAR(9) NOT NULL,
    taxAmount DECIMAL(12,2) NOT NULL,
    dueDate DATE NOT NULL,
    paid BOOLEAN DEFAULT FALSE,
    paymentDate DATE,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    CHECK (taxAmount > 0)
);

/* Maintenance Requests */
CREATE TABLE Maintenance (
    requestId INT PRIMARY KEY AUTO_INCREMENT,
    propertyId INT NOT NULL,
    raisedBy INT NOT NULL,
    issueType VARCHAR(30) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'Pending',
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolvedAt DATETIME,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    FOREIGN KEY (raisedBy) REFERENCES Users(userId)
);

/* Amenities */
CREATE TABLE Amenities (
    amenityId INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

/* Property Amenities Mapping */
CREATE TABLE PropertyAmenities (
    propertyId INT,
    amenityId INT,
    PRIMARY KEY (propertyId, amenityId),
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    FOREIGN KEY (amenityId) REFERENCES Amenities(amenityId)
);

/* Payment Records */
CREATE TABLE Payment (
    paymentId INT PRIMARY KEY AUTO_INCREMENT,
    transactionId INT,
    rentalId INT,
    taxId INT,
    amount DECIMAL(12,2) NOT NULL,
    paymentDate DATETIME NOT NULL,
    method VARCHAR(20) NOT NULL,
    referenceNumber VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Completed',
    FOREIGN KEY (transactionId) REFERENCES Transaction(transactionId),
    FOREIGN KEY (rentalId) REFERENCES RentalAgreement(agreementId),
    FOREIGN KEY (taxId) REFERENCES PropertyTax(taxId),
    CHECK (amount > 0),
    CHECK (
        (transactionId IS NOT NULL AND rentalId IS NULL AND taxId IS NULL) OR
        (transactionId IS NULL AND rentalId IS NOT NULL AND taxId IS NULL) OR
        (transactionId IS NULL AND rentalId IS NULL AND taxId IS NOT NULL)
    )
);

/* Property Valuation */
CREATE TABLE Valuation (
    valuationId INT PRIMARY KEY,
    propertyId INT NOT NULL,
    valuationDate DATE NOT NULL,
    marketValue DECIMAL(12,2) NOT NULL,
    rentalValue DECIMAL(12,2),
    conductedBy VARCHAR(50) NOT NULL,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId),
    CHECK (marketValue > 0),
    CHECK (rentalValue > 0)
);

/* Legal Cases */
CREATE TABLE LegalCase (
    caseId INT PRIMARY KEY,
    propertyId INT NOT NULL,
    caseType VARCHAR(50) NOT NULL,
    courtName VARCHAR(50),
    status VARCHAR(30),
    nextHearing DATE,
    description TEXT,
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId)
);

/* User Favorites */
CREATE TABLE Favorites (
    userId INT,
    propertyId INT,
    addedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (userId, propertyId),
    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (propertyId) REFERENCES Property(propertyId)
);

/* Contact Messages */
CREATE TABLE ContactMessages (
    messageId INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    message TEXT NOT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('New', 'Read', 'Responded') DEFAULT 'New'
);

/* Search Analytics */
CREATE TABLE SearchAnalytics (
    searchId INT PRIMARY KEY AUTO_INCREMENT,
    userId INT,
    searchTimestamp DATETIME NOT NULL,
    city VARCHAR(30),
    propertyType VARCHAR(30),
    minPrice DECIMAL(12,2),
    maxPrice DECIMAL(12,2),
    minArea INT,
    maxArea INT,
    bedrooms INT,
    bathrooms INT,
    furnishingType VARCHAR(20),
    propertyAge VARCHAR(20),
    ownershipType VARCHAR(20),
    listingType VARCHAR(20),
    ipAddress VARCHAR(45),
    userAgent VARCHAR(255),
    FOREIGN KEY (userId) REFERENCES Users(userId)
);

/* Performance Metrics */
CREATE TABLE PerformanceMetrics (
    metricId INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL,
    avgResponseTime DECIMAL(10,2),
    searchesPerMinute INT,
    errorsPerMinute INT,
    activeUsers INT,
    cpuUsage DECIMAL(5,2),
    memoryUsage DECIMAL(5,2),
    alertSent BOOLEAN DEFAULT FALSE,
    alertType VARCHAR(50),
    INDEX idx_timestamp (timestamp)
);

-- User Roles
INSERT INTO UserRole (roleId, roleName) VALUES
(1, 'Admin'), (2, 'Agent'), (3, 'Buyer'), (4, 'Seller'), 
(5, 'Tenant'), (6, 'Legal Officer'), (7, 'Tax Consultant'),
(8, 'Property Manager');

-- Users
INSERT INTO Users (userId, username, password, mobile, email, roleId) VALUES
(1, 'admin_mumbai', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '9820123456', 'admin@realestate.com', 1),
(2, 'rahul_agent', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '9876543210', 'rahul@metrobrokers.com', 2),
(3, 'priya_buyer', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '8888877777', 'priya.sharma@email.com', 3),
(4, 'singh_properties', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '7777766666', 'singh.properties@email.com', 4),
(5, 'mehta_brokers', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '9999955555', 'mehta@ncrproperties.com', 2),
(6, 'kumar_tenant', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '8888888888', 'kumar.tenant@email.com', 5),
(7, 'legal_ravi', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '7777777777', 'ravi@legal.com', 6),
(8, 'tax_consult', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '6666666666', 'tax@consultant.com', 7),
(9, 'ncr_investor', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '9876509876', 'investor@ncr.com', 3),
(10, 'hyderabad_prop', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '9876543211', 'owner@hyderabadprop.com', 4),
(11, 'property_mgr', 'scrypt:32768:8:1$FjPq4e2FFnmKON5e$8138e93a046aeaffa63c30e1ebb8129567ac6bf543659b3f58ae00725d6a164d3efabea767fbd36a1b9b798cb60a4e8957fcbee9304d5d590bacb72fe775e3d6', '9876543212', 'manager@realestate.com', 8);

-- Indian Identity Documents
INSERT INTO IndianIdentity VALUES
(101, 2, '123412341234', 'ABCTY1234D'),
(102, 4, '567856785678', 'XYZZY5678X'),
(103, 3, '901290129012', 'PQRST9012U'),
(104, 9, '345634563456', 'NCRTY3456M'),
(105, 10, '789078907890', 'HYDER7890A'),
(106, 5, '234523452345', 'MHREA5678X'),
(107, 6, '678967896789', 'TENAN9012U'),
(108, 7, '012301230123', 'LEGAL3456M'),
(109, 8, '456745674567', 'TAXCO7890A'),
(110, 1, '890189018901', 'ADMIN1234D');

-- Property Types
INSERT INTO PropertyType VALUES
(1, 'Apartment'), (2, 'Villa'), (3, 'Farm House'), 
(4, 'Commercial Office'), (5, 'Retail Shop'), 
(6, 'Industrial Warehouse'), (7, 'Plot');

-- Property Configurations
INSERT INTO PropertyConfiguration VALUES
(101, 1, '1BHK'), (102, 1, '2BHK'), (103, 1, '3BHK'),
(104, 2, '3BHK'), (105, 2, '4BHK'), (106, 2, '5BHK'),
(107, 4, 'Small Office'), (108, 4, 'Medium Office'), (109, 4, 'Large Office'),
(110, 5, 'Small Shop'), (111, 5, 'Medium Shop'), (112, 5, 'Large Shop');

-- Locations
INSERT INTO IndianLocation VALUES
(1001, 'Mumbai', 'Maharashtra', '400001', 'MahaRERA Zone 1'),
(1002, 'Bangalore', 'Karnataka', '560001', 'Karnataka RERA'),
(1003, 'Gurgaon', 'Haryana', '122001', 'HRERA Gurugram'),
(1004, 'Hyderabad', 'Telangana', '500001', 'TSRERA Hyderabad'),
(1005, 'Pune', 'Maharashtra', '411001', 'MahaRERA Zone 2'),
(1006, 'Noida', 'Uttar Pradesh', '201301', 'UP RERA NCR'),
(1007, 'Chennai', 'Tamil Nadu', '600001', 'TNRERA Chennai'),
(1008, 'Kolkata', 'West Bengal', '700001', 'West Bengal RERA');

-- Properties
INSERT INTO Property (propertyId, address, ownerId, price, carpetArea, typeId, locationId, reraRegistered) VALUES
(5001, 'Sea View Apartment, Worli', 4, 125000000, 1800, 1, 1001, TRUE),
(5002, 'IT Park Office, Andheri East', 10, 80000000, 5000, 4, 1001, TRUE),
(5003, 'Tech Villa, Whitefield', 4, 97500000, 4500, 2, 1002, TRUE),
(5004, 'Startup Office, Koramangala', 10, 32000000, 2000, 4, 1002, FALSE),
(5005, 'Farmhouse, Sohna Road', 9, 50000000, 10000, 3, 1003, TRUE),
(5006, 'Retail Space, DLF Mall', 4, 120000000, 3000, 5, 1006, TRUE),
(5007, 'HITEC City Office Tower', 10, 67000000, 6000, 4, 1004, TRUE),
(5008, 'Banjara Hills Villa', 4, 180000000, 8000, 2, 1004, TRUE),
(5009, 'Residential Plot, Wakad', 9, 25000000, 5000, 7, 1005, TRUE),
(5010, 'Commercial Showroom, Hinjewadi', 10, 45000000, 2500, 5, 1005, TRUE);

-- Residential Properties
INSERT INTO ResidentialProperty VALUES
(5001, 2, 2, 22, 30, TRUE),
(5003, 4, 4, 1, 3, TRUE),
(5008, 5, 5, 2, 3, FALSE);

-- Commercial Properties
INSERT INTO CommercialProperty VALUES
(5002, 'IT Office', 15, 50),
(5004, 'Co-working', 5, 20),
(5006, 'Retail', 2, 150),
(5007, 'Tech Park', 10, 100),
(5010, 'Showroom', 1, 10);

-- Agents
INSERT INTO Agent VALUES
(201, 2, 'MH-REA-2024-123', 8, 'Metro Brokers', TRUE),
(202, 5, 'HR-REA-4567-456', 12, 'NCR Properties Ltd.', TRUE),
(203, 11, 'TS-REA-7890-789', 5, 'Hyderabad Realty', TRUE);

INSERT INTO Listing 
(listingId, propertyId, agentId, listPrice, bookingAmount, maintenanceCharges, availableFrom, isActive)
VALUES 
(3001, 5001, 201, 135000000, 500000, 15000, '2023-06-01', TRUE),
(3002, 5005, 202, 55000000, 1000000, NULL, '2023-07-15', TRUE),
(3003, 5007, 203, 70000000, NULL, 50000, '2023-08-01', TRUE),
(3004, 5003, 201, 100000000, 750000, 20000, '2023-09-01', TRUE),
(3005, 5009, 202, 27500000, 250000, NULL, '2023-10-01', TRUE);
-- Property Documents
INSERT INTO PropertyDocuments VALUES
(401, 5001, 'Sale Deed', 'SD/MH/2023/1234', '2023-01-15', 'Mumbai Registrar', '/docs/5001/sale_deed.pdf'),
(402, 5005, 'GPA', 'GPA/HR/456/2023', '2023-03-20', 'Gurgaon SDM', '/docs/5005/gpa.pdf'),
(403, 5007, 'Khata', 'TS/KHATA/789', '2023-05-01', 'GHMC Hyderabad', '/docs/5007/khata.pdf'),
(404, 5003, 'Sale Deed', 'SD/KA/2023/567', '2023-02-10', 'Bangalore Registrar', '/docs/5003/sale_deed.pdf'),
(405, 5009, 'Title Deed', 'TD/MH/2023/890', '2023-04-05', 'Pune Registrar', '/docs/5009/title_deed.pdf');

-- Property Images
INSERT INTO PropertyImages (propertyId, imageURL, isPrimary) VALUES
(5001, '/images/5001/1.jpg', TRUE),
(5001, '/images/5001/2.jpg', FALSE),
(5001, '/images/5001/3.jpg', FALSE),
(5003, '/images/5003/1.jpg', TRUE),
(5003, '/images/5003/2.jpg', FALSE),
(5005, '/images/5005/1.jpg', TRUE),
(5007, '/images/5007/1.jpg', TRUE),
(5008, '/images/5008/1.jpg', TRUE),
(5009, '/images/5009/1.jpg', TRUE),
(5010, '/images/5010/1.jpg', TRUE);

-- Update existing image paths to use correct format
UPDATE PropertyImages 
SET imageURL = CONCAT('/static/images/properties/', 
    SUBSTRING_INDEX(SUBSTRING_INDEX(imageURL, '/', 2), '/', -1),
    '/',
    SUBSTRING_INDEX(imageURL, '/', -1))
WHERE imageURL LIKE '/images/%';

INSERT INTO Buyer 
(buyerId, userId, minBudget, maxBudget, preferredLocations)
VALUES
(301, 3, 5000000, 150000000, 'Mumbai,Bangalore'),
(302, 9, 10000000, 100000000, 'Gurgaon,Noida,Hyderabad');

-- Transactions
INSERT INTO Transaction VALUES
(6001, 5001, 3, 4, 201, '2023-09-01', 132000000, 650000, 150000, 'RTGS', 'Completed'),
(6002, 5007, 9, 10, 203, '2023-10-15', 68500000, 320000, 120000, 'Cheque', 'Completed'),
(6003, 5005, 3, 9, 202, '2024-01-20', 52500000, 275000, 95000, 'UPI', 'Completed'),
(6004, 5003, 9, 4, 201, '2024-02-10', 95000000, 475000, 142500, 'RTGS', 'Completed');

-- Rental Agreements
INSERT INTO RentalAgreement VALUES
(7001, 5004, 10, 6, '2023-11-01', '2024-10-31', 450000, 2000000, TRUE, 'Active'),
(7002, 5002, 4, 9, '2023-12-01', '2024-11-30', 1200000, 5000000, FALSE, 'Active'),
(7003, 5006, 4, 3, '2024-01-15', '2024-12-14', 750000, 3000000, TRUE, 'Active');

-- Property Tax
INSERT INTO PropertyTax VALUES
(8001, 5001, '2023-24', 275000, '2023-12-31', TRUE, '2023-12-15'),
(8002, 5005, '2023-24', 150000, '2023-12-31', FALSE, NULL),
(8003, 5007, '2023-24', 420000, '2024-03-31', TRUE, '2024-03-15'),
(8004, 5003, '2023-24', 195000, '2023-12-31', TRUE, '2023-12-20'),
(8005, 5008, '2023-24', 350000, '2023-12-31', TRUE, '2023-12-10');

-- Amenities
INSERT INTO Amenities VALUES
(1, 'Swimming Pool', 'Olympic-sized pool with lifeguard'),
(2, 'Clubhouse', '5000 sqft with banquet facilities'),
(3, 'EV Charging', 'Fast charging stations'),
(4, '24/7 Security', 'CCTV and biometric access'),
(5, 'Gym', 'Fully equipped fitness center'),
(6, 'Childrens Play Area', 'Safe play area for kids'),
(7, 'Landscaped Garden', 'Beautifully maintained gardens'),
(8, 'Power Backup', 'Full power backup for common areas');

-- Property Amenities
INSERT INTO PropertyAmenities VALUES
(5001,1), (5001,2), (5001,4), (5001,5), (5001,6),
(5003,1), (5003,2), (5003,3), (5003,7), (5003,8),
(5005,3), (5005,7), (5005,8),
(5008,1), (5008,2), (5008,3), (5008,4), (5008,5), (5008,7), (5008,8);

-- Payments
INSERT INTO Payment (transactionId, rentalId, taxId, amount, paymentDate, method, referenceNumber, status) VALUES
(6001, NULL, NULL, 132000000, '2023-09-01 12:00:00', 'RTGS', 'TX1234', 'Completed'),
(NULL, 7001, NULL, 2000000, '2023-11-01 10:30:00', 'NEFT', 'RNT456', 'Completed'),
(NULL, NULL, 8001, 275000, '2023-12-15 15:45:00', 'UPI', 'TAX789', 'Completed'),
(6002, NULL, NULL, 68500000, '2023-10-15 11:20:00', 'Cheque', 'TX5678', 'Completed'),
(NULL, 7002, NULL, 5000000, '2023-12-01 09:15:00', 'RTGS', 'RNT901', 'Completed');

-- Valuations
INSERT INTO Valuation VALUES
(10001, 5001, '2023-01-15', 120000000, 180000, 'JLL India'),
(10002, 5007, '2023-06-20', 65000000, 420000, 'CBRE Hyderabad'),
(10003, 5003, '2023-03-10', 95000000, 350000, 'Knight Frank'),
(10004, 5008, '2023-07-05', 175000000, 550000, 'Colliers International'),
(10005, 5005, '2023-05-15', 48000000, 150000, 'ANAROCK');

-- Legal Cases
INSERT INTO LegalCase VALUES
(11001, 5005, 'Land Ownership', 'Gurgaon District Court', 'Ongoing', '2024-04-15', 'Dispute over land ownership with adjacent property'),
(11002, 5008, 'Inheritance Dispute', 'Telangana High Court', 'Stay Order', '2024-05-20', 'Multiple claimants to the property'),
(11003, 5002, 'Rental Agreement Violation', 'Mumbai City Civil Court', 'Filed', '2024-06-10', 'Tenant violating rental agreement terms');

-- Maintenance Requests
INSERT INTO Maintenance (propertyId, raisedBy, issueType, description, status) VALUES
(5001, 3, 'Plumbing', 'Bathroom leakage from ceiling', 'In Progress'),
(5004, 6, 'Electrical', 'AC not working in main hall', 'Resolved'),
(5008, 4, 'Structural', 'Crack in living room wall', 'Pending'),
(5003, 9, 'Pest Control', 'Termite infestation noticed', 'Completed'),
(5007, 10, 'HVAC', 'Central AC system not cooling properly', 'In Progress');

-- Favorites
INSERT INTO Favorites VALUES
(3,5001, '2023-08-15 10:30:00'),
(3,5003, '2023-09-20 11:45:00'),
(3,5008, '2023-10-05 09:15:00'),
(9,5005, '2023-07-10 14:20:00'),
(9,5007, '2023-08-25 16:30:00'),
(6,5002, '2023-11-15 12:00:00');