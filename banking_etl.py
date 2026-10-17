
import boto3
import json
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("BankingETL").getOrCreate()

# Get credentials securely
client = boto3.client("secretsmanager", region_name="eu-north-1")
secret = json.loads(
    client.get_secret_value(
        SecretId="banking/rds/postgres"
    )["SecretString"]
)

# Read data from RDS PostgreSQL
url = f"jdbc:postgresql://{secret['host']}:{secret['port']}/{secret['dbname']}"

df = spark.read \
    .format("jdbc") \
    .option("url", url) \
    .option("dbtable", "banking_data") \
    .option("user", secret["username"]) \
    .option("password", secret["password"]) \
    .option("driver", "org.postgresql.Driver") \
    .load()

# Save as Parquet in S3
df.write.mode("overwrite").parquet(
    "s3a://practicebanking/raw/banking_data/"
)

spark.stop()

