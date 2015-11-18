import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount2 {

    // swap word and count
    public static class SortMapper
      extends Mapper<Object, Text, Text,Text>{
      // word and count
      private Text cou = new Text();
      private Text wor = new Text();

      public void map(Object key, Text values, Context context) 
        throws IOException, InterruptedException {
        StringTokenizer itr = new StringTokenizer(values.toString(),"\n");
        while (itr.hasMoreTokens()) {
          String record = itr.nextToken();
          
          String[] parts = record.split("\t");
          String p1 = String.format("%20s", parts[0]);
          String p2 = String.format("%5s", parts[1]);
          
          wor.set(p1);
          cou.set(p2);
          
          context.write(cou, wor);
        }
      }
    } 
    
    public static class SortReducer
       extends Reducer<Text, Text, Text, Text> {
       public void reduce(Text key, Text values, Context context) 
        throws IOException, InterruptedException {
          context.write(values, key);
        }
    }

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		
		Job sortjob = Job.getInstance(conf, "sorting");
		sortjob.setJarByClass(WordCount2.class);
		sortjob.setMapperClass(SortMapper.class);
		sortjob.setReducerClass(SortReducer.class);
		sortjob.setOutputKeyClass(Text.class);
		sortjob.setOutputValueClass(Text.class);
		
		// take the output of wc as input here
		FileInputFormat.addInputPath(sortjob, new Path(args[0] ));
		// generate a new output file with sorted count
		FileOutputFormat.setOutputPath(sortjob, new Path(args[1]));
		
		// exit after two jobs are finished
		System.exit(sortjob.waitForCompletion(true) ? 0 : 1);
	}
}
