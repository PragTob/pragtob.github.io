---
layout: post
title: Secure your Rails apps!
description: None
date: 2012-03-06 01:11:51 -0000
last_modified_at: 2012-03-06 10:48:51 -0000
publish: true
pin: false
categories:
- Ruby
- Software Engineering
tags:
- brakeman
- github
- hacked
- mass assignment vulnerability
- Ruby on Rails
- security
- static analysis
- vulnerability scanner
---
It is time to secure your Rails apps! I mean it is always time to do that, but (as you [might have heard](http://www.h-online.com/open/news/item/GitHub-security-incident-highlights-Ruby-on-Rails-problem-1463207.html "H-online article about the vulnerability")) [github](https://github.com/) just got hacked. So if you have a public facing Rails app you should really ask yourself "Can I be sure that our security standards are better than the ones of github?"

## What happened?

A russian programmer [started an argument about the mass assignment vulnerability](https://github.com/rails/rails/issues/5228) and how Rails could provide better protection against it. However the issue got closed again and again as it was basically argued that securing the app is the responsibility of the programmer. So he took a different approach, demonstrating that the vulnerability is even present in one of the biggest and well-known Rails applications: github itself. He managed to [make a commit to the Rails master branch](https://github.com/rails/rails/commit/b83965785db1eec019edf1fc272b1aa393e6dc57 "Hacked commit on Rails master branch"), which turned into a lengthy discussion including some memes. He also created a ticket which [appears to be from the future](https://github.com/rails/rails/issues/5239 "Ticket from the future") by abusing this vulnerability. For the sake of completeness, he informed github of the presence of these vulnerabilities first. You may also want to checkout [github's summary about the incident](https://github.com/blog/1068-public-key-security-vulnerability-and-mitigation "github security incident summary"). I don't want to discuss whether his actions were right or wrong, but in the end Rails [changed the default for new apps](https://github.com/rails/rails/commit/06a3a8a458e70c1b6531ac53c57a302b162fd736 "New default for white listing attributes") to make this vulnerability less common, which is a good thing to my mind.

## What is this mass assignment vulnerability?

The mass assignment vulnerability is described pretty well in the [Rails security guide](http://guides.rubyonrails.org/security.html#mass-assignment "mass assignment described in the Rails security guide") \- which you should absolutely read in its entirety! Basically the problem is the following: Whenever you scaffold generate code for some resource in Rails, which is pretty common, you can see a snippet like this for creating a resource: [sourcecode language="ruby"] @user = User.new(params[:user]) [/sourcecode] What this does is create a new user, with all the attributes set to the values that got transmitted from a form and are now in the params[:user] hash. This is very concise as here you can _mass assign_ everything the user entered: name, email, description etc. Cool right? This is why it's not only generated but also written pretty often. Yeah so far so good. The problem starts when you got some attributes in your model, which you don't want your users to have direct access to. For instance the boolean admin, determining if a user is an admin or not. The attacker may use tools to manipulate the html form and hence the transmitted parameters to include the key value pair: admin: true ! So params[:user] may look like this: [sourcecode language="ruby"] params[:user] = { name: 'Evil', email: 'evil@example.com', description: 'I am an admin soon', admin: true} [/sourcecode] And all of a sudden our newly created user is an admin and can do everything he/she wants to do - which was totally unintended by the developer! Of course this also works with updating records and not just with creating them. This issue is actually pretty damn well-known and was also a big story during the [start of the Diaspora social network](http://www.kalzumeus.com/2010/09/22/security-lessons-learned-from-the-diaspora-launch/ "Diaspora starting vulnerabilities") (among many other vulnerabilities).

## Holy sh**! What can I do to protect my app?

Well in general it is pretty easy to protect against this kind of attack you just have to add _attr_accessible_ to all your rails models. This white lists the attributes, that can be assigned during mass assignments. Everything else can not be assigned during mass assignments. So for our example this would look like this: [sourcecode language="ruby"] class User < ActiveRecord::Base attr_accessible :name, :email, :description # rest of class omitted end [/sourcecode] Notice that admin is missing from the attributes after attr_accessible. That's because we don't want to have it mass assigned during creation/update. So now go ahead and secure your Rails applications, or stay for the pro-tip...

## Pro-tip: Use Brakeman

[Brakeman](http://brakemanscanner.org/ "Brakeman") (can also be found [on github](https://github.com/presidentbeef/brakeman "brakeman github repository")) is a static analysis tool (fancy term for: looks at your code, doesn't execute it), looking for vulnerabilities. So it is a vulnerability scanner for Ruby on Rails. It takes a good look at your source code and informs you of any found security vulnerabilities including the confidence of the scanner that this is indeed a problem (e.g. not a false positive). It seems to find mass assignment vulnerabilities very reliably and it also informed me of a possible Cross-site scripting (XSS) vulnerability in my Rails version (3.2.0) and recommended an update to 3.2.2, as this version fixes the problem. So it is also pretty up to date and I can only recommend it. Now go ahead and _gem_ _install brakeman_ or add it to your Gemfile. However the default output isn't very beautiful on my system and hides many important parts so I'd recommend you to run: [source] brakeman -f html -o brakeman.html path/to/app [/source] For a bit prettier html output. Hope that this helps. And don't forget to add this  _brakeman.html_ to your gitignore. Oh by the way: they also have a [plugin for Jenkins/Hudson](http://brakemanscanner.org/docs/jenkins/ "Brakeman plugin for Jenkins/Hudson"). So now go ahead and make your Rails apps more secure!
