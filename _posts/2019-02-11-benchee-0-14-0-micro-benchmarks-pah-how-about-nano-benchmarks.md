---
layout: post
title: Benchee 0.14.0 - Micro Benchmarks? Pah, how about Nano Benchmarks!
description: None
date: 2019-02-11 15:30:17 -0000
last_modified_at: 2019-02-10 19:17:34 -0000
publish: true
pin: false
categories:
- benchmark
- Elixir
tags:
- benchee
- nano benchmarks
- release
---
Long time since the last benchee release, heh? Well, this one really packs a punch to compensate! It brings you a higher precision while measuring run times as well as a better way to specify formatter options. Let's dive into the most notable changes here, the full list of changes can be found in the [Changelog](https://github.com/PragTob/benchee/blob/master/CHANGELOG.md#0140-2019-02-10).

Of course, all formatters are also released in compatible versions.

## **Nanosecond precision measurements**

Or in other words making measurements 1000 times more precise 💥

This new version gives you much more precision which matters especially if you benchmark very fast functions. It even enables you to see when the compiler might completely optimize an operation away. Let's take a look at this in action:



Source: [https://gist.github.com/PragTob/8d82972e582129e971a4a3dc7def50fb](https://gist.github.com/PragTob/8d82972e582129e971a4a3dc7def50fb)

**File: `fast.exs`**
```elixir
range = 1..10
integer1 = :rand.uniform(100)
integer2 = :rand.uniform(100)

Benchee.run(
  %{
    "Integer addition (wrong)" => fn -> 1 + 1 end,
    "Integer addition" => fn -> integer1 + integer2 end,
    "String concatention (wrong)" => fn -> "1" <> "1" end,
    "adding a head to an array (wrong)" => fn -> [1 | [1]] end,
    "++ array concat (wrong)" => fn -> [1] ++ [1] end,
    "noop" => fn -> 0 end,
    "Enum.map(10)" => fn -> Enum.map(range, fn i -> i end) end
  },
  time: 1,
  warmup: 1,
  memory_time: 1,
  formatters: [{Benchee.Formatters.Console, extended_statistics: true}]
)
```

**File: `output`**
```
tobi@speedy:~/github/benchee$ mix run samples/fast_functions.exs 
Operating System: Linux
CPU Information: Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz
Number of Available Cores: 8
Available memory: 15.61 GB
Elixir 1.8.0
Erlang 21.2.2

Benchmark suite executing with the following configuration:
warmup: 1 s
time: 1 s
memory time: 1 s
parallel: 1
inputs: none specified
Estimated total run time: 21 s


Benchmarking ++ array concat (wrong)...
Benchmarking Enum.map(10)...
Benchmarking Integer addition...
Benchmarking Integer addition (wrong)...
Benchmarking String concatention (wrong)...
Benchmarking adding a head to an array (wrong)...
Benchmarking noop...

Name                                        ips        average  deviation         median         99th %
String concatention (wrong)            814.22 M        1.23 ns  ±2868.77%           0 ns          21 ns
++ array concat (wrong)                749.67 M        1.33 ns  ±2705.83%           0 ns          23 ns
noop                                   639.06 M        1.56 ns  ±2388.12%           0 ns          35 ns
adding a head to an array (wrong)      553.47 M        1.81 ns  ±2228.78%           0 ns          29 ns
Integer addition (wrong)               544.93 M        1.84 ns  ±2803.80%           0 ns          31 ns
Integer addition                       179.88 M        5.56 ns   ±737.19%           4 ns          39 ns
Enum.map(10)                             2.30 M      435.06 ns  ±2872.78%         356 ns         667 ns

Comparison: 
String concatention (wrong)            814.22 M
++ array concat (wrong)                749.67 M - 1.09x slower
noop                                   639.06 M - 1.27x slower
adding a head to an array (wrong)      553.47 M - 1.47x slower
Integer addition (wrong)               544.93 M - 1.49x slower
Integer addition                       179.88 M - 4.53x slower
Enum.map(10)                             2.30 M - 354.23x slower

Extended statistics: 

Name                                      minimum        maximum    sample size                     mode
String concatention (wrong)                  0 ns        9219 ns         1.54 M                     0 ns
++ array concat (wrong)                      0 ns       17501 ns         1.54 M                     0 ns
noop                                         0 ns        9220 ns         1.53 M                     0 ns
adding a head to an array (wrong)            0 ns       23216 ns         1.54 M                     0 ns
Integer addition (wrong)                     0 ns       16040 ns         1.52 M                     0 ns
Integer addition                             0 ns        9818 ns         1.52 M                     4 ns
Enum.map(10)                               335 ns     7385903 ns       952.30 K                   354 ns

Memory usage statistics:

Name                                 Memory usage
String concatention (wrong)                   0 B
++ array concat (wrong)                       0 B
noop                                          0 B
adding a head to an array (wrong)             0 B
Integer addition (wrong)                      0 B
Integer addition                              0 B
Enum.map(10)                                424 B

**All measurements for memory usage were the same**
```



You can see that the averages aren't 0 ns because sometimes the measured run time is very high - garbage collection and such. That's also why the standard deviation is huge (big difference from 0 to 23000 or so). However, if you look at the median (basically if you sort all measured values, it's the value is in the middle) and the mode (the most common value) you see that both of them are 0. Even the accompanying memory measurements are 0. Seems like there isn't much happening there.

So why is that? The compiler optimizes these "benchmarks" away, because they evaluate to one static value that can be determined at compile time. If you write `1 + 1` \- the compiler knows you probably mean `2`. Smart compilers. To avoid these, we have to trick the compiler by randomizing the values, so that they're not clear at compile time (see the "right" integer addition).

That's the one thing we see thanks to our more accurate measurements, the other is that we can now measure how long a map over a range with 10 elements takes (which is around 355 ns for me (I trust the mode and median more her than the average).

How did we accomplish this? Well it all started looking into [why measurements on Windows seemed to be weird](https://github.com/PragTob/benchee/pull/195#issuecomment-377010006). We noticed that the implementation of [`:timer.tc/1` had hard coded the values to be measured in micro seconds](https://github.com/erlang/otp/blob/master/lib/stdlib/src/timer.erl#L164-L169):



Source: [https://gist.github.com/PragTob/ac87f3ef02b144aa7240452566dbed09](https://gist.github.com/PragTob/ac87f3ef02b144aa7240452566dbed09)

**File: `timer.erl`**
```erlang
tc(F) ->
    T1 = erlang:monotonic_time(),
    Val = F(),
    T2 = erlang:monotonic_time(),
    Time = erlang:convert_time_unit(T2 - T1, native, microsecond),
    {Time, Val}.
```



But, in fact nanoseconds are supported! So we now have [our own simple time measuring code](https://github.com/PragTob/benchee/blob/e885f6b41e016da778cf038fdccab132644490f7/lib/benchee/benchmark/measure/time.ex). This is operating system dependent though, as the BEAM knows about _native_ time units. To the best of our knowledge nanosecond precision is **available on Linux and MacOS** \- not on Windows.

It wasn't just enough to switch to nano second precision though. See, once you get down to nanoseconds the overhead of simply invoking an anonymous function (which benchee needs to do a lot) becomes noticeable. On my system this overhead is 78 nanoseconds. To compensate, **benchee now measures the function call overhead and deducts it from the measured times**. That's how we can achieve measurements of 0ns above - all the code does is return a constant as the compiler optimized it away as the value can be determined at compile time.

A nice side effect is that the overhead heavy **function repetition is practically not used anymore** on Linux and macOS as no function is faster than nanoseconds. Hence, no more imprecise measurements due to function repetition to make it measurable at all (on Windows we still repeat the function call for instance 100 times and then divide the measured time by this).

## **Formatter Configuration**

This is best shown with an example, up until now if you wanted to pass options to any of the formatters you had to do it like this:



Source: [https://gist.github.com/PragTob/89b4eee2dd8b87f47c9f21234a29c1c4](https://gist.github.com/PragTob/89b4eee2dd8b87f47c9f21234a29c1c4)

**File: `benchee.exs`**
```elixir
Benchee.run(
  %{
    "function" => fn -> something end
  },
  formatters: [
    Benchee.Formatters.HTML,
    Benchee.Formatters.Console
  ],
  formatter_options: [
    html: [file: "output/my.html", auto_open: false, inline_assets: true]
  ]
)
```



This always felt awkward to me, but it really hit hard when I watched a benchee video tutorial. There the presenter said "...here we configure the formatter to be used and then down here we configure where it should be saved to..." - why would that be in 2 different places? They could be far apart in the code. There is no immediate visible connection between `Benchee.Formatters.HTML` and the `html:` down in the `formatter_options:`. Makes no sense.

That API was never really well thought out, sadly.  
So, what can we do instead? Well of course, bring the options closer together:



Source: [https://gist.github.com/PragTob/db958cce14196224103dd1c0b228568c](https://gist.github.com/PragTob/db958cce14196224103dd1c0b228568c)

**File: `new_formatter_options.exs`**
```elixir
Benchee.run(
  %{
    "function" => fn -> something end
  },
  formatters: [
    {Benchee.Formatters.HTML, file: "output/my.html", auto_open: false, inline_assets: true},
    Benchee.Formatters.Console
  ]
)
```



So, if you want to pass along options instead of just specifying the module, you specify a tuple of module and options. Easy as pie. You know exactly what formatter the options belong to.

## **Road to 1.0?**

Honestly, 1.0 should have happened many versions ago. Right now the plan is for this to be the last release with user facing features. We'll mingle the data structure a bit more ([see the PR if interested](https://github.com/PragTob/benchee/pull/264)), then put in deprecation warnings for functionality we'll remove and call it `0.99`. Then, remove deprecated functionality and call it `1.0`. So, this time indeed - it should be soon (tm). I have a track record of sneaking in _just one more thing_ before 1.0 though 😅. You can track our 1.0 progress [here](https://github.com/PragTob/benchee/milestone/7).

## **Why did this take so long?**

Looking at this release it's pretty packed. It should have been 2 releases (one for every major feature described above) that should have happened much sooner.

It's definitely sad, I double checked: [measuring with best available precision landed 21st of May](https://github.com/PragTob/benchee/pull/219#event-1637662236) and [function call overhead measurement was basically done 27th of June](https://github.com/PragTob/benchee/pull/229#event-1734173476). And the [formatter options landed 10th of August](https://github.com/PragTob/benchee/pull/242#event-1781790397). Keeping those out of your hands for so long really saddens me 😖.

Basically, these required updating the formatters, which isn't particularly fun, but necessary as I want all formatters to be ready to release along a new benchee version. In addition, we put in even more work (specifically Devon in big parts) and added support for memory measurements to all the formatters.

Beyond this? Well, I think life. Life happened. I moved apartments, which is a bunch of work. Then a lot of things happened at work leading to me eventually quitting my job. Some times there's just no time or head space for open source. I'm happy though that I'm as confident as one can be in that benchee is robust and bug free software, so that I don't have to worry about it breaking all the time. I can already see this statement haunting me if this release features numerous weird bugs ;)

In that vain, hope you enjoy the new benchee version - happy to hear feedback, bugs or feature ideas!

And because you made it so far, you deserve an adorable bunny picture:

![IMG_20190127_150119.jpg](https://pragtob.wordpress.com/wp-content/uploads/2019/02/img_20190127_150119.jpg)
