---
layout: post
title: 'Released: deep_merge 0.1.0 for Elixir'
description: None
date: 2016-11-10 19:40:30 -0000
last_modified_at: 2016-11-10 20:05:40 -0000
publish: true
pin: false
categories:
- Software Engineering
tags:
- deep_merge
- Elixir
- keyword
- keywordlist
- map
- merge
---
As you might have seen on this blog or on twitter I'm thoroughly enjoying elixir. One thing that I found to be thoroughly missing is _deep_merge_ \- given two maps merge them together and if a merge conflict occurs but both values are maps go on and recursively merge them as well. In Ruby it is provided by ActiveSupport - you don't need it THAT often but when you need it, it's really great to have. The most common use case for me is merging a user specified configuration with some sort of default configuration to get the final configuration. https://twitter.com/pragtob/status/757195227576893440 So at first no one else seemed to have the need for deep_merge, strange huh? About 1.5 months later it seemed others were having the same problem/question as in [this stackoverflow question](http://stackoverflow.com/questions/38864001/elixir-how-to-deep-merge-maps) or the gist linked here: https://twitter.com/lepoetemaudit35/status/761269690287128576 So others do want it! Time to propose it to the [elixir-core mailing list](https://groups.google.com/forum/#!topic/elixir-lang-core/ak3kVqJ4-8g)! Lots of people seemed to like the idea and were in favor of it, none of the core team members though and the discussion soon went on to be a bit more about implementation details. So, after some time I went and thought "might as well draft up an implementation in a PR so we can discuss this" - and so [it was](https://github.com/elixir-lang/elixir/pull/5339).

As you might have guessed from the blog post title, this PR didn't get through as the core team thought it was a bit too specific of a use case, the implementation had its flaws (not handling structs properly - I learned something!) and it wasn't general enough as it didn't handle keyword lists. During the discussion José also mentioned that using [protocols](http://elixir-lang.org/getting-started/protocols.html) might be the way to go.

> Using protocols seems to be the most correct but it feels a very niche feature to justify adding a new protocol to the language.

While I'd have liked to see it in Elixir core I gotta commend the elixir maintainers on rejecting features - I know it can sometimes be hard but in the end it's for the better keeping the language focused and maintenance low. And one can always write a library so one can pick and choose to get the functionality in. So what do you do? Well, implement it as a library of course! Meet [deep_merge 0.1.0](https://github.com/PragTob/deep_merge)! https://gist.github.com/pragtobgists/13210711d3cb7416173ded2c2a4f6d75 Why would you want to use deep_merge?

* It handles both maps and keyword lists
* It does not merge structs or maps with structs...
* ...but you can implement the simple [DeepMerge.Resolver protocol](https://github.com/PragTob/deep_merge/blob/master/lib/deep_merge/resolver.ex) for types/structs of your choice to also make them deep mergable
* a _deep_merge/3_ variant that gets a function similar to _Map.merge/3_ to modify the merging behavior, for instance in case you don't want keyword lists to be merged or you want all lists to be appended

All of these features - especially pit falls like the struct merging - are reasons why it might be profitable to adopt a library and not implement it yourself. So, go on check it out on [github](https://github.com/PragTob/deep_merge), [hex](https://hex.pm/packages/deep_merge) and [hexdocs](https://hexdocs.pm/deep_merge/api-reference.html).
