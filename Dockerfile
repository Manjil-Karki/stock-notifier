FROM apache/airflow:2.5.3
# USER root
USER airflow
RUN pip install yfinance



# FROM apache/airflow:2.5.3
# COPY requirements.txt .
# RUN pip install -r requirements.txt