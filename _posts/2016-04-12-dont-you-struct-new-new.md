---
layout: post
title: Don't you Struct.new(...).new(...)
description: None
date: 2016-04-12 16:42:19 -0000
last_modified_at: 2016-04-12 16:42:19 -0000
publish: true
pin: false
categories:
- Ruby
tags:
- benchmark
- class
- concept
- performance
- ruby
- struct
---
As I just happened upon it again, I gotta take a moment to talk about one my most despised ruby code patterns: `Struct.new(...).new` \- ever since I happened upon it [for the first time](https://github.com/PragTob/shoes4/commit/1869209254124b4cf2d8c26df2b9df60f6b553ce).

## Struct.new?

[Struct.new](http://ruby-doc.org/core-2.3.0/Struct.html) is a convenient way to create a class with accessors:
  
    2.2.2 :001 > Extend = Struct.new(:start, :length)
     => Extend 
    2.2.2 :002 > instance = Extend.new(10, 20)
     => #<struct Extend start=10, length=20> 
    2.2.2 :003 > instance.start
     => 10 
    2.2.2 :004 > instance.length
     => 20

That's neat, isn't it? It is, but like much of Ruby's power it needs to be wielded with caution.

## Where Struct.new goes wrong - the second new

When you do `Struct.new` you create an anonymous class, another new on it creates an instance of that class. Therefore, `Struct.new(...).new(...)` creates an anonymous class and creates an instance of it at the same time. This is bad as we create a whole class to **create only one instance of it!** That is a capital waste. As a one-off use it might be okay, for instance when you [put it in a constant](https://github.com/rails/rails/blob/cb4f6875b6a27894f3456cda79cb929f7243a1ac/activerecord/lib/active_record/associations/preloader.rb#L57). The sad part is, that this is not the only case I've seen it used. As in the first case where I encountered it, I see it used inside of code that is invoked frequently. Some sort of _hot loop_ with calculations where more than one value is needed to represent some result of the calculation. Here programmers sometimes seem to reach for `Struct.new(...).new(...)`.

## Why is that bad?

Well it incurs an unnecessary overhead, creating the class every time is unnecessary. Not only that, as far as I understand it also creates new independent entries in the method cache. For JITed implementations (like JRuby) the methods would also be JITed independently. And it gets in the way of profiling, as you see lots of anonymous classes with only 1 to 10 method calls each. But how bad is that performance hit? I wrote a little benchmark where an instance is created with 2 values and then those 2 values are read one time each. Once with `Struct.new(...).new(...)`, once where the `Struct.new(...)` is saved in an intermediary constant. For fun and learning I threw in a similar usage with Array and Hash. 

```ruby
Benchmark.ips do |bm|
  bm.report "Struct.new(...).new" do
    value = Struct.new(:start, :end).new(10, 20)
    value.start
    value.end
  end

  SavedStruct = Struct.new(:start, :end)
  bm.report "SavedStruct.new" do
    value = SavedStruct.new(10, 20)
    value.start
    value.end
  end

  bm.report "2 element array" do
    value = [10, 20]
    value.first
    value.last
  end

  bm.report "Hash with 2 keys" do
    value = {start: 10, end: 20}
    value[:start]
    value[:end]
  end

  bm.compare!
end
```

 I ran those benchmarks with CRuby 2.3. And the results, well I was surprised how huge the impact really is. The _"new-new"_ implementation is over **33 times slower** than the _SavedStruct_ equivalent. And over 60 times slower than the fastest solution (Array), although that's also not my preferred solution.
  
    Struct.new(...).new    137.801k (± 3.0%) i/s -    694.375k
    SavedStruct.new      4.592M (± 1.7%) i/s -     22.968M
    2 element array      7.465M (± 1.4%) i/s -     37.463M
    Hash with 2 keys      2.666M (± 1.6%) i/s -     13.418M
    Comparison:
    2 element array:  7464662.6 i/s
    SavedStruct.new:  4592490.5 i/s - 1.63x slower
    Hash with 2 keys:  2665601.5 i/s - 2.80x slower
    Struct.new(...).new:   137801.1 i/s - 54.17x slower

[![Benchmark in iterations per second \(higher is better\)](/assets/uploads/2016/04/struct_new_benchmark2.png)](https://pragtob.wordpress.com/2016/04/12/dont-you-struct-new-new/struct_new_benchmark-3/) Benchmark in iterations per second (higher is better)

## But that's not all...

This is not just about performance, though. When people take this "shortcut" they also circumvent one of the hardest problems in programming - **Naming**. What is that Struct with those values? Do they have any connection at all or were they just smashed together because it seemed convenient at the time. What's missing is the identification of the _core concept_ that these values represent. Anything that says that this is more than a clump of data with these two values, that performs very poorly. So, please avoid using `Struct.new(...).new(...)` \- use a better alternative. Don't recreate a class over and over - give it a name, put it into a constant and enjoy a better understanding of the concepts and increased performance.
