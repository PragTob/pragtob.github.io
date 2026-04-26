---
layout: post
title: The not so low cost of calling dynamically defined methods
description: None
date: 2015-10-20 07:53:54 -0000
last_modified_at: 2015-10-23 16:00:44 -0000
publish: true
pin: false
categories:
- Ruby
tags:
- benchmark
- define_method
- metaprogramming
- performance
- ruby
---
There are a couple of mantras that exist across programming communities, one of them is to avoid duplication or to keep it [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself). Programming languages equip us with different tools to avoid duplication. In Ruby a popular way to achieve this is [Metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming). Methods are dynamically defined to get rid off all duplication and we rejoice - yay! There might be other problems with metaprogrammed solutions, but at least we are sure that the performance is the same as if we'd had written that duplicated code. Or are we? As the title suggests this post examines the performance of these meta programmed methods _._ If you are looking for method definition performance or pure call overhead you'll find this information in [this post by Aaron Patterson](http://tenderlovemaking.com/2013/03/03/dynamic_method_definitions.html). Before we get into the details I want to quickly highlight that this is not some theoretical micro benchmark I pulled out of thin air. These examples are derived from performance improvements on an actual project. That work was done by my friend [Jason R. Clark](http://jasonrclark.com/) on [this pull request](https://github.com/shoes/shoes4/pull/1080) over at [Shoes 4](https://github.com/shoes/shoes4). As he doesn't have time to write it up - I get to, so let's get to it!

### Let's look at some methods!

(Please be aware that this example is simplified, of course the real code has varying parts most importantly the name of the instance_variable which is the reason why the code was meta programmed in the first place) 

```ruby
 class FakeDimension def initialize(margin_start) @margin_start = margin_start @margin_start_relative = relative? @margin_start end def relative?(result) result.is_a?(Float) && result <= 1 end def calculate_relative(result) (result * 100).to_i end define_method :full_meta do instance_variable_name = '@' + :margin_start.to_s value = instance_variable_get(instance_variable_name) value = calculate_relative value if relative? value value end IVAR_NAME = "@margin_start" define_method :hoist_ivar_name do value = instance_variable_get(IVAR_NAME) value = calculate_relative value if relative? value value end define_method :direct_ivar do value = @margin_start value = calculate_relative value if relative? value value end eval <<-CODE def full_string value = @margin_start value = calculate_relative value if relative? value value end CODE def full_direct value = @margin_start value = calculate_relative value if relative? value value end end 
```

 Starting at the first _define_method_ these are all more or less the same method. We start at a fully meta programmed version, that even converts a symbol to an instance variable name, and end with the directly defined method without any meta programming. Now with all these methods being so similar you'd expect them all to have roughly the same performance characteristics, right? Well, such is not the case as demonstrated by the following benchmark. I benchmarked these methods both for the case where the value is relative and for when it is not. The results are not too different - 

Source: [https://gist.github.com/PragTob/17f7dcab51ad98a3f064](https://gist.github.com/PragTob/17f7dcab51ad98a3f064)

**File: `meta_benchmark.rb`**
```ruby
require 'benchmark/ips'

class FakeDimension
  def initialize(margin_start)
    @margin_start = margin_start
    @margin_start_relative = relative? @margin_start
  end

  def relative?(result)
    result.is_a?(Float) && result <= 1
  end

  def calculate_relative(result)
    (result * 100).to_i
  end

  define_method :full_meta do
    instance_variable_name = '@' + :margin_start.to_s
    value = instance_variable_get(instance_variable_name)
    value = calculate_relative value if relative? value
    value
  end

  IVAR_NAME = "@margin_start"
  define_method :hoist_ivar_name do
    value = instance_variable_get(IVAR_NAME)
    value = calculate_relative value if relative? value
    value
  end

  define_method :direct_ivar do
    value = @margin_start
    value = calculate_relative value if relative? value
    value
  end

  eval <<-CODE
  def full_string
    value = @margin_start
    value = calculate_relative value if relative? value
    value
  end
  CODE

  def full_direct
    value = @margin_start
    value = calculate_relative value if relative? value
    value
  end
end

def do_benchmark(description, margin_start)
  puts description

  Benchmark.ips do |benchmark|
    dim = FakeDimension.new margin_start
    benchmark.report("full_meta")             { dim.full_meta }
    benchmark.report("hoist_ivar_name")       { dim.hoist_ivar_name }
    benchmark.report("direct_ivar")           { dim.direct_ivar }
    benchmark.report("full_string")           { dim.full_string }
    benchmark.report("full_direct")           { dim.full_direct }
    benchmark.compare!
  end
end

do_benchmark('Non relative margin start', 10)
do_benchmark('Relative margin start', 0.8)
```

. Running the non relative version on CRuby 2.2.2 with [benchmark-ips](https://github.com/evanphx/benchmark-ips) I get the following results (higher is better): 

```
 full_meta 1.840M (± 3.0%) i/s - 9.243M hoist_ivar_name 3.147M (± 3.3%) i/s - 15.813M direct_ivar 5.288M (± 3.1%) i/s - 26.553M full_string 6.034M (± 3.2%) i/s - 30.179M full_direct 5.955M (± 3.2%) i/s - 29.807M Comparison: full_string: 6033829.1 i/s full_direct: 5954626.6 i/s - 1.01x slower direct_ivar: 5288105.5 i/s - 1.14x slower hoist_ivar_name: 3146595.7 i/s - 1.92x slower full_meta: 1840087.6 i/s - 3.28x slower 
```

 And look at that, the _full_meta_ version is **over 3 times slower** than the directly defined method! Of course _direct_ivar_ is also pretty close, but it's an unrealistic scenario as the instance variable name is what is really changing. You can interpolate the string of the method definition in the _full_string_ version, though. This achieves results as if the method had been directly defined. But what's happening here? It seems that there is a higher than expected cost associated with calling _instance_variable_get_ , creating the necessary string and calling methods defined by _define_method_ overall. If you want to keep the full performance but still alter the code you have to resort to the _evil eval_ and stitch your code together in string interpolation. Yay.

### So what, do we all have to eval method definitions for metaprogramming now?

Thankfully **no**. The performance overhead is constant - if your method does more expensive calculations the overhead diminishes. This is the somewhat rare case of a method that doesn't do much (even the slowest version can be executed almost 2 Million times per second) but [is called a lot](https://github.com/shoes/shoes4/pull/1080#issuecomment-85768978). It is one of the core methods when positioning UI objects in Shoes. Obviously we should also do the hard work and try not to call that method that often, we're working on that and already made some nice progress. But, to quote Jason, _"regardless what we do I think that`Dimension` is bound to always be in our hot path."_. What about methods that do more though? Let's take a look at an example where we have an object that has an array set as an instance variable and has a method that concatenates another array and sorts the result (

Source: [https://gist.github.com/PragTob/c843d4f5aca6113d94e9](https://gist.github.com/PragTob/c843d4f5aca6113d94e9)

**File: `more_meta.rb`**
```ruby
require 'benchmark/ips'

class Try

  def initialize(array)
    @array = array
  end

  define_method :meta_concat_sort do |array|
    value = instance_variable_get '@' + :array.to_s
    new_array = value + array
    new_array.sort
  end

  def concat_sort(array)
    new_array = @array + array
    new_array.sort
  end
end

BASE_ARRAY        = [8, 2, 400, -4, 77]
SMALL_INPUT_ARRAY = [1, 88, -7, 2, 133]
BIG_INPUT_ARRAY   = (1..100).to_a.shuffle


def do_benchmark(description, input)
  puts description
  Benchmark.ips do |b|
    try = Try.new BASE_ARRAY

    b.report('meta_concat_sort') { try.meta_concat_sort(input) }
    b.report('concat_sort')      { try.concat_sort(input) }
    b.compare!
  end
end

do_benchmark('Small input array', SMALL_INPUT_ARRAY)
do_benchmark('Big input array', BIG_INPUT_ARRAY)
```

): 

```ruby
 class Try def initialize(array) @array = array end define_method :meta_concat_sort do |array| value = instance_variable_get '@' + :array.to_s new_array = value + array new_array.sort end def concat_sort(array) new_array = @array + array new_array.sort end end 
```

 We then benchmark those two methods with the same base array but two differently sized input arrays: 

```ruby
 BASE_ARRAY = [8, 2, 400, -4, 77] SMALL_INPUT_ARRAY = [1, 88, -7, 2, 133] BIG_INPUT_ARRAY = (1..100).to_a.shuffle 
```

 What's the result? 

```
 Small input array Calculating ------------------------------------- meta_concat_sort 62.808k i/100ms concat_sort 86.143k i/100ms \------------------------------------------------- meta_concat_sort 869.940k (± 1.4%) i/s - 4.397M concat_sort 1.349M (± 2.6%) i/s - 6.805M Comparison: concat_sort: 1348894.9 i/s meta_concat_sort: 869940.1 i/s - 1.55x slower Big input array Calculating ------------------------------------- meta_concat_sort 18.872k i/100ms concat_sort 20.745k i/100ms \------------------------------------------------- meta_concat_sort 205.402k (± 2.7%) i/s - 1.038M concat_sort 231.637k (± 2.5%) i/s - 1.162M Comparison: concat_sort: 231636.7 i/s meta_concat_sort: 205402.2 i/s - 1.13x slower 
```

 With the small input array the dynamically defined method is still over 50% slower than the non meta programmed method! When we have the big input array (100 elements) the meta programmed method is still 13% slower, which I still consider very significant. I ran these with CRuby 2.2.2, in case you are wondering if this is implementation specific. I ran the same benchmark with JRuby and got comparable results, albeit the fact that JRuby is usually 1.2 to 2 times faster than CRuby, but the slowdowns were about the same. So in the end, what does it mean? **Always benchmark.** Don't blindly optimize calls like these as in the grand scheme of things they might not make a difference. This will only be really important for you if a method gets called **a lot**. If it is in your library/application, then replacing the meta programmed method definitions might yield surprising performance improvements. **UPDATE 1:** Shortly after this post was published coincidentally [JRuby 9.0.0.3.0 was released with improvements to the call speed of methods defined by _define_method_](http://blog.jruby.org/2015/10/performance_improvements_in_jruby_9030/). I added the 

Source: [https://gist.github.com/PragTob/17f7dcab51ad98a3f064](https://gist.github.com/PragTob/17f7dcab51ad98a3f064)

**File: `meta_benchmark.rb`**
```ruby
require 'benchmark/ips'

class FakeDimension
  def initialize(margin_start)
    @margin_start = margin_start
    @margin_start_relative = relative? @margin_start
  end

  def relative?(result)
    result.is_a?(Float) && result <= 1
  end

  def calculate_relative(result)
    (result * 100).to_i
  end

  define_method :full_meta do
    instance_variable_name = '@' + :margin_start.to_s
    value = instance_variable_get(instance_variable_name)
    value = calculate_relative value if relative? value
    value
  end

  IVAR_NAME = "@margin_start"
  define_method :hoist_ivar_name do
    value = instance_variable_get(IVAR_NAME)
    value = calculate_relative value if relative? value
    value
  end

  define_method :direct_ivar do
    value = @margin_start
    value = calculate_relative value if relative? value
    value
  end

  eval <<-CODE
  def full_string
    value = @margin_start
    value = calculate_relative value if relative? value
    value
  end
  CODE

  def full_direct
    value = @margin_start
    value = calculate_relative value if relative? value
    value
  end
end

def do_benchmark(description, margin_start)
  puts description

  Benchmark.ips do |benchmark|
    dim = FakeDimension.new margin_start
    benchmark.report("full_meta")             { dim.full_meta }
    benchmark.report("hoist_ivar_name")       { dim.hoist_ivar_name }
    benchmark.report("direct_ivar")           { dim.direct_ivar }
    benchmark.report("full_string")           { dim.full_string }
    benchmark.report("full_direct")           { dim.full_direct }
    benchmark.compare!
  end
end

do_benchmark('Non relative margin start', 10)
do_benchmark('Relative margin start', 0.8)
```

. It is 7-15% faster for _full_meta_ and _hoist_ivar_name_ but now the _direct_ivar_ is about as fast as its _full_meta_ and _full_string_ counterparts thanks to the optimizations! **UPDATE 2:** I wrote a 

Source: [https://gist.github.com/PragTob/fdeb46356702bf9943ca](https://gist.github.com/PragTob/fdeb46356702bf9943ca)

**File: `instance_variabe_get.rb`**
```ruby
require 'benchmark/ips'

class Test
  def intitialize
    @ivar = 'test'
  end

  def direct
    @ivar
  end

  IVAR_NAME = "@ivar"
  def hoist_ivar_name
    instance_variable_get IVAR_NAME
  end

  def instance_variable_get_symbol
    instance_variable_get :"@ivar"
  end

  def instance_variable_get_frozen
    instance_variable_get('@ivar'.freeze)
  end

  def instance_variable_get_frozen_symbol
    instance_variable_get('@ivar'.freeze.to_sym)
  end
end

Benchmark.ips do |benchmark|

  instance = Test.new
  benchmark.report("direct") {instance.direct}
  benchmark.report("hoist_ivar_name") {instance.hoist_ivar_name}
  benchmark.report("ivar get symbol") {instance.instance_variable_get_symbol}
  benchmark.report("ivar get frozen") {instance.instance_variable_get_frozen}
  benchmark.report("ivar get frozen sym") {instance.instance_variable_get_frozen_symbol}
end
```

 about what I think is the bottle neck here - _instance_variable_get_. It is missing the slowest case but is still up to 3 times slower than the direct access.
