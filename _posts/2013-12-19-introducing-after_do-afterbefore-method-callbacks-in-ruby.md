---
layout: post
title: 'Introducing after_do: after/before method callbacks in Ruby'
description: None
date: 2013-12-19 14:34:28 -0000
last_modified_at: 2013-12-19 14:34:28 -0000
publish: true
pin: false
categories:
- Ruby
tags:
- after
- after_do
- aop
- aspect oriented programming
- before
- blocks
- callbacks
- cross-cutting concerns
- gem
- ruby
---
I want to introduce you to a little gem I built and use in some of my projects: [after_do](https://github.com/PragTob/after_do "after_do github page"). What it does is pretty simple: you can attach callback blocks before/after methods are executed. And it looks like this: 
```
 MyClass.after :some_method do whatever_you_want end # or/and MyClass.before :some_method do pure_magic end 
```
 As I don't fancy monkeypatching you will have to extend classes that you want to use after_do on with the AfterDo module. E.g. for the code above to work: 
```
 MyClass.extend AfterDo 
```
 after_do has no external runtime dependencies and the code is around 160 lines (blank lines and documentation included) with lots of small methods. So simplecov reports there are a little above 70 relevant lines code (it ignores blank lines, docs etc.). It works and is tested with current releases of all major ruby interpreters, e.g. MRI (1.9.3 and 2.0), JRuby and rubinius. The [github repo](https://github.com/PragTob/after_do) has some more documentation about use cases etc. - I won't go into all of it here.

## Why would I want to do that?

For me this catches the essence of Aspect Oriented Programming - doing something before or after a method is executed to fight cross-cutting concerns. What are these cross-cutting concerns? Glad you asked! They are aspects of your application that you can't confine to a single class but are rather spread over multiple classes. One of the most common examples is logging: Logging is done in many classes and many methods. As a result the real purpose of a method is cluttered with logging statements and it's hard to get an overview of all the logging statements in your application at once. Another example would be statistics: You might want to keep track of successful purchases, failed logins etc... the code to do so goes in the method that handle these cases but really doesn't contribute much to its actual purpose. And I've seen people use global variables to make statistics gathering available everywhere. Yikes. With aspect oriented programming you could have all of those in a single file and as a result not clutter the original methods at all.

## Access to parameters and the object

For a lot of purposes it's nice to have access to the parameters of a method call and the object itself - after_do gives you [just that](https://github.com/PragTob/after_do#getting-a-hold-of-the-method-arguments-and-the-object "part of after_do README"): 
```
 MyClass.after :two_arg_method do |arg1, arg2, obj| something(arg1, arg2, obj) end 
```
 With this you can log events like a succesful purchase: 
```
 # Assuming CheckoutProcess#complete gets user as an argument CheckoutProcess.after :complete do |user, checkout| @logger.log "#{user.name} checked out #{checkout.id}" end 
```


## Removing repetition

Another use case is removing repetition from within a class. E.g. if you want to call the save method of an object after several different methods you can do the following: 
```
 class CoolClass extend AfterDo # lots of methods after :m1, :m2, :m3 do |*args, object| object.save end end 
```
 This might remind you a bit of before_action/filter in Rails controllers.

## How does it work?

When you attach a callback to a method with after_do what it basically does is it creates a copy of that method and then redefines the method to basically look like this (pseudo code): 
```
 execute_before_callbacks return_value = original_method execute_after_callbacks return_value 
```


## Why build something like this?

I was working on a [side project](https://github.com/PragTob/pomodoro_tracker) after reading Objects on Rails and wanted to try to separate the persistence concern from the actual Object domain logic. For the fun of it and remove repetition along the way. My initial research didn't come up with a good maintained tiny library to serve my purpose. So I wrote one myself, named it after_do et voila there is the solution to my initial problem: 
```
 persistor = FilePersistor.new Activity.extend AfterDo Activity.after :start, :pause, :finish, :resurrect, :do_today, :do_another_day do |activity| persistor.save activity end 
```
 Nice, isn't it?

## Is this a good idea?

Always depends on what you are doing with it. As many things out there it has its use cases but can easily be misused.

### Advantages

* Get cross cutting concerns packed together in one file - don't have them scattered all over your code base obfuscating what the real responsibility of that class is
* Don't repeat yourself, define what is happening when in one file
* I feel like it helps the Single Responsibility principle, as it enables classes to focus on what their main responsibility is and not deal with other stuff

### Drawbacks

* You lose clarity. With callbacks after a method it is not immediately visible what happens when a method is called as some behavior might be defined elsewhere.
* You could use this to modify the behavior of classes everywhere. Don't. Use it for what it is meant to be used for - a concern that is not the primary concern of the class you are adding the callback to but that class is still involved with.

A use case I feel this is particularly made for is redrawing. That's what we use it for over at [shoes4](https://github.com/shoes/shoes4). E.g. we have multiple objects and different actions on these objects may trigger a redraw (such changing the position of a circle). This concern could be littered and repeated all over the code base. Or nicely packed into [one file](https://github.com/shoes/shoes4/blob/master/lib/shoes/swt/redrawing_aspect.rb "Redrawing Aspect") where you don't repeat yourself for similar redrawing scenarios and you see all the redraws at one glance. Furthermore it makes it easier to do things like "Just do one redraw every 1/30s" (not yet implemented though). Ultimately, **you be the judge**. I'd be happy if you were to go ahead and give [after_do](http://rubygems.org/gems/after_do) a try, say what you think about it, report bugs and feature requests.
