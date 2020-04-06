import sys
import string, re
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

schema = types.StructType([ # commented-out fields won't be read
    #types.StructField('archived', types.BooleanType(), False),
    #types.StructField('author_flair_css_class', types.StringType(), False),
    #types.StructField('author_flair_text', types.StringType(), False),
])


def main(in_directory, out_directory):

    sentences = spark.read.text(in_directory)
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
    sentences = sentences.select(functions.explode(functions.split(sentences.value, wordbreak)).alias('words')).collect() #https://stackoverflow.com/questions/38210507/explode-in-pyspark
    sentences = spark.createDataFrame(sentences)
    sentences = sentences.select(functions.lower(sentences.words).alias('words')) \
                .filter(sentences.words != "")
    sentences = sentences.groupBy('words').agg(functions.count('*').alias('count'))
    sentences = sentences.orderBy(['count', 'words'], ascending=[0,1]) #https://stackoverflow.com/questions/50824543/how-to-sort-a-dataframe-in-pyspark
    sentences.write.csv(out_directory)


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
