from pyspark.sql import SparkSession



# Create SparkSession
spark = SparkSession.builder \
    .appName("readdata") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

# Sample DataFrame
data = [("Alice", 1), ("Bob", 2), ("Charlie", 3), ("David", 4), ("Eve", 5)]
columns = ["Name", "ID"]
df = spark.createDataFrame(data, columns)

# Show DataFrame
df.show()
