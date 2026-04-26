---
layout: post
title: Setting up PostgreSQL for Ruby on Rails on Linux
description: None
date: 2012-09-12 10:26:20 -0000
last_modified_at: 2015-01-06 16:09:02 -0000
publish: true
pin: false
categories:
- Ruby
- Solution
tags:
- adapter
- database
- Linux
- pg
- PostgreSQL
- Ruby on Rails
- setup
---
So every once upon a time I run into the situation, that I have a newly set up machine and have to configure my system again to use PostgreSQL and play nicely with Ruby on Rails. And I don't want to have to google the set up every time, hence this post (and of course to help people with similar problems). Why PostgreSQL? Well many people like it and you need it for instance for deploying on [heroku](http://www.heroku.com/) and your development environment should be as close to your production environment as possible. What I do here is a way that works for me on my Linux Mint Debian Testing machines. Be aware that this is **my development set up** \- I don't use this in production. I'm no PostgreSQL expert so, this just works for me and I hope that it will for other people as well :-). Suggestions/Improvements are welcome as always. Let's get started! So at first we have to install PostgreSQL: [sourcecode language="bash"] sudo apt-get install postgresql [/sourcecode] After we've don this we need to create a user in PostgreSQL. So we use the user account of PostgreSQL to create a user with sufficient rights. I just take my own account and grant it sufficient rights with PostgreSQL. Don't forget to **substitute my username** with yours! [sourcecode language="bash"] tobi@speedy ~ $ sudo su postgres [sudo] password for tobi: # the behavior of createuser seems to have changed in recent postgresql versions # So now do the following (-d says allowed to create databases): postgres@speedy /home/tobi $ createuser tobi -d # replace tobi with your user acc name # In older versions it used to work like this: postgres@speedy /home/tobi $ createuser tobi # (substitute with your username) Shall the new role be a superuser? (y/n) n Shall the new role be allowed to create databases? (y/n) y Shall the new role be allowed to create more new roles? (y/n) n [/sourcecode] At this point it would be good to install the [pg gem](https://bitbucket.org/ged/ruby-pg/wiki/Home) \- which is the adapter for the PostgreSQL database. So simply add [sourcecode language="ruby"] gem 'pg' [/sourcecode] to your Gemfile. Also make sure to replace existing database gems - like sqlite. Now run: [sourcecode language="bash"] bundle install [/sourcecode] to update your dependencies. That should go smoothly, otherwise you are probably missing dependencies. Now you still need to modify your config/database.yml. Most of all you need to change the adapter to "postgresql". Here is the development part of my database.yml for reference: [sourcecode] development: adapter: postgresql database: ArbitaryDatabaseName pool: 5 timeout: 5000 [/sourcecode] Make sure that the different environments (development, test and production) have got different databases (meaning the database property should be different). Otherwise they will influence each other and you don't want that. In order to finish the set up you need to create all the databases, which should work flawlessly by now: [sourcecode language="bash"] rake db:create:all [/sourcecode] When this is done you should be able to "rake db:migrate" your database as you are used to (and be sure to do so). I hope this post helped you with setting up PostgreSQL for Ruby on Rails on Linux. If something didn't work for you, you feel that a step is missing or you just have a useful tip - please feel free to comment!
