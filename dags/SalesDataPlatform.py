import Utilities.Utilities as u
from airflow.sdk import dag , task , task_group , asset

@asset(schedule = None)
def SalesTables():
    pass

@dag(schedule = SalesTables)
def SalesDataPlatfromDag():
    
    @task_group()
    def Address():

        @task()
        def AddressETL():
            raw_df = u.extract_parquet("address.parquet")
            transformed_df = u.AddressTransform(raw_df)
            u.load_to_postgresql(transformed_df=transformed_df , Database= "salesdatawarehouse" , schema = "silver" , table = "dimaddress")
        AddressETL()

    @task_group()
    def CreditCard():
        @task
        def CreditCardETL():
            RawDataFrame =  u.extract_parquet("CreditCard.parquet")
            TransformedDataFrame = u.CreditCardTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "dimcreditcard")
        CreditCardETL()

    @task_group()
    def ShipMethod():
        @task
        def ShipMethodETL():
            RawDataFrame =  u.extract_parquet("ShipMethod.parquet")
            TransformedDataFrame = u.ShipMethodTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimShipMethod")
        ShipMethodETL()

    @task_group()
    def Territory():
        @task
        def TerritoryETL():
            RawDataFrame =  u.extract_parquet("SalesTerritory.parquet")
            TransformedDataFrame = u.TerritoryTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimTerritory")
        TerritoryETL()

    @task_group()
    def Store():
        @task
        def StoreETL():
            RawDataFrame = u.extract_parquet("Store.parquet")
            TransformedDataFrame = u.StoreTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimStore")            
        StoreETL()

    @task_group()
    def Person():
        @task
        def PersonETL():
            RawDataFrame = u.extract_parquet("Person.parquet")
            TransformedDataFrame = u.PersonTransform(RawDataFrame)
            u.load_to_postgresql(TransformedDataFrame , Database = "salesdatawarehouse" , schema = "silver" , table = "DimPerson") 
        PersonETL()


    @task_group()
    def CurrencyRate():
        pass

    @task_group()
    def SalesOrderHeader_Customer():
        pass

    Address() >> CreditCard() >> ShipMethod() >> Territory() >> Store() >> Person() >> CurrencyRate() >> SalesOrderHeader_Customer()



SalesDataPlatfromDag()