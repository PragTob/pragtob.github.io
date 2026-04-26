---
layout: post
permalink: https://pragtob.wordpress.com/2023/12/22/benchee-1-3-0-published-oh-save-the-memory/
title: Benchee 1.3.0 published - oh, save the memory!
description: None
date: 2023-12-22 11:40:21 -0000
last_modified_at: 2023-12-22 11:40:21 -0000
publish: true
pin: false
categories:
- Elixir
tags:
- benchee
- memory consumption
- release
---
As per usual you can check out the [official Changelog](https://github.com/bencheeorg/benchee/blob/main/CHANGELOG.md#130-2023-12-22) for what exactly happened. This is a more personal look, featuring both the highlights of the release and some more musings.

The highlights are:

* Vastly reduced memory usage when benchmarking with big inputs
* New `Benchee.report/1` to simplify working with saved benchmarks
* finally configured times will be shown in a human compatible format

So let's dig in a bit.

## How did this release happen?

I didn't want to release a new benchee version so soon. What happened is I sat down to write a huge benchmark and you can check out this handy list for what transpired going on from there:

1\. Write huge benchmark  
2\. Fix missing ergonomics in benchee  
3\. memory consumption high, investigate  
4\. Implement new feature as fix  
5\. Realize it was the wrong fix, worked by accident  
6\. Fix real issue  
7\. Blog about issue cos 🤦‍♂️ (see [post](https://pragtob.wordpress.com/2023/12/18/careful-what-data-you-send-or-how-to-tank-your-performance-with-task-async/))  
8\. Remove now unneeded feature as it doesn't fix it  
9\. Release new benchee version** <\--- we are here**  
10\. Write actual benchmark

So... we're close to me blogging about that benchmark 😅 Maybe... next week?

And I mean that's fine and fun - one of the biggest reasons why benchee exists is because I love writing benchmarks and benchee is here to make that (along with blogging about it) as easy, seamless and friction-less as possible. So, me pushing the boundaries of benchee and making it better in the process is working as intended.

## How big are those memory savings?

To put it into context [the benchmark I'm working on](https://github.com/PragTob/tco_elixir), has 3 functions and 4 inputs (10k list --> 10M list) - so 12 scenarios in total. This is then run on 4 different elixir x erlang combinations - totaling 48 scenarios.

The changes on the 1.3 branch had the following impact:

* Memory consumption for an individual run (12 scenarios, saving them) went from **~6.5 GByte to ~5.1 GByte - saving more than 20%.**
* The **size of saving the results of one run went from ~226MB to ~4MB**. That is with a _long_ benchmarking time, decreasing it to 10 seconds we're looking at ~223MB down to 1MB.
* Before the change creating the report (all 48 scenarios) took between **12.8 GB and 18.6GB (average ~15.3 GB). Afterwards? 1.8 GB - a reduction down to ~12%.**
* The time it takes to create the report also **went from ~18 seconds to ~3.4 seconds, more than 5 times as fast.**

So, while I'm still 🤦‍♂ that this was ever an issue, I'm also happy about the fix and shipping those changes to you. I go more into what the actual issue was and how it was fixed in my [previous post](https://pragtob.wordpress.com/2023/12/18/careful-what-data-you-send-or-how-to-tank-your-performance-with-task-async/).

## Downsides of the change

At its heart the change that enabled this is just "stop sending inputs and benchmarking functions into other processes when they are not needed" - which is reasonable, I know statistics calculation does not need access and formatters _should not_ need access. However, **it is still a breaking change for formatter plugins** which I generally don't want to put onto people - but in this case in my head it's a bug. This data was never intended to be available there - it was a pure oversight of mine due to magic.

## The feature that never was

As perhaps a fun anecdote, during the (short) 1.3 development period **I implemented and removed an entire feature**. The short of it is that when I ran into the outrageous memory consumption problems, I first thought it was (in part) due to formatters being executed in parallel and so holding too much memory in memory. I implemented a new function `sequential_output` that allowed formatting a something and immediately writing it out. This was opposed to how benchee generally works - first formatting everything, and then writing it out.

And... it worked! Memory consumption was down - but how? Well, when running it I didn't execute it in a separate process - hence the data copying issue never occurred. It worked by accident.

Thankfully I ran a benchmark and put it head to head against `format` and `write` \- both without processes around - and was shocked to find out that they were the same performance wise. So... that's how I started to see that the actual problem was launching the extra processes and copying the data to them.

In the end, that feature didn't provide enough upside any more to justify its existence. You can [say goodbye to it here](https://github.com/bencheeorg/benchee_html/pull/63).

## Closing

With that, all that's left to say is: Hope you're doing well, always benchmark and happy holidays! 🌟
