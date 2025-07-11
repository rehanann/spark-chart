from pyspark.sql import SparkSession

# MinIO configuration
minio_access_key = "bU0c4naTz98KynxEsHf1"
minio_secret_key = "dNOkRi7cbUsw0ZHnN9coosKO0iyu21XJpieAayZd"
minio_endpoint = "http://minio.default.svc.cluster.local:9000"  # or "http://minio.default.svc.cluster.local:9000"
output_path = "s3a://historyservice/logs"  # Target path in MinIO

# Create SparkSession with S3A/MinIO support
spark = SparkSession.builder \
    .appName("WriteParquetToMinIO") \
    .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint) \
    .config("spark.hadoop.fs.s3a.access.key", minio_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key) \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

# Sample DataFrame
data = [("Alice", 1), ("Bob", 2), ("Charlie", 3), ("David", 4), ("Eve", 5)]
columns = ["Name", "ID"]
df = spark.createDataFrame(data, columns)

# Print the DataFrame
print("Showing DataFrame contents before writing to Parquet:")
df.show()

# Write as Parquet to MinIO
df.write.format("parquet").mode("overwrite").save(output_path)
print(f"✅ Data written to Parquet at: {output_path}")

# Read the data back from MinIO
df_read = spark.read.format("parquet").load(output_path)

# Print read-back DataFrame
print("✅ DataFrame read back from S3A (MinIO):")
df_read.show()

spark.stop()
