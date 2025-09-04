-- Address Dimension
CREATE OR REPLACE FUNCTION FnTrgAddress()
RETURNS TRIGGER
AS
$$
	BEGIN
		DELETE FROM silver.DimAddress 
		WHERE "addressid" = NEW."addressid";  
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL

CREATE OR REPLACE TRIGGER TrgAddress
BEFORE INSERT ON silver.DimAddress
FOR EACH ROW
EXECUTE PROCEDURE FnTrgAddress()

-- Credit Card Dimension
CREATE OR REPLACE FUNCTION FnTrgCreditCard()
RETURNS TRIGGER
AS 
$$
	BEGIN
		DELETE FROM silver.DimCreditCard
		WHERE "creditcardid" = NEW."creditcardid";
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL

CREATE OR REPLACE TRIGGER TrgCreditCard
BEFORE INSERT ON silver.DimCreditCard
FOR EACH ROW
EXECUTE PROCEDURE FnTrgCreditCard()

-- Territory Dimension
CREATE OR REPLACE FUNCTION FnTrgTerritory()
RETURNS TRIGGER
AS 
$$
	BEGIN
		DELETE FROM silver.DimTerritory
		WHERE "territoryid" = NEW."territoryid";
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL

CREATE OR REPLACE TRIGGER TrgTerritory
BEFORE INSERT ON silver.DimTerritory
FOR EACH ROW
EXECUTE PROCEDURE FnTrgTerritory()


-- Ship Method Dimension

CREATE OR REPLACE FUNCTION FnTrgShipMethod()
RETURNS TRIGGER
AS 
$$
	BEGIN
		DELETE FROM silver.DimShipMethod
		WHERE "shipmethodid" = NEW."shipmethodid";
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL


CREATE OR REPLACE TRIGGER TrgShipMethod
BEFORE INSERT ON silver.DimShipMethod
FOR EACH ROW
EXECUTE PROCEDURE FnTrgShipMethod()


-- Store Dimension
CREATE OR REPLACE FUNCTION FnTrgStore()
RETURNS TRIGGER
AS 
$$
	BEGIN
		DELETE FROM silver.DimStore
		WHERE "businessentityid" = NEW."businessentityid";
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL

CREATE OR REPLACE TRIGGER TrgStore
BEFORE INSERT ON silver.DimStore
FOR EACH ROW
EXECUTE PROCEDURE FnTrgStore()


-- Person Dimension

CREATE OR REPLACE FUNCTION FnTrgPerson()
RETURNS TRIGGER
AS 
$$
	BEGIN
		DELETE FROM silver.DimPerson
		WHERE "businessentityid" = NEW."businessentityid";
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL


CREATE OR REPLACE TRIGGER TrgPerson
BEFORE INSERT ON silver.DimPerson
FOR EACH ROW
EXECUTE PROCEDURE FnTrgPerson()

-- CurrencyRate Dimension


CREATE OR REPLACE FUNCTION FnTrgCurrencyRate()
RETURNS TRIGGER
AS 
$$
	BEGIN
		DELETE FROM silver.DimCurrencyRate
		WHERE "currencyrateid" = NEW."currencyrateid";
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL


CREATE OR REPLACE TRIGGER TrgCurrencyRate
BEFORE INSERT ON silver.DimCurrencyRate
FOR EACH ROW
EXECUTE PROCEDURE FnTrgCurrencyRate()

-- Sales Fact Table
CREATE OR REPLACE FUNCTION FnTrgFactSales()
RETURNS TRIGGER
AS 
$$
	BEGIN
		DELETE FROM silver.FactSales
		WHERE "salesorderid" = NEW."salesorderid";
		RETURN NEW;
	END;
$$ LANGUAGE PLPGSQL

CREATE OR REPLACE TRIGGER TrgFactSales
BEFORE INSERT ON silver.FactSales
FOR EACH ROW
EXECUTE PROCEDURE FnTrgFactSales()
