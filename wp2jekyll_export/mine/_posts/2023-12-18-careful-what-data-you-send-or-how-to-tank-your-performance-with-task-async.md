---
layout: post
permalink: https://pragtob.wordpress.com/2023/12/18/careful-what-data-you-send-or-how-to-tank-your-performance-with-task-async/
title: Careful what data you send or how to tank your performance with Task.async
description: None
date: 2023-12-18 13:48:49 -0000
last_modified_at: 2023-12-22 11:41:58 -0000
publish: true
pin: false
image:
  path: https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot.png
categories: []
tags:
- beam
- benchee
- benchmark
- Elixir
- Erlang
- misconception
- parallelism
- sequential
- Task.async
---
In Elixir and on the BEAM (Erlang Virtual Machine) in general we love our processes - lightweight, easily run millions of them, easy lock-less parallelism - you've probably heard it all. Processes are great and one of the many reasons people gravitate towards the BEAM.

Functions like `[Task.async/1](https://hexdocs.pm/elixir/Task.html#async/1)` make parallelism effortless and can feel almost magical. Cool, let's use it in a simple benchmark! Let's create some random lists, and then let's run some non trivial `Enum` functions on them: `uniq`, `frequencies` and `shuffle` and let's compare doing them sequentially (one after the other) and running them all in parallel. This kind of work is super easy to parallelize, so we can just fire off the tasks and then await them:

https://gist.github.com/PragTob/65a7abbded3360fa071cee665643ceb2

Cool, let's check out the results! You can check the [HTML report online](https://www.pragtob.info/benchee/task-no-task/) here, uncollapse for the console formatter version or just check out the pictures.

Console formatter output
  
    Operating System: Linux
    CPU Information: AMD Ryzen 9 5900X 12-Core Processor
    Number of Available Cores: 24
    Available memory: 31.25 GB
    Elixir 1.16.0-rc.1
    Erlang 26.1.2
    JIT enabled: true
    
    Benchmark suite executing with the following configuration:
    warmup: 15 s
    time: 1 min
    memory time: 0 ns
    reduction time: 0 ns
    parallel: 1
    inputs: 10k, 1M, 10M
    Estimated total run time: 7.50 min
    
    ##### With input 10k #####
    Name                 ips        average  deviation         median         99th %
    sequential        315.29        3.17 ms    ±20.76%        2.96 ms        5.44 ms
    parallel          156.77        6.38 ms    ±31.08%        6.11 ms       10.75 ms
    
    Comparison: 
    sequential        315.29
    parallel          156.77 - 2.01x slower +3.21 ms
    
    Extended statistics: 
    
    Name               minimum        maximum    sample size                     mode
    sequential         2.61 ms        7.84 ms        18.91 K         2.73 ms, 3.01 ms
    parallel           3.14 ms       11.99 ms         9.40 K4.80 ms, 4.87 ms, 8.93 ms
    
    ##### With input 1M #####
    Name                 ips        average  deviation         median         99th %
    sequential          1.14         0.87 s     ±7.16%         0.88 s         0.99 s
    parallel            0.94         1.07 s     ±3.65%         1.07 s         1.16 s
    
    Comparison: 
    sequential          1.14
    parallel            0.94 - 1.22x slower +0.194 s
    
    Extended statistics: 
    
    Name               minimum        maximum    sample size                     mode
    sequential          0.74 s         0.99 s             69                     None
    parallel            0.98 s         1.16 s             57                     None
    
    ##### With input 10M #####
    Name                 ips        average  deviation         median         99th %
    sequential        0.0896        11.17 s    ±10.79%        11.21 s        12.93 s
    parallel          0.0877        11.40 s     ±1.70%        11.37 s        11.66 s
    
    Comparison: 
    sequential        0.0896
    parallel          0.0877 - 1.02x slower +0.23 s
    
    Extended statistics: 
    
    Name               minimum        maximum    sample size                     mode
    sequential          9.22 s        12.93 s              6                     None
    parallel           11.16 s        11.66 s              6                     None

[![](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot.png?w=450)](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot.png)10k input, iterations per second (higher is better) [![](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-1.png?w=450)](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-1.png)Boxplot for 10k, measured run time (lower is better). Sort of interesting how many "outliers" (blue dots) there are for sequential though. [![](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-2.png?w=450)](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-2.png)1M input, iterations per second (higher is better) [![](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-3.png?w=450)](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-3.png)Boxplot for 1M, measured run time (lower is better).  [![](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-4.png?w=450)](https://pragtob.wordpress.com/wp-content/uploads/2023/12/newplot-4.png)10M input, iterations per second (higher is better). Important to know, they take so long here the sample size is only 6 for each.

And just as we all expected the parallel... **no wait a second the sequential version is faster for all of them? How could that be?** This was easily parallelizable work, split into 3 work packages with many more cores available to do the work. **Why is the parallel execution slower?**

## What happened here?

There's no weird trick to this: It ran on a system with 12 physical cores that was idling save for the benchmark. Starting processes is extremely fast and lightweight, so that's also not it. By most accounts, parallel processing should win out.

What _is the problem then?_

The problem here are the huge lists the tasks need to operate on and the return values that need to get back to the main process. The BEAM works on a "share nothing" architecture, this means in order to process theses lists in parallel **we have to copy the lists over entirely to the process** (Tasks are backed by processes). And once they're done, we need **to copy over the result as well**. Copying, esp. big data structures, is both **CPU intensive** and **memory intensive**. In this case the additional copying work we do outweighs the gains we get by processing the data in parallel. You can also see that this effect seems to be diminishing the bigger the lists get - so it seems like the parallelization is catching up there.

The full copy may sound strange - after all we're dealing with _immutable data structures_ which should be safe to share. Well, once processes share data garbage collection becomes a whole other world of complex, or in the words of the OTP team in ["A few notes on message passing"](https://www.erlang.org/blog/message-passing/) (emphasis mine):

> Sending a message is straightforward: we try to find the process associated with the process identifier, and if one exists we insert the message into its signal queue.
>
> **Messages are always copied before being inserted into the queue**. As wasteful as this may sound it greatly reduces garbage collection (GC) latency as the **GC never has to look beyond a single process.** Non-copying implementations have been tried in the past, but they turned out to be a bad fit as low latency is more important than sheer throughput for the kind of soft-realtime systems that Erlang is designed to build.
>
> [John Högberg](https://www.erlang.org/blog/message-passing/#sending-messages)

[Robert Virding (co-inventor of Erlang) also puts some more color to it in a thread on elixir forum](https://elixirforum.com/t/why-is-data-deep-copied-when-sending-to-another-process/26330/11?u=pragtob).

In case you're interested in other factors for this particular benchmark: I chose the 3 functions semi-randomly looking for functions that traverse the full list at least once doing some non trivial work. If you do heavier work on the lists the parallel solution will fare better. We can also not completely discount that CPU boosting (where single core performance may increase if the other cores are idle) is shifting benchmark a bit in favor of _sequential_ but overall it should be solid enough for demonstration purposes. Due to the low sample size for the 10M list, parallel execution may sometimes come out ahead, but usually doesn't (and I didn't want the benchmark take even longer).

## The Sneakyness

Now, the problem here is a bit**more sneaky - as we're not _explicitly_ sending messages**. Our code looks like this: `Task.async(fn -> Enum.uniq(big_list) end)` \- there is no `send` or `GenServer.call` here! However, that function still needs to make its way to the process for execution. As the **closure of the function automatically captures referenced variables - all that data ends up being copied over as well!** (Technically speaking [`Task.async` does a `send` under the hood](https://github.com/elixir-lang/elixir/blob/d79c0d2b7a5fb1d6cc3fee7bdc26640813d644a6/lib/elixir/lib/task.ex#L504C57-L504C63), but `spawn/1` also behaves like this.)

This is what caught me off-guard with this - I knew messages were copied, but somehow `Task.async` was so magical I didn't think about it sending messages or needing to copy its data to a process. Let's call it a blind spot and broken mental model I've had for way too long. Hence, this blog post is for you dear reader - may you avoid the mistake I made!

Let's also be clear here that normally this isn't a problem and the benefits we get from this behavior are worth it. When a process terminates we can just free all its memory. It's also not super common to shift so much data to a process to do comparatively lightweight work. The problem here is a bit, how easy it is for this problem to sneak up on you when using these high level abstractions like `Task.async/1`.

## Real library, real problems

Yup. While I feel some shame about it, I've always been an advocate for sharing mistakes you made to spread some of the best leanings. This isn't a purely theoretical thing I ran into - it stems from real problems I encountered. As you may know I'm the author of [benchee](https://github.com/bencheeorg/benchee) \- the best benchmarking library (tm) ;) . Benchee's design, in a nut shell, revolves around a big data structure - the suite - data is enriched throughout the process of benchmarking. You may get a better idea by looking at the [breakdown of the steps](https://github.com/bencheeorg/benchee). This has worked great for us.

However, some of the data in that suite may reference large chunks of data if the benchmark operates on large data. Each `Scenario` references its given _input_ as well as its _benchmarking function_. Given what we just learned both of these may be huge. More than that, the `Configuration` also holds all the configured `inputs` and is part of the suite as well.

Now, when benchee tries to compute your statistics in parallel it happily creates a new process for each scenario (which may be 20+) copying over the benchmarking function and input although it really doesn't need them.

Even worse formatters are run in parallel handing over the _entire suite_ \- including all scenarios (function and input) as well as all the inputs _again_ as part of the Configuration - none of which a formatter should need. 😱

To be clear, you will only encounter this problem if you deal with huge sets of data and if you do it's "just" more memory and time used. However, for a library about measuring things and making them fast this is no good.

## The remedy

Thankfully, there are multiple possible remedies for this problem:

* **Limiting the data** you send to the absolute necessary minimum, instead of just sending the whole struct. For example, don't send an entire `Suite` struct if all you need is a couple of fields.
* If only the process needs the data, it may **fetch the data itself** instead. I.e. instead of putting the result of a giant query into the process, the process could be the one doing the query if it's the only one that needs the data.
* There are **some data structures that are shared between processes** and hence don't need copying, such as [ets](https://www.erlang.org/doc/man/ets) and [persistent_term](https://www.erlang.org/doc/man/persistent_term.html).

As teased above, the most common and easiest solution is just to pass along the data you need, if you ended up accidentally sending along more than you wanted to. You can see one step of it in this [pull request](https://github.com/bencheeorg/benchee/pull/408) or [this one](https://github.com/bencheeorg/benchee/pull/414).

The results are quite astounding, for a benchmark I'm working on (blog post coming _soon (tm)_) this change got it from practically being unable to run the benchmark due to memory constraints (on a 32GB RAM system) to easily running the benchmark - maximum resident size set size got almost halfed.

The magnitude of this can also be shown perhaps by the size of the files I [saved](https://github.com/bencheeorg/benchee#saving-loading-and-comparing-previous-runs) for this benchmark. Saving is actually implemented as a formatter, and so automatically benefits from these changes - **the file size for this benchmark went down from ~200MB per file to 1MB aka a reduction to 0.5% in size.** You can read more about how it improved in the [benchee 1.3.0 release notes](https://pragtob.wordpress.com/2023/12/22/benchee-1-3-0-published-oh-save-the-memory/).

Naturally this change will also make its way to you all as benchee 1.3.0 soon (edit: [out now!](https://pragtob.wordpress.com/2023/12/22/benchee-1-3-0-published-oh-save-the-memory/)).

Also when pursuing to fix this **be mindful that you need to completely remove the variable from the closure**. You can't just go: `Task.async(fn -> magic(suite.configuration) end)` \- the entire `suite` will still be sent along.
  
    iex(1)> list = Enum.to_list(1..100_000)
    iex(2)> # do not benchmark in iex, this is purely done to get a suite with some data
    iex(3)> suite = Benchee.run(%{map: fn -> Enum.map(list, fn i -> i * i end) end })
    iex(4)> :erts_debug.size(suite)
    200642
    iex(5)> :erts_debug.size(fn -> suite end)
    200675
    iex(6)> :erts_debug.size(fn -> suite.configuration end)
    200841
    iex(7)> :erts_debug.size(fn -> suite.configuration.time end)
    201007
    iex(8)> configuration = suite.configuration
    iex(9)> :erts_debug.size(fn -> configuration.time end)
    295
    iex(10)> time = configuration.time
    iex(11)> :erts_debug.size(fn -> time end)
    54

## Helping others avoid making the same mistake

All of that discovery, and partially shame, left me with the question: How can I help others avoid making the same mistake? Well, one part of it is right here - publish a blog post. However, that's one point.

We [already added documentation to the `Task` module mentioning this](https://github.com/elixir-lang/elixir/pull/13173), and as proposed by José are working on [adding a section to the process anti-patterns section](https://github.com/elixir-lang/elixir/pull/13194).

Also don't forget: **processes are still awesome and lightweight** **\- you should use them!** This is just a cautionary tale of how things _might_ go wrong if you're dealing with big chunks of data and that the work you're doing on that data _may_ not be extensive enough to warrant a full copy. Or that you're accidentally sending along _too much data_ unaware of the consequences. There are many more use cases for processes and tasks that are **absolutely great, appropriate and will save you a ton of time.**

What does this leave us with? As usual: **don't assume, always benchmark!**

Also, be careful about the data you're sending around and if you really need it! 💚
