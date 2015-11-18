import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map.Entry;
 
import org.apache.commons.lang.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
 
public class MutualFriendFinder {
 
    private static final String IS_FRIEND = "IsFriendsWith";
    private static final String IS_MUTUAL_FRIEND = "IsMutualFriendsWith";
    private static final int MAX_RECOMMENDATION_COUNT = 5;
    
    public static class Map extends Mapper<LongWritable, Text, IntWritable, Text> {
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] group = line.split("\t");
            
            // For user's with no friends :(
            if(group.length == 2){
                String user = group[0];
                IntWritable userKey = new IntWritable(Integer.parseInt(user));
                if(!group[1].trim().isEmpty()){
                    String[] friends = group[1].split(",");
                    String directFriend;
                    IntWritable directFriendKey = new IntWritable();
                    Text directFriendValue = new Text();
                    String mutualFriend;
                    IntWritable mutualFriendKey = new IntWritable();
                    Text mutualFriendValue = new Text();
                    for (int i = 0; i < friends.length; i++) {
                        directFriend = friends[i];
                        directFriendValue.set(IS_FRIEND + "," + directFriend);
                        context.write(userKey, directFriendValue);   // User's direct friend
                        directFriendKey.set(Integer.parseInt(directFriend));
                        directFriendValue.set(IS_MUTUAL_FRIEND + "," + directFriend);
                        
                        for (int j = i+1; j < friends.length; j++) {
                            mutualFriend = friends[j];
                            mutualFriendKey.set(Integer.parseInt(mutualFriend));
                            mutualFriendValue.set(IS_MUTUAL_FRIEND + "," + mutualFriend);
                            context.write(directFriendKey, mutualFriendValue);   // User's direct friend is mutual friend with user's another friend
                            context.write(mutualFriendKey, directFriendValue);   // Vice - versa
                        }
                    }
                }
            }
        }
    } 
 
    public static class Reduce extends Reducer<IntWritable, Text, IntWritable, Text> {
        public void reduce(IntWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            String[] value;
            HashMap<String, Integer> mutualFriendCounter = new HashMap<>();
            for (Text val : values) {
                value = (val.toString()).split(",");
                String relation = value[0];
                String UID = value[1];
                if (relation.equals(IS_FRIEND)) { 
                    // User's friend already, don't include.
                    mutualFriendCounter.put(UID, -1);
                } else if (relation.equals(IS_MUTUAL_FRIEND)) { 
                    // Pair has a mutual friend, check if they are already friends
                    if (mutualFriendCounter.containsKey(UID)) {
                        if (mutualFriendCounter.get(UID) != -1) { 
                            // Increment mutual friend count
                            mutualFriendCounter.put(UID, mutualFriendCounter.get(UID) + 1);
                        }
                    } else {
                        // First mutual friend, insert into map
                        mutualFriendCounter.put(UID, 1);
                    }
                }
            }
            // Remove all the negative counts(already friends)
            ArrayList<Entry<String, Integer>> mutualFriends = new ArrayList<>();
            for (Entry<String, Integer> potentialMutualFriend : mutualFriendCounter.entrySet()) {
                // If not already a friend,  potential mutual friend becomes a mutual friend
                if (potentialMutualFriend.getValue() != -1) {
                    mutualFriends.add(potentialMutualFriend);
                }
            }
            
            // Sort mutual friends by frequency.
            Collections.sort(mutualFriends, new Comparator<Entry<String, Integer>>() {
                @Override
                public int compare(Entry<String, Integer> pair1, Entry<String, Integer> pair2) {
                    // Just comparing the value part of the entry.
                    return pair2.getValue().compareTo(pair1.getValue());
                }
            });
            
            ArrayList<String> recommendedFriends = new ArrayList<>();
            // If mutual friends are less than max needed recommended friends
            for (int i = 0; i < Math.min(MAX_RECOMMENDATION_COUNT, mutualFriends.size()); i++) {
                recommendedFriends.add(mutualFriends.get(i).getKey());
            }
            context.write(key, new Text(StringUtils.join(recommendedFriends, ",")));
            
        }
    }
 
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
 
        Job job = new Job(conf, "MutualFriendFinder");
        job.setJarByClass(MutualFriendFinder.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
 
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
 
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
 
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
 
        job.waitForCompletion(true);
    }
}
