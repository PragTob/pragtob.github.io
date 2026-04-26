---
layout: post
permalink: https://pragtob.wordpress.com/2022/03/08/benchee-1-1-0-released-why-did-it-take-so-long/
title: Benchee 1.1.0 released + why did it take so long
description: None
date: 2022-03-08 16:53:41 -0000
last_modified_at: 2022-03-08 16:59:26 -0000
publish: true
pin: false
categories:
- Elixir
tags:
- benchee
- open source
- release
---
[Benchee](https://github.com/bencheeorg/benchee) 1.1.0 has finally hit hex.pm. After, well, almost 3 years. So, in this blog post we'll dive into:

  1. What are the changes
  2. Why did it take so long, with some (significant) musings on Open Source and bugs as well as my approach to it

## What does Benchee 1.1.0 Bring to the table

The star of the show certainly are the two new major features: reduction measurements and profiling! Then there is also a nasty bug that was squashed. Check out the [Changelog](https://github.com/bencheeorg/benchee/blob/main/CHANGELOG.md#110-2022-03-08) for all.

### Reduction Counting

Reductions joins execution time and memory consumption as the third measure Benchee can take. This one was kicked off way back when someone asked in our #benchee channel about adding this feature. What reductions are, is hard to explain. In short, it's not very well defined but a "unit of work". The BEAM uses them to keep track of how long a process has run. As the [Beam Book puts it as follows](https://blog.stenmans.org/theBeamBook/#_scheduling_non_preemptive_reduction_counting):

> BEAM solves this by keeping track of how long a process has been running. This is done by counting reductions. The term originally comes from the mathematical term beta-reduction used in lambda calculus.
>
> The definition of a reduction in BEAM is not very specific, but we can see it as a small piece of work, which shouldn’t take too long. Each function call is counted as a reduction. BEAM does a test upon entry to each function to check whether the process has used up all its reductions or not. If there are reductions left the function is executed otherwise the process is suspended.
>
> [Beam Book, Chapter 5.3](https://blog.stenmans.org/theBeamBook/#_scheduling_non_preemptive_reduction_counting)

This can help you, as it's not affected by system load so you could make assumptions in your CI about performance. It's not 1:1 but it helps. Of course, check out Benchee's [docs](https://github.com/bencheeorg/benchee#measuring-reductions) about it. Biggest shout out goes to [Devon](https://twitter.com/devoncestes) for [implementing it](https://github.com/bencheeorg/benchee/pull/307).

You can simply specify `reduction_time` and there you go:

https://gist.github.com/PragTob/37ea85a6d984714a63cc4d7e8c195b52

It's worth noting that reduction counts will differ between different elixir and erlang versions - as we often noticed in our own CI setup.

### Profile after benchmarking

Another feature that I'd never imagined having in Benchee, but thanks to community suggestions (and implementation!) it came to be. This one in particular was even suggested by José Valim himself - chatting with him he asked if there were plans to include something like this as his workflow would often be:

1\. benchmark to see results

2\. profile to find improvement opportunities

3\. improve code

4\. Start again at 1.

Makes perfect sense, I just never thought of it. So, you can now say `profile_after: true` or even specify a specific profiler + options.

https://gist.github.com/PragTob/d723d6c8eab930d28e8937d92a1eade3

We didn't implement the profiling ourselves, but instead we rely on the builtin profiling tasks like [this one](https://hexdocs.pm/mix/1.13/Mix.Tasks.Profile.Eprof.html#profile/2). To make the feature fully compatible with hooks, I also had to send a [small patch to elixir](https://github.com/elixir-lang/elixir/pull/11657) and so `after_each` hooks won't work with profiling until it's released. But, nobody uses hooks anyhow so, who cares? 😛

This feature made it in thanks to [Pablo Costas](https://twitter.com/pablocostass), and his [great work](https://github.com/bencheeorg/benchee/pull/317). I'm happy to highlight that not only did this contribution give us all a great Benchee feature, but also a friendship to boot. Oh, the wonders of Open Source. 💚

### Measurement accuracy on Mac

Now to the least fun part about this release. There is a bugfix, a quite important one at that. Basically on Mac OS previous Benchee versions might report inaccurate results for very fast benchmarks (< 10 microseconds). There are many more musings in [this issue](https://github.com/bencheeorg/benchee/issues/313), but basically we relied on the operating system clock returning times in a value that it can accurately measure in. Alas, OSX reports in nanoseconds but only has microsecond accuracy (leading to measurements being multiples of 1000). However, even the operating system clock reported nanosecond accuracy - so I even [reported a bug on erlang/otp](https://github.com/erlang/otp/issues/3911) that was thankfully fixed in 22.2.

Fixing this was hard and stressful, which leads nicely into the next major section...

## Why it took so long, perfectionism and open source

So, why did it take so long? I blogged earlier today about some of the things that held me back the past 1.5 years in ["The Silence Between"](https://pragtob.wordpress.com/2022/03/08/the-silence-between/). However, you can see that a lot of these features already landed in early 2020, so what gives?

The short answer is the bug above was hard to fix and I needed to fix it. The long answer is... well, long.

I think I could describe myself as a pragmatic perfectionist. I'm happy to implement an MVP, I constantly ask "Do we really need this?" or "Can we make this simpler and deliver it faster?", but what I end up shipping I want to... well, almost need to be great for what we decided to ship. I don't want to release with bugs, constant error notifications or barely anything tested. I can make lots of tradeoffs, as long as I decide on them like: Ok we'll duplicate this code now, as we have no idea what a good abstraction might be and we don't wanna lock ourselves in. But something misbehaving that I thought was sublime? Oh, the pain.

Why am I highlighting this? Well, Benchee reporting **wrong results** **is frightening to me. Benchee has one core promise, and that promise is to measure your functions as accurately as possible.** Also, in my opinion fixing critical bugs such as this one should have the highest priority. I can't, for myself, justify working on Benchee while not working on that bug. I know, it's not a great attitude and I should have released the features on main and just released the bug fix later. I do. But I felt like, all energy had to be spent on fixing that bug.

And working on that bug was **hard**. It's a Mac only bug and I famously do not own or want to own a Mac. My partner owns one, but when I'm doing Open Source chances are she's at her computer as well. And then, to investigate something like this, I need a couple of hours of interrupted time with no distractions on my mind as well. I might as well not even start otherwise. It certainly didn't help that the [bug randomly disappeared](https://github.com/bencheeorg/benchee/issues/313#issuecomment-778835256), when trying to look at it.

The problem that I did not have a Mac to fix this was finally solved when I started a new job, but then first the stress was too high and then my arms were injured (as mentioned in the other blog post). My arms finally got better and I had a good 4h+ to set aside to fix this bug. It can be kind of hard, to get that dedicated time but it's absolutely needed for an intricate bug such as this one.

So, that's the major reason it took so long. I mean, it involved finding a bug in Erlang _itself_. And, me working around that bug which is [some code](https://github.com/bencheeorg/benchee/blob/main/lib/benchee/utility/erlang_version.ex) that well... was almost harder to write than the actual fix.

I would be amiss not to mention something else: **It's perfectly fine for Open Source project not to update!** Sometimes, they are just done. Or the maintainers have more important things to do. I certainly consider Benchee "done" since 1.0 as it has all features I really wanted it to have. You see, reduction counting and profiler after are great features, but they are hardly essential.

Still, Benchee having a rather important bug for so long really made me feel guilty and bad. Even worse, because I didn't fix the bug those great contributions from Devon and Pablo were never released. That's another thing, that's very important to me: **Whoever takes the time to contribute should have a great experience and their contribution should be valued.** The ultimate show of appreciation is releasing the feature they worked on is getting it released into people's hands.

At times those negative feelings ("Oh no there is a bug" & "Oh no these great features lie around unreleased") paradoxically lead me to stay away from Benchee even more since I felt bad about this state. Yes, it was only on mac and only affected benchmarks where individual function invocations took less than 10 microseconds. But still, that's the perfectionist in me. This should be fixed within weeks, not 2.5 years. Most certainly, ready to ship features shouldn't just chill on main for _years_. Release early, release often.

Anyhow, thanks for reading my musings on Open Source, responsibility, pragmatism and perfectionism. The bug is fixed now, the features are released and I'm happy. Who knows what's next for Benchee.

Happy benchmarking!
