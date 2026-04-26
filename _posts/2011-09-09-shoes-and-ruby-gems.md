---
layout: post
title: Shoes and ruby gems
description: None
date: 2011-09-09 12:33:22 -0000
last_modified_at: 2011-09-21 16:28:49 -0000
publish: true
pin: false
categories:
- Ruby
- Solution
tags:
- gem
- ruby
- rubygem
- shoes
- solution
---
As I just stumbled upon this and I need this: So how do you use ruby gems with shoes? Shoes is kind of a ruby interpreter on it's own, so you got no access to your normal ruby gems there. It's actually pretty easy as described in an [old saved blogpost by why](http://shoesrb.com/_why-archive/clearing-up-the-whole-shoes-and-rubygems-deal "Shoes and ruby gems"). What you need to do is something like this: 
```ruby
 Shoes.setup do gem 'twitter' gem 'oauth' gem 'launchy' end require 'launchy' 
```
 In the Shoes.setup block you set up all the gems you need. Then you can require them in this file, or in any other file which is required by this file. As you can see, I only require launchy here, the rest is required in other files of my project. What happens when you next launch the application is the following: Shoes goes on to install the gems: [![](http://pragtob.wordpress.com/wp-content/uploads/2011/09/shoes_gem_install1.png)](http://pragtob.wordpress.com/wp-content/uploads/2011/09/shoes_gem_install1.png)[](http://pragtob.wordpress.com/wp-content/uploads/2011/09/shoes_gem_install.png)So and there you got it, ready to play with shoes and some ruby gems! edit: Of course this only applies to red shoes, as green shoes is a gem itself you may use other gems with it exactly like you are used to.
