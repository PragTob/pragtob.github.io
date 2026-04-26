---
layout: post
title: 'Released: Statistex 1.0 an Elixir Statistics calculation library'
description: None
date: 2019-07-05 17:24:48 -0000
last_modified_at: 2019-07-05 17:24:48 -0000
publish: true
pin: false
categories: []
tags:
- Elixir
- library
- package
- statistex
- statistics
---
I just released [statistex](https://github.com/bencheeorg/statistex) \- a library to calculate statistics based on a given data sample. It's an extraction from my benchmarking library [benchee](https://github.com/bencheeorg/benchee) and part of what I'll henceforth call the "benchee library family". As it's been running in benchee basically since its inception I dubbed it 1.0. The extraction is good because it helps the benchee code base focus on benchmarking and not things around it. It removes about [800 lines from the repo](https://github.com/bencheeorg/benchee/pull/305/files) and it makes that code reusable for everyone else. It also makes it easier to introduce new statistics as it's clearer that we'll first introduce the logic inside statistex and later on just display it in benchee and friends. It's good design.

## Do we really need another statistics library?

I struggled with this question. I don't want to split the eco system unnecessarily. To be honest, I thought there was no other library out there. There are at least [statistics](https://github.com/msharp/elixir-statistics) and [Numerix](https://github.com/safwank/Numerix), though. Not sure how I missed them when I started incorporating more advanced statistics. Both include more functions than just for statistics: general math and more (drawing of random values for instance). They also support more statistical values than statistex at the time of this writing. So if you're looking for something, that statistex doesn't provide (yet) these are some of the first places I'd look. Why would you still want to use statistex? Well there are some things it offers that the others don't (to the best of my knowledge):

## statistics/2 - Give me everything!

As mentioned before, statistex was extracted and the way it was used in benchee is just "give me all the statistics so that formatters can display them!" - so there's a function that does exactly this: 

Source: [https://gist.github.com/PragTob/ed815974d54bb3adf547aef9e43ea879](https://gist.github.com/PragTob/ed815974d54bb3adf547aef9e43ea879)

**File: `statistex.exs`**
```elixir
iex> samples = [1, 3.0, 2.35, 11.0, 1.37, 35, 5.5, 10, 0, 2.35]
iex> Statistex.statistics(samples)
%Statistex{
  average: 7.156999999999999,
  frequency_distribution: %{
    0 => 1,
    1 => 1,
    10 => 1,
    35 => 1,
    1.37 => 1,
    2.35 => 2,
    3.0 => 1,
    5.5 => 1,
    11.0 => 1
  },
  maximum: 35,
  median: 2.675,
  minimum: 0,
  mode: 2.35,
  percentiles: %{50 => 2.675},
  sample_size: 10,
  standard_deviation: 10.47189577445799,
  standard_deviation_ratio: 1.46316833512058,
  total: 71.57,
  variance: 109.6606011111111
}
```

 What's cool about this? Well, little effort, big result! This is quite nice to explore data sets in iex for instance. Behind the scenes **statistex reuses previously calculated values so that no value is calculated twice**. For instance first you get the `sampe_size` and the `total`, both are then used to calculate the `average`. The `average` and `sample_size` are then passed on to calculate the `variance` and so forth. This way statistex is fast by not duplicating work if you want a bunch of statistical values (and benchee wants most of them). But you don't want all of these values but would still like to reuse previously calculated values? Got you covered!

## Manually reuse previously calculated values

Say you want to calculate the variance but have already calculated the average and sample_size. Easy: 

Source: [https://gist.github.com/PragTob/a015648fbf2200ec8a81531c13c687e6](https://gist.github.com/PragTob/a015648fbf2200ec8a81531c13c687e6)

**File: `reuse.ex`**
```elixir
iex> Statistex.variance([4, 9, 11, 12, 17, 5, 8, 12, 12], sample_size: 9, average: 10.0)
16.0
```

 Like `variance/2` a lot of function take an optional keyword list as arguments where you can provide previously calculated values (options are of course documented).

## Raising on empty list input

Thanks to a [discussion on elixir forum](https://elixirforum.com/t/library-api-design-error-returns-nil-vs-error-tuple-vs-exception/23177) I made the decision to raise an `ArgumentError` when statistex is handed an empty list in most functions. Why? The statistics don't make any sense at this point and it's likely some kind of error either way/you probably want to display something other than a bunch of `nil`s. I know many won't consider this a feature, I quite like the direction it pushes client code towards, though.

## Is this enough for a new library?

I think so. :) Especially getting all values at once and reusing previously calculated values are incredibly valuable properties. I also like that statistex is solely focussed on statistics. And the statistics it can't compute yet? We'll catch up on that over time. Moreover, it's not like I spent some huge amount of work writing it as it was a simple extraction. I'd be happy if you gave statistex a trial run and left some feedback.  
