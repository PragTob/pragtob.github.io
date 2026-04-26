---
layout: post
title: Benchee 0.5.0 released - unit scaling for your convenience!
description: None
date: 2016-10-13 15:15:45 -0000
last_modified_at: 2016-10-13 08:21:56 -0000
publish: true
pin: false
categories:
- Uncategorized
tags: []
---
Another month and another release of my Elixir (micro-) benchmarking library [benchee](https://github.com/PragTob/benchee). This particular release focusses on unit scaling. E.g. instead of displaying that you had 12_345_678 iterations per second it will now say that there were 12.35 M iterations per second. The same goes for the time as well. There are [four different strategies](https://hexdocs.pm/benchee/Benchee.Config.html) to choose from determining how units should be scaled. My friend and old [Shoes](http://shoesrb.com/) (Ruby tooklkit/DSL for building GUIs) companion [Eric Watson aka @wasnotrice](https://twitter.com/wasnotrice) did the bulk of the work. Thanks! As usual, the nitty-gritty details are in the [Changelog](https://github.com/PragTob/benchee/blob/master/CHANGELOG.md#050-october-13-2016).

## Why unit scaling?

The units employed so far were not ideal. Who really works with microseconds all the time and like to read full numbers over a million while only the first couple of places really have an impact? I think it's easier to work with units closer to what a number really is. If something takes 5_632 microseconds to execute I'm much better off knowing that it takes about 5.63 milliseconds. So from now on benchee will use one of its four strategies (one of which is none, if you don't like this behaviour at all) to determine what the best unit to represent the benchmarking results in might be. For the canonical flat_map vs. map.flatten example the result might look like this: https://gist.github.com/pragtobgists/0e37be2494d80271f698e3469193ea51 See how the units were automatically scaled to thousands/milliseconds respectively? Now, you might not like that because you always want there to at least be a "1" before the dot. No problem, just use another scaling strategy: _smallest_! https://gist.github.com/pragtobgists/8e05c96083c8f53afa43cc7788da4d04 This is now (in this case) pretty much like the output you'd get in previous benchee versions. Still, _smallest_ is different from _none_ in that if both averages were at least a millisecond they would still be displayed in milliseconds. Under the hood this is all nicely handled by units (Count, Duration) implementing the [Scale](https://github.com/PragTob/benchee/blob/master/lib/benchee/conversion/scale.ex) and [Format](https://github.com/PragTob/benchee/blob/master/lib/benchee/conversion/format.ex) behaviours while relying on a [Unit](https://github.com/PragTob/benchee/blob/master/lib/benchee/conversion/unit.ex) struct.

## What's next for benchee?

The next bigger topic that I've put quite some time and experiments in is an HTML formatter with fancy graphs and an image export. Want a sneak-peak? Ok, since you asked nicely: [![IPS comparison](https://pragtob.wordpress.com/wp-content/uploads/2016/10/newplot.png)](https://pragtob.wordpress.com/wp-content/uploads/2016/10/newplot.png)[![Boxplot](https://pragtob.wordpress.com/wp-content/uploads/2016/10/newplot1.png)](https://pragtob.wordpress.com/wp-content/uploads/2016/10/newplot1.png)
