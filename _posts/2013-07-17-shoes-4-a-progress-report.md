---
layout: post
title: Shoes 4 - a progress report
description: None
date: 2013-07-17 19:58:47 -0000
last_modified_at: 2013-07-17 19:58:47 -0000
publish: true
pin: false
image:
  path: https://pragtob.wordpress.com/wp-content/uploads/2013/07/shoes-icon.png
categories:
- Uncategorized
tags:
- google summer of code
- Graphical user interface
- JRuby
- pre-alpha
- progress
- ruby
- shoes
- shoes4
- simple
- SWT
---
My Google Summer of Code has been going on for one month now. The first commit on the [shoes4 repository](https://github.com/shoes/shoes4) is almost one year and two months old. I think this is a good time to introduce shoes4 to more people and take a look and see what we have accomplished so far.

## Shoes?

[Shoes](http://shoesrb.com/) is a multi-platform gui toolkit for Ruby aimed at simplicity. The probably most well-known Shoes program is [Hacketyhack](http://www.hackety.com/), a tool to teach programming to beginners. Shoes truly is one of a kind, for instance with its very own layout mechanisms "stack" and "flow". Personally I always wanted to write little GUI applications but always found it to be too cumbersome and frustrating. Until I met shoes. See how simple it is: [code language="ruby"] Shoes. app title: 'Hello Shoes' do background gradient limegreen..blue para 'This is just a very basic app' button 'Click me' do alert 'Hello there!' end image 'http://shoesrb.com/img/shoes-icon.png' end [/code]

## [![Screenshot from 2013-07-17 21:14:29](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-211429.png)](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-211429.png)

But this is not the only great feature of shoes, although it's certainly one of the reasons why I have fallen in love with shoes. Another feature is packaging: You can package your shoes applications as standalone applications for the different operating systems.

## Shoes 4?

Shoes4 is a complete rewrite of its predecessor keeping its features and enhancing the DSL here ant there. **"Why rewrite?"** , you might ask. Well [Shoes3](https://github.com/shoes/shoes) (or red shoes) is more of a C-project than a Ruby project. It has separate backends for each one of the major three operating systems. It's really hard to maintain. Unfortunately there are some bugs that make the install fail on some systems, a shot at a dependency upgrade was basically a frustrating story for everybody involved, packaging (sadly) is mostly broken etc. Also there always was the dream, that shoes could be a gem. That was just hard to accomplish with shoes3, so it is an executable embedding a ruby interpreter. Over time people have also started writing their own Shoes versions. There are a lot of them out there, by our count it's [9 versions of shoes right now](https://github.com/shoes/shoes4/wiki/Shoes-Implementations). Shoes4 is an effort for all implementers to join forces and work together so shoes can be shiny and new again. To accommodate the apparent desire of people to build their own pair of shoes we now use a new architecture. Basically there is a DSL layer with all the elements that the user will interact with. This layer already implements quite some of the logic. However an exchangeable backend does the real heavy lifting of drawing etc. . So almost every DSL class has a matching backend implementation. For now the default backend implementation uses [JRuby](http://www.jruby.org/) \+ [SWT](http://www.eclipse.org/swt/), but there also is a proof of concept backend in [Qt](https://github.com/wasnotrice/shoes-qt). One of the advantages of SWT is that it aims to have a native look and feel, which is in the spirit of the original shoes. And already using a cross-platform GUI library takes a lot of load from our shoulders. [caption id="attachment_848" align="aligncenter" width="490"][![Screenshot from 2013-07-17 21:23:27](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-212327.png)](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-212327.png) A very basic and yet to be polished graphic illustrating the DSL + backend approach.[/caption]

## Where are we at?

Here are some numbers to give you a feeling of where we are at right now:

* we are closing in on the 1000 commits mark
* Code coverage is at 92%
* 62 samples (little scripts to test things, some of them real shoes programs) are known to work
* 30 samples are not yet working / for many of them only tiny bids of implementation are missing to make them work and some of them are not scheduled to ship with 4.0 (e.g. video support)
* 21 people have contributed code and a lot more have helped with reporting issues, trying stuff out, being helpful etc. - THANK YOU ALL! :-)

As mentioned in the beginning there is a Google Summer of Code going on: [Faraaz](https://twitter.com/fism88) and me (with the help of our mentor [Davor](http://www.davor.se/)) are working hard to push Shoes4 forward. Here are some numbers concerning the first month of Google Summer of Code, we...

* closed 46 issues
* opened 18 issues
* pushed 193 commits...
* ..changing 202 files.
* Code Climate score has improved from 3.1 to 3.3 (and there is a continued effort to refactor the other offenders)

And since we are talking about graphical things, here are some screenshots of working samples with shoes4 as of now: [caption id="" align="aligncenter" width="729"]![](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-202924.png) The shoes4 builtin manual[/caption] [caption id="" align="aligncenter" width="709"]![](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-2032343.png) A little tank game[/caption] There are a lot more samples... you can play pong, watch some fancy animations, a simple to do list etc... One of the apparent questions is: **"Can I use shoes4 right now?"** The answer is: **"Not yet."** We are in pre-alpha stage. While a lot of things work, some don't. We will let you know when we release an alpha release or a release candidate for you to check out. However if you're adventurous you can check out the master on [github](https://github.com/shoes/shoes4) no matter what, feedback and reports about bugs are highly appreciated! So what is missing? Here are a couple of bigger things that are missing as of now:

* The span element to style parts of a text (used in a lot of samples)
* Reliable packaging for all platforms (there is basic .jar and Mac packaging though)
* quite some styling options for the different elements
* The shoes console and the methods that go with it

## Contributing

In general the shoes community is really nice and helpful, so if you want to take a swing at something we're happy to help and even happier about your contribution! We also have a new "Newcomer Friendly" tag to show the way to potentially good issues to get started on. Otherwise just look at [the issues](https://github.com/shoes/shoes4/issues) and comment there if you're interested in helping out. However just trying shoes4 out, fooling around or running a couple of samples is highly appreciated and helpful as well. Just refer to the README of the [shoes4 repository](https://github.com/shoes/shoes4) to get started. Lastly I want to thank the JRuby organization and Google for giving me the opportunity to work on an open source project I love full-time. [![Screenshot from 2013-07-17 21:02:08](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-210208.png)](http://pragtob.wordpress.com/wp-content/uploads/2013/07/screenshot-from-2013-07-17-210208.png)Furthermore, if you want to know more about shoes you might consider going to [JRuby Conf 2013](http://2013.jrubyconf.eu/) \- I will be speaking there about shoes and there are lots of other great talks as well! Shoes on! Tobi
