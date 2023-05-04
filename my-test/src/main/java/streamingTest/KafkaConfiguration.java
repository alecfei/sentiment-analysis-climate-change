package streamingTest;

public class KafkaConfiguration {
    public static final String BOOTSTRAPSERVERS = "localhost:9092";
    public static final String TOPIC = "irish weather";
    public static final String ACKS_CONFIG = "all";
    public static final String MAX_IN_FLIGHT_CONN = "5";
    public static final String COMPRESSION_TYPE = "snappy";
    public static final String RETRIES_CONFIG = Integer.toString(Integer.MAX_VALUE);
    public static final String LINGER_CONFIG = "20";
    public static final String BATCH_SIZE = Integer.toString(32*1024);
    public static final long SLEEP_TIMER = 1000;
}
