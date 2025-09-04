import pyspark.sql as ps
import pyspark.sql.functions as f
import pyspark.sql.types as types
import logging 
import os 
import datetime 
from pyspark.sql.window import Window


# current_dir = os.getcwd()
# logging_file = os.path.join(current_dir ,"logs.log")
spark = ps.SparkSession.builder \
        .config("spark.jars" , "/usr/local/nifi/sqljdbc/enu/jars/postgresql-42.7.7.jar")\
        .appName("spark app").getOrCreate()


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler(logging_file)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

pyspark_log = logging.getLogger('pyspark').setLevel(logging.CRITICAL)
py4j_logger = logging.getLogger("py4j").setLevel(logging.CRITICAL)

def extract_parquet(filename):
    try:
       # logger.info(f"start the extraction of {filename}")
        df = spark.read.parquet(f"hdfs:/nifi_dest/files/{filename}")
       # logger.info(f"extraction of {filename} has been done successfully")
        return df
    except Exception as e:
       # logger.error(e)
       return None


def load_to_postgresql(transformed_df : ps.DataFrame , Database , schema , table):
    transformed_df.write.format("jdbc") \
        .option("url", f"jdbc:postgresql://172.21.96.1:5432/{Database}") \
        .option("dbtable", f"{schema}.{table}") \
        .option("user", "postgres") \
        .option("password", "Gemy0100") \
        .option("driver", "org.postgresql.Driver")\
        .mode("append").save()
    
def GetFKReplacement(RawDataFrame : ps.DataFrame , PrimaryKey , TargetColumn):
    """
        NOTE
        ----
        USE THIS ON THE FOREGIN KEY TABLE , THEN REMOVE THE DUPLICATES FROM THE PRIMARKY KEY TABLE
        

        USAGE
        -----
        - RawDataFrame : Dataframe of the Primary key table
        - Primary key : the Primary key of the RawDataFrame
        - TargetColumn : The column which will lead to remove of rows in primary table 

    """
    duplicates_df = RawDataFrame.alias("df_1").crossJoin(RawDataFrame.alias("df_2")).filter((f.col(f"df_1.{PrimaryKey}") != f.col(f"df_2.{PrimaryKey}")) & (f.col(f"df_1.{TargetColumn}") == f.col(f"df_2.{TargetColumn}")))
    d_df_v_1 = duplicates_df.select(f.col(f"df_1.{PrimaryKey}") , f.col(f"df_1.{TargetColumn}"))
    window = Window.partitionBy(f"{TargetColumn}").orderBy(f"{PrimaryKey}")
    d_df_v_2 = d_df_v_1.withColumn("smallest" , f.min(f"{PrimaryKey}").over(window))
    d_df_v_3 = d_df_v_2.filter(f.col(f"{PrimaryKey}") != f.col("smallest"))
    # rdd_v = d_df_v_3.rdd.collect()
    # replacements = [*map(lambda row : {row["BusinessEntityID"] : row["smallest"]} , rdd_v.collect())]
    # replacements = {}
    # for row in rdd_v:
    #     replacements[row["BusinessEntityID"]] = row["smallest"]
    replacements = d_df_v_3.drop_duplicates([f"{PrimaryKey}"])
    return replacements

def AddressTransform(RawDataFrame) -> ps.DataFrame:
    df_v_1 = RawDataFrame.withColumn("AddressLine1" , f.trim("AddressLine1")).withColumn("AddressLine2" , f.trim("AddressLine2")).withColumn("City" , f.trim("City"))
    df_v_2 = df_v_1.dropna("any" , subset=["AddressLine1"])
    df_v_3 = df_v_2.withColumn("AddressLine1" , f.initcap("AddressLine1")).withColumn("AddressLine2" , f.initcap("AddressLine2")).withColumn("City" , f.initcap("City"))
    df_v_4 = df_v_3.withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType()))
    df_final_v = df_v_4.withColumn("ModifiedDate" , f.lit(datetime.datetime.now()))
    return df_final_v 


def CreditCardTransform(RawDataFrame) -> ps.DataFrame:
    df_v_1 = RawDataFrame.filter(f.length(f.col("CardNumber")) == 14)
    df_v_2 = df_v_1\
    .withColumn("CardType" , f.initcap("CardType"))\
    .withColumn("ExpMonth" , f.when(f.col("ExpMonth") > 12 , 12)
                .when(f.col("ExpMonth") < 1 , 1)
                .otherwise(f.col("ExpMonth")))
    df_v_3 = df_v_2.drop_duplicates(subset=["CardNumber"])
    df_final_v = df_v_3.orderBy("CreditCardID").withColumn('ModifiedDate' , f.col("ModifiedDate").cast(types.DateType()))
    return df_final_v


def TerritoryTransform(RawDataFrame) -> ps.DataFrame:
    df_v_1 = RawDataFrame.withColumn("Name" , f.trim("Name"))\
        .withColumn("CountryRegionCode" , f.trim("CountryRegionCode"))\
        .withColumn("Group" , f.trim("Group"))
    
    df_v_2 = df_v_1.withColumn("Name" , f.initcap("Name"))\
        .withColumn("CountryRegionCode" , f.upper("CountryRegionCode"))\
        .withColumn("Group" , f.initcap("Group"))\
        .drop_duplicates(subset=["Name"])\
        .orderBy("TerritoryID")
    
    cols = df_v_2.columns
    cols.remove('rowguid')

    df_final_v = df_v_2.select(cols)\
    .withColumn("SalesYTD" , f.col("SalesYTD").cast(types.DecimalType(20 , 4)))\
    .withColumn("SalesLastYear" , f.col("SalesLastYear").cast(types.DecimalType(20 , 4)))\
    .withColumn("CostYTD" , f.col("CostYTD").cast(types.DecimalType(20 , 4)))\
    .withColumn("CostLastYear" , f.col("CostLastYear").cast(types.DecimalType(20 , 4)))\
    .withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType()))
    return df_final_v    



def ShipMethodTransform(RawDataFrame):
    cols = RawDataFrame.columns
    cols.remove("rowguid")
    df_v_1 = RawDataFrame.select(cols)

    df_v_2 = df_v_1.withColumn("Name" , f.trim("Name")).withColumn("Name" , f.upper("Name"))
    df_v_3 = df_v_2.drop_duplicates(["Name"])
    df_v_4 = df_v_3.withColumn("ShipBase" , f.col("ShipBase").cast(types.DecimalType(10 , 4)))\
                .withColumn("ShipRate" , f.col("ShipRate").cast(types.DecimalType(10 , 4)))
    df_final_v = df_v_4.withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType())).orderBy("ShipMethodID")

    return df_final_v



def load_to_duplicates_archive(DataFrame , Name):
    DataFrame.write.mode("overwrite").format("csv").option("header" , True).save(f"hdfs:/nifi_dest/duplicates_mapping/{Name}")



def StoreTransform(RawDataFrame):
    df_v_1 = RawDataFrame.select(["BusinessEntityID" , "Name" , "ModifiedDate"])
    df_v_2 = df_v_1.withColumn("Name" , f.trim("Name")).withColumn("Name" , f.initcap("Name"))
    df_v_3 = df_v_2.drop_duplicates(subset=["Name"])
    df_final_v = df_v_3.withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType())).orderBy("BusinessEntityID")
    return df_final_v


def PersonTransform(RawDataFrame):
    df_v_1 = RawDataFrame.withColumn("PersonType" , f.when(f.col("PersonType").isNull() , "OT").otherwise(f.col("PersonType")))
    df_v_2 = df_v_1.withColumn("Title" , f.when(f.col("Title").isNull() , "Mx.").otherwise(f.col("Title")))
    df_v_3 = df_v_2.withColumn("PersonType" , f.upper("PersonType")).withColumn("Title" , f.initcap("Title"))\
                .withColumn("FirstName" , f.initcap("FirstName"))\
                .withColumn("MiddleName" , f.initcap("MiddleName"))\
                .withColumn("LastName" , f.initcap("LastName"))\
                .withColumn("Suffix" , f.initcap("Suffix"))
    df_v_4 = df_v_3.withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType()))
    cols = df_v_4.columns
    cols.remove("NameStyle")
    df_final_v = df_v_4.orderBy("BusinessEntityID").select(cols)

    return df_final_v

def extract_duplicates_mapping(CsvName):
    try:
        return spark.read.format("csv").option("header" , True).load(f"hdfs:/nifi_dest/duplicates_mapping/{CsvName}")
    except Exception as e:
        return None
def CurrencyRateTransform(RawDataFrame):
    df_v_1 = RawDataFrame.withColumn("CurrencyRateDate" , f.col("CurrencyRateDate").cast(types.DateType()))\
                     .withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType()))
    df_v_2 = df_v_1.withColumn("FromCurrencyCode" , f.upper("FromCurrencyCode"))\
                .withColumn("ToCurrencyCode" , f.upper("ToCurrencyCode"))
    df_v_3 = df_v_2.withColumn("AverageRate" , f.col("AverageRate").cast(types.DecimalType(10 , 4)))\
                .withColumn("EndOfDayRate" , f.col("EndOfDayRate").cast(types.DecimalType(10 , 4)))

    df_final_v = df_v_3.orderBy("CurrencyRateID")

    return df_final_v


def proccess_duplicates(DataFrame , DuplicatesDataFrame , DuplicatesPrimaryKey , ReplacementKey):
    RawDupRdd = DuplicatesDataFrame.rdd.collect()
    to_replace = [*map(lambda row : int(row[f"{DuplicatesPrimaryKey}"]) , RawDupRdd)]
    value = [*map(lambda row : int(row["smallest"]) , RawDupRdd)]
    return DataFrame.replace(to_replace = to_replace , value = value , subset = [f"{ReplacementKey}"])

def FactSalesTransform(SalesRawDataFrame , CustomerRawDataFrame):
    JoinedRawDataFrame = SalesRawDataFrame.alias("sales").join(CustomerRawDataFrame.alias("customer") , on = "CustomerID" , how = "inner")
    df_v_1 = JoinedRawDataFrame.select(["SalesOrderID" , "PersonID" , "StoreID" , "customer.TerritoryID" , "BillToAddressID" , "ShipToAddressID" 
                                    , "ShipMethodID" , "CreditCardID" , "CurrencyRateID" ,"customer.AccountNumber" ,  "OrderDate"
                                    , "DueDate" , "ShipDate" , "Status" 
                                     , "SubTotal" , "TaxAmt" , "Freight" , "TotalDue" , "sales.ModifiedDate"])
    
    df_v_2 = df_v_1.withColumn("OrderDate" , f.col("OrderDate").cast(types.DateType()))\
               .withColumn("DueDate" , f.col("DueDate").cast(types.DateType()))\
               .withColumn("ShipDate" , f.col("ShipDate").cast(types.DateType()))\
               .withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType()))
    
    DuplicatessDataFrame = extract_duplicates_mapping("Store")
    df_v_3 = proccess_duplicates(df_v_2 , DuplicatessDataFrame , 'BusinessEntityID' , 'StoreID')

    df_v_4 = df_v_3.withColumn("SubTotal" , f.col("SubTotal").cast(types.DecimalType(10 , 4)))\
                .withColumn("TaxAmt" , f.col("TaxAmt").cast(types.DecimalType(10 , 4)))\
                .withColumn("Freight" , f.col("Freight").cast(types.DecimalType(10 , 4)))\
                .withColumn("TotalDue" , f.col("TotalDue").cast(types.DecimalType(10 , 4)))
    
    df_final_v = df_v_4

    return df_final_v