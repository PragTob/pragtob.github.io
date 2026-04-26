---
layout: post
title: Writing DSLs in Ruby without monkeypatching Object
description: None
date: 2014-11-19 17:06:44 -0000
last_modified_at: 2014-11-20 13:09:35 -0000
publish: true
pin: false
categories:
- Uncategorized
tags: []
---
Ruby is well known for being a good language to build [Domain Specific Languages](http://www.martinfowler.com/bliki/DomainSpecificLanguage.html) (DSLs). Want to take a look at an example? [Sinatra](http://www.sinatrarb.com/) is a beautiful example of a DSL to create web applications: 
```ruby
 get '/hi'do 'Hello world!' end 
```
 For another example, check out [wingtips](https://github.com/PragTob/wingtips) a DSL for writing presentation slides: 
```ruby
 slide 'Why' do fullscreen_image 'images/_why.png' para '_why', left: 100, top: 100 end 
```
 As you can see above, often DSLs involve adding top-level methods for convenience. Methods like `get` or `slide` above that are available outside of a class definition whatsoever, just like your standard ruby `puts`. These methods are often used as an entry point into the DSL, internally create a new object and then `instance_eval` the block or something like that. Unfortunately many times developers monkey patch `Object` to reach their goal, to make this methods available. That is totally unnecessary! We can write beautiful DSLs, like the above, without polluting every Ruby object ever with our methods. I decided to share this method/article, as I noticed that this seems to be rather unknown even to a lot of experienced developers. As a little disclaimer, I didn't come up with this by myself, [Konstantin Haase](http://rkh.im/), maintainer of Sinatra, presented this idea at the fish bowl discussion at [eurucamp](http://eurucamp.org/) 2012\.

### The traditional way: monkey patching Object

Let's first have a look at the "traditional way" to implement DSLs. The traditional way is to use Ruby's open class system to define the method straight on the `Object` class, making it available everywhere: 
```
 class Object private def dsl_method puts 'Nice dsl you got' end end dsl_method # => 'Nice dsl you got' 
```
 This works. However, now there is a private method `dsl_method` defined on every object (as almost all objects inherit from `Object`). Even worse, as modules and classes are also objects, the `dsl_method` is also defined on them. That's not an ideal situation. 
```
 Object.new.send :dsl_method # => 'Nice dsl you got' module MyModule end MyModule.send :dsl_method # => 'Nice dsl you got' 
```


### What about def dsl_method?

That unfortunately creates much the same problems as the monkeypatching Object approach, described above: 
```
 def dsl_method puts "Nice dsl you got" end dsl_method # => Nice dsl you got Object.send :dsl_method # => Nice dsl you got Object.new.send :dsl_method # => Nice dsl you got 
```


### Main Object to the rescue!

You probably know that in ruby you can call methods without an explicit receiver, if the receiver is `self`. What `self` is depends on the context. But what is `self` at the top level of a ruby script? Let's check: 
```
 p self # => main p self.class # => Object 
```
 It's the `main` object, an instance of the `Object` class. How about we only add our DSL methods to that one object instead of a whole class hierarchy? How can we do that? Well we could use `define_singleton_method`, but I'm more a fan of defining a module and then calling `extend` on the main object. Let's see how that plays out: 
```
 module DSL def dsl_method puts 'Nice dsl you got' end end extend DSL dsl_method # => 'Nice dsl you got' 
```
 That works nicely. The method is only defined on the main object, not unnecessarily polluting objects with methods. Other instances of `Object` know nothing about it, when asked for that method they throw a `NoMethodError`. 
```
 Object.send :dsl_method # => NoMethodError 
```
 Great! But it would have worked just the same with `define_singleton_method`, so why do I prefer the module based approach? Reusability! Imagine you want to use the DSL inside of other classes or with other objects. By nature all of that is possible with the old "monkeypatch" approach, as every object just has that method defined. With the module based approach we can introduce our DSL methods into inheritance hierarchies in a much more fine-grained way. 
```
 class WantDSL include DSL end WantDSL.new.dsl_method # => 'Nice dsl you got' 
```


### Do projects actually use this?

The aforementioned Sinatra uses this approach since shortly after eurucamp 2012 I believe. The main object is extended [here](https://github.com/sinatra/sinatra/blob/master/lib/sinatra/main.rb#L28-L30) with the methods defined [here](https://github.com/sinatra/sinatra/blob/master/lib/sinatra/base.rb#L1981-L2005). It's working fine and in production at many companies ;) I use this approach in some of my projects. We use it in Shoes 4 to make our ["built-in methods"](https://github.com/shoes/shoes4/blob/master/lib/shoes/builtin_methods.rb) available both at the top-level and inside an app, as there are some methods that are available both outside and inside of the app scope such as `alert`. Lastly we use it in wingtips to make the [slide declaration DSL](https://github.com/PragTob/wingtips/blob/master/lib/wingtips/dsl.rb) available at the top-level. You can also check out [the pull request, that introduced the approach described here](https://github.com/PragTob/wingtips/pull/19) at wingtips and moved away from yet another approach, which was instance_evaling the code of ruby files. Anyway, I hope you find this blog post useful in your endeavours to create beautiful DSLs without polluting other objects :) **Edit/Update:** Added some clarification, to show that this proposed method is just to be used for the "entry point" to the DSL, not for the whole DSL. Also added a section showing that using `def` is basically the same here as monkeypatching `Object`. Thanks for the feedback on reddit.
