---
layout: post
title: 4 lessons learned from teaching at Rails Girls Berlin
description: None
date: 2012-08-13 22:08:55 -0000
last_modified_at: 2012-08-21 06:49:44 -0000
publish: true
pin: false
categories:
- Ruby
- Software Engineering
tags:
- beginner
- coaching
- rails girls
- ruby
- Ruby on Rails
- student
- teaching
---
This is just a little post recapping some of my experiences from the last [RailsGirls Berlin](http://railsgirlsberlin.tumblr.com/) workshop. By the way, we've got a [new workshop upcoming this Friday](http://2012.eurucamp.org/2012/08/13/about-beginners-workshops) and you can still register! Most of this is a reminder to myself in order to be an even better coach at our next workshop :-)

## 1\. irb can be great for teaching - but confusing as well

I love irb for teaching. You can show many things quickly and instantly. And you get feedback. You can play. It's awesome. However, especially for real beginners it is kind of confusing, even more so if it is the first time that they work with a console. So it's hard to distinguish what irb is and what the normal console is. In a later mentoring session I also had someone who disliked irb as a whole and rather wanted to write a _real_ program with real files. Everybody likes to learn his/her own way :-) However my main take away with irb is the following: Be aware of the nesting! And by that I mean **missing parentheses****and keywords!** You know the result: irb is waiting for the matching keyword/parenthesis. Beginners often don't notice this and are just wondering why it isn't working and behaving like with all the others. During our introduction to Ruby this was one of the most common blockers I saw, especially when we started working with blocks. So to get them out of this: **Ctrl + C**

## 2\. Restart the server after installing a new gem

We all know this one. In order to pick up on some changes the rails server has to be restarted. Although when you're teaching multiple students it's sometimes hard to remember. So if a step involving a new gem isn't working make sure it is installed and restart the server.

## 3\. Save the damn file

Yes save it. Please do. I know it's the simplest thing in the world but we are sometimes so used to saving our files that it doesn't even come to mind anymore. I once spent 15 minutes discovering that an unsaved file was the cause of an error. Before that another coach had already spent ~30mins on the same problem. We checked everything until we noticed the little star next to the file name in the tab bar. Then we saved the file, which we had previously looked at like a million times, and everything went well.

## 4\. Explain, but simplify

Explain what which part does but don't aim for perfection or total correctness. In other words: **Lie to simplify**. Focus on the most important knowledge. I gave very short introductions to the MVC-pattern (while looking through the code) and refined them until the student seemed satisfied. And don't omit the explanation. I know that Rails involves a lot of magic and it might be hard to explain, however I heard from some students that nobody explained the distinct roles of the model, the view and the controller to them. They didn't know what happened where. This left them really dissatisfied. They've built this awesome thing but had no idea how it works. I hope that these tips might be helpful for you when you are coaching. There are probably some more of these to come after the next workshop :-)
