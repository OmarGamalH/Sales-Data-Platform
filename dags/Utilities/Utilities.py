import pyspark.sql as ps
import pyspark.sql.functions as f
import pyspark.sql.types as types
import logging 
import os 
import datetime 

current_dir = os.getcwd()
logging_file = os.path.join(current_dir ,"logs.log")
spark = ps.SparkSession.builder \
        .config("spark.jars" , "/usr/local/nifi/sqljdbc/enu/jars/postgresql-42.7.7.jar")\
        .appName("spark app").getOrCreate()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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
       pass


def AddressTransform(RawDataFrame : ps.DataFrame = None) -> ps.DataFrame:
    df_v_1 = RawDataFrame.withColumn("AddressLine1" , f.trim("AddressLine1")).withColumn("AddressLine2" , f.trim("AddressLine2")).withColumn("City" , f.trim("City"))
    df_v_2 = df_v_1.dropna("any" , subset=["AddressLine1"])
    df_v_3 = df_v_2.withColumn("AddressLine1" , f.initcap("AddressLine1")).withColumn("AddressLine2" , f.initcap("AddressLine2")).withColumn("City" , f.initcap("City"))
    df_v_4 = df_v_3.withColumn("ModifiedDate" , f.col("ModifiedDate").cast(types.DateType()))
    df_final_v = df_v_4.withColumn("ModifiedDate" , f.lit(datetime.datetime.now()))
    return df_final_v 


def load_to_postgresql(transformed_df : ps.DataFrame , Database , schema , table):
    transformed_df.write.format("jdbc") \
        .option("url", f"jdbc:postgresql://172.21.96.1:5432/{Database}") \
        .option("dbtable", f"{schema}.{table}") \
        .option("user", "postgres") \
        .option("password", "Gemy0100") \
        .option("driver", "org.postgresql.Driver")\
        .mode("overwrite").save()