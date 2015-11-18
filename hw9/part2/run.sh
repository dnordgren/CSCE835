#!/bin/sh

export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.91.x86_64/
export HADOOP_CLASSPATH=$JAVA_HOME/lib/tools.jar
export HADOOP_HOME=/usr/lib/hadoop-0.20-mapreduce

# mkdir 
hdfs dfs -mkdir /hw9_2

# input files
hadoop fs -put uid_of_friends.txt  /hw9_2/

# complie the hadoop code
hadoop com.sun.tools.javac.Main MutualFriendFinder.java
jar cf mff.jar MutualFriendFinder*.class

# clean the out files form pervious run
rm -fr out/
hadoop fs -rm -f -r /hw9_2/out

# run hadoop 
hadoop jar mff.jar MutualFriendFinder /hw9_2/uid_of_friends.txt /hw9_2/out

#get output
hadoop fs -get /hw9_2/out

cp ./out/part-r-00000 ./MutualFriendFinder.txt

