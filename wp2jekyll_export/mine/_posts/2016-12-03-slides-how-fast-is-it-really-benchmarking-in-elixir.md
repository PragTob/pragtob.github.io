---
layout: post
permalink: https://pragtob.wordpress.com/2016/12/03/slides-how-fast-is-it-really-benchmarking-in-elixir/
title: 'Slides: How fast is it really? Benchmarking in Elixir'
description: None
date: 2016-12-03 17:31:56 -0000
last_modified_at: 2016-12-03 17:31:56 -0000
publish: true
pin: false
categories:
- Software Engineering
tags:
- benchee
- benchmark
- benchmarking
- Elixir
- elixirlive
---
I'm at [Elixirlive](http://www.elixirlive.com/) in Warsaw right now and just gave a talk. This talk is about benchmarking - the greater concepts but concrete examples are in Elixir and it works with my very own library [benchee](https://github.com/PragTob/benchee) to also show some surprising Elixir benchmarks. The concepts are applicable in general and it also gets into categorizing benchmarks into micro/macro/application etc. If you've been here and have feedback - positive or negative. Please tell me :) Slides are available as [PDF](https://pragtob.wordpress.com/wp-content/uploads/2016/12/elixirlive.pdf), [speakerdeck](https://speakerdeck.com/pragtob/how-fast-ist-it-really-benchmarking-in-practice) and [slideshare](http://www.slideshare.net/PragTob/how-fast-ist-it-really-benchmarking-in-practice). [slideshare id=69791915&doc=elixirlive-161203172735]

### Abstract

> “What’s the fastest way of doing this?” - you might ask yourself during development. Sure, you can guess what’s fastest or how long something will take, but do you know? How long does it take to sort a list of 1 Million elements? Are tail-recursive functions always the fastest? Benchmarking is here to answer these questions. However, there are many pitfalls around setting up a good benchmark and interpreting the results. This talk will guide you through, introduce best practices and show you some surprising benchmarking results along the way.
