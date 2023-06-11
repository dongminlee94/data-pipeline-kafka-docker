FROM confluentinc/cp-kafka-connect:7.3.0

RUN confluent-hub install --no-prompt snowflakeinc/snowflake-kafka-connector:1.5.5 \
  && confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.2.2 \
  && confluent-hub install --no-prompt confluentinc/kafka-connect-avro-converter:7.3.0 \
  && confluent-hub install --no-prompt confluentinc/kafka-connect-s3:10.5.1
