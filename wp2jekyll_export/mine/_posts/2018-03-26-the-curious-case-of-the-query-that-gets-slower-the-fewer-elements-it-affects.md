---
layout: post
permalink: https://pragtob.wordpress.com/2018/03/26/the-curious-case-of-the-query-that-gets-slower-the-fewer-elements-it-affects/
title: The curious case of the query that gets slower the fewer elements it affects
description: None
date: 2018-03-26 12:58:20 -0000
last_modified_at: 2018-03-23 13:58:39 -0000
publish: true
pin: false
categories:
- benchmark
- Elixir
tags:
- benchee
- sql
---
I wrote a nice blog post for the company I'm working at ([Liefery](https://www.liefery.com/)) called ["The curious case of the query that gets slower the fewer elements it affects](http://engineering.liefery.com/2018/02/27/the-mysterious-query.html)", which goes through a real world benchmarking with [benchee](https://github.com/PragTob/benchee). It involves a couple of things that can go wrong but how combined indexes and PostgreSQL's EXPLAIN ANALYZE can help you overcome it problems. It's honestly one of the blog posts I think I ever wrote so head over and read it if that sounds interesting to you :)
