---
layout: post
permalink: https://pragtob.wordpress.com/2019/04/08/revisiting-tail-call-optimization-in-elixir-erlang-with-benchee-1-0/
title: Revisiting "Tail Call Optimization in Elixir &amp; Erlang" with benchee 1.0
description: None
date: 2019-04-08 15:00:51 -0000
last_modified_at: 2019-04-08 12:56:30 -0000
publish: true
pin: false
categories:
- Elixir
- Software Engineering
tags:
- benchee
- benchee_html
- benchmark
- tail call optimization
- tail-recursive
---
All the way back in June 2016 I wrote a well received [blog post about tail call optimization in Elixir and Erlang](https://pragtob.wordpress.com/2016/06/16/tail-call-optimization-in-elixir-erlang-not-as-efficient-and-important-as-you-probably-think/). It was probably the first time I really showed off my benchmarking library [benchee](https://github.com/bencheeorg/benchee), it was just a couple of days after the 0.2.0 release of benchee after all. Tools should get better over time, allow you to do things easier, promote good practices or enable you to do completely new things. So how has benchee done? Here I want to take a look back and show how we've improved things.

## What's better now?

In the old benchmark **I had to** :

* manually collect Opearting System, CPU as well as Elixir and Erlang version data
* manually create graphs in Libreoffice from the CSV output
* be reminded that performance might vary for multiple inputs
* crudely measure memory consumption in one run through on the command line

The **new benchee** :

* collects and shows system information
* produces extensive HTML reports with all kinds of graphs I couldn't even produce before
* has an inputs feature encouraging me to benchmark with multiple different inputs
* is capable of doing memory measurements showing me what consumers more or less memory

I think that these are all great steps forward of which I'm really proud.

## Show me the new benchmark!

Here you go, careful it's long ([implementation of MyMap for reference](https://github.com/PragTob/elixir_playground/blob/master/lib/my_map.ex)): https://gist.github.com/PragTob/f4ff9e4dc01bd0271effbdd8402fc244 We can easily see that the tail recursive functions seem to always consume more memory. Also that our tail recursive implementation with the switched argument order is mostly faster than its sibling (always when we look at the median which is worthwhile if we want to limit the impact of outliers). Such an (informative) wall of text! How do we spice that up a bit? How about the [HTML report generated from this](http://www.pragtob.info/benchee/tco//tco_focussed_detailed_inputs.html)? It contains about the same data but is enhanced with some nice graphs for comparisons sake: ![newplot\(4\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot4.png) ![newplot\(5\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot5.png) It doesn't stop there though, some of my favourite graphs are the once looking at individual scenarios: ![newplot\(6\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot6.png) This Histogram shows us the distribution of the values pretty handily. We can easily see that most samples are in a 100Million - 150 Million Nanoseconds range (100-150 Milliseconds in more digestible units, scaling values in the graphs is somewhere on the road map ;)) ![newplot\(7\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot7.png) Here we can just see the raw run times in order as they were recorded. This is helpful to potentially spot patterns like gradually increasing/decreasing run times or sudden spikes.

## Something seems odd?

Speaking about spotting, have you noticed anything in those graphs? Almost all of them show that some big outliers might be around screwing with our results. The basic comparison shows pretty big standard deviation, the box plot one straight up shows outliers (little dots), the histogram show that for a long time there's nothing and then there's a measurement that's much higher and in the raw run times we also see one enormous spike. All of this is even more prevalent when we look at the graphs for the small input (10 000 elements): ![newplot\(8\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot8.png) Why could this be? Well, my favourite suspect in this case is garbage collection. It can take quite a while and as such is a candidate for huge outliers - the more so the faster the benchmarks are. So let's try to **take garbage collection out of the equation**. This is somewhat controversial and we can't take it out 100%, but we can significantly limit its impact through [benchee's hooks feature](https://github.com/bencheeorg/benchee#hooks-setup-teardown-etc). Basically through adding `after_each: fn _ -> :erlang.garbage_collect() end` to our configuration we tell benchee to run garbage collection after every measurement to minimize the chance that it will trigger during a measurement and hence affect results. You can have a look at it in [this HTML report](http://www.pragtob.info/benchee/tco/tco_focussed_detailed_inputs_gc.html). We can immediately see in the results and graphs that standard deviation got a lot smaller and we have way fewer outliers now for our smaller input sizes: ![newplot\(9\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot9.png)

##

## ![newplot\(10\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot10.png)

Note however that our sample size also went down significantly (from over 20 000 to... 30) so increasing benchmarking time might be worth while to get more samples again. How does it look like for our big 5 Million input though? ![newplot\(11\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot11.png) Not much of an improvement... Actually slightly worse. Strange. We can find the likely answer in the raw run time graphs of all of our contenders: ![newplot\(13\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot13-1.png)![newplot\(12\).png](https://pragtob.wordpress.com/wp-content/uploads/2019/04/newplot12-1.png) The first sample is always the slowest (while running _with_ GC it seemed to be the third run). My theory is that for the larger amount of data the BEAM needs to repeatedly grow the memory of the process we are benchmarking. This seems strange though, as that should have already happened during warmup (benchee uses one process for each scenario which includes warmup and run time). It might be something different, but it very likely is a one time cost.

## To GC or not to GC

Is a good question. Especially for very micro benchmarks it can help stabilize/sanitize the measured times. Due to the high standard deviation/outliers whoever is fastest can change quite a lot on repeated runs. However, Garbage Collection happens in a real world scenario and the amount of "garbage" you produce can often be directly linked to your run time - taking the cleaning time out of equation can yield results that are not necessarily applicable to the real world. You could also significantly increase the run time to level the playing field so that by the law of big numbers we come closer to the true average - spikes from garbage collection or not.

## Wrapping up

Anyhow, this was just a little detour to show how some of these graphs can help us drill down and find out why our measurements are as they are and find likely causes. The improvements in benchee mean the promotion of better practices and much less manual work. In essence I could just link the HTML report and then just discuss the topic at hand (well save the benchmarking code, that's not in there... yet ;) ) which is great for publishing benchmarks. Speaking about discussions, I omitted the discussions around tail recursive calls etc. with comments from José Valim and Robert Virding. Feel free to still read the [old blog post](https://pragtob.wordpress.com/2016/06/16/tail-call-optimization-in-elixir-erlang-not-as-efficient-and-important-as-you-probably-think/) for that - it's not that old after all. Happy benchmarking!
