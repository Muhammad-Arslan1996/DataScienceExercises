import sys
from pyspark.sql import SparkSession, functions, types
import os


spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


comments_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('number_of_requests', types.StringType()),
    types.StructField('number_of_bytes', types.LongType()),
])

def getFileName(x):
    head,tail = os.path.split(x)
    #https://www.geeksforgeeks.org/python-os-path-split-method/
    result = tail[11:-7]
    return result

def main(in_directory, out_directory):
    df = spark.read.csv(in_directory, schema=comments_schema, sep=' ').withColumn('filename', functions.input_file_name())
    path_to_hour = functions.udf(getFileName, returnType=types.StringType())
    df = df.select(
        df['language'],
        df['title'],
        df['number_of_requests'],
        path_to_hour(df['filename']).alias('filename')
    )

    df = df.filter(
        (df['language'] == 'en')
        & (df['title'] != 'Main Page')
        & (functions.substring(df['title'], 0, 8) != 'Special:'))

    grouped = df.groupBy('filename', 'title')
    count = grouped.agg(functions.sum(df['number_of_requests']).alias('count'))

    grouped2 = count.groupBy('filename')
    maxi = grouped2.agg(functions.max(count['count']))

    joined = count.join(maxi, on = 'filename')
    joined = joined.filter(joined['count'] == joined['max(count)'])\
    .select(joined['filename'], joined['title'], joined['count'])
    joined = joined.cache()
    sorted_ = joined.sort('filename', 'title')

    sorted_.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
