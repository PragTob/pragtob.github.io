---
layout: post
permalink: https://pragtob.wordpress.com/2011/10/02/regexes-non-greedy-and-matching-whitespaces-rubular-to-the-rescue/
title: 'Regexes: non-greedy and . matching whitespaces - Rubular to the rescue!'
description: None
date: 2011-10-02 18:01:04 -0000
last_modified_at: 2011-10-02 18:04:17 -0000
publish: true
pin: false
categories:
- Ruby
- Solution
tags:
- matching
- non-greedy
- regex
- rubular
- ruby
---
So some weeks ago (unfortunately I didn't really have the time to post this immediately) I ran into the following problem, I wanted to match the following snippet: [sourcecode language="ruby"] Shoes.setup do gem 'twitter' gem 'oauth' gem 'launchy' gem 'feedzirra' end [/sourcecode] I wanted to do this in order to transform a (red) Shoes application to a green shoes application (where the gems are handled by ruby gems as you are used to, as it uses a normal ruby interpreter). So how do you match this with a regex? I ran into 2 little problems. First: I wanted to match Shoes.setup do - end, and everything in between. Unfortunately "." just matches any single character, no whitespaces. After a bit of google action I found out that the m-switch exists to alter this behavior for the regex. So there we go... But what is this? It replaced the whole file! How could that be? Oh yeah, underneath there is a whole program with its own "end" - and regexes are by default greedy and try to match as many characters as possible. So everything in between Shoes.setup do (the first thing in the program) and the last end... so how to make a matcher non greedy? Just add a question mark (?) after the matcher!

## Solution

So in the end the regex looks like this: [sourcecode language="ruby"] /Shoes\\.setup do.*?end/m [/sourcecode] I could have known this way faster if I would have just stick with my favorite Ruby Regex reference, [Rubular](http://www.rubular.com/ "Rubular")! It has an amazing short reference and now is also linked at the [Resource](http://pragtob.wordpress.com/resources/ "Resources")[s](http://pragtob.wordpress.com/resources/ "Resources") page.
