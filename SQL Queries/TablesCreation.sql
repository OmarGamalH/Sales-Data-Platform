CREATE TABLE Silver.DimAddress
(
		AddressID BIGINT PRIMARY KEY,
		AddressLine1 VARCHAR(255) NOT NULL,
		AddressLine2 VARCHAR(255),
		City VARCHAR(255),
		StateProvinceID INT,
		PostalCode VARCHAR(255),
		ModifiedDate DATE

);

CREATE TABLE Silver.DimCreditCard
(
		CreditCardID BIGINT PRIMARY KEY,
		CardType VARCHAR(255) NOT NULL,
		CardNumber VARCHAR(255) NOT NULL,
		ExpMonth INT,
		ExpYear INT,
		ModifiedDate DATE
);

CREATE TABLE Silver.DimTerritory
(
		TerritoryID BIGINT PRIMARY KEY,
		Name VARCHAR(255) NOT NULL,
		CountryRegionCode VARCHAR(2),
		"Group" VARCHAR(255),
		SalesYTD DECIMAL(20 , 4),
		SalesLastYear DECIMAL(20 , 4),
		CostYTD DECIMAL(20 , 4),
		CostLastYear DECIMAL(20 , 4),
		ModifiedDate DATE
);


CREATE TABLE Silver.DimShipMethod
(
		ShipMethodID BIGINT PRIMARY KEY,
		Name VARCHAR(255),
		ShipBase DECIMAL(10 , 4),
		ShipRate DECIMAL(10 , 4),
		ModifiedDate DATE
);

CREATE TABLE Silver.DimStore
(
		BusinessEntityID BIGINT PRIMARY KEY,
		Name VARCHAR(255),
		ModifiedDate DATE
);

CREATE TABLE Silver.DimPerson
(
		BusinessEntityID BIGINT PRIMARY KEY,
		PersonType VARCHAR(2) NOT NULL,
		Title VARCHAR(255),
		FirstName VARCHAR(255),
		MiddleName VARCHAR(255),
		LastName VARCHAR(255),
		Suffix VARCHAR(255),
		EmailPromotion INT,
		ModifiedDate DATE
);

CREATE TABLE Silver.DimCurrencyRate
(
		CurrencyRateID BIGINT PRIMARY KEY,
		CurrencyRateDate DATE,
		FromCurrencyCode VARCHAR(255),
		ToCurrencyCode VARCHAR(255),
		AverageRate DECIMAL(10 , 4),
		EndOfDayRate DECIMAL(10 , 4),
		ModifiedDate DATE
)

CREATE TABLE Silver.FactSales
(
		SalesOrderID BIGINT PRIMARY KEY,
		PersonID BIGINT  REFERENCES Silver.DimPerson(businessentityid),
		StoreID BIGINT REFERENCES Silver.DimStore(businessentityid),
		TerritoryID BIGINT  REFERENCES Silver.DimTerritory(territoryid),
		BillToAddressID BIGINT  REFERENCES Silver.DimAddress(addressid),
		ShipToAddressID BIGINT  REFERENCES Silver.DimAddress(addressid),
		ShipMethodID BIGINT  REFERENCES Silver.DimShipMethod(shipmethodid),
		CreditCardID BIGINT  REFERENCES Silver.DimCreditCard(creditcardid),
		CurrencyRateID BIGINT  REFERENCES Silver.DimCurrencyRate(currencyrateid),
		AccountNumber VARCHAR(255),
		OrderDate DATE,
		DueDate DATE,
		ShipDate DATE,
		Status INT,
		SubTotal DECIMAL(10 , 4),
		TaxAmt DECIMAL(10 , 4),
		Freight DECIMAL(10 , 4),
		TotalDue DECIMAL(10 , 4),
		ModifiedDate DATE


)