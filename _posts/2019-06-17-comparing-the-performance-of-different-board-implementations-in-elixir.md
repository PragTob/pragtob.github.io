---
layout: post
title: What's the Fastest Data Structure to Implement a Game Board in Elixir?
description: None
date: 2019-06-17 15:00:49 -0000
last_modified_at: 2019-06-18 11:55:29 -0000
publish: true
pin: false
image:
  path: /assets/uploads/2019/06/runtime_final.png
categories:
- Uncategorized
tags:
- benchee
- benchmark
- board
- data structures
- Elixir
- ets
- list
- map
- performance
- tuple
---
{% raw %}
Ever wanted to implement something board game like in Elixir? Chess? Go? Islands? Well, then you're gonna need a board! But what data structure would be the most efficient one to use in Elixir? Conventional wisdom for a lot of programming languages is to use some sort of array. However, most programming languages with immutable data structures don't have a "real" array data structure (we'll talk about erlangs [`array`](http://erlang.org/doc/man/array.html) later, it's not really like the arrays in non functional languages) . Elixir is one of those languages. As I like board games [this was one of the first questions I ever asked the community](https://groups.google.com/d/msg/elixir-lang-talk/wZdchFo4JUU/X72oA5JJEQAJ). It's also an interesting and relatable example to see and understand the performance trade-offs of different data structures. Complete sources can be found in my [elixir_boards_benchmark repo](https://github.com/PragTob/elixir_boards_benchmark).

## Benchmark Design

For this benchmark I didn't have a very specific board game in mind so **I settled for a board size of 9x9** . It's a bit bigger than a normal chess board (8x8), it's exactly the size of the smallest "normal" Go-board and it's one smaller than the board used in Islands implemented in [Functional Web Development with Elixir, OTP and Phoenix](https://pragprog.com/book/lhelph/functional-web-development-with-elixir-otp-and-phoenix), so it seemed like a good compromise. Different sizes are likely to sport different performance characteristics. Without a concrete usage scenario in mind I settled on a couple of different benchmarks:

* **get** ting a value at the coordinates (0,0), (4, 4) and (8,8). This is a fairly nano/micro benchmark for data access and provides a good balance of values at the beginning/middle/end when thinking in list terms.
* **set** ting a value at the coordinates (0,0), (4, 4) and (8,8).
* a still nano/micro benchmark that combines the two previous benchmarks by getting and setting all three mentioned values. I call this **"mixed bag".**
* Why stop at the previous one? The last benchmark just sets and gets every possible coordinate once (first it sets (0,0) then gets it, then it sets (0, 1), then gets it and so forth). This also simulates the board filling which can be important for some data structures. Completely filling a board is unrealistic for most board games however, as most games finish before this stage. This one is called **"getting and setting full board"**.

Something that is notably not benchmarked is the creation of boards. For (almost) all of the board implementations it could resolve to a constant value which should be similar in the time it takes to create. I wasn't overly interested in that property and didn't want to make the code less readable by inlining the constant after creation when I didn't need to. Also noteworthy is that these benchmark mostly treat reading and writing equally while in my experience most AIs/bots are much more read-heavy than write-heavy. Take all these caveats of the benchmark design into consideration when looking at the results and if in doubt of course best write your own benchmark taking into account the concrete usage patterns of your domain. Without further ado then let's look at the different implementations I have benchmarked so far:

## Contenders

All boards need to implement a simple [Board behaviour](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board.ex): 

Source: [https://gist.github.com/PragTob/c38269e5e1b9eb7b8f6c3bf46d0b9e0c](https://gist.github.com/PragTob/c38269e5e1b9eb7b8f6c3bf46d0b9e0c)

**File: `board.ex`**
```elixir
defmodule Board do
  # can't be more specific witht types as each implementation has its own representation
  @type board :: any
  @type field :: any

  @callback new() :: board
  @callback get(board, non_neg_integer, non_neg_integer) :: field
  @callback set(board, non_neg_integer, non_neg_integer, field) :: board
end
```

 All boards are built so that accessing a previously unset field will return nil. No assumptions about the data stored in the board have been made, which rules out String as an implementation type. In the benchmarks atoms are used as values. In the descriptions of the data types below `(x, y)` is used to mark where what value is stored.

* **[List2D](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/list2d.ex): **A 2 dimensional list representing rows and columns: `[[(0, 0), (0, 1), (0, 2), ...], [(1, 0), (1, 1), ..], ..., [..., (8, 8)]]`
* **[List1D](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/list1d.ex): **Using the knowledge of a constant board size you can encode it into a one-dimensional list resolving the index as `dimension * x + y`: `[(0, 0), (0, 1), (0, 2), ..., (1, 0), (1, 1), ..., (8, 8)]`
* [**Tuple2D**](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/tuple_2d.ex): Basically like **List2D** but with tuples instead of lists: `{{(0, 0), (0, 1), (0, 2), ...}, {(1, 0), (1, 1), ..}, ..., {..., (8, 8)}}`
* **[Tuple1D](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/tuple_1d.ex)** : Basically like **List1D** but with a tuple instead of a list: `{(0, 0), (0, 1), (0, 2), ..., (1, 0), (1, 1),... (8, 8)}`
* [**Array2D**](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/array2d.ex): [erlang arrays](http://erlang.org/doc/man/array.html) aren't exactly a common sight, even [learn you some Erlang basically skims over them and says to be cautious when using them](https://learnyousomeerlang.com/a-short-visit-to-common-data-structures#arrays). I even forgot about them for the first version of this post 😅. They internally map to tuple usage in an interesting way that will be discussed/illustrated further below. With that out of the way, conceptually this is much like **Tuple2D**.
* [**Array1D**](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/array1d.ex): see above for the data structure in general, otherwise conceptually like **Tuple1D**.
* **[MapTuple](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/map_tuple.ex)** : A map that takes the tuple of the coordinates `{x, y}` as the key with the value being whatever is on the board: `%{{0, 0} => (0, 0), {0, 1} => (0, 1), ..., {8, 8} => (8, 8)}`. It's a bit unfair compared to others shown so far as it can start with an empty map which of course is a much smaller data structure that is not only smaller but usually faster to retrieve values from. As the benchmarks start with an _empty_ board that's a massive advantage, so I also included a full map in the benchmark, see next/
* [**MapTupleFull**](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/map_tuple_full.ex): Basically the same as above but initialized to already hold all key value pairs initialized as nil. Serves not only the purpose to see how this performs but also to see how **MapTuple** performs once it has "filled up".
* **[MapTupleHalfFull](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/map_tuple_half_full.ex)** : Only looking at complete full performance and empty performance didn't seem good either, so I added another one initialized from 0 to 4 on all columns (a bit more than a board half, totalling 45 key/value pairs).
* [**MapTupleQuarterFull**](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/map_tuple_quarter_full.ex): Another one of these, this time with 27 key/value pairs. Why? Because there is an interesting performance characteristic, read on to find out :)
* **[Map2D](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/map2d.ex)** : Akin to **List2D** etc. a map of maps: `%{0 => %{0 => (0, 0), 1 => (0, 1), ...}, 1 => %{0 => (1, 0), ...}, ..., 8 => %{..., 8 => (8, 8)}}`
* **[ETSSet](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/ets_set.ex)** : [erlang ETS](http://erlang.org/doc/man/ets.html) storage with table type `set`. Storage layout wise it's basically the same as MapTuple, with a tuple of coordinates pointing at the stored value.
* **[ETSOrderedSet](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/ets_ordered_set.ex)** : Same as above but with table type `ordered_set`.
* **[ProcessDictionary](https://github.com/PragTob/elixir_boards_benchmark/blob/master/lib/board/process_dictionary.ex)** : On a [special request for Michał](https://twitter.com/michalmuskala/status/1140642976030494721) ;) This is probably not a great default variant as you're practically creating (process-) global state which means you can't have two boards within the same process without causing mayham. Also might accidentally conflict with other code using the process dictionary. Still might be worth considering if you want to always run a board in its own process.

It's significant to point out that all mentioned data types except for ETS and the process dictionary are immutable. This means that especially for those in the benchmark a new board is created in a before_each hook (does not count towards measured time) to avoid "contamination". Another notable exception (save for String for the aforementioned constraints) is [Record](https://hexdocs.pm/elixir/Record.html). Records are internally represented as tuples but give you the key/value access of maps, however in elixir it is more common to use [Structs](https://elixir-lang.org/getting-started/structs.html) (which are backed by maps). As both maps and tuples are already present in the benchmark including these likely wouldn't lead to new insights.

## System Setup

Operating System | Linux  
---|---  
CPU Information | Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz  
Number of Available Cores | 8  
Available Memory | 15.61 GB  
Elixir Version | 1.8.2  
Erlang Version | 22.0  
  
## Benchmarking Results

Benchmarks of course were run with [benchee](https://github.com/bencheeorg/benchee) and the benchmarking script is [here](https://github.com/PragTob/elixir_boards_benchmark/blob/master/benchmark.exs) (nothing too fancy). You can check them out in the [repo](https://github.com/PragTob/elixir_boards_benchmark) as markdown (thanks to [benchee_markdown](https://github.com/hrzndhrn/benchee_markdown)) or HTML reports ([benchee_html](https://github.com/bencheeorg/benchee_html)). Careful though if you're on mobile some of the HTML reports contain the raw measurements and hence **go up to 9MB in size and can take a while to load** also due to the JS drawing graphs!

* [getting and setting full board](http://www.pragtob.info/benchee/board9x9/getting_and_setting_full_board.html)
* [mixed bag](http://www.pragtob.info/benchee/board9x9/mixed_bag.html)
* [get(0, 0)](http://www.pragtob.info/benchee/board9x9/get_0_0.html)
* [get(4, 4)](http://www.pragtob.info/benchee/board9x9/get_4_4.html)
* [get(8, 8)](http://www.pragtob.info/benchee/board9x9/get_8_8.html)
* [set(0, 0)](http://www.pragtob.info/benchee/board9x9/set_0_0.html)
* [set(4, 4)](http://www.pragtob.info/benchee/board9x9/set_4_4.html)
* [set(8, 8)](http://www.pragtob.info/benchee/board9x9/set_8_8.html)

The results of getting and setting full board: ![runtime_final.png](/assets/uploads/2019/06/runtime_final.png) getting and setting full board iterations per second (higher is better) It's a tight race at the top when it comes to run time! **Tupl1D** , **Tuple2D** and **MapTuple** are all within striking range of each other and then there's a sharp fall off. Also there is a fair bit of variance involved as shown by the black "whiskers" (this is usual for benchmarks that finish in nanoseconds or microseconds because of garbage collection, interference etc.). Which one of these is best? To get a better picture let's look at the whole table of results:  Name | IPS | Average | Deviation | Median | Mode | Minimum | Maximum  
---|---|---|---|---|---|---|---  
Tuple1D | 133.95 K | 7.47 μs | ±23.29% | 6.93 μs | 6.88 μs | 6.72 μs | 492.37 μs  
Tuple2D | 132.16 K | 7.57 μs | ±29.17% | 7.21 μs | 7.16 μs | 7.03 μs | 683.60 μs  
MapTuple | 126.54 K | 7.90 μs | ±25.69% | 7.59 μs | 7.56 μs | 7.43 μs | 537.56 μs  
ProcessDictionary | 64.68 K | 15.46 μs | ±14.61% | 15.12 μs | 15.05 μs | 14.89 μs | 382.73 μs  
ETSSet | 60.35 K | 16.57 μs | ±9.17% | 16.04 μs | 15.95 μs | 15.79 μs | 161.51 μs  
Array2D | 56.76 K | 17.62 μs | ±17.45% | 17.15 μs | 17.04 μs | 16.54 μs | 743.46 μs  
MapTupleFull | 55.44 K | 18.04 μs | ±11.00% | 16.92 μs | 16.59 μs | 16.43 μs | 141.19 μs  
MapTupleHalfFull | 53.70 K | 18.62 μs | ±8.36% | 17.96 μs | 17.87 μs | 17.67 μs | 160.86 μs  
Array1D | 50.74 K | 19.71 μs | ±10.60% | 19.29 μs | 18.99 μs | 18.81 μs | 469.97 μs  
ETSOrderedSet | 39.53 K | 25.30 μs | ±10.51% | 24.82 μs | 24.57 μs | 24.34 μs | 390.32 μs  
Map2D | 36.24 K | 27.59 μs | ±8.32% | 27.71 μs | 25.90 μs | 25.12 μs | 179.98 μs  
List2D | 29.65 K | 33.73 μs | ±4.12% | 33.31 μs | 33.04 μs | 31.66 μs | 218.55 μs  
MapTupleQuarterFull | 28.23 K | 35.42 μs | ±3.86% | 34.96 μs | 34.61 μs | 34.39 μs | 189.68 μs  
List1D | 15.41 K | 64.90 μs | ±2.84% | 64.91 μs | 64.14 μs | 62.41 μs | 175.26 μs  
Median, and Mode are good values to look at when unsure what is usually fastest. These values are the "middle value" and the most common respectively, as such they are much less likely to be impacted by outliers (garbage collection and such). These seem to reinforce that **Tuple1D** is really the fastest, if by a negligible margin. **MapTuple** is very fast, but its sibling **MapTupleFull** , that already starts "full", is more than 2 times slower. Whether this is significant for you depends if you start with a truly empty board (Go starts with an empty board, chess doesn't for instance). Somewhat expectedly **List1D** does worst as getting values towards to the end of the list it has to traverse the entire list which is incredibly slow. As an aside, it's easy to see in the box plot that the high deviation is mainly caused by some very big outliers: ![boxplot_final.png](/assets/uploads/2019/06/boxplot_final.png) Boxplot of getting and setting full board - dots are outliers The dots denote outliers and they are so big (but few) that the rest of the chart is practically unreadable as all that remains from the actual box is practically a thick line. What about memory consumption? ![memory_final.png](/assets/uploads/2019/06/memory_final.png) getting and setting full board memory usage (lower is better) Here we can see the immediate drawback of **Tuple1D** \- it's memory consumption is many times worse than that of the others. My (educated) guess is that it's because it has to replace/copy/update the whole tuple with it's 9*_9 = 81_ values for every update operation. **Tuple2D** is much more economical here, as it only needs to to update the tuple holding the columns and the one holding the specific column we're updating (_2 * 9 = 18_) to the best of my understanding. Big Tuples like this are relatively uncommon in "the real world" in my experience though as their fixed size nature makes them inapplicable for a lot of cases. Luckily, our case isn't one of them. **MapTuple** does amazingly well overall as it's probably the structure quite some people would have intuitively reached for for good constant memory access speed. It's memory consumption is also impressively low. **ProcessDictionary** is very memory efficient and also constantly in the top 4 when it comes to run time. However, at least run time wise there's quite the margin ~15 μs to ~7 μs which doesn't seem to make the risks worth it overall.

## Other Observations

Let's take a look at some other things that seem note worthy:

### ETS isn't the winner

This surprised me a bit (however I haven't used ETS much). ETS was always tagged as the go to option for performance in my mind. Looking at the docs and use cases I know it makes sense though - we're likely to see benefits for much larger data sets as ours is relatively small:

> These (ETS) provide the ability to store very large quantities of data in an Erlang runtime system, and to have constant access time to the data.

81 values hardly qualifies as "very large". Don't blindly follow conventional "wisdom" - always benchmark! 💪

### **get(0,0) vs. get(8,8)**

Let's have a look at some of the time it takes to retrieve a value - usually a much more common operation than writing:

#### get(0,0)

Name | IPS | Average | Deviation | Median | Mode | Minimum | Maximum  
---|---|---|---|---|---|---|---  
Tuple1D | 44.12 M | 22.66 ns | ±842.77% | 20 ns | 20 ns | 9 ns | 35101 ns  
Tuple2D | 42.46 M | 23.55 ns | ±846.67% | 20 ns | 19 ns | 7 ns | 36475 ns  
Array1D | 30.38 M | 32.92 ns | ±84.61% | 32 ns | 32 ns | 20 ns | 8945 ns  
MapTuple | 29.09 M | 34.38 ns | ±111.15% | 32 ns | 31 ns | 19 ns | 10100 ns  
MapTupleQuarterFull | 18.86 M | 53.03 ns | ±37.27% | 50 ns | 49 ns | 38 ns | 2579 ns  
Array2D | 18.62 M | 53.70 ns | ±67.02% | 50 ns | 49 ns | 34 ns | 10278 ns  
List1D | 18.26 M | 54.75 ns | ±56.06% | 53 ns | 52 ns | 42 ns | 8358 ns  
ProcessDictionary | 17.19 M | 58.18 ns | ±1393.09% | 52 ns | 51 ns | 39 ns | 403837 ns  
Map2D | 15.79 M | 63.34 ns | ±25.86% | 60 ns | 54 ns | 41 ns | 388 ns  
MapTupleHalfFull | 10.54 M | 94.87 ns | ±27.72% | 91 ns | 89 ns | 76 ns | 2088 ns  
MapTupleFull | 10.29 M | 97.16 ns | ±18.01% | 93 ns | 89 ns | 70 ns | 448 ns  
ETSSet | 9.74 M | 102.63 ns | ±26.57% | 100 ns | 99 ns | 78 ns | 2629 ns  
List2D | 9.04 M | 110.57 ns | ±69.64% | 105 ns | 109 ns | 82 ns | 4597 ns  
ETSOrderedSet | 6.47 M | 154.65 ns | ±19.27% | 152 ns | 149 ns | 118 ns | 1159 ns  
  
#### get(8, 8)

Name | IPS | Average | Deviation | Median | Mode | Minimum | Maximum  
---|---|---|---|---|---|---|---  
Tuple2D | 42.47 M | 23.55 ns | ±788.60% | 21 ns | 20 ns | 7 ns | 33885 ns  
Tuple1D | 40.98 M | 24.40 ns | ±725.07% | 22 ns | 21 ns | 10 ns | 34998 ns  
Array1D | 29.67 M | 33.70 ns | ±161.51% | 33 ns | 32 ns | 21 ns | 18301 ns  
MapTuple | 28.54 M | 35.03 ns | ±986.95% | 32 ns | 32 ns | 20 ns | 230336 ns  
ProcessDictionary | 19.71 M | 50.73 ns | ±1279.45% | 47 ns | 47 ns | 34 ns | 377279 ns  
Array2D | 17.88 M | 55.92 ns | ±85.10% | 52 ns | 51 ns | 35 ns | 13720 ns  
Map2D | 13.28 M | 75.31 ns | ±32.34% | 73 ns | 65 ns | 56 ns | 2259 ns  
MapTupleHalfFull | 12.12 M | 82.53 ns | ±31.49% | 80 ns | 80 ns | 60 ns | 1959 ns  
ETSSet | 9.90 M | 101.05 ns | ±16.04% | 99 ns | 95 ns | 78 ns | 701 ns  
MapTupleFull | 9.85 M | 101.53 ns | ±19.29% | 99 ns | 90 ns | 70 ns | 487 ns  
ETSOrderedSet | 5.59 M | 178.80 ns | ±41.70% | 169 ns | 170 ns | 135 ns | 4970 ns  
MapTupleQuarterFull | 4.09 M | 244.65 ns | ±16.85% | 242 ns | 240 ns | 226 ns | 9192 ns  
List2D | 3.76 M | 265.82 ns | ±35.71% | 251 ns | 250 ns | 231 ns | 9085 ns  
List1D | 1.38 M | 724.35 ns | ±10.88% | 715 ns | 710 ns | 699 ns | 9676 ns  
The top 3 remain relatively unchanged. What is very illustrative to look at is **List1D** and **List2D** though. For `get(0, 0)` List1D vastly outperforms its 2D sibling even being closest to the top group. That is easy to explain because it basically translates to looking at the first element of the list which is very fast for a linked list. However, looking at the last element is very slow and this is what `get(8, 8)` translates to. All elements have to be traversed until the end is reached. As such the whole thing is almost 16 times slower for List1D. List2D is still very slow but through it's 2-dimenstional structure it only needs to look at 18 elements instead of 81.

### MapTuple vs. MapTupleQuarterFull vs. MapTupleHalfFull vs. MapTupleFull

In most scenarios, including the biggest scenario, MapTupleQuarterFull performs worse than MapTuple (expected), MapTupleHalfFull (unexpected) and MapTupleFull (unexpected). I had expected its performance to be worse than MapTuple but better than MapTupleFull and MapTupleHalfFull. Why is that? I had no idea but [Johanna had one](https://twitter.com/joladev/status/1140637903636303873): it might have to do with the "magic" limit at which a map _"really"_ becomes a map and not just a list that is linearly searched. That limit is defined as **[32 entries in the erlang source code](https://github.com/erlang/otp/blob/b286b7f1de4aed13ba71b817321673eb67df941e/erts/emulator/beam/erl_map.h#L72-L76)** (link also [provided by Johanna](https://twitter.com/joladev/status/1140655352159121408)). Our quarter full implementation is below that limit (27 entries) and hence often performance characteristics more akin to **List1D** (see good get(0, 0) performance but bad get(8, 8) performance) than its "real" map cousins. To the best of my understanding this "switch the implementation at size 32" is a performance optimization. With such a small data set a linear search often performs better than the overhead introduced by hashing, looking up etc. You can also see that **the trade-off pays off** as in the big benchmark where the whole board is filled incrementally **MapTuple** (which is initially empty and grows) still provides **top performance**. What I still don't fully understand is that sometimes MapTupleFull seems to still outperform MapTupleHalfFull - but only by a very negligible margin (most notably in the "big" getting and setting full board benchmark). The difference however is so small that it doesn't warrant further investigation I believe, unless you have an idea of course.

### Performance difference of Array vs. Tuple

In the introduction I said arrays are backed by tuples - how come their performance is way worse then? Well, let's have a look at what an array actually looks like:
  
    iex(3)> mine = :array.new(81, default: nil)
    {:array, 81, 0, nil, 100}
    iex(4)> :array.set(13, :boom, mine)
    {:array, 81, 0, nil,
    {10, {nil, nil, nil, :boom, nil, nil, nil, nil, nil, nil}, 10, 10, 10, 10, 10,
    10, 10, 10, 10}}

It cleverly doesn't even initialize all the fields but uses some kind of **length encoding** saying "the value is the default value of nil for the next 100 fields" but also saving its set size limit of 81 (fun fact: these arrays can be configured to also dynamically grow!). Once we set a value (at index 13) the representation changes showing still some length encoding "there is nothing here for the first 10 entries" but then the indexes **10..19 are expanded as a whole tuple that's holding our value**. So, to the best of my understanding arrays work by adding "stretches" of tuples the size of 10 as they need to. In general this is a [performance optimization especially making writes/updates faster as compared to huge tuples](http://erlang.org/pipermail/erlang-questions/2009-March/042705.html) as mainly the 10-tuple holding the concrete value needs to get updated instead of the whole thing. However, our custom tuple implementations are perfectly sized to begin with and not too huge. Moreover, their whole size being set at compile-time probably enables some optimizations (or so I believe). Hence the tuple implementations outperform them while arrays don't do too shabby (especially with read access) as compared to other implementations.

## Conclusion

Tuples can be very good for the use case of known at compile time sized collections that need fast access and a simple flat map performs amazingly well. All that least for the relatively small board size (9x9 = 81 fields) benchmarked against here. There is a big caveat for the map though - it is so fast if we can start with an empty map and grow it in size as new pieces are set. The completely initialized map (MapTupleFull) performs way worse, tuples are the clear winners then. **Missing a data structure? Please do a PR!** There's a behaviour to implement and then just to lists to add your module name to - [more details](https://github.com/PragTob/elixir_boards_benchmark#adding-your-own-implemenation). **Update 1 (2019-06-17):** Fixed MapTupleHalfFull. Before the update it was actually just quarter full 😅 which has wildly different performance characteristics for reasons now described along with the MapTupleQuarterFull implementation. Thanks goes to [Johanna for pointing that out](https://twitter.com/joladev/status/1140637903636303873). Also the process registry has been added as another possible implementation on a [suggestion from Michał](https://twitter.com/michalmuskala/status/1140642976030494721) ;) . Also added a run time box plot to show outliers clearer and visually. **Update 2 (2019-06-18):** Added and investigated Arrays thanks to [/u/Hauleth over on reddit](https://www.reddit.com/r/elixir/comments/c1s8sn/whats_the_fastest_data_structure_to_implement_a/erflczj/). Also added a remark about records thanks to [/u/friendlysock over on lobste.rs](https://lobste.rs/s/yl7t41/what_s_fastest_data_structure_implement#c_46zsxe).
{% endraw %}
