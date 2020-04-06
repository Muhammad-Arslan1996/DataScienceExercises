import sys
import numpy as np
from pyspark.sql import SparkSession, functions, types, Row
from math import sqrt
import re

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        rdd_object = "{},{}".format(m.group(1), m.group(2))
        hostname, number_of_bytes = rdd_object.split(',')
        return Row(hostname = hostname, number_of_bytes = int(number_of_bytes))
    else:
        return None

def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    log_lines = log_lines.map(line_to_row) \
        .filter(not_none)
    return log_lines
    # TODO: return an RDD of Row() objects


def main(in_directory):
    logs = spark.createDataFrame(
    create_row_rdd(in_directory),
    schema = 'hostname:string, number_of_bytes:int')
    logs = logs.cache()
    count = logs.groupBy(logs.hostname).agg(functions.count(logs['hostname']).alias('count_requests(x)'))
    sum_ = logs.groupBy(logs.hostname).agg(functions.sum(logs['number_of_bytes']).alias('sum_request_bytes(y)'))
    joined = count.join(sum_, on='hostname').drop('hostname')
    joined = joined.withColumn('x^2', joined['count_requests(x)']**2).\
        withColumn('y^2', joined['sum_request_bytes(y)']**2) .\
        withColumn('xy', joined['count_requests(x)'] * joined['sum_request_bytes(y)']).\
        withColumn('ones', functions.lit(1))
    #for multiple add columns https://stackoverflow.com/questions/46222077/how-to-add-multiple-row-and-multiple-column-from-single-row-in-pyspark
    #lit function: https://stackoverflow.com/questions/38587609/spark-add-new-column-with-the-same-value-in-scala
    total = joined.groupBy()
    total = total.agg(functions.sum(joined['ones']),
        functions.sum(joined['count_requests(x)']),
        functions.sum(joined['sum_request_bytes(y)']),
        functions.sum(joined['x^2']),
        functions.sum(joined['y^2']),
        functions.sum(joined['xy']))
    total = total.first()
    n = total['sum(ones)']
    x = total['sum(count_requests(x))']
    y = total['sum(sum_request_bytes(y))']
    xy = total['sum(xy)']
    x_2 = total['sum(x^2)']
    y_2 = total['sum(y^2)']
    r = (n*xy - x*y)/(sqrt(n*x_2 - x**2) * sqrt(n*y_2 - y**2))

    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
