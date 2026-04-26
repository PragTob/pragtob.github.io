---
layout: post
permalink: https://pragtob.wordpress.com/2014/01/19/after_do-0-3-0-released/
title: after_do 0.3.0 released
description: None
date: 2014-01-19 14:36:37 -0000
last_modified_at: 2014-01-19 14:36:37 -0000
publish: true
pin: false
categories:
- Ruby
tags:
- after_do
- callbacks
- gem
- methods
- release
- ruby
---
I just released version 0.3.0 of my little aspect oriented programming/adding callbacks to methods library [after_do](https://github.com/PragTob/after_do)! You can find an introduction [here](http://pragtob.wordpress.com/2013/12/19/introducing-after_do-afterbefore-method-callbacks-in-ruby/). So what is in 0.3.0? Basically 2 things:

* after_do now **works properly with modules** , meaning you can attach callbacks to the methods of a module and objects of classes including those methods will call them!
* Fixed bugs around inheritance where it could happen that a block might get called too often or not at all

At the same time this release was able to delete code and remove complexity while improving functionality. How is that possible? Well thanks to **block scoping** it is! One problem I always had is to figure out callbacks of which class to execute in combination with inheritance. You know - self is always the current object and callbacks might be defined in super classes. I wanted to have a way to know which class the currently called method is defined in, not what the class of the current object is. Luckily there is one point where I know that - the moment when I add the callbacks (since they are added on that exact class/module). So we just need to save it: [sourcecode lang="ruby"] callback_klazz = self define_method method do |*args| callback_klazz.send(:_after_do_execute_callbacks, :before, method, self, *args) return_value = send(alias_name, *args) callback_klazz.send(:_after_do_execute_callbacks, :after, method, self, *args) return_value end [/sourcecode] Simple yet powerful. Enjoy the 0.3 release of after_do :-)
