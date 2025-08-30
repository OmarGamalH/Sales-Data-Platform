import pyspark.sql as ps
import pyspark.sql.functions as f
import Utilities.Utilities as u
from airflow.sdk import dag , asset , task



spark = ps.SparkSession.builder \
        .config("spark.jars" , "/usr/local/nifi/sqljdbc/enu/jars/postgresql-42.7.7.jar")\
        .appName("spark app").getOrCreate()


@asset(
    schedule = None,
    uri="hdfs:/nifi_dest/files/address.parquet"
)
def address_table():
    pass


@dag(schedule = address_table)
def Address_Dag():
    @task()
    def Address_ETL():
        raw_df = u.extract_parquet("address.parquet")
        transformed_df = u.AddressTransform(raw_df)
        u.load_to_postgresql(transformed_df=transformed_df , Database= "salesdatawarehouse" , schema = "Silver" , table = "DimAddress")
    Address_ETL()  

Address_Dag()
