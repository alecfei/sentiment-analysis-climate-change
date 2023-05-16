## Sentiment analysis on Irish weather

In this project, the author initially planned to build a maven project using Kafka to stream tweets about Irish weather in the past two years and then initiate sentimental analysis and make prediction of the sentiment at one week, one month and three months going forward. It is an time-series oriented analysis. However, due to the change made by Twitter company recently, gaining higher level of its API access is problematic for individuals. Therefore, the author downloaded the required data from the archive instead. 

### Apache Maven and Apache Kafka
Apache Maven is an useful tool for build and monitor projects either from scratch or with existing archetypes. Besides, Maven also has many available remote repositories that can be added according to the project we want to create (https://mvnrepository.com/) for use. For example, to build a project using Apache Kafka to stream tweets and put them into a created topic and then consume from it and potentially transfer the data into an ideal database storage system for future use, kafka-clients and twitter-api-java-sdk are the two essential dependencies needed. The my-test folder displayed the simple pipeline of the whole streaming process created by author. However, due to the restricted access level of the API keys, only recent tweets can be retrieved, which does not meet the main purpose of this project. In a real-world project within companies and organisations, this approach would be more feasible.

### Download data from archive


