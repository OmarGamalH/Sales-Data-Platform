echo "WARNING: Make sure to set The Environment variable of HADOOP_HOME to the location of hadoop folder"
echo "WARNING: Make sure to set The Environment variable of NIFI_HOME to the location of nifi folder"
echo "WARNING: Make sure to Download Apache Airflow is downloaded first"
# Starting hadoop for Data Lake
echo "Starting Hadoop to use HDFS as Data Lake..."
cd "$HADOOP_HOME"/sbin/
./start-all.sh

# Starting Apache Nifi for Data Ingestion Layer
echo "Starting Apache Nifi to use it as Ingestion Layer..."
cd "$NIFI_HOME"/bin/
sudo ./nifi.sh start

# Starting Apache Airflow for Data Orchestration Layer
echo "Starting Apache Airflow to use it as Orchestration Layer..."
airflow standalone

