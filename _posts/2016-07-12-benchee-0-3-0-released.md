---
layout: post
title: Benchee 0.3.0 released - formatters, parallel benchmarking &amp; more
description: None
date: 2016-07-12 14:30:32 -0000
last_modified_at: 2016-07-12 15:48:11 -0000
publish: true
pin: false
categories: []
tags:
- benchee
- benchmarking
- Elixir
- hex.pm
- micro benchmarking
- package
- release
---
Yesterday I released [benchee](https://github.com/PragTob/benchee) 0.3.0! Benchee is a tool for (micro) benchmarking in elixir focussing on being simple, extensible and to provide you with good statistics. You can refer to the [Changelog](https://github.com/PragTob/benchee/blob/master/CHANGELOG.md) for detailed information about the changes. This post will look at the bigger changes and also give a bit of the _why_ for the new features and changes.

## Multiple formatters

Arguably the biggest feature in Benchee 0.3.0 is that it is now easy and built-in to configure multiple formatters for a benchmarking suite. This means that first the benchmark is run, and then multiple formatters are run on the benchmarking results. This way you can get both the console output and the corresponding csv file using [BencheeCSV](https://github.com/PragTob/benchee_csv). This was a pain point for me before, as you could either get one or the other or you needed to use the [more verbose API](https://github.com/PragTob/elixir_playground/blob/master/bench/tco_blog_post_detailed.exs). 

Source: [https://gist.github.com/pragtobgists/d6a970e975ea56718eff9c5930171d3d](https://gist.github.com/pragtobgists/d6a970e975ea56718eff9c5930171d3d)

**File: `multiple_formatters.exs`**
```elixir
list = Enum.to_list(1..10_000)
map_fun = fn(i) -> [i, i * i] end

Benchee.run(
  %{
    formatters: [
      &Benchee.Formatters.CSV.output/1,
      &Benchee.Formatters.Console.output/1
    ],
    csv: %{file: "my.csv"}
  },
  %{
    "flat_map"    => fn -> Enum.flat_map(list, map_fun) end,
    "map.flatten" => fn -> list |> Enum.map(map_fun) |> List.flatten end
})
```

 You can also see the new _output/1_ methods at work, as opposed to _format/1_ they also really do the output themselves. BencheeCSV uses a custom configuration options to know which file to write to. This is also new, as now formatters have access to the full benchmarking suite, including configuration, raw run times and function definitions. This way they can be configured using configuration options they define themselves, or a plugin could graph all run times if it wanted to. Of course, _formatters_ default to just the built-in console formatter.

## Parallel benchmarking

Another big addition is [parallel benchmarking](https://github.com/PragTob/benchee/pull/15). In Elixir, this just feels natural to have. You can specify a _parallel_ key in the configuration and that tells Benchee how many tasks should execute any given benchmarking job in parallel. 

Source: [https://gist.github.com/pragtobgists/39686e4c09cc9cdef4b364847df2b9ce](https://gist.github.com/pragtobgists/39686e4c09cc9cdef4b364847df2b9ce)

**File: `run_parallel.exs`**
```elixir
list = Enum.to_list(1..10_000)
map_fun = fn(i) -> [i, i * i] end

Benchee.run(%{time: 3, parallel: 2}, %{
  "flat_map"    => fn -> Enum.flat_map(list, map_fun) end,
  "map.flatten" => fn -> list |> Enum.map(map_fun) |> List.flatten end
})
```

 Of course, if you want to see how a system behaves under load - overloading might be exactly what you want to stress test the system. And this was exactly the reason why L[eon contributed this change back to Benchee](https://github.com/PragTob/benchee/pull/15#issuecomment-230149595):

> I needed to benchmark integration tests for a telephony system we wrote - with this system the tests actually interfere with each other (they're using an Ecto repo) and I wanted to see how far I could push the system as a whole. Making this small change to Benchee worked perfectly for what I needed :)

(Of course it makes me extremely happy that people found adjusting Benchee for their use case simple, that's one of the main goals of Benchee. Even better that it was contributed back <3 ) If you want to see more information and detail about "to benchmark in parallel or not" you can [check the Benchee wiki](https://github.com/PragTob/benchee/wiki/Parallel-Benchmarking). Spoiler alert: The more parallel benchmarks run, the slower they get to an acceptable degree until the system is overloaded (more tasks execute in parallel than there are CPU cores to take care of them). Also deviation skyrockets. While the effect seems not to be very significant for _parallel: 2_ on my system, the default in Benchee remains _parallel: 1_ for the mentioned reasons.

## Print configuration information

Partly also due to the _parallel_ change, Benchee wil now print a brief summary of the benchmarking suite before executing it. 

```
tobi@happy ~/github/benchee $ mix run samples/run_parallel.exs

Benchmark suite executing with the following configuration:
warmup: 2.0s
time: 3.0s
parallel: 2

Estimated total run time: 10.0s

Benchmarking flat_map...
Benchmarking map.flatten...

Name                 ips      average  deviation      median
map.flatten       1268.15      788.55us   (±13.94%)   759.00us
flat_map           706.35     1415.72us    (±8.56%)  1419.00us

Comparison:
map.flatten       1268.15
flat_map           706.35 - 1.80x slower
```

 This was done so that when people share their benchmarks online one can easily see the configuration they ran it with. E.g. was there any warmup time? Was the amount of parallel tasks too high and therefore the results are that bad? It also prints an estimated total run time (_number of jobs * (warmup + time)_), so you know if there's enough time to go and get a coffee before a benchmark finishes.

## Map instead of a list of tuples

What is also marked as a _"breaking"_ change in the Changelog is actually not THAT breaking. The main data structure handed to _Benchee.run_ was changed to a map instead of a list of tuples and all corresponding data structures changed as well (important for plugins to know). It used to be a list of tuples because of the possibility that benchmarks with the same name would override each other. However, having benchmarks with the same name is nonsensical as you can't discern their results in the output any way. So, this now feels like a much more fitting data structure. The old main data structure of a list of tuples still works and while I might remove it, I don't expect me to right now as all that is required to maintain it is [4 lines of code](https://github.com/PragTob/benchee/blob/0.3.0/lib/benchee.ex#L24-L27). This makes duplicated names no longer working the only real deprecation, although one might even call it a feature ;) Last, but not least, this release is the first one that got some community contributions in, which makes me extremely happy. So, thanks [Alvin](https://github.com/alvinlindstam) and [Leon](https://github.com/ldr)! :D
