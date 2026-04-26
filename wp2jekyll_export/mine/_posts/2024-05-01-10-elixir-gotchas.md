---
layout: post
permalink: https://pragtob.wordpress.com/2024/05/01/10-elixir-gotchas/
title: 10 Elixir gotchas
description: None
date: 2024-05-01 14:39:18 -0000
last_modified_at: 2024-05-11 07:28:58 -0000
publish: true
pin: false
image:
  path: https://pragtob.wordpress.com/wp-content/uploads/2024/05/image.png
categories:
- Beginner
tags:
- Elixir
- Erlang
- gotchas
- learning
---
No, I've not gone to the click-baiters ("10 tips that will change your life today!!!"), but I chose to limit myself to just 10 so that I don't pull what is considered a "Tobi" and spend days writing a blog post so huge no one wants to read it anyhow. I'll write a follow-up post with more :)

Anyhow, what are **"gotchas"**? For this purpose I'd define them as "**slightly confusing or irritating behavior, prone to lead to errors especially when you're new to Elixir** ". There are good reasons for many of these, however some of them are also more arcane. Running on the great basis that [Erlang](https://www.erlang.org/) built is probably Elixir's biggest asset - it gives us a lot of functionality and properties that helps Elixir thrive especially in the modern multi-core and multi-node environment. However, Erlang also comes with its fair share of baggage as a programming language conceived almost 40 years ago. Erlang's focus on backwards compatibility also means many of these decisions still live on today.

The list is brought to you by:

  1. My own experience learning Elixir
  2. Me teaching Elixir to folks both at Liefery and at Remote over the years
  3. Horrifying discoveries in production code

Apologies for the lack of syntax highlighting, but wordpress borked the last way that was working for elixir and I didn't want to yak shave this too far. I hope that you can sill enjoy them and may learn from them!

## 1\. A list of numbers becomes text in iex

[![](https://pragtob.wordpress.com/wp-content/uploads/2024/05/image.png?w=325)](https://pragtob.wordpress.com/wp-content/uploads/2024/05/image.png)

Let's start with an oldie but goldie that pretty much every beginner book tells you about: **Why does this random list of integers print out as text?**
  
    iex> [69, 108, 105, 120, 105, 114]
    ~c"Elixir"

This is because [charlists](https://hexdocs.pm/elixir/1.16.2/binaries-strings-and-charlists.html#charlists), denoted by `~c"text"` or `'text'`, are actually just that - a **list of integers**. So `iex` literally can't tell the difference and does its own best guess work: it checks if the integers are in a range between 0 and 127 and will then print it as text.

You can also show that it literally is a list by using `Enum` functions on it:
  
    iex> Enum.map(~c"elixir", fn integer -> integer + 100 end)
    [201, 208, 205, 220, 205, 214]
    iex> Enum.map(~c"elixir", fn integer -> integer - 32 end)
    ~c"ELIXIR"

The first line changes the integers to be outside of the printable range with +100 so `iex` prints it as a list of integers again. The second one just uses the knowledge that the difference between lower case and upper case letters in ASCII is 32 to transform it.

## 2\. Charlists vs. Strings

All this brings us to the following questions: **Why do we even have charlists and strings in elixir?** What's the difference between them? When do I use which one? Great question! It's a source of a lot of confusion, esp. since **in most languages single and double-quoted strings only sport minor differences** \- in Elixir they are backed by entirely different data structures. While single-quoted strings are just a list of integers, **double-quoted strings are UTF-8 encoded binaries** and so resemble strings you are used to in most modern programming languages.

**As a rule of thumb, use strings aka double-quotes (`"string")`**. The major use case for charlists / `'charlists'`/`~c"charlists"` is interfacing with erlang or erlang libraries. Or in the words of the [documentation](https://hexdocs.pm/elixir/binaries-strings-and-charlists.html#charlists):

> In practice, you will not come across them often, only in specific scenarios such as interfacing with older Erlang libraries that do not accept binaries as arguments.

The other mystery here are the 2 different syntaxes in use for charlists - single quotes (`'charlist'`) vs. the `~c"charlist"` sigil. That's a rather recent development, it was changed in [Elixir 1.15](https://hexdocs.pm/elixir/1.15/changelog.html#1-enhancements-4), after [some discussion](https://elixirforum.com/t/convert-charlists-into-c-charlists/49455). The reason for this is what I mentioned initially - it caused a lot of confusion:

> In many languages, `'foobar'` is equivalent to `"foobar"`, that’s not the case in Elixir and we believe it leads to confusion.

So, it's now less confusing but still confusing - which is why it made this list.

## 3\. `%{}` matches any Map

Pattern matching is one of Elixir's chief features! You can see it utilized frequently, for instance in a recursive function where we want to end recursion on empty list:
  
    def list([]) do
      IO.puts("list is empty")
    end

That works flawlessly, however **if you try the same with a map it'll always match** \- no matter the map:
  
    def map(%{}) do
      IO.puts("Empty map or is it?")
    end
    
    
    iex> map(%{not: "empty"})
    Empty map or is it?

The reason is simple - pattern matches on lists and maps just work different. In a list we're looking for an exact match of the elements, whereas for maps it is basically checked if the structure is included:
  
    iex> [a, b, c] = [1, 2, 3]
    [1, 2, 3]
    iex> [a, b, c] = [1, 2, 3, 4]
    ** (MatchError) no match of right hand side value: [1, 2, 3, 4]
    iex> [] = [1, 2, 3]
    ** (MatchError) no match of right hand side value: [1, 2, 3]
    iex> %{action: action} = %{action: "learn"}
    %{action: "learn"}
    iex> %{action: action} = %{action: "learn", more: "can be", provided: true}
    %{
      more: "can be",
      action: "learn",
      provided: true
    }
    iex> %{} = %{action: "learn", more: "can be", provided: true}
    %{
      more: "can be",
      action: "learn",
      provided: true
    }
    iex> %{action: action} = %{no_action: "sad"}
    ** (MatchError) no match of right hand side value: %{no_action: "sad"}

If you do want to execute a function only when given an empty map you can **use either of the following guards:`map_size(map) == 0` or `map == %{}`** \- which also showcases the difference between the match `(=)` and equality (`==`) operators. One full example from [the docs](https://hexdocs.pm/elixir/1.16.2/patterns-and-guards.html#why-guards):
  
    def empty_map?(map) when map_size(map) == 0, do: true
    def empty_map?(map) when is_map(map), do: false

## 4\. Structs are Maps

While we're in the topic of maps let's talk about structs! We can easily create and use a struct:
  
    iex> defmodule Human do
    ...> defstruct [:name, :age]
    ...> end
    iex> tobi = %Human{name: "Tobi", age: 34}
    %Human{name: "Tobi", age: 34}

It gets more interesting around pattern matching again, let's try `%{}` from the previous section:
  
    iex> %{} = %Human{name: "Tobi", age: 34}
    %Human{name: "Tobi", age: 34}
    iex> is_map(%Human{name: "Tobi", age: 34})
    true

It matches and it is a map! **Structs are nothing more than special maps with a`__struct__` key** that tells it which struct it is. It gets even weirder when you know that some of the built-in data types are structs and hence maps:
  
    iex> is_map(1..10)
    true
    iex> is_map(Date.utc_today())
    true
    iex> is_map(~r/elixir/)
    true

We can see their map nature more easily in an example! With a bit of meddling we can also tell `IO.inspect` to not print a prettified version showing us the real map underneath:
  
    iex> tobi = %Human{name: "Tobi", age: 34}
    %Human{name: "Tobi", age: 34}
    iex> tobi.__struct__
    Human
    iex> Map.keys(tobi)
    [:name, :__struct__, :age]
    iex> Map.values(tobi)
    ["Tobi", Human, 34]
    iex> IO.inspect(tobi, structs: false)
    %{name: "Tobi", __struct__: Human, age: 34}
    %Human{name: "Tobi", age: 34}
    iex> IO.inspect(1..10, structs: false)
    %{first: 1, last: 10, step: 1, __struct__: Range}
    1..10

Now, you might think this all doesn't matter too much. But it does! Be aware that **every pattern match on a map might also match on a struct with the same keys, so will every`is_map` check**. And yes, dates and ranges may match as well as shown above:
  
    iex> %{first: number} = 1..10
    1..10
    iex> number
    1

I have seen bugs in code that first matched on something being a map and only later matched on specific structs. So, instead of the struct specific code the more general map code was run - and hence another hard to track down bug was born.

In order to combat this, the Elixir team i[ntroduced a new `is_non_struct_map/1` guard](https://github.com/elixir-lang/elixir/pull/13534).

## 5\. Structs don't implement Access

So, I just told you that structs are just maps. But then you try to use random key access via `[]` on them and you are confused again:
  
    iex(18)> tobi[:age]
    ** (UndefinedFunctionError) function Human.fetch/2 is undefined (Human does not implement the Access behaviour
    
    You can use the "struct.field" syntax to access struct fields. You can also use Access.key!/1 to access struct fields dynamically inside get_in/put_in/update_in)
        Human.fetch(%Human{name: "Tobi", age: 34}, :age)
        (elixir 1.16.0-rc.1) lib/access.ex:309: Access.get/3
        iex:18: (file)
    iex(18)> tobi.age
    34
    iex(19)> map_tobi = %{name: "Tobi", age: 34}
    %{name: "Tobi", age: 34}
    iex(20)> map_tobi[:age]
    34
    iex(21)> map_tobi.age
    34

As usual, elixir is amazing and already tells us that the problem is that the struct doesn't implement the [Access behaviour](https://hexdocs.pm/elixir/main/Access.html). **As structs have predefined keys, you should use the dot-syntax of`struct.key` to access them.** However, since sometimes you do still want to randomly access struct keys you can use the fact that structs are still just maps to your advantage using functions like [`Map.get/`3](https://hexdocs.pm/elixir/1.16/Map.html#get/3):
  
    iex(22)> attribute = :age
    :age
    iex(23)> Map.get(tobi, attribute)
    34

You can also take it further than that and use `[get_in/2](https://hexdocs.pm/elixir/main/Kernel.html#get_in/2)`. It doesn't work in a plain attempt, but can work thanks to `[Access.key/2](https://hexdocs.pm/elixir/1.16.2/Access.html#key/2)`:
  
    iex(25)> get_in(tobi, [attribute])
    ** (UndefinedFunctionError) function Human.fetch/2 is undefined (Human does not implement the Access behaviour
    # etc....
    iex(25)> get_in(tobi, [Access.key(attribute)])
    34

Be mindful to only use these if you really do need random key access on structs. Otherwise there are [many other ways](https://hexdocs.pm/elixir/main/Kernel.html#get_in/2-working-with-structs), such as good old plain dot-based access or pattern matching even.

## 6\. Keyword lists are a bit awkward as options and in pattern matches

Another somewhat special data structure in elixir are [keyword lists](https://hexdocs.pm/elixir/main/keywords-and-maps.html#keyword-lists). Again, these are backed by "syntactic sugar" on top of lists. A keyword list is a list of 2 element tuples, where the first element is an atom.
  
    iex> [{:option, true}] == [option: true]
    true

When you call functions with keywordlists as the last argument you can even omit the brackets as seen before when we wrote `IO.inspect(tobi, structs: false)` \- `structs: false` is a keyword list here. These properties make it the default data structure for passing along options to functions in Elixir.

However, since it's a list the order matters here (and keys can be duplicated!) which often isn't what you want for options: order usually doesn't matter and duplicated options should not be a thing. It's great for DSLs such as [ecto](https://github.com/elixir-ecto/ecto), but when used as options it means it's hard to pattern match on them. Let's check out the following function:
  
    def option(warning: true) do
      IO.puts "warning!"
    end
    
    def option(_anything) do
      IO.puts "No warning!"
    end

It only matches when our options are **exactly** `warning: true` \- any additional data makes it a different list and hence fails the pattern match:
  
    iex> option warning: true
    warning!
    iex> option warning: true, more: true
    No warning!
    iex> option more: true, warning: true
    No warning!

It's an issue[I struggled with early in my Elixir days](https://elixirforum.com/t/passing-in-options-maps-vs-keyword-lists/1963). There are plenty of solutions for this. What I do in [benchee](https://github.com/bencheeorg/benchee) is accept the options as a keyword list but **internally convert it to a map** (well, actually a struct even!). So, internally I can work with a nice structure that is easy to pattern match, but preserves the nice & idiomatic interface.

You can also use `[Keyword.get/3](https://hexdocs.pm/elixir/main/Keyword.html#get/3)` to get the value of whatever option you're looking for. You can also use `[Keyword.validate/2](https://hexdocs.pm/elixir/1.16.2/Keyword.html#validate/2)` to make sure only well known options are supplied and that you provide good defaults - [hat tip to Vinicius](https://www.linkedin.com/feed/update/urn:li:activity:7191447313477718016?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7191447313477718016%2C7191455673849671680%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287191455673849671680%2Curn%3Ali%3Aactivity%3A7191447313477718016%29).

## 7\. Everything can be compared to Everything

Another surprise might be that **you can compare literally every elixir term with one another** without raising an exception:
  
    iex> nil < 8
    false
    iex> 8 < "hello"
    true
    iex> {1, 2} < ["a"]
    true

Most people would probably expect this to raise an error as it does in many other languages. It doesn't, as Elixir does [structural comparisons](https://hexdocs.pm/elixir/main/Kernel.html#module-structural-comparison) and follows **Erlang's[term ordering](https://hexdocs.pm/elixir/main/Kernel.html#module-term-ordering)** which basically gives all terms a predetermined order:

`number < atom < reference < function < port < pid < tuple < map < list < bitstring`

Why is it done like this?

> This means **comparisons in Elixir are structural** , as it has the goal of comparing data types as efficiently as possible to create flexible and performant data structures.

All in all being able to compare everything to everything may sound mildly annoying but can also lead to some really bad bugs. In a conditional, this will just silently run the wrong code:
  
    iex> maximum = "100" # forgot to parse
    "100"
    iex> if 9999 < maximum, do: "you pass"
    "you pass"

I have seen similar bugs in production code bases, esp. since `nil` also doesn't raise and is more likely to slip through. Thankfully, if you try to compare structs elixir issues a warning these days:
  
    iex> %Human{} > nil
    warning: invalid comparison with struct literal %Human{}. Comparison operators (>, <, >=, <=, min, and max) perform structural and not semantic comparison. Comparing with a struct literal is unlikely to give a meaningful result. Struct modules typically define a compare/2 function that can be used for semantic comparison
    └─ iex:6
    
    true

It's note-worthy that this gotcha and the next one are currently [already being addressed at Elixir targeted for the 1.17 release](https://twitter.com/josevalim/status/1785989792141890015), thanks to the introduction of the type system. Beyond that, [sabiwara also wrote the micro library `cmp` to take care of the problem](https://github.com/sabiwara/cmp).

## 8\. Proper Date comparisons

Speaking of which, how do you compare dates?
  
    iex(18)> ~D[2024-05-01] > ~D[2024-05-02]
    warning: invalid comparison with struct literal ~D[2024-05-01]. Comparison operators (>, <, >=, <=, min, and max) perform structural and not semantic comparison. Comparing with a struct literal is unlikely to give a meaningful result. Struct modules typically define a compare/2 function that can be used for semantic comparison
    └─ iex:18
    false

Whoops, there is that warning again! Obviously, we shouldn't compare them like this - but it still works, and **might even produce the correct result by accident slipping through tests**!

The correct way to [compare dates](https://hexdocs.pm/elixir/1.16.2/Date.html#module-comparing-dates) is `[Date.compare/2](https://hexdocs.pm/elixir/1.16.2/Date.html#compare/2)` and friends:
  
    iex> Date.compare(~D[2024-05-01], ~D[2024-05-02])
    :lt

Again, you may be surprised how often this has snuck past someone.

## `9. nil["something"]` is valid and returns `nil`

Another surprise may be this:
  
    iex> nil["something"]
    nil

Of course, you'd never write it like this but if a `nil` value had gotten past you and was in your `map` variable there'd be no way to tell:
  
    iex> map = nil
    nil
    iex> map["something"]
    nil

Which, can be very dangerous. Why is it like this? So that you can use `[]` to safely access nested values:
  
    iex> map = %{a: %{b: :c}}
    %{a: %{b: :c}}
    iex> map[:a][:b]
    :c
    iex> map[:d][:b]
    nil

In that last example `map[:d]` returns `nil` and then `nil[:b]` evaluates to `nil` again without crashing. If you wanted to assure that the keys are there, you got a lot of possibilities but one of them is pattern matching:
  
    iex> %{a: %{b: value}} = map
    %{a: %{b: :c}}
    iex> value
    :c
    iex> %{d: %{b: value}} = map
    ** (MatchError) no match of right hand side value: %{a: %{b: :c}}

## 10\. How to use constants

Another question that's common among Elixir newcomers is: "Cool, so how do I define constants?" and the answer is... there are no real constants in Elixir/Erlang. The best workaround we have are [module attributes](https://hexdocs.pm/elixir/1.16.2/module-attributes.html#as-constants). However, they are not visible to the outside by default so you have to provide a function to access them:
  
    defmodule Constants do
      @my_constant "super constant"
      def my_constant do
        @my_constant
      end
    end
    
    
    iex> Constants.my_constant()
    "super constant"

That works, however one unfortunate thing about module attributes is that they aren't... **you know, truly constant.** You can redefine a module attribute later on in a module without any warning and if you then use it again below the new definition - with its value will have changed:
  
    defmodule Constants do
      @my_constant "super constant"
      def my_constant do
        @my_constant
      end
    
      @my_constant "ch-ch-changes!"
      def my_constant_again do
        @my_constant
      end
    end
    
    
    iex> Constants.my_constant_again()
    "ch-ch-changes!"
    iex> Constants.my_constant()
    "super constant"

Interestingly, the **value is _not_ changed retroactively** so `my_constant/0` still returns the original value (and is a true constant in that sense). But it _can_ change throughout the module, which is necessary for other use cases of module attributes. So, if you accesses it in a function and someone happened to define it again with a newer value above, you may be in for a bad time.

Hence, I whole-heartedly agree with my friend Michał here:

https://twitter.com/michalmuskala/status/1785313458470191559

It's also worth nothing that you don't _need_ module attributes - you can also just define a function that returns a constant value:
  
    def my_other_constant do
      "This is cool as well"
    end

In many cases, the compiler is smart enough to realize it's a constant value (even with some operations applied) and so you won't suffer a performance penalty for this. However, there are cases where it doesn't work (f.ex. reading a file) and certain [guards](https://hexdocs.pm/elixir/1.16.2/patterns-and-guards.html#guards) require module attributes (f.ex. around enum checking). Hat tip to [discussing this with José](https://twitter.com/josevalim/status/1785781791682372044).

To help with this, [hauleth has also created a new miny library called `defconst`](https://github.com/hauleth/defconst).

## Closing

Hope you enjoyed these gotchas and they helped you! What gotchas are missing? Let me know in the comments or elsewhere and I'll try to cover them in future editions - I still got ~10 on my TODO list so far though 😅

It's also worth mentioning that Elixir is well aware of a lot of these - if you follow the links I posted, they will frequently send you to Elixir's own documentation explaining these. From the early days, there have also already been quite some improvements and more warnings emitted to help you. As **Elixir is amazing, and cares a lot about the developer experience**.

If you enjoyed this post and think "Working with Tobi may be cool!" - you're in luck as [**I'm still looking for a job**](https://pragtob.wordpress.com/2024/04/08/looking-for-a-job-2/) \- so give me a shout, will ya? 💚

Update 1 (2024-05-02):

* Extended on using just functions as constant after [discussion with José](https://twitter.com/josevalim/status/1785781791682372044).
* [Recent advancements for more warnings, again by José.](https://twitter.com/josevalim/status/1785989792141890015)
* Point to `Keyword.validate/`2 [thanks to Vinicius](https://www.linkedin.com/feed/update/urn:li:activity:7191447313477718016?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7191447313477718016%2C7191455673849671680%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287191455673849671680%2Curn%3Ali%3Aactivity%3A7191447313477718016%29).

Update 2 (2024-05-04)

* [José pointed out why structural comparison/term ordering are a thing](https://elixirforum.com/t/blog-post-10-elixir-gotchas/63278/30?u=pragtob)
* Clarify that the changing nature of module attributes has a reason
* Mention `[defconst](https://github.com/hauleth/defconst)`

Update 3 (2024-05-11)

* A new [`is_non_struct_map/1` guard was added to Elixir](https://github.com/elixir-lang/elixir/pull/13534)!
* Mention `[cmp](https://github.com/sabiwara/cmp)`
