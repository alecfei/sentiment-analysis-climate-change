## Sentimental analysis on climate change

In this project, the author initially planned to build a maven project using Kafka to stream tweets about Irish weather in the past two years and then initiate sentimental analysis and make prediction of the sentiment at one week, one month and three months going forward. Overall, it is an time-series oriented analysis. 

However, due to the change made by Twitter company recently, gaining its API authentication with full access is problematic and expensive for individuals. Thereafter, the author tried to collect data utilising an efficient scraping tool, however, we encountered some major problems. Eventually, we downloaded a dataset from Kaggle for study.

---

- **Apache Maven and Apache Kafka**

*Apache Maven is an useful tool for build and monitor java projects either from scratch or with existing archetypes. Besides, Maven also has many available [remote repositories](https://mvnrepository.com/) that can be added according to the project we want to create for use. For example, to build a project using Apache Kafka to stream tweets and put them into a created topic and then consume from it and potentially transfer the data into an ideal database storage system for future use, kafka-clients and twitter-api-java-sdk are the two essential dependencies needed. The ***my-test folder*** displayed a simple pipeline of the whole streaming process created by author. However, due to the restricted access level of the API keys, only recent tweets can be retrieved through experimentation, which does not meet the purpose of this study. But it is worth noting that this approach would be more feasible within companies and organisations where supplementary budget could be guaranteed.*

- **Collect data using *snscrape* library**

*Alternatively, the author found an useful python library - **snscrape** - that can efficiently scrape tweets posted in relate to Irish weather from 2018-01-01 to 2023-05-01. However, the data collected were too small (see in ***sample folder***). Therefore, the topic was expanded to the weather globally.* 

*Through experimenting, the "#weather" topic turned out to be too general. The retrieval of the tweets was extremely time-consuming. As a result, we narrowed down to **#global warming** and made some adjustments when scraping data, such as setting limitation on the number of tweets being collected (see in ***sample folder***). However, besides the duplicating issue, one fatal issue was the continuity of the timestamp which would seriously affect our analysis. To ensure the validity of the research, the author downloaded a dataset with comments about climate change until the end of August 2022 from Kaggle.*

---

### Download data

The original data from `Kaggle` is owned by Lexyr and collected using [SocialGrep Exports](https://socialgrep.com/exports). This dataset contains all the posts and comments on Reddit mentioning the terms "climate" and "change", all the way until 2022-08-31. To preserve users' anonymity and to prevent targeted harassment, the data does not include usernames.

### Database benchmarking

Before determining which databases to use for storing the raw and processed data, we use `YCSB` (Yahoo! Cloud Serving Benchmark) as a tool to test the performance of each database, i.e. MySQL, MongoDB, Apache Cassandra and Apache Hbase. Workloada and workloadb were evaluated. Workloada has ratios of 50% for inserting, 40% for reading and 10% for updating. On the other hand, workloadb is more reading focused (90% read and 10% update).

Additionally, we set the recordcount and operationcount both to 10000. Ideally, configuring the count close to the actual number in our dataset can provide a more precise information. But considering the running time with higher counts, especially in MySQL, we decided on 10000 to provide some general insights. Results see in ***benchmark testing*** folder. After comparison, we decided to use MongoDB for the raw dataset and Hbase for the processed one.

### Upload original data onto MongoDB and modify

- The following code was used to upload local datset onto `MongoDB` server (a `database` called **climate_change** and a new `collection` named **original** were created beforehand):

```bash
mongoimport --db climate_change --collection original --file /home/alec_fei/Downloads/the-reddit-climate-change-dataset-comments.csv --type csv --headerline
```

- After that, we made some neccessary modification (another `collection` **modified** was created for storing):
  * Deleting `documents` that are before 2021-09-01, which is labelled as 1630435200 in created_utc timestamp;
  * Dropping unneccessary `documents`, i.e. "_id", "type", "id", "subreddit", "permalink", "sentiment" and "score";
  * Transforming the UTC timestamp into a more readable version;
  * Changing the `field names` of the documents.

### Process on Hadoop system using Mapreduce and Apache Spark

The documents in modified collection on MongoDB became our final data for processing and analysing. We then export the data to our local machine using the code below:

```bash
mongoexport --db climate_change --collection modified --out /home/alec_fei/Downloads/climate_change_reddit.json
```

The exported json file was then uploaded onto `Hadoop` manually. Processing and analysing were implemented afterwards based on HDFS.

#### *Mapreduce*

- word count in "type" field

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar -file ./wordCountMapper.py -mapper ./wordCountMapper.py -file ./wordCountReducer.py -reducer ./wordCountReducer.py -input /climate_change/climate_change_reddit.json -output /output/word_count
```

- top 10 single-word in "text" field

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar -file ./topTenSingleWordMapper.py -mapper ./topTenSingleWordMapper.py -file ./topTenSingleWordReducer.py -reducer ./topTenSingleWordReducer.py -input /climate_change/climate_change_reddit.json -output /output/top10_single_word
```

- top 10 double-words in "text" field

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar -file ./topTenDoubleWordMapper.py -mapper ./topTenDoubleWordMapper.py -file ./topTenDoubleWordReducer.py -reducer ./topTenDoubleWordReducer.py -input /climate_change/climate_change_reddit.json -output /output/top10_double_word
```

- top 10 triple-words in "text" field

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar -file ./topTenTripleWordMapper.py -mapper ./topTenTripleWordMapper.py -file ./topTenTripleWordReducer.py -reducer ./topTenTripleWordReducer.py -input /climate_change/climate_change_reddit.json -output /output/top10_triple_word
```

- dropping fields, i.e. "_id", "type"

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar -file ./dropFieldsMapper.py -mapper ./dropFieldsMapper.py -file ./dropFieldsReducer.py -reducer ./dropFieldsReducer.py -input /climate_change/climate_change_reddit.json -output /climate_change_dropped
```

- text processing

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.4.jar -file ./textProcessingMapper.py -mapper ./textProcessingMapper.py -file ./textProcessingReducer.py -reducer ./textProcessingReducer.py -input /climate_change_dropped/part-00000 -output /climate_change_processed/climate_change_processed
```


#### *Apache Spark*


?MongoDB connector and happybase?

##### References

- [Apache Kafka](https://kafka.apache.org/)
- [Apache Maven](https://maven.apache.org/)
- [Kafka_Harshali](https://github.com/Harshali15/Real-WorldProject-Kafka)
- [Kafka_Twitter_David](https://github.com/david-romero/demo-twitter-kafka/tree/master)
- [Snscrape](https://github.com/JustAnotherArchivist/snscrape)
- [Kaggle Dataset](https://www.kaggle.com/datasets/pavellexyr/the-reddit-climate-change-dataset?select=the-reddit-climate-change-dataset-posts.csv)
- [YCSB](https://github.com/brianfrankcooper/YCSB/tree/master)
- [MongoDB Tutorial](https://www.tutorialspoint.com/mongodb/index.htm)
- [Apache Hadoop](https://hadoop.apache.org/)
- [Mrjob_Yelp](https://github.com/Yelp/mrjob/tree/master)
- [Apache Hbase](https://hbase.apache.org/book.html#quickstart)

