---
layout: post
title: How to get started with contributing to open source
description: None
date: 2014-01-13 14:10:14 -0000
last_modified_at: 2014-01-13 14:10:14 -0000
publish: true
pin: false
categories:
- Beginner
tags:
- beginner
- contribute
- contribution
- find project
- first
- github
- newcomer
- open source
---
I often see people who really want to contribute to open source projects. And that's great! But often it's not easy to get started. "What project should I contribute to?", "What can I do on that project?" and "How does contributing work?" are common questions. It can be scary. I found myself in the same place around 3 years ago. Since then I contributed to a variety of open source projects and am heavily involved in a few (including my own projects). This post is here to answer these questions, give you some help, guidance and share experience.

## Step 1 - Find a project

"Where to start?" "Which project can I contribute to?" These are usual questions. The most important principle here is **"Scratch your own itch!"** \- work on a project that you use and that matters to you. There is no point in investing energy into something you don't care about. Even better if you have a specific issue with a project: some odd behavior, a bug that you work around, a sub optimal API, lack of documentation... you name it. If you use some projects you'll find a couple of those. I guarantee it - nothing is perfect. Also try to see if the project isn't too far off your comfort zone - e.g. if you are a ruby programmer and don't know much C then contributing to a gem which is primarily a C-extension is probably not the best idea. Have a look at how active the project is. You'll want to contribute to a project that is still actively developed and where the maintainers react to issues and pull requests. For this you can look at a couple of things: When was the latest commit made? Look at the recent pull requests and issues: Did anyone comment on them? Is there a crazy amount of open pull requests, some of them like half a year old without activity? Another advice: Try not to contribute code to a really big project (think: rails) straight away, especially if you are a beginner. Those projects are... well... big. It's often hard to find the right place where a fix should occur. Familiarizing yourself with the code base unfortunately takes a lot longer as well. Also due to their nature, they often have a lot more issues and pull requests that the maintainers have to take care of. Often that results in longer feedback cycles, somebody else trying to fix the same problem and it diminishes the chance of making "a real impact". It's not the ideal scenario for first time contributors in my opinion. With small to medium-sized projects I often experienced that maintainers are a lot happier to get contributions and faster to respond.

## Step 2 - What to work on?

If you've got an itch you want to scratch you are already mostly ready to go. But first make sure that the problem persists even in the latest release of the software (even better on master). Then search the issue tracker of the project to check if the fault has already been reported. If not, report an issue (or feature request) to see if this actually is a problem/a wanted feature. In the best case you provide a small sample script demonstrating the error along with an expected behavior from your side. You can already mention that you'd like to work on this. If you don't have an itch to scratch but a project you'd love to help out: have a look at the issue tracker. Some projects feature tags/categories for newcomer friendly issues - check those out first. Otherwise look for something that seems appealing to you and not too complex. I want to stress that contributions aren't limited to fixing bugs and implementing new features. Helping out with documentation is very valuable, that's how quite some contributors get started. Also writing tests to increase test coverage or refactoring code (hint: some projects use [Code Climate](https://codeclimate.com/) \- you can check out code smells there) to remove duplication/make it more readable is often very welcome. I especially recommend the latter two as to do this you have to understand the code and therefore get a good first view of the code base without having to add anything. Make sure to have a look at the README of the project. It often highlights how to figure out what to work on and which kinds of contribution are welcome.

## Step 3 - Get your changes in!

Mostly you should make sure that there is an issue for what you want to work on (exceptions include small refactorings). In that issue comment that you would like to work on the problem, maybe outline a strategy to solve it if you already have one and ask for pointers and advice how to go about that issue. Also look at the README - a lot of projects mention how they'd like contributions to be handled. Also they might have references to style guides or guidelines such as "provide test cases that fail". A lot of them will also have instructions like these (at least on the most popular platform these days, [github](https://www.github.com)):

  1. Fork it
  2. Create your feature branch (`git checkout -b my-new-feature`)
  3. Commit your changes (`git commit -am 'Add some feature'`)
  4. Push to the branch (`git push origin my-new-feature`)
  5. Create new Pull Request

Forking is basically creating your own copy of the repository which you can write to. Creating a Pull Request is like saying: "Hey, I made these changes do you want to have them?" In a Pull Request the changes are discussed, commented and it's basically the way to get your changes in. I recommend opening pull requests early - as soon as the basing building blocks are standing. The feature doesn't need to work yet. This way you can get valuable feedback about whether this is the right approach as well as hints and tips leading to the right solution.

## Closing Notes

**Have fun contributing to open source!** There are a lot of nice people out there happy to get contributions of any form. And I can tell you - it's a great feeling to know you made something better for a lot of people (including yourself!). You might have seen an occasional story about big discussions or fights in pull requests/issues. Please don't let that scare you. I can tell you that from my experience these are the exception not the rule. **Most people in open source are really nice** and work together for a common goal. Two and a half years ago I started contributing to the [Shoes project](http://shoesrb.com/). To this day this is the nicest online community I ever met with a lot of really helpful and polite people around! I stayed with the project ever since - gradually increasing my contributions. I hope this post helps you to get started on your journey into the open source world. If there is something missing or you got more questions please feel free to add a comment.
