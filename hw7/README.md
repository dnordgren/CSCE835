HW_7 README

In this homework, we conducted experiments of:
(1) measure the communication time for our clusters by using the ping-pong method;
(2) examine the impact of latency hiding method on communication time.

As a result, the point to point communication time is recorded as following(hw7.out):

Here n is the size of the message being sent. Increase the size of the message exponentially on every ping. We multiply n with size of double and this buffer as the message.

```
Kind		n	time (sec)	Rate (MB/sec)
Send/Recv	1	0.000002	4.969187
Send/Recv	2	0.000002	10.171092
Send/Recv	4	0.000002	20.591858
Send/Recv	8	0.000002	41.348653
Send/Recv	16	0.000002	66.109228
Send/Recv	32	0.000002	130.023424
Send/Recv	64	0.000003	194.049727
Send/Recv	128	0.000003	360.057139
Send/Recv	256	0.000004	510.293144
Send/Recv	512	0.000008	512.831916
Send/Recv	1024	0.000009	869.866794
Send/Recv	2048	0.000015	1126.548799
Send/Recv	4096	0.000024	1340.867839
Send/Recv	8192	0.000037	1750.814694
Send/Recv	16384	0.000068	1925.589541
Send/Recv	32768	0.000120	2183.737096
Send/Recv	65536	0.000234	2240.471987
Send/Recv	131072	0.000468	2238.191609
Send/Recv	262144	0.000929	2257.434370
Send/Recv	524288	0.001894	2215.082604
Send/Recv	1048576	0.004238	1979.151854
```
And the output we received latency hiding which was acheived by using non-blocking process(Isend and Irecv) was(hw7_2.out),

```
Kind		n	time (sec)	Rate (MB/sec)
Send/Recv	1	0.000002	3.682444
Send/Recv	2	0.000002	9.828480
Send/Recv	4	0.000001	27.027331
Send/Recv	8	0.000001	60.842125
Send/Recv	16	0.000002	82.698128
Send/Recv	32	0.000001	198.722367
```
We received segmentation errors and could not perform more than 32*8 bytes in a ping for non-blocking processes.
 
Moreover, we found that latency hiding method actually shorten the communication time and improved the rate of data transportation. The comparison result is showed in "HW7.png".

Instructions to run the code:
The first part of the assignment can be executed using the bin file ping_pong or by creating the bin file from ping_pong.c
The first part of the assignment can be executed using the bin file non_blocking or by creating the bin file from non_blocking.c

References:
1. https://www.hpc2n.umu.se/node/230


