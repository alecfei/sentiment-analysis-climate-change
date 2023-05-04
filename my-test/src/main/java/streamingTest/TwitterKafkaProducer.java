package streamingTest;

import com.google.gson.Gson;
import com.twitter.hbc.ClientBuilder;
import com.twitter.hbc.core.Client;
import com.twitter.hbc.core.Constants;
import com.twitter.hbc.core.endpoint.StatusesFilterEndpoint;
import com.twitter.hbc.core.processor.StringDelimitedProcessor;
import com.twitter.hbc.httpclient.auth.Authentication;
import com.twitter.hbc.httpclient.auth.OAuth1;
import streamingTest.KafkaConfiguration;
import streamingTest.TwitterConfiguration;
import streamingTest.TweetDetails;
import streamingTest.BasicCallback;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.LongSerializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;


public class TwitterKafkaProducer {
    private Client client;
    private BlockingQueue<String> queue;
    private Gson gson;
    private Callback callback;

    public TwitterKafkaProducer() {
        // Configuring authentication of using twitter API
        Authentication authentication = new OAuth1(
                TwitterConfiguration.CONSUMER_KEY,
                TwitterConfiguration.CONSUMER_SECRET,
                TwitterConfiguration.ACCESS_TOKEN,
                TwitterConfiguration.TOKEN_SECRET);

        // Limiting streaming topic, i.e. irish weather
        StatusesFilterEndpoint endpoint = new StatusesFilterEndpoint();
        endpoint.trackTerms(Collections.singletonList(TwitterConfiguration.HASHTAG));

        queue = new LinkedBlockingQueue<>(10000);

        client = new ClientBuilder()
                .hosts(Constants.STREAM_HOST)
                .authentication(authentication)
                .endpoint(endpoint)
                .processor(new StringDelimitedProcessor(queue))
                .build();
        gson = new Gson();
        callback = new BasicCallback();
    }

    // Kafka producer
    private Producer<Long, String> getProducer() {
        // Creating producer properties
        Properties properties = new Properties();
        properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, KafkaConfiguration.BOOTSTRAPSERVERS);
        properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, LongSerializer.class.getName());
        properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        
        // Creating safer producer
        properties.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "ture");
        properties.put(ProducerConfig.ACKS_CONFIG, KafkaConfiguration.ACKS_CONFIG);
        properties.put(ProducerConfig.RETRIES_CONFIG, KafkaConfiguration.RETRIES_CONFIG);
        properties.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, KafkaConfiguration.MAX_IN_FLIGHT_CONN);
        
        // Adding more setting for higher performance
        properties.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, KafkaConfiguration.COMPRESSION_TYPE);
        properties.put(ProducerConfig.LINGER_MS_CONFIG, KafkaConfiguration.LINGER_CONFIG);
        properties.put(ProducerConfig.BATCH_SIZE_CONFIG, KafkaConfiguration.BATCH_SIZE);

        // Finalising
        return new KafkaProducer<>(properties);
    }

    public void run() {
        client.connect();
        try (Producer<Long, String> producer = getProducer()) {
            while (true) {
                TweetDetails tweet = gson.fromJson(queue.take(), TweetDetails.class);
                System.out.printf("Fetched tweet id %d\n", tweet.getId());
                long key = tweet.getId();
                String msg = tweet.toString();
                ProducerRecord<Long, String> record = new ProducerRecord<>(KafkaConfiguration.TOPIC, key, msg);
                producer.send(record, callback);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            client.stop();
        }
    }
}
