CREATE OR REPLACE VIEW Gold.FullView AS
(	
	SELECT F.* 
		 , A.addressline1 AS BillToAdressLine1
		 , A.addressline2 AS BillToAddressLine2
		 , A.City AS BillToAddressCity
		 , A.stateprovinceid AS BillToAddressStateProvinceID
		 , A.PostalCode AS BillToAddressPostalCode
		 , A2.addressline1 AS ShipToAdressLine1
		 , A2.addressline2 AS ShipToAddressLine2
		 , A2.City AS ShipToAddressCity
		 , A2.stateprovinceid AS ShipToAddressStateProvinceID
		 , A2.PostalCode AS ShipToAddressPostalCode
		 , CC.Cardtype AS CreditCardType
		 , CC.CardNumber AS CreditCardNumber
		 , CC.ExpMonth AS CreditCardExpMonth
		 , CC.ExpYear AS CreditCardExpYear
		 , P.PersonType AS PersonType
		 , P.Title AS PersonTitle
		 , P.FirstName AS PersonFirstName
		 , P.MiddleName AS PersonMiddleName
		 , P.LastName AS PersonLastName
		 , P.Suffix AS PersonSuffix
		 , P.EmailPromotion AS PersonEmailPromotion
		 , SM.Name AS ShipMethodName
		 , SM.ShipBase AS ShipMethodBase
		 , SM.ShipRate AS ShipMethodRate
		 , S.Name AS StoreName
		 , T.Name AS TerritoryName
		 , T.CountryRegionCode AS TerritoryCountryRegionCode
		 , T."Group" AS TerritoryGroup
		 , T.SalesYTD AS TerritorySalesYTD
		 , T.SalesLastYear AS TerritorySalesLastYear
		 , T.CostYTD AS TerritoryCostYTD
		 , T.CostLastYear AS TerritoryCostLastYear
		 , CR.CurrencyRateDate
		 , CR.FromCurrencyCode
		 , CR.ToCurrencyCode
		 , CR.AverageRate
		 , CR.EndOfDayRate
	FROM Silver.FactSales F 
	LEFT JOIN Silver.DimAddress A
	ON A."addressid" = F."billtoaddressid"
	LEFT JOIN Silver.DimAddress A2
	ON A2."addressid" = F."shiptoaddressid"
	LEFT JOIN Silver.DimCreditCard CC
	ON F."creditcardid" = CC."creditcardid"
	LEFT JOIN Silver.DimPerson P
	ON F."personid" = P."businessentityid"
	LEFT JOIN Silver.DimShipMethod SM
	ON F."shipmethodid" = SM."shipmethodid"
	LEFT JOIN Silver.DimStore S
	ON F."storeid" = S."businessentityid"
	LEFT JOIN Silver.DimTerritory T
	ON F."territoryid" = T.territoryid
	LEFT JOIN Silver.DimCurrencyRate CR
	ON F."currencyrateid" = CR."currencyrateid"
)

