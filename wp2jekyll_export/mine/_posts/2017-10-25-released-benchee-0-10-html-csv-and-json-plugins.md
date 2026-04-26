---
layout: post
permalink: https://pragtob.wordpress.com/2017/10/25/released-benchee-0-10-html-csv-and-json-plugins/
title: 'Released: benchee 0.10, HTML, CSV and JSON plugins'
description: None
date: 2017-10-25 15:00:59 -0000
last_modified_at: 2017-10-25 08:02:14 -0000
publish: true
pin: false
categories:
- benchmark
- Elixir
- Software Engineering
tags:
- benchee
- benchee_html
- benchmarking
- hex
- hooks
- package
- release
---
It's been a little time since the last [benchee](https://github.com/PragTob/benchee) release, have we been lazy? Au contraire mes ami! We've been hard at work, greatly improving the internals, adding a full system for hooks (before_scenarion, before_each, after_each, after_scenario) and some other great improvements thanks to many contributions. The releases are [benchee](https://github.com/PragTob/benchee) 0.10.0 ([CHANGELOG](https://github.com/PragTob/benchee/blob/master/CHANGELOG.md#0100-2017-10-24)), [benchee_csv](https://github.com/PragTob/benchee_csv/) 0.7.0 ([CHANGELOG](https://github.com/PragTob/benchee_csv/blob/master/CHANGELOG.md#070-2017-10-24)), [benchee_html](https://github.com/PragTob/benchee_html) 0.4.0 ([CHANGELOG](https://github.com/PragTob/benchee_html/blob/master/CHANGELOG.md#040-2017-10-24)) and [benchee_json](https://github.com/PragTob/benchee_json) 0.4.0 ([CHANGELOG](https://github.com/PragTob/benchee_json/blob/master/CHANGELOG.md)). Sooo... what's up? Why did it take so long?

## benchee

Before we take a look at the exciting new features, here's a small summary of major things that happened in previous releases that I didn't manage to blog about due to lack of time: **0.7.0** added mainly convenience features, but benchee_html **0.2.0** split up the HTML reports which made it easier to find what you're looking for but also alleviated problems with rendering huge data sets (the graphing library was reaching its limits with that many graphs and input values) **0.8.0** added type specs for the major public functions, configuration is now a struct so errors out on unrecognized options **0.9.0** is one of my favorite releases as it now gathers and shows system data like number of cores, operating system, memory and cpu speed. I love this, because normally when I benchmark I and write about it I need to write it up in the blog post. Now with benchee I can just copy & paste the output and I get all the information that I need! This version also facilitates calling benchee from Erlang, so _benchee:run_ is in the cards. Now ahead, to the truly new stuff:

### Scenarios

In benchee each processing step used to have its own main key in the main data structure (suite): run_times, statistics, jobs etc. Philosophically, that was great. However, it got more cumbersome in the formatters especially after the introduction of inputs as access now required an additional level of indirection (namely, the input). As a result, to get all the data for a combination of job and input you want to format you have got to merge the data of multiple different sources. Not exactly ideal. To make matters worse, we want to add memory measurements in the future... even more to merge. Long story short, [Devon](https://duckduckgo.com/?q=devon+c+estes+&t=lm&atb=v78-2&ia=web) and I sat down in person for 2 hours to discuss how to best deal with this, how to name it and all accompanying fields. We decided to keep all the data together from now on - for every entry of the result. That means each combination of a job you defined and an input. The data structure now keeps that along with its raw run times, statistics etc. After some research we settled on calling it a **scenario**. https://gist.github.com/pragtobgists/23969003bb3ad86d4dacaddfb6d3807d This was a huge refactoring but we really like the improvements it yielded. Devon [wrote about the refactoring process](https://duckduckgo.com/?q=devon+c+estes+&t=lm&atb=v78-2&ia=web) in more detail. It took a long time, but it didn't add any new features - so no reason for a release yet. Plus, of course all formatters also needed to get updated.

### **Hooks**

Another huge chunk of work went into a hooks system that is pretty fully featured. It allows you to execute code before and after invoking the benchmark as well as setup code before a scenario starts running and teardown code for after a scenario stopped running. That seems weird, as **most of the time you won't need hooks**. We could have released with part of the system ready, but I didn't want to (potentially) break API again and so soon if we added arguments or found that it wasn't quite working to our liking. So, we took some time to get everything in. So what did we want to enable you to do?

* Load a record from the database in before_each and pass it to the benchmarking function, to perform an operation with it without counting the time for loading the record towards the benchmarking results
* Start up a process/service in before_scenario that you need for your scenario to run, and then...
* ...shut it down again in after_scenario, or bust a cache
* Or if you want your benchmarks to run without a cache all the time, you can also bust it in before_each or after_each
* after_each is also passed the return value of the benchmarking function so you can run assertions on it - for instance for all the jobs to see if they are truly doing the same thing
* before_each could also be used to randomize the input a bit to benchmark a more diverse set of inputs without the randomizing counting towards the measured times

All of these hooks can be configured either globally so that they run for all the benchmarking jobs or they can be configured on a per job basis. The [documentation for hooks over at the repo](https://github.com/PragTob/benchee#hooks-setup-teardown-etc) is a little blog post by itself and I won't repeat it here ;) As a little example, here is me benchmarking hound: https://gist.github.com/pragtobgists/b9b1ec129d19a734d50f619933400cf5 Hound needs to start before we can benchmark it. Howeer, hound seems to remember the started process by the pid of self() at that time. That's a problem because each benchee scenario runs in its own process, so you couldn't just start it before invoking Benchee.run. I found no way to make the benchmark work with good old benchee 0.9.0, which is also what finally brought me to implement this feature. Now in benchee 0.10.0 with before_scenario and after_scenario it is perfectly feasible!

### Why no 1.0?

With all the major improvements one could easily call this a 1.0. Or 0.6.0 could have been a 1.0 then we'd be at 2.0 now - wow that sounds mature! Well, I see 1.0 as a promise - a promise for plugin developers and others that compatibility won't be broken easily and not soon. Can't promise this when we just broke plugin compatibility in a major way. That said, I really feel good about the new structure, partly because we put so much time and thought into figuring it out, but also because it has greatly simplified some implementations and thinking about some future features it also makes them a lot easier to implement. Of course, we didn't break compatibility for users. That has been stable since 0.6.0 and to a (quite big) extent beyond that. So, 1.0 will of course be coming some time. We might get some more bigger features in that could break compatibility (although I don't think they will, it will just be new fields):

* Measuring memory consumption
* recording and loading benchmarking results
* ... ?

Also before a 1.0 release I probably want to extract more not directly benchmarking related functionality from benchee and provide as general purpose libraries. We have some sub systems that we build for us and would provide value to other applications:
* Unit: convert units (durations, counts, memory etc.), scale them to a "best fit" unit, format them accordingly, find a best fit unit for a collection of values
* Statistics: All the statistics we provide including not so easy/standard ones like nth percentile and mode
* System: gather system data like elixir/erlang version, CPU, Operating System, memory, number of cores

Thanks to the design of benchee these are all already fairly separate so extracting them is more a matter of when, not how. Meaning, that we have all the functionality in those libraries that we need so that we don't have to make a coordinated release for new features across n libraries.

## benchee_html

![Selection_045.png](https://pragtob.wordpress.com/wp-content/uploads/2017/10/selection_045.png) Especially due to many great community contributions (maybe because of [Hacktoberfest](https://hacktoberfest.digitalocean.com/)?) there's a number of stellar improvements!

* System information is now also available and you can toggle it with the link in the top right
* unit scaling from benchee "core" is now also used so it's not all in micro seconds as before but rather an appropriate unit
* reports are automatically opened in your browser after the formatter is done (can of course be deactivated)
* there is a default file name now so you don't HAVE to supply it

## What's next?

Well this release took long - hope the next one won't take as long. There's a couple of improvements that didn't quite make it into the release so there might be a smaller new release relatively soon. Other than that, work on either serializing or the often requested "measure memory consumption" will probably start some time. But first, we rest a bit ;) Hope you enjoy benchmarking and if you are missing a feature or getting hit by a bug, please [open an issue](https://github.com/PragTob/benchee/issues/new) <3    
