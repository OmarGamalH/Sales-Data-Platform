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