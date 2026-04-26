---
layout: post
title: Setting instance variables when instance_evaling a block in Ruby (Dual-Purpose
  Accessors to the rescue!)
description: None
date: 2011-09-13 20:48:53 -0000
last_modified_at: 2011-09-13 20:48:53 -0000
publish: true
pin: false
categories:
- Ruby
- Solution
tags:
- block
- Dual-Purpose Accessors
- instance_eval
- ruby
---
Yesterday I ran into a nasty problem while doing a task for [Mendicant University](http://university.rubymendicant.com/ "Mendicant University") (it is an awesome free university for learning Ruby and other stuff). I am not allowed to show you my work from there yet so please go with this kind of constructed example for now: [sourcecode language="ruby"] class Person attr_accessor :name, :age # just for demonstration purposes # (otherwise it'd be initialize(name, age) ) def initialize(&block) instance_eval(&block) if block_given? self end end p = Person.new do name = "Tobi" age = 22 end puts p.name # nothing (nil) puts p.age # nothing (nil) [/sourcecode] So what's wrong with this? What happens in the block is that local variables are assigned. So Ruby doesn't use the setters for the instance variables.

# Solution

We could go ahead and do: [sourcecode language="ruby"] p = Person.new do self.name = "Tobi" self.age = 22 end [/sourcecode] But who would want that? I don't want to write self. all the time, it feels like too much repetition to me! Well Dual-Purpose Accessors to the rescue! Those are accessors that work as getters and setters at the same time (you'll see how in a second). This way you are able to maintain a nice DSL feel to what you are doing: [sourcecode language="ruby"] class Person def name(n=nil) return @name unless n @name = n end def age(a=nil) return @age unless a @age = a end # keep the other cool setters alias_method :name=, :name alias_method :age=, :age # just for demonstration purposes # (otherwise it'd be initialize(name, age) def initialize(&block) instance_eval(&block) if block_given? self end end p = Person.new do name "Tobi" age 22 end puts p.name # Tobi puts p.age # 22 [/sourcecode] This is more code, yes. But it really comes in handy when you have got a lot of different values you want to set. I really like this technique as it has a real nice DSL-ish feeling to it. However you shouldn't overdo it, as in this case it'd be overkill and you could just write an initialize method which as name and age as arguments. However I looked for a small simple example and hopefully nailed it. The idea is taken from Gregory Browns free awesome book ["Ruby Best Practices"](http://rubybestpractices.com/ "Ruby Best Practices") which is also part of my [Resources page](http://pragtob.wordpress.com/resources/ "Resources"). Opinions or anything else you want to say? Please comment! PS: Thanks again to everyone on IRC who helped me track down the problem :-)
