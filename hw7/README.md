HW_7 README

In this homework, we conducted experiments of:
(1) measure the communication time for our clusters by using the ping-pong method;
(2) examine the impact of latency hiding method on communication time.

As a result, the point to point communication time is recorded as following:
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

Moreover, we found that latency hiding method actually shorten the communication time and improved the rate of data transportation. The comparison result is showed in "HW7.png".

