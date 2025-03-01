# -*- coding: utf-8 -*-
"""kafka project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_uiQNM-HTqCc5JDoVW-iiEfra2WcklFa
"""

!pip install kafka-python

pip install pyspark kafka-python matplotlib

!bin/zookeeper-server-start.sh config/zookeeper.properties

!bin/kafka-server-start.sh config/server.properties

import random
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from kafka import KafkaProducer, KafkaConsumer
import json
import matplotlib.pyplot as plt

# 1. Generate student data (10000 students and 6 subjects)
subjects = ['Electronics', 'Programming', 'Database', 'Data Science', 'Mathematics', 'DSA']
students_data = []

for student_id in range(1, 10001):
    marks = [random.randint(0, 100) for _ in subjects]
    student_record = [student_id] + marks
    students_data.append(student_record)

# Save the data to a CSV file
with open('student_marks.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Student_ID', 'Electronics', 'Programming', 'Database', 'Data Science', 'Mathematics', 'DSA'])
    writer.writerows(students_data)

# 2. Process data using Spark
spark = SparkSession.builder.appName("Result Management System").getOrCreate()
student_df = spark.read.csv('student_marks.csv', header=True, inferSchema=True)

# Calculate total and average marks
student_df = student_df.withColumn('Total_Marks', sum(col(subject) for subject in student_df.columns[1:]))
student_df = student_df.withColumn('Average_Marks', col('Total_Marks') / 6)

# Show subject-wise average marks
subject_averages = student_df.select(*[col(subject).alias(subject) for subject in student_df.columns[1:]]).agg(*[avg(col(subject)) for subject in student_df.columns[1:]])
subject_averages.show()

# Save the processed data
student_df.write.mode("overwrite").csv('processed_student_data.csv')


# 3. Kafka Producer (sending statistics to Kafka)
from kafka import KafkaProducer
import json

# Kafka Producer (sending statistics to Kafka)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # Change to your Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sending a message
data = {'student_id': 12345, 'average_marks': 80}
producer.send('student_results', value=data)

# Close the producer
producer.close()

# Example statistics
stats_data = {
    'total_students': 10000,
    'average_marks': 75,
    'highest_marks': 98,
    'lowest_marks': 40,
}

# Send data to Kafka topic
producer.send('student_statistics_topic', stats_data)

# 4. Kafka Consumer (receiving statistics from Kafka)
consumer = KafkaConsumer(
    'student_statistics_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='result-consumers',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume and print the received message
for message in consumer:
    print("Received message:", message.value)
    break  # Exit after receiving the first message

# 5. Store Feedback
def store_feedback(student_id, feedback):
    with open('student_feedback.txt', 'a') as file:
        file.write(f'{student_id},{feedback}\n')

# Example feedback
store_feedback(1, "Happy with results")
store_feedback(2, "Not happy with results")

# 6. Display Dashboard (matplotlib for visualization)
subjects = ['Electronics', 'Programming', 'Database', 'Data Science', 'Mathematics', 'DSA']
average_marks = [70, 80, 65, 75, 60, 85]  # You can replace this with actual calculated averages

plt.bar(subjects, average_marks)
plt.xlabel('Subjects')
plt.ylabel('Average Marks')
plt.title('Subject-wise Average Marks')
plt.show()

bootstrap_servers=['localhost:9092']

bootstrap_servers=['<cloud_kafka_broker>:9092']

import os
os.system('netstat -an | grep 9092')
import subprocess
subprocess.run('netstat -an | grep 9092', shell=True)

pip install pyspark kafka-python matplotlib