---
layout: post
title: 'Benchmarking a Go AI in Ruby: CRuby vs. Rubinius vs. JRuby vs. Truffle/Graal'
description: None
date: 2015-11-30 17:48:34 -0000
last_modified_at: 2020-08-29 07:46:35 -0000
publish: true
pin: false
categories:
- Ruby
- Software Engineering
tags:
- AI
- benchmark
- CRuby
- Go
- JRuby
- Monte Carlo Tree Search
- performance
- Rubinius
- ruby
- rubykon
- TruffleRuby
---
The world of Artificial Intelligences is often full of performance questions. How fast can I compute a value? How far can I look ahead in a tree? How many nodes can I traverse?

In Monte Carlo Tree Search one of the most defining questions is "How many simulations can I run per second?". If you want to learn more about Monte Carlo Tree Search and its application to the board game Go I recommend you [the video and slides of my talk about that topic from Rubyconf 2015](https://pragtob.wordpress.com/2015/11/21/slides-beating-go-thanks-to-the-power-of-randomness-rubyconf-2015/).

Implementing my own AI - [rubykon](https://github.com/PragTob/rubykon) \- in ruby of course isn't going to get me the fastest implementation ever. It forces you to really do less and therefore make nice performance optimization, though. This isn't about that either. Here I want to take a look at another question: **"How fast can Ruby go?"** Ruby is a language with surprisingly many well maintained implementations. Most prominently [CRuby](https://www.ruby-lang.org/en/), [Rubinius](http://rubini.us/), [JRuby](http://jruby.org/) and the newcomer [JRuby + Truffle](https://github.com/jruby/jruby/wiki/Truffle). How do they perform in this task?

### The project

[Rubykon](https://github.com/PragTob/rubykon) is a relatively small project - right now the lib directory has less than 1200 lines of code (which includes a small benchmarking library... more on that later). It has no external runtime dependencies - not even the standard library. So it is very minimalistic and also tuned for performance.

### Setup

The benchmarks were run pre the 0.3.0 rubykon version on the 8th of November (sorry writeups always take longer than you think!) with the following concrete ruby versions (versions slightly abbreviated in the rest of the post):

* CRuby 1.9.3p551
* CRuby 2.2.3p173
* Rubinius 2.5.8
* JRuby 1.7.22
* JRuby 9.0.3.0
* JRuby 9.0.3.0 run in server mode and with invoke dynamic enabled (denoted as + id)
* JRuby + Truffle Graal with master from 2015-11-08 and commit hash fd2c179, running on graalvm-jdk1.8.0

You can find the raw data (performance numbers, concrete version outputs, benchmark results for different board sizes and historic benchmark results) in [this file](https://github.com/PragTob/rubykon/blob/master/benchmark/results/HISTORY.md). This was run on my pretty dated desktop PC (i7 870): 

```text
tobi@tobi-desktop ~ $ uname -a
Linux tobi-desktop 3.16.0-38-generic #52~14.04.1-Ubuntu SMP Fri May 8 09:43:57 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux

tobi@tobi-desktop ~ $ java -version
openjdk version "1.8.0_45-internal"
OpenJDK Runtime Environment (build 1.8.0_45-internal-b14)
OpenJDK 64-Bit Server VM (build 25.45-b02, mixed mode)

tobi@tobi-desktop ~ $ lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                8
On-line CPU(s) list:   0-7
Thread(s) per core:    2
Core(s) per socket:    4
Socket(s):             1
NUMA node(s):          1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 30
Stepping:              5
CPU MHz:               1200.000
BogoMIPS:              5887.87
Virtualization:        VT-x
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              8192K
NUMA node0 CPU(s):     0-7
```


### First benchmark: Simulation + Scoring on 19x19

This benchmark uses benchmark-ips to see how many playouts (simulation + scoring) can be done per second. This is basically the "evaluation function" of the Monte Carlo Method. Here we start with an empty board and then play random valid moves until there are no valid moves anymore and then we score the game. The performance of a MCTS AI is hugely dependent on how fast that can happen. Benchmarks were run with a warmup time of 60 seconds and a run time of 30 seconds. The small black bars in the graph denote standard deviation. Results: ![19_19_ips.png](https://pragtob.wordpress.com/wp-content/uploads/2015/11/19_19_ips.png) Full 19x19 playout, iterations per second (higher is better)  Ruby Version | iterations per second | standard deviation  
---|---|---  
CRuby 1.9.3p551 | 44.952 | 8.90%  
CRuby 2.2.3p173 | 55.403 | 7.20%  
Rubinius 2.5.8 | 40.911 | 4.90%  
JRuby 1.7.22 | 63.456 | 15.80%  
JRuby 9.0.3.0 | 73.479 | 6.80%  
JRuby 9.0.3.0 + invoke dynamic | 121.265 | 14.00%  
JRuby + Truffle | 192.42 | 14.00%  
  
JRuby + Truffle runs on a [slightly modified version of benchmark-ips](https://github.com/PragTob/rubykon/blob/master/benchmark/support/benchmark-ips_shim.rb). This is done because it is a highly optimizing and speculative runtime that leads to bad results after warmup. This is explained [here](https://github.com/jruby/jruby/issues/3355#issuecomment-145352041).

### Second benchmark: Full UCT Monte Carlo Tree Search with 1000 playouts

This benchmark does a full Monte Carlo Tree Search, meaning choosing a node to investigate, doing a full simulation and scoring there and then propagating the results back in the tree before starting over again. As the performance is mostly dependent on the playouts the graph looks a lot like the one above. This uses [benchmark-avg](https://github.com/PragTob/rubykon/tree/master/lib/benchmark/avg), which I wrote myself and (for now) still lives in the rubykon repository. Why a new benchmarking library? In short: I needed something for more "macro" benchmarks that gives nice output like benchmark-ips. Also, I wanted a benchmarking tool that plays nice with Truffle - which means doing warmup and run of a benchmark directly after one another, as [detailed in this issue](https://github.com/jruby/jruby/issues/3387). This uses a warmup time of 3 minutes and a run time of 2 minutes. Along with the iterations per minute, we have another graph depicting average run time. ![19_19_ipm.png](https://pragtob.wordpress.com/wp-content/uploads/2015/11/19_19_ipm.png) MCTS on 19x19 with 1000 playouts, iterations per minute (higher is better) ![19_19_avg.png](https://pragtob.wordpress.com/wp-content/uploads/2015/11/19_19_avg.png) MCTS on 19x19 with 1000 playouts, average run time (lower is better)  Ruby Version | iterations per minute | average time (s) | standard deviation  
---|---|---|---  
CRuby 1.9.3p551 | 1.61 | 37.26 | 2.23%  
CRuby 2.2.3p173 | 2.72 | 22.09 | 1.05%  
Rubinius 2.5.8 | 2.1 | 28.52 | 2.59%  
JRuby 1.7.22 | 3.94 | 15.23 | 1.61%  
JRuby 9.0.3.0 | 3.7 | 16.23 | 2.48%  
JRuby 9.0.3.0 + invoke dynamic | 7.02 | 8.55 | 1.92%  
JRuby + Truffle | 9.49 | 6.32 | 8.33%  
Results here pretty much mirror the previous benchmark, although standard deviation is smaller throughout which might be because more non random code execution is involved. Otherwise the relative performance of the different implementations is more or less the same, with the notable exception of JRuby 1.7 performing better than 9.0 (without invoke dynamic). That could be an oddity, but it is also well within the margin of error for the first benchmark. For the discussion below I'll refer to this benchmark, as it ran on the same code for all implementations and has a lower standard deviation overall.

### Observations

The most striking observation certainly is JRuby + Truffle/Graal sits atop in the benchmarks with a good margin. It's not that surprising when you look at previous work done here [suggesting speedups of 9x to 45x as compared to CRuby](http://chrisseaton.com/rubytruffle/pushing-pixels/). Here the speedup relative to CRuby is "just" 3.5 which teaches us to always run your own benchmarks. It is also worth noting that Truffle first was unexpectedly very slow (10 times slower than 1.9) so [I opened an issue and reported that somewhat surprising lack in performance](https://github.com/jruby/jruby/issues/3355). Then Chris Season was quick to fix it and along the way he kept an amazing log of things he did to diagnose and make it faster. If you ever wanted to take a peek into the mind of a Ruby implementer - go ahead and [read it](https://github.com/jruby/jruby/issues/3355)! At the same time I gotta say that the warmup time it takes has got me worried a bit. This is a very small application with one very hot loop (generating the valid moves). It doesn't even use the standard library. The warmup times are rather huge exactly for Truffle and I made sure to call no other code in benchmark/avg as this might deoptimize everything again. However, it is still in an early stage and I know they are working on it :) Second, "normal" JRuby is faster than CRuby which is not much of a surprise to me - in most benchmarks I do JRuby comes up ~twice as fast CRuby. So when it was only ~30% faster I was actually a bit disappointed, but then remembered the `--server -Xcompile.invokedynamic=true` switches and enabled them. BOOM! Almost 2.6 times faster than CRuby! Almost 90% faster than JRuby without those switches. Now you might ask: "Why isn't this the default?" Well, it was the default. Optimizing takes time and that slows down the startup time, for say rails, significantly which is why [it was deactivated by default](https://github.com/jruby/jruby/issues/1858#issuecomment-53601054). If I'm missing any of these magic switches for any of the other implementations please let me know and I'll add them. I'm also a bit sad to see rubinius somewhere between 1.9 and 2.2 performance wise, I had higher hopes for its performance with some appropriate warmup time. Also [opal](http://opalrb.org/) is notably missing, I couldn't get it to run but will try again in a next version to see what V8 can optimize here. An important word of warning to conclude the high level look at the different implementations: **These benchmarks are most likely not true for your application! Especially not for rails! Benchmark yourself :)** Now for another question that you probably have on your mind: **"How fast is this compared to other languages/implementations?"** See, that's hard to answer. No serious Go engine does pure random playouts, they all use some heuristics slowing them down significantly. But, they are still faster. Here's some data from [this computer go thread](http://computer-go.org/pipermail/computer-go/2015-October/008036.html), they all refer to the 19x19 board size:

* it is suggested than one should be able to do at least 100 000 playouts per second without heuristics
* With _light_ playouts Aya did 25 000 playouts in 2008
* well known C engine [pachi](https://github.com/pasky/pachi) does 2000 heavy playouts per thread per second

Which leads us to the question...

### Is this the end of the line for Ruby?

No, there are still a couple of improvements that I have in mind that can make it much faster. How much faster? I don't know. I have this goal of 1000 playouts on 19x19 per second per thread in mind. It's still way behind other languages, but hey we're talking about Ruby here ;) Some possible improvements:

* Move generation can still be improved a lot, instead of always looking for a new valid random moves a list of valid moves could be kept around, but it's tricky
* Scoring can also be done faster by leveraging neighbouring cells, but it's not the bottleneck (yet)
* a very clever but less accurate data structure can be used for liberty counting
* also, of course, actually parallelize it and run on multiple threads
* I could also use an up to date CPU for a change ;)

Other than that, I'm also looking over to the ruby implementations to get better, optimize more and make it even faster. I have especially high hopes for JRuby and JRuby + Truffle here. So in the future I'll try to find out how fast this can actually get, which is a fun ride and has taught me a lot so far already! You should try playing the benchmark game for yourselves :)
