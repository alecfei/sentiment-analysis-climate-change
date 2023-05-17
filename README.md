## Sentimental analysis on global warming 

In this project, the author initially planned to build a maven project using Kafka to stream tweets about Irish weather in the past two years and then initiate sentimental analysis and make prediction of the sentiment at one week, one month and three months going forward. Overall, it is an time-series oriented analysis. 

However, due to the change made by Twitter company recently, gaining its API authentication with full access is problematic and expensive for individuals. Therefore, the author downloaded the required data utilising an efficient scraping tool instead.

- **Apache Maven and Apache Kafka**

*Apache Maven is an useful tool for build and monitor projects either from scratch or with existing archetypes. Besides, Maven also has many available remote repositories that can be added according to the project we want to create (https://mvnrepository.com/) for use. For example, to build a project using Apache Kafka to stream tweets and put them into a created topic and then consume from it and potentially transfer the data into an ideal database storage system for future use, kafka-clients and twitter-api-java-sdk are the two essential dependencies needed. The ***my-test folder*** displayed a simple pipeline of the whole streaming process created by author. However, due to the restricted access level of the API keys, only recent tweets can be retrieved through experimentation, which does not meet the purpose of this study. But it is worth noting that this approach would be more feasible within companies and organisations where they have supplementary budget.*

### Collect data using *snscrape* library

Alternatively, the author found an useful python library - **snscrape** - that can efficiently scrape tweets posted in relate to Irish weather from 2018-01-01 to 2023-05-01. However, the data collected were too small (see ***"sample folder"***). Therefore, the topic was expanded to the weather globally. 

Unfortunately, through experimenting, the "#weather" topic turned out to be too general. The retrieval of the tweets was extremely time-consuming. As a result, we narrowed down to **#global warming** as the final topic. See ***collect tweets folder***.

### Transfer data into database


### Process tweets on Hadoop system using Mapreduce

#### References

- https://github.com/Harshali15/Real-WorldProject-Kafka
- https://github.com/david-romero/demo-twitter-kafka/tree/master
- https://github.com/JustAnotherArchivist/snscrape
