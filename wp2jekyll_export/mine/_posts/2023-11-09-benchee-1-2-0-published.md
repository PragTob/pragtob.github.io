---
layout: post
permalink: https://pragtob.wordpress.com/2023/11/09/benchee-1-2-0-published/
title: Benchee 1.2.0 Published!
description: None
date: 2023-11-09 13:39:23 -0000
last_modified_at: 2023-11-09 13:39:23 -0000
publish: true
pin: false
categories:
- Elixir
- open source
tags:
- benchee
- release
---
Not really a big blog post this time around but benchee 1.2.0 was just published to hex.pm.

The highlights are the following:

* You'll be warned now when trying to benchmark evaluated function:

> Evaluated functions perform slower than compiled functions.
>
> You can move the Benchee caller to a function in a module and invoke `Mod.fun()` instead.
>
> Alternatively, you can move the benchmark into a benchmark.exs file and run mix run benchmark.exs

* Support for the `Table.Reader` protocol was baked into benchee for a better direct Livebook experience!
* Otherwise it's just been house keeping: compiler warnings and an error when running from escript.

Full changelog [here](https://github.com/bencheeorg/benchee/blob/main/CHANGELOG.md#120-2023-11-09).

## That's all... and that's good!

I'm glad that that's all, not to say I don't have ideas on what else to improve although I won't promise things. It's great that **benchee just works**. It's a mature piece of software that works well. We need to move away from declaring projects that haven't seen a release in a while as "dead". That said, of course some occasional updates on the repo to make sure they work with the most recent versions would be nice.

In particular I'm happy that **benchee already started out with warmup** as simply the right thing to do(tm). So, when erlang implemented a JIT I had nothing new to do as I new benchee already supported it perfectly.

And that's also true for all of benchee's "sister" libraries. I took some time for some house cleaning today to fix their CIs and run them against all the newest versions and... none of them needed any meaningful adjustment that would warrant a new release. That makes me happy.

Take care y'all! 💚

[![](https://pragtob.wordpress.com/wp-content/uploads/2023/11/img20230429163945.jpg?w=1024)](https://pragtob.wordpress.com/wp-content/uploads/2023/11/img20230429163945.jpg)
