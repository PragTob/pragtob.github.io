---
layout: post
title: 'Released: benchee 0.99, 1.0 &amp; friends'
description: None
date: 2019-03-28 18:11:00 -0000
last_modified_at: 2019-03-28 18:11:00 -0000
publish: true
pin: false
categories:
- Elixir
tags:
- '1.0'
- benchee
- benchee_html
- release
- stable
---
**It's finally here - benchee 1.0! 🎉🎉🎉** The first benchee release was almost 3 years ago - it started a mission to improve benchmarking tooling in the elixir eco system. And now we're not at the goal - after all it's never done and we're not short of [ideas of what to do](https://github.com/bencheeorg/benchee/issues).

## What's in a 1.0?

Also called _"Why did you take so long to call it_ 1.0?" - 1.0 for me means a **good level of stability**. A level where not every second new benchee version all formatters would _need_ updates because they would break otherwise. And in recent releases we have still shuffled major data structures around A LOT (just check all the [Breaking Changes (Plugins)](https://github.com/bencheeorg/benchee/blob/master/CHANGELOG.md)). Benchee was mostly stable from a user perspective - but this means it's less of a risk factor to go ahead and write your own plugins, something that benchee always encouraged/was built to empower. I don't have any plans for 2.0 right now - all features that I know of can easily be added to the existing structure. It also means I'm **happy with the features**. What benchee offers is great, we have:

* nano second precise run time measurements
* memory measurements
* rich statistics
* show information such as CPU, elixir and erlang versions about the system running the benchmarks
* support for multiple inputs
* hooks to support even unconventional scenarios
* you can access it all via your CLI, CSV, JSON or HTML (including nice graphs!)
* and actually a lot more ;)

Benchee might have started out as "I want [benchmark-ips](https://github.com/evanphx/benchmark-ips) in elixir" but it has surpassed it in many ways so that I'd actually want to have benchee in Ruby but that's another topic. However, that makes me proud of what we accomplished. With that amount of polish I can also easily sit back and not work on benchee for some time because I know it's good - it is "done" in the sense that it can do everything I wanted it to do when I started the project (and even more!). As for what is actually _in it_ mostly removing deprecations. You can check out the [Changelog](https://github.com/bencheeorg/benchee/blob/master/CHANGELOG.md).

## What's 0.99?

I found it nice how rspec did their 2.99 --> 3.0 switch - get it to run on 2.99 without deprecation warnings and then you can safely use 3.0. That was a great user experience. Ember.js handles their major versions similarly. Now, benchee is nowhere near as complex as those 2 but we thought providing that nicety would still be great.

## Features

As mentioned before 0.99/1.0 don't actually include many features - [the previous 0.14.0 release from about a month ago was very feature packed](https://pragtob.wordpress.com/2019/02/11/benchee-0-14-0-micro-benchmarks-pah-how-about-nano-benchmarks/). These releases are a lot about **polish**. Redoing the documenation, updating names, fixing typespecs, being more careful about what is and isn't exposed in the public interface. A small but important feature made it in though - displaying the **absolute difference between measurements:**
  
    Comparison:
    flat_map           2.34 K
    map.flatten        1.22 K - 1.92x slower +393.09 μs

See that little`+393.09 μs`? It's how much slower it was on average in absolute terms. With these comparisons people often focus too much on "OMG it's almost 2 times as slow!!!" but this number helps put it into context: It's not even half a millisecond. If you only do this once in a web request the difference likely doesn't matter. It's a calculation I always did in my head, I'm happy to make it easily accessible for everyone. Along with this patch those values were added to our Statistics struct - including the "x-times slower" values, which means formatters no longer have to implement this themselves! Hooray!

## We're an org now!

An astute observer might have seen that all my benchee repos have been moved to the github organization [bencheeorg](https://github.com/bencheeorg). What's that all about? It's mostly a tribute to benchee not being a personal project but a **community project**. Many people have contributed massively to benchee, most notably [Devon](https://github.com/devonestes) and [Eric](https://github.com/wasnotrice). Without Devon we probably still wouldn't have memory measurements and without Eric our unit scaling wouldn't be as great as it is. Others such as [Michał](https://github.com/michalmuskala) and [OvermindDL1](https://github.com/OvermindDL1) have also contributed a lot through ideas, testing and help (especially with memory measurements :)). Feels wrong to keep the repositories attached to a single person. Also, should anything happen to me (which I hope won't happen), the others could still add people to the organization and carry on. It also helps with another problem I've had: I want to extract small useful libraries from benchee: Statistics (introduced by me), System Information gathering (introduced by Devon) and unit scaling (introduced by Eric) - where do I put these repos? All under their own name space? All under my name space? Nah, I put them in the benchee organization where we share ownership - that's where they belong.

## The future of benchee

As I said benchee isn't done - there is[an open PR to add reference jobs](https://github.com/bencheeorg/benchee/pull/281) which didn't make it into the release. We'd like to add [more types of memory measurements](https://github.com/bencheeorg/benchee/issues/262), as well as [measuring reductions,](https://github.com/bencheeorg/benchee/issues/156) incorporating [profiling right after benchmarking to drill down on those bottle necks](https://github.com/bencheeorg/benchee/issues/250) sounds great, [more compact console output](https://github.com/bencheeorg/benchee/issues/246) and also [include the benchmarking code itself in the suite](https://github.com/bencheeorg/benchee/issues/209) so that formatters could display it. Finally, now might finally be the time to brush up on meta programming and write that [DSL wrapper that people apparently want](https://github.com/bencheeorg/benchee/issues/236). Help with all of those is very welcome. Personally, I'm really itching to extract these libraries I mentioned - let's see about that. Also to showcase benchee with some nice benchmarks - after all what good is a great benchmarking tool if you rarely use it?
