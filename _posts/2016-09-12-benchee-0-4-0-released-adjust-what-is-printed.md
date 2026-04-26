---
layout: post
title: Benchee 0.4.0 released - adjust what is printed
description: None
date: 2016-09-12 09:30:30 -0000
last_modified_at: 2016-09-12 08:23:28 -0000
publish: true
pin: false
categories: []
tags:
- benchee
- benchmarking
- Elixir
- release
---
Today I made a little 0.4.0 release of my elixir benchmarking library [benchee](https://github.com/PragTob/benchee). As always the [Changelog has all the details](https://github.com/PragTob/benchee/blob/master/CHANGELOG.md#040-september-11-2016). This release mainly focusses on making all non essential output that benchee produces optional. This is mostly rooted in user feedback of people who wanted to [disable the fast execution warnings](https://github.com/PragTob/benchee/issues/17) or [the comparison report](https://github.com/PragTob/benchee/issues/22). I decided to go full circle and also make it configurable if benchee prints out which job it is currently benchmarking or if the general configuration information is printed. I like this sort of verbose information and progress feedback - but clearly it's not to everyone's taste and that's just fine :) So **what's next for benchee**? As a keen github observer might have noticed I've taken [a few](https://github.com/PragTob/benchee_d3) [stabs](https://github.com/PragTob/benchee_chart_js) at rendering charts in HTML + JS for benchee and in the process created [benchee_json](https://github.com/PragTob/benchee_json). I'm a bit dissatisfied as of now, as I'd really want to have graphs showing error bars and that seems to be harder to come by than I thought. After D3 and chart.js I'll probably give [highcharts](http://www.highcharts.com/products/highcharts) a stab now. However, just reading the _non-commercial_ terms again I'm not too sure if it's good in all sense (e.g. what happens if someone in a commercial corporation uses and generates the HTML?). Oh, but the wonders of the Internet in a new search I found [plotly which seems to have some great error bars support](https://plot.ly/javascript/error-bars/). Other future plans include benchmarking with multiple input sizes to see how different approaches perform or the good old topic of lessening the impact of garbage collection :)  
