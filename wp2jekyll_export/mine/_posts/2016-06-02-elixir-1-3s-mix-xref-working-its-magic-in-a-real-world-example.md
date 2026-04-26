---
layout: post
permalink: https://pragtob.wordpress.com/2016/06/02/elixir-1-3s-mix-xref-working-its-magic-in-a-real-world-example/
title: Elixir 1.3's mix xref working its magic in a real world example
description: None
date: 2016-06-02 14:30:14 -0000
last_modified_at: 2016-06-06 19:39:26 -0000
publish: true
pin: false
categories: []
tags:
- '1.3'
- cross reference
- Elixir
- mix
- mix xref
- undefined function
- undefined module
---
The upcoming elixir 1.3, available as a [release candidate](https://github.com/elixir-lang/elixir/releases/tag/v1.3.0-rc.0), brings along many cool new features such as Calendar Types and (finally!) test groups for ExUnit. My favorite new feature hasn't been discussed a lot though. It's also missing in the ["What's coming in Elixir 1.3"](http://tuvistavie.com/2016/elixir-1-3/) blog post. So, I'd like to show it off: **mix xref** So what is [mix xref](https://github.com/elixir-lang/elixir/blob/master/CHANGELOG.md#mix-xref)? In the words of the changelog:

> Mix v1.3 includes a new task called `xref` that performs cross reference checks in your code. One of such checks is the ability to find calls to modules and functions that do not exist

Which is a great addition, finding these bugs where you have a typo or forgot an alias/import at compile time! Frankly I thought/hoped elixir already did this, and it did but only sometimes (e.g. you couldn't import a module that isn't there). The even better information is that mix xref is executed by default when you code (and its dependencies) are compiled - so check the warnings after upgrading! Your tests should generally capture these bugs, but a compile time warning is even earlier in the process and not everything is well tested. We experienced that first hand last week where it took us some time to trace a test failure back to a bug in [timex_ecto](https://github.com/bitwalker/timex_ecto/issues/29) and [opened a PR improving test coverage with failing test cases for the bug](https://github.com/bitwalker/timex_ecto/pull/30). Curios mind that I am I wanted to see if mix xref would have found that call to an undefined module and let's see:
  
    tobi@airship ~/github/timex_ecto $ elixir -v
    Erlang/OTP 18 [erts-7.3] [source] [64-bit] [smp:8:8] [async-threads:10] [kernel-poll:false]
    
    Elixir 1.3.0-rc.0 (7881123)
    tobi@airship ~/github/timex_ecto $ mix clean
    tobi@airship ~/github/timex_ecto $ mix compile
    Compiling 7 files (.ex)
    warning: undefined protocol function dump/1 (for protocol Ecto.DataType)
      lib/datatype.ex:1
    
    warning: undefined protocol function dump/1 (for protocol Ecto.DataType)
      lib/datatype.ex:23
    
    warning: function Ecto.Type.blank?/1 is undefined or private
      lib/types/date.ex:14
    
    warning: function Ecto.Type.blank?/1 is undefined or private
      lib/types/datetime.ex:14
    
    warning: function Ecto.Type.blank?/1 is undefined or private
      lib/types/datetimetz.ex:34
    
    warning: function Ecto.DateTimeWithTimezone.cast/1 is undefined (module Ecto.DateTimeWithTimezone is not available)
      lib/types/datetimetz.ex:57
    
    warning: function Ecto.Type.blank?/1 is undefined or private
      lib/types/time.ex:14
    
    Generated timex_ecto app
  
It found not only the bug we were hitting (`Ecto.DateTimeWithTimeZone` is undefined) but more sources of potential bugs. Which is great, as my hope is that those would have never made it into a hex package release with mix xref. This is why I believe that **mix xref** **might have the biggest impact on the Elixir eco system** of all changes coming in 1.3. Don't get me wrong, I love test groups, calendar types and all the other updates. But this should directly improve the quality of both released libraries and the development experience. Sure, these should all be caught by tests but (sadly) not everybody tests that rigorously. There are over 30 of such problems reported by xref in the dependencies of our relatively small phoenix app (standard phoenix + edeliver + maybe 5 other dependencies and their dependencies). That's potential crashes, bugs and dead code looming that I'd rather avoid. Hence, I'm REALLY excited for Elixir 1.3 and mix xref and you should be too ;)  
