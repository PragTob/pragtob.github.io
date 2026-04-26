---
layout: post
title: Benchee 0.2.0 - warmup &amp; nicer console output
description: None
date: 2016-06-13 20:22:36 -0000
last_modified_at: 2016-06-13 20:22:36 -0000
publish: true
pin: false
categories:
- Uncategorized
tags:
- benchee
- benchmarking
- Elixir
- hex
- micro benchmaring
- tools
---
Less than a week after the initial release of my benchmarking library [Benchee](https://github.com/PragTob/benchee) there is a new version - 0.2.0! The details are in the [Changelog](https://github.com/PragTob/benchee/blob/master/CHANGELOG.md). That's the what, but what about the _why_?

### Warmup

Arguably the biggest change is introduction of a warmup phase to the benchmarks. That is the benchmark jobs are first run for some time without taking measurements to simulate a "warm" already running system. I didn't think it'd be that important as the BEAM VM isn't JITed (as opposed to the JVM) for all hat I know. It is important once benchmarks get to be "macro" - for instance databases usually respond faster once they got used to some queries and our webservers serve most of their time "hot". However, even in my micro benchmarks I noticed that it could have an effect when a benchmark was moved around (being run first versus being run last). So I don't know to what effect, but at least to a small effect there is warmup now. If you don't want warmup - just set warmup: 0.

### Nicer console output



```
Name                        ips      average  deviation      median
bodyrecusrive map      40047.87      24.97us   (±32.55%)    25.00us
stdlib map             39724.07      25.17us   (±61.41%)    25.00us
map tco no reverse     36388.50      27.48us   (±23.22%)    27.00us
map with TCO and reverse 33309.43    30.02us   (±45.39%)    29.00us
map with TCO and ++      465.25    2149.40us    (±4.84%)  2138.00us

Comparison:
bodyrecusrive map      40047.87
stdlib map             39724.07 - 1.01x slower
map tco no reverse     36388.50 - 1.10x slower
map with TCO and reverse 33309.43 - 1.20x slower
map with TCO and ++      465.25 - 86.08x slower
```

 The ouput of numbers is now aligned right, which makes them easier to read and compare, as you can see orders of magnitude differences much more easily. Also the ugly empty line at the end of the output has been removed :)

### Benchee.measure

This is the API incompatible change. It felt weird to me in version 0.1.0 that Benchee.benchmark would already run the function given to it. Now the jobs are defined through Benchee.benchmark and kept in a datastructure (similar to the one Benchee.run uses). Benchee.measure then runs the jobs and measures the outcome and provides them under the new run_times key instead of overriding the jobs key. This feels much nicer overall, of course the high level Benchee.run is unaffected by this. These additions already nicely improve what Benchee can do and got a couple of items off my "I want to do this in benchee" bucket list. There's still more to come :)
