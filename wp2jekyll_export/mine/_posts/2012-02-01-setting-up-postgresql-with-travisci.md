---
layout: post
permalink: https://pragtob.wordpress.com/2012/02/01/setting-up-postgresql-with-travisci/
title: Setting up PostgreSQL with TravisCI
description: None
date: 2012-02-01 17:45:34 -0000
last_modified_at: 2012-02-01 17:45:34 -0000
publish: true
pin: false
categories:
- Ruby
- Solution
tags:
- continuous integration
- database
- PostgreSQL
- Rails
- setup
- TravisCI
---
[TravisCI](http://travis-ci.org/ "TravisCI") is an awesome free continuous integration system that just takes your [github](https://github.com/ "github") repositories and then runs all your tests - it is pure awesomeness and easy as cake. However when testing a web application you also have to setup a database - they have got [good docs](http://about.travis-ci.org/docs/user/database-setup/ "TravisCi database docs") for that, but still I ran into problems. What was my problem? In their description the database name is "myapp_test" and I believed that it would not matter and it could be anything like "Tracketytrack Test" I wanted. I got proven wrong. Apparently it has to be "myapp_test". Also for some reason I had to add a manual call to "rake db:migrate" - I may check into this later. For your reference, here the relevant parts of my .travis.yml as a [gist](https://gist.github.com/1718229). And here they are as well for your reference: [sourcecode] postgres: adapter: postgresql database: myapp_test username: postgres before_script: \- "psql -c 'create database myapp_test;' -U postgres" \- "rake db:migrate" [/sourcecode]
