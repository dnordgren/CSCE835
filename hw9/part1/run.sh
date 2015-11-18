#!/bin/sh

# mkdir 
hdfs dfs -mkdir /hw9_1

# input files

#chmod 777 full_wordcount_text.txt
#sudo chown hdfs:hdfs full_wordcount_text.txt
hadoop fs -put full_wordcount_text.txt /hw9_1/

# complie the hadoop code
hadoop com.sun.tools.javac.Main WordCount1.java
jar cf wc1.jar WordCount1*.class

hadoop com.sun.tools.javac.Main WordCount2.java
jar cf wc2.jar WordCount2*.class


# clean the out files form pervious run
rm -fr out1/
rm -fr out2/
hadoop fs -rm -f -r /hw9_1/counts.txt/
hadoop fs -rm -f -r /hw9_1/out/*

# run hadoop 
hadoop jar wc1.jar WordCount1 /hw9_1/full_wordcount_text.txt  /hw9_1/out/out1  

# get the output
hadoop fs -get /hw9_1/out/out1
hadoop fs -put ./out1/part-r-00000 /hw9_1/counts.txt

# sort 
hadoop jar wc2.jar WordCount2 /hw9_1/counts.txt  /hw9_1/out/out2

hadoop fs -get /hw9_1/out/out2

cp ./out2/part-r-00000 ./wc_sored.txt
awk '{print $2,"\t",$1}' ./wc_sored.txt > ./wc_sored_word_counts.txt
