---
layout: post
title: 'Released: benchee 0.6.0, benchee_csv 0.5.0, benchee_json and benchee_html
  - HTML reports and nice graphs!'
description: None
date: 2016-12-01 15:06:44 -0000
last_modified_at: 2016-12-01 15:06:44 -0000
publish: true
pin: false
image:
  path: https://pragtob.wordpress.com/wp-content/uploads/2016/12/report.png
categories:
- Software Engineering
tags:
- benchee
- benchmarking
- Elixir
- graph
- png export
---
The last days I've been hard at work to polish up and finish releases of [benchee](https://github.com/PragTob/benchee) (0.6.0 - [Changelog](https://github.com/PragTob/benchee/blob/master/CHANGELOG.md)), [benchee_csv](https://github.com/PragTob/benchee_csv) (0.5.0 - [Changelog](https://github.com/PragTob/benchee_csv/blob/master/CHANGELOG.md)) as well as the initial releases of [benchee_html](https://github.com/PragTob/benchee_html) and [benchee_json](https://github.com/PragTob/benchee_json)! I'm the proudest and happiest of finally getting benchee_html out of the door along with great HTML reports including plenty of graphs and the ability to export them! You can check out the [example online report](http://www.pragtob.info/benchee/tco_detailed_big_\(1_million\).html) or glance at this screenshot of it: [![report](https://pragtob.wordpress.com/wp-content/uploads/2016/12/report.png)](https://pragtob.wordpress.com/wp-content/uploads/2016/12/report.png)While benchee_csv had some mere updates for compatibility and benchee_json just transforms the general suite to JSON (which is then used in the HTML formatter) I'm particularly excited about the **big new features** in benchee and of course benchee_html!

## Benchee

The 0.6.0 is probably the biggest release of the "core" benchee library with some needed API changes and great features.

### New run API - options last as keyword list

The "old" way you'd optionally pass in options as the first argument into run as a map and then define the jobs to benchmark in another map. I did this because in my mind the configuration comes first and maps are much easier to work with through pattern matching as opposed to keyword lists. However, having an optional first argument already felt kind of weird... Thing is, that's not the most elixir way to do this. It is rather conventional to pass in options as the last argument and as a keyword list. After voicing my concerns in the [elixirforum](https://elixirforum.com/t/passing-in-options-maps-vs-keyword-lists/1963), the solution was to allow passing in options as keyword lists but convert to maps internally to still have the advantage of good pattern matching among other advantages. https://gist.github.com/pragtobgists/d3cd52cb68c935c39f6ca6b3c9cf1511 The old style still works (thanks to pattern matching!) - but it might get deprecated in the future. In this process though the run interface of the very first version of run, which used a list of tuples, doesn't work anymore :(

### Multiple inputs

The great new feature is that benchee now supports multiple inputs - so that in one suite you can run the same functions against multiple different inputs. That is important as functions can behave very differently on inputs of different sizes or a different structure. Therefore it's good to check the functions against multiple inputs. The feature was [inspired by a discussion on an elixir issue with José Valim](https://github.com/elixir-lang/elixir/issues/5082). So what does this look like? Here it goes: https://gist.github.com/pragtobgists/81adfbdc0d54760666a6887650e26d9f The hard thing about it was that it changed how benchmarking results had to be represented internally, as another level to represent the different inputs was needed. This lead to quite some work both in benchee and in plugins - but in the end it was all worth it :)

## benchee_html

This has been in the making for way too long, should have released a month or 2 ago. But now [it's here](https://github.com/PragTob/benchee_html)! It provides a nice HTML table and four different graphs - 2 for comparing the different benchmarking jobs and 2 graphs for each individual job to take a closer look at the distribution of run times of this particular job. There is a [wiki page at benchee_html to discern between the different graphs](https://github.com/PragTob/benchee_html/wiki/Chart-Types) highlighting what they might be useful for. You can also export PNG images of the graphs at click of a simple icon :) Wonder how to use it? Well it was already shown earlier in this post when showing off the new API. You just specify the formatters and the file where it should be written to :) But without further ado you can check out the [sample report](http://www.pragtob.info/benchee/tco_detailed_big_\(1_million\).html) or just take a look at these images :) [![ips](https://pragtob.wordpress.com/wp-content/uploads/2016/12/ips.png)](https://pragtob.wordpress.com/wp-content/uploads/2016/12/ips.png)[![boxplot](https://pragtob.wordpress.com/wp-content/uploads/2016/12/boxplot.png)](https://pragtob.wordpress.com/wp-content/uploads/2016/12/boxplot.png)[![histogram](https://pragtob.wordpress.com/wp-content/uploads/2016/12/histogram.png)](https://pragtob.wordpress.com/wp-content/uploads/2016/12/histogram.png)

## [![raw_run_times](https://pragtob.wordpress.com/wp-content/uploads/2016/12/raw_run_times.png)](https://pragtob.wordpress.com/wp-content/uploads/2016/12/raw_run_times.png)Closing Thoughts

Hope you enjoy benchmarking, with different inputs and then see great reports of them. Let me know what you like about benchee or what you don't like about it and what could be better.
