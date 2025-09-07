import Utilities.Utilities as u
import Utilities.DataQuality as d
from airflow.sdk import dag , task , task_group , asset

@asset(schedule = None)
def SalesTables():
    pass

@dag(schedule = SalesTables)
def SalesDataPlatfromDag():
    
    @task_group()
    def Address():
        @task
        def AddressBDP():
            RawDataFrame = u.extract_parquet("Address.parquet")
            DataQualityFrame = d.AddressDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        @task()
        def AddressETL():
            raw_df = u.extract_parquet("Address.parquet")
            transformed_df = u.AddressTransform(raw_df)
            u.load_to_postgresql(transformed_df=transformed_df , Database= "salesdatawarehouse" , schema = "silver" , table = "dimaddress")
        
        @task()
        def AddressADP():
            RawDataFrame = u.extract_postgres(Database= "salesdatawarehouse" , schema = "silver" , table = "dimaddress")
            DataQualityFrame = d.AddressDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")
        
        AddressBDP() >> AddressETL() >> AddressADP()

    @task_group()
    def CreditCard():

        @task
        def CreditCardBDP():
            RawDataFrame =  u.extract_parquet("CreditCard.parquet")
            DataQualityFrame = d.CreditCardDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")



        @task
        def CreditCardETL():
            RawDataFrame =  u.extract_parquet("CreditCard.parquet")
            TransformedDataFrame = u.CreditCardTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "dimcreditcard")
        
        @task
        def CreditCardADP():
            RawDataFrame =  u.extract_postgres(Database = "salesdatawarehouse" , schema = "silver" , table = "dimcreditcard")
            DataQualityFrame = d.CreditCardDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")
        
        CreditCardBDP() >> CreditCardETL() >> CreditCardADP()


    @task_group()
    def ShipMethod():

        @task
        def ShipMethodBDP():
            RawDataFrame =  u.extract_parquet("ShipMethod.parquet")
            DataQualityFrame = d.ShipMethodDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        @task
        def ShipMethodETL():
            RawDataFrame =  u.extract_parquet("ShipMethod.parquet")
            TransformedDataFrame = u.ShipMethodTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimShipMethod")
        
        @task
        def ShipMethodADP():
            RawDataFrame =  u.extract_postgres(Database = "salesdatawarehouse" , schema = "silver" , table = "DimShipMethod")
            DataQualityFrame = d.ShipMethodDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")
        
        ShipMethodBDP() >> ShipMethodETL() >> ShipMethodADP()

    @task_group()
    def Territory():
        @task
        def TerritoryBDP():
            RawDataFrame =  u.extract_parquet("SalesTerritory.parquet")
            DataQualityFrame = d.TerritoryDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        @task
        def TerritoryETL():
            RawDataFrame =  u.extract_parquet("SalesTerritory.parquet")
            TransformedDataFrame = u.TerritoryTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimTerritory")
        
        @task
        def TerritoryADP():
            RawDataFrame = u.extract_postgres(Database = "salesdatawarehouse" , schema = "silver" , table = "DimTerritory")
            DataQualityFrame = d.TerritoryDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        
        TerritoryBDP() >> TerritoryETL() >> TerritoryADP()

    @task_group()
    def Store():
        @task 
        def StoreBDP():
            RawDataFrame = u.extract_parquet("Store.parquet")
            DataQualityFrame = d.StoreDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        @task
        def StoreDuplicatesSaving():
            RawDataFrame = u.extract_parquet("Store.parquet")
            DuplicatesDataFrame = u.GetFKReplacement(RawDataFrame = RawDataFrame , PrimaryKey = "BusinessEntityID" , TargetColumn = "Name")
            u.load_to_duplicates_archive(DataFrame = DuplicatesDataFrame , Name = "Store")

        @task
        def StoreETL():
            RawDataFrame = u.extract_parquet("Store.parquet")
            TransformedDataFrame = u.StoreTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimStore")            
         
        @task
        def StoreADP():
            RawDataFrame = u.extract_postgres(Database = "salesdatawarehouse" , schema = "silver" , table = "DimStore")
            DataQualityFrame = d.StoreDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")


        StoreBDP() >> StoreDuplicatesSaving() >> StoreETL() >> StoreADP()

    @task_group()
    def Person():
        @task
        def PersonBDP():
            RawDataFrame = u.extract_parquet("Person.parquet")
            DataQualityFrame = d.PersonDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        @task
        def PersonETL():
            RawDataFrame = u.extract_parquet("Person.parquet")
            TransformedDataFrame = u.PersonTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimPerson") 
        
        @task
        def PersonADP():
            RawDataFrame = u.extract_postgres(Database = "salesdatawarehouse" , schema = "silver" , table = "DimPerson")
            DataQualityFrame = d.PersonDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        
        PersonBDP() >> PersonETL() >> PersonADP()


    @task_group()
    def CurrencyRate():
        @task 
        def CurrencyRateBDP():
            RawDataFrame = u.extract_parquet("CurrencyRate.parquet")
            DataQualityFrame = d.CurrencyRateDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")


        @task
        def CurrencyRateETL():
            RawDataFrame = u.extract_parquet("CurrencyRate.parquet")
            TransformedDataFrame = u.CurrencyRateTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimCurrencyRate")
        
        
        @task
        def CurrencyRateADP():
            RawDataFrame = u.extract_postgres(Database = "salesdatawarehouse" , schema = "silver" , table = "DimCurrencyRate")
            DataQualityFrame = d.CurrencyRateDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")

        
        CurrencyRateBDP() >> CurrencyRateETL() >> CurrencyRateADP()

    @task_group()
    def SalesOrderHeader_Customer():
        @task
        def SalesBDP():
            RawDataFrame = u.extract_parquet("SalesOrderHeader.parquet")
            DataQualityFrame = d.SalesOrderHeaderDP(RawDataFrame , "Before")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")
 
        @task
        def SalesETL():
            SalesRawDataFrame = u.extract_parquet("SalesOrderHeader.parquet")
            CustomerRawDataFrame = u.extract_parquet("Customer.parquet")
            TransformedDataFrame = u.FactSalesTransform(SalesRawDataFrame = SalesRawDataFrame , CustomerRawDataFrame = CustomerRawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "FactSales")
        
        @task
        def SalesADP():
            RawDataFrame = u.extract_postgres(Database = "salesdatawarehouse" , schema = "silver" , table = "FactSales")
            DataQualityFrame = d.SalesOrderHeaderDP(RawDataFrame , "After")
            u.load_to_postgresql(transformed_df = DataQualityFrame , Database= "salesdatawarehouse" , schema = "dataquality" , table = "dataquality")
        
        
        SalesBDP() >> SalesETL() >> SalesADP()
        
    Address() >> CreditCard() >> ShipMethod() >> Territory() >> Store() >> Person() >> CurrencyRate() >> SalesOrderHeader_Customer()



SalesDataPlatfromDag()