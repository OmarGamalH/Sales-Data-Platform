FROM apache/airflow:latest

WORKDIR ~/

VOLUME /data

EXPOSE 8080:8080/tcp

CMD bash