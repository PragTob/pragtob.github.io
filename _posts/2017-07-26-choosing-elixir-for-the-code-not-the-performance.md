---
layout: post
title: Choosing Elixir for the Code, not the Performance
description: None
date: 2017-07-26 13:00:35 -0000
last_modified_at: 2017-08-01 11:11:18 -0000
publish: true
pin: false
categories:
- Software Engineering
tags:
- clarity
- code
- Elixir
- performance
- programming languages
- ruby
---
People like to argue about programming languages: "This one is better!" "No this one!". In these discussion, often the _performance card_ is pulled. This language is that much faster in these benchmarks or this company just needs that many servers now. Performance shouldn't matter that much in my opinion, and Nate Berkopec makes a good point about that in his blog post ["Is Ruby too slow for web scale?"](https://www.speedshop.co/2017/07/11/is-ruby-too-slow-for-web-scale.html) (TLDR; we can add more servers and developer time often costs more than servers):

> The better conversation, the more meaningful and impactful one, is which framework **helps me write software faster, with more quality, and with more happiness**.

I agree with lots of the points Nate makes and I like him and the post, but still it rubbed me the wrong way a bit. While it also states the above, it makes it seem like people just switch languages for the performance gains. And that brought up a topic that has been bugging me for a while: If you're switching your main language purely for performance, there's a high chance you're doing it wrong. **Honestly, if all we cared about was performance we'd all still be writing Assembly** , or C/C++ at least. It's also true, that performance is often hyped a lot around new languages and specifically Elixir can also be guilty of that. And sure, performance is great and we read some amazing stories about that. Two of the most prominent adoption stories that I can recall are usually cited and referred to for their great performance numbers. There is [Pinterest "our API responses are in microseconds now"](https://medium.com/@Pinterest_Engineering/introducing-new-open-source-tools-for-the-elixir-community-2f7bb0bb7d8c) and there is [Bleacher Report "we went from 150 servers to 5"](http://www.techworld.com/apps-wearables/how-elixir-helped-bleacher-report-handle-8x-more-traffic-3653957/). If you re-read the articles though, other benefits of elixir are mentioned as well ore are even discussed more than performance or even more. The Pinterest article focuses first on Elixir as a good language, performance is arguably secondary in the post. Before we ever talk about microseconds there is lots of talk such as:

> The language makes heavy use of pattern matching, a technique that prevents *value* errors which are much more common than *type* errors. It also has an innovative pipelining operator, which allows data to flow from one function to the next in a clear and easy to read fashion.

Then the famous microseconds drops in one paragraph, and then it immediately turns around and talks about code clarity again:

> We’ve also seen an improvement in code clarity. We’re converting our notifications system from Java to Elixir. The Java version used an Actor system and weighed in at around 10,000 lines of code. The new Elixir system has shrunk this to around 1000 lines.

The Bleacher Report article has performance in its headline and at its heart, but it also mentions different benefits of Elixir:

> The new language has led to cleaner code base and much less technical debt, according to Marx. It has also increased the speed of development(...)

So why do people rave about performance so much? Performance numbers are "objective", they are "rationale", they are impressive and people like those. It's an easy argument to make that bleacher report uses just 5 servers instead of 150 in the old ruby stack. That's a fact. It's easy to remember and easy to put into a headline. Discussing the advantages of immutable data structures, pattern matching and "let it crash" philosophy is much more subjective, personal and nuanced. Before we jump in, this blog post is general but some specific points might resonate the best with a ruby crowd as that is my main programming language/where I'm coming from. So, from other languages some of the points I'll make will be like "meh I already got this" while I might miss out obvious cool things both Ruby and Elixir have. Hence, after this lengthy introduction let's focus on something different - **what makes Elixir a language worth learning - how can it make day to day coding more productive in spite of performance?**

### Let's get some performance stuff out of the way first...

(The irony of starting the first section of a blog post decisively not about performance by discussing performance is not lost on me) First, I wanna touch the topic of performance again really quickly - does it really not matter? Can we seamlessly scale horizontally? Does performance not impact productivity? Well it certainly does, as remarked by Devon: https://twitter.com/devoncestes/status/885867267438891009 In a more general sense, if my runtime is already fast enough I don't need to bother with more complex algorithms and extra concepts. I can just leave it as is. **No extra engineering spent on "making it faster"** \- just on to the next. That's a good thing. Especially caching can be just _wonderful_ to debug. What about performance of big tasks? Like Data processing, or in the case of the company I'm working for solving a vehicle routing problem1? You can't just scale those up by throwing servers at it. You might be able to parallelize it, but that's not too easy in Ruby and in general is often a bigger engineering effort. And some languages make that easier as well, like Elixir's [flow](https://github.com/elixir-lang/flow). Vertical Scaling has its limits there. It works fine for serving more web requests, working on more background jobs but it gets more complicated when you have a big problem to solve that aren't easily parallelizable especially if they need to be done wihin a given time frame. Also, I might not be one of the cool docker + kubernetes kids, but if you tell me that there's no overhead to managing 125 servers versus 5 servers, I tend to not believe it. If simply because the chance of anyone of your servers failing at any time is much bigger just cause you got more of them. Well then, finally enough performance chatter in a post not about performance. **Let's look at the code and how it can make your life easier!** I swear I try to keep these sections short and sweet, although admittedly that's not exactly my strength (who would have guessed by now? ;) )

### Pattern Matching



Source: [https://gist.github.com/PragTob/39514ae5d48f4da8912f1392fd4cc5e7](https://gist.github.com/PragTob/39514ae5d48f4da8912f1392fd4cc5e7)

**File: `matching.exs`**
```elixir
defmodule Patterns do
  def greet(%{name: name, age: age}) do
    IO.puts "Hi there #{name}, what's up at #{age}?"
  end
  def greet(%{name: "José Valim"}) do
    IO.puts "Hi José, thanks for elixir! <3"
  end
  def greet(%{name: name}) do
    IO.puts "Hi there #{name}"
  end
  def greet(_) do
    IO.puts "Hi"
  end
end

Patterns.greet %{name: "Tobi", age: 27} # Hi there Tobi, what's up at 27?
Patterns.greet %{name: "José Valim"} # Hi José, thanks for elixir! <3
Patterns.greet %{name: "dear Reader"} # Hi there dear Reader
Patterns.greet ["Mop"] # Hi
```

 Pattern Matching is my single favorite feature. **If I could pick a single feature to be adopted in other programming languages it would be pattern matching.** I find myself writing pattern matching code in Ruby, then sighing... _"Ugh right I can't do this"._ **It changed the way I think.** Enough "this is soo great". With pattern matching you basically make assertions on the structure and can get values directly out of a deeply nested map and put their value into a variable. It runs deeper than that though. You also have method overloading and elixir will try to match the functions from top to bottom which means you can have different function definitions based on the structure of your input data. You can't just use it on maps though. You can use it on lists as well, so you can have a separate function clause for an empty or one element list which is really great for recursion and catching edge cases. One of the most fascinating uses I've seen was for parsing files as you can also use it for strings and so can [separate the data and different headers of mp3 files all in just a couple of lines of elixir:](http://benjamintan.io/blog/2014/06/10/elixir-bit-syntax-and-id3/) 

Source: [https://gist.github.com/PragTob/0b13314c9980da964409efc28d0be1d3](https://gist.github.com/PragTob/0b13314c9980da964409efc28d0be1d3)

**File: `mp3.ex`**
```elixir
mp3_byte_size = (byte_size(binary) - 128)
<< _ :: binary-size(mp3_byte_size), id3_tag :: binary >> = binary

<< "TAG",
    title   :: binary-size(30), 
    artist  :: binary-size(30), 
    album   :: binary-size(30), 
    year    :: binary-size(4), 
    comment :: binary-size(30), 
    _rest   :: binary >> = id3_tag
```



### Immutable Data Structures and Pure Functions

If you're unfamiliar with immutable data structures you might wonder how the hell one ever gets anything done? Well, you have to reassign values to the return values of functions if you wanna have any sort of change. You get pure functions, which means no side effects. The only thing that "happens" is the return value of the function. But, how does that help anyone? Well, it means you have all your dependencies and their effect right there - there is no state to hold on which execution could depend. **Everything that the function depends on is a parameter.** That makes for superior understandability, debugging experience and testing. Already months into my Elixir journey I noticed that I was seemingly much better at debugging library code than I was in Ruby. The reason, I believe, is the above. When I debug something in Ruby what a method does often depends on one or more instance variables. So, if yo wanna understand why that method "misbehaves" you gotta figure out which code sets those instance variables, which might depend on other instance variables being set and so on... Similarly a method might have the side effect of changing some instance variable. What is the effect in the end? You might never know. With pure functions I can see all the dependencies of a function at a glance, I can see what they return and how that new return value is used in further function calls. It reads more like a straight up book and less like an interconnected net where I might not know where to start or stop looking.

### The Pipeline Operator



Source: [https://gist.github.com/PragTob/488fb38850daad46eb1eb2a0c471bf78](https://gist.github.com/PragTob/488fb38850daad46eb1eb2a0c471bf78)

**File: `pipe.exs`**
```elixir
config
|> Benchee.init
|> Benchee.system
|> Benchee.benchmark("job", fn -> magic end)
|> Benchee.measure
|> Benchee.statistics
|> Benchee.Formatters.Console.output
|> Benchee.Formatters.HTML.output
```

 How does a simple operator make it into this list? Well, it's about the code that it leads you to. The pipeline operator passes the value of the previous expression into the next function as the first argument. That gives you a couple of guidelines. First, when determining the order of arguments thinking about which one is the main data structure and putting that one first gives you a new guideline. Secondly, it leads you to a design with a main data structure per function, which can turn out really nice. The above is an actual interface to my benchmarking library [benchee](https://github.com/PragTob/benchee). One of the design goals was to be "pipable" in elixir. This lead me to the design with a main _Suite_ data structure in which all the important information is stored. As a result, implementing formatters is super easy as they are just a function that takes the suite and they can pick the information to take into account. Moreover, each and every one of those steps is interchangeable and well suited for plugins. As long you provide the needed data for later processing steps there is nothing stopping you from just replacing a function in that pipe with your own. Lastly, the pipeline operator represents very well how I once learned to think about Functional Programming, it's a **transformation of inputs**. The pipeline operator perfectly mirrors this, we start with some data structure and through a series of transformations we get some other data structure. We start with a configuration and end up with a complete benchmarking suite. We start with a URL and some parameters which we transform into some HTML to send to the user.

### Railway Oriented Programming



Source: [https://gist.github.com/PragTob/5b708fda67d2e0bbcd63a513390430e5](https://gist.github.com/PragTob/5b708fda67d2e0bbcd63a513390430e5)

**File: `railway.ex`**
```elixir
with {:ok, record} <- validate_data(params),
     {:ok, record} <- validate_in_other_system(record),
     {:ok, record} <- Repo.insert(record) do
  {:ok, record}
else
  {:error, changeset} -> {:error, changeset}
end
```

 I'd love to ramble on about Railway Oriented Programming, [but there's already good blog posts about that out there](http://www.zohaib.me/railway-programming-pattern-in-elixir/). Basically, instead of always checking if an error had already occurred earlier we can just branch out to the error track at any point. It doesn't seem all that magical until you use it for the first time. I remember suggesting using it to a colleague on a pull request (without ever using it before) and my colleague came back like "It's amazing"! It's been a pattern in the application ever since. It goes a bit like this:

  1. Check the basic validity of data that we have (all fields present/sensible data)
  2. Validate that data with another system (business logic rules in some external service)
  3. Insert record into database

Anyone of those steps could fail, and if it fails executing the other steps makes no sense. So, as soon as a function doesn't return `{:ok, something}` we error out to the error track and otherwise we stay on the happy track.

### Explicit Code

[The Python folks were right all along.](https://zen-of-python.info/) Implicit code feels like magic. It just works without writing any code. My controller instance variables are just present in the view? The name of my view is automatically inferred I don't have to write anything? Such magic, many wow. [Phoenix](http://www.phoenixframework.org/), the most popular elixir web framework, takes another approach. You have to specify a template (which is like a Rails view) by name and explicitly pass parameters to it: 

Source: [https://gist.github.com/PragTob/3fa527b57eb1123ddf139ab22e509417](https://gist.github.com/PragTob/3fa527b57eb1123ddf139ab22e509417)

**File: `phoenix_controller_explicit.ex`**
```elixir
def new(conn, _params) do
  changeset = User.new_changeset(%User{})
  render conn, "new.html", changeset: changeset
end
```

 No magic. What happens is right there, you can see it. No accidentally making something accessible to views (or partials) anymore! You know what else is there? The connection and the parameters so we can make use of them, and pattern match on them. Another place where the elixir eco system is more explicit is when loading relations of a record: 

Source: [https://gist.github.com/PragTob/e541d0e742d6464ff2ec2e6ab7eda52c](https://gist.github.com/PragTob/e541d0e742d6464ff2ec2e6ab7eda52c)

**File: `ecto_preloading.ex`**
```elixir
iex(13)> user = Repo.get_by(User, name: "Homer")
iex(14)> user.videos
#Ecto.Association.NotLoaded<association :videos is not loaded>
iex(17)> user = Repo.preload(user, :videos)
iex(18)> user.videos
# all the videos
```

 This is [ecto](https://github.com/elixir-ecto/ecto), the "database access layer" in the elixir world. As you see, we have to explicitly preload associations we want to use. Seems awful bothersome, doesn't it? **I love it!** No more [N+1 queries](https://encrypted.google.com/search?hl=en&q=rails%20n%20%2B%201%20query), as Rails loads things magically for me. Also, I get more control. I know about the db queries my application fires against the database. Just the other day I fixed a severe performance degradation as our app was loading countless records from the database and instantiated them for what should have been a simple count query. Long story short, it was a presenter object so `.association` loaded all the objects, put them in presenters and then let my `.size` be executed on that. I would have never explicitly preloaded that data and hence found out much earlier that something is wrong with this. Speaking of explicitness and ecto...

### Ecto Changesets



Source: [https://gist.github.com/PragTob/797c4e49489450e2d5d391607f0c70b6](https://gist.github.com/PragTob/797c4e49489450e2d5d391607f0c70b6)

**File: `changeset.ex`**
```elixir
def new_changeset(model, params \\ %{}) do
  model
  |> cast(params, ~w(name username))
  |> validate_required(~w(name username))
  |> unique_constraint(:username)
  |> validate_length(:username, min: 1, max: 20)
end

def registration_changeset(model, params) do
  model
  |> new_changeset(params)
  |> cast(params, ~w(password))
  |> validate_required(~w(password))
  |> validate_length(:password, min: 6, max: 100)
  |> put_pass_hash()
end
```

 Callbacks and validations are my nemesis. The problem with them is the topic for another topic entirely but in short, validations and callbacks are executed all the time (before save, validation, create, whatever) but lots of them are just added for one feature that is maybe used in 2 places. Think about the user password. Validating it and hashing/salting it is only ever relevant when a user registers or changes the password. But that code sits there and is executed in a not exactly trivial to determine order. Sometimes that gets in the way of new features or tests so you start to throw a bunch of ifs at it. [Ecto Changesets](https://hexdocs.pm/ecto/Ecto.Changeset.html) were one of the strangest things for me to get used to coming to Elixir. Basically they just encapsulate a change operation, saying which parameters can take part, what should be validated and other code to execute. You can also easily combine changesets, in the code above the `registration_changeset` uses the `new_changeset` and adds just password functionality on top. I only deal with password stuff when I **explicitly** want to. I know which parameters were allowed to go in/change so I just need to validate those. **I know exactly when what step happens** so it's easy to debug and understand. Beautiful.

### Optional Type-Checking



Source: [https://gist.github.com/PragTob/3d4f282861a15f979451b3833027f4f2](https://gist.github.com/PragTob/3d4f282861a15f979451b3833027f4f2)

**File: `type_specs.ex`**
```elixir
  @type job_name :: String.t | atom
  
  @spec benchmark(Suite.t, job_name, fun, module) :: Suite.t
  def benchmark(suite = %Suite{scenarios: scenarios}, job_name, function, printer \\ Printer) do
    #...
  end
```

 Want to try typing but not all the time? Elixir has got something for you! It's cool, but not enough space here to explain it, [dialyxir](https://github.com/jeremyjh/dialyxir) makes the [dialyzer](http://erlang.org/doc/man/dialyzer.html) tool quite usable and it also goes beyond "just" type checking and includes other static analysis features as well. Still, in case you don't like types it's optional.

### Parallelism

_"Wait, you swore this was it about performance! This is outrageous!"_ Relax. While Parallelism can be used for better performance it's not the only thing. What's great about parallelism in elixir/the Erlang VM in general is how low cost and seamless it is. Spawning a new _process_ (not like an Operating System process, they are more like actors) is super easy and has a very low overhead, unlike starting a new thread. You can have millions of them on one machine, no problem. Moreover thanks to our immutability guarantees and every process being isolated you don't have to worry about processes messing with each other. So, first of all if I want to geocode the pick up and drop off address in parallel I can just do that with a bit of [Task.async and Task.await](https://hexdocs.pm/elixir/Task.html). I'd never just trust whatever ruby gems I use for geocoding to be threadsafe due to global et. al. How does this help? Well, I have something that is easily parallelizable and I can just do that. Benchee generates statistics for different scenarios in parallel just because I can easily do so. That's nice, because for lots of samples it might actually take a couple of seconds per scenario. Another point is that there's less need for background workers. Let's take web sockets as an example. To the best of my knowledge it is recommended to load off all bigger tasks in the communication to a background workers in an evented architecture as we'd block our thread/operating system process from handling other events. In Phoenix every connection already runs in its own elixir process which means they are already executed in parallel and doing some more work in one won't block the others. This ultimately makes applications easier as you don't have to deal with background workers, off loading work etc.

### OTP

Defining what OTP really is, is hard. It's somewhat a set of tools for concurrent programming and it includes everything from an in memory database to the Dialyzer tool mentioned earlier. It is probably most notorious for its "behaviours" like supervisors that help you build concurrent and distributed systems in the famous "Let it crash! (and restart it in a known good state maybe)" philosophy. There's big books written about this so I'm not gonna try to explain it. Just so much, years of experience about highly available systems are in here. There is so much to learn here and change how you see programming. It might be daunting, but don't worry. People built some nice abstractions that are better to use and often it's the job of a library or a framework to set these up. Phoenix and ecto do this for you (web requests/database connections respectively). I'll out myself right now: I've never written a [Supervisor](https://hexdocs.pm/elixir/Supervisor.html) or a [GenServer](https://hexdocs.pm/elixir/GenServer.html) for production purposes. I used abstractions or relied on what my framework brought with it. If this has gotten you interested I warmly recommend ["The Little Elixir & OTP Guidebook"](https://www.manning.com/books/the-little-elixir-and-otp-guidebook). It walks you through building a complete worker pool application from simple to a more complex fully featured version.

### Doctests



Source: [https://gist.github.com/PragTob/7ace9f03f09ec1f8e1397beef3cbd89d](https://gist.github.com/PragTob/7ace9f03f09ec1f8e1397beef3cbd89d)

**File: `doctest.ex`**
```elixir
  @doc """
  ## Examples

      iex> {:ok, pid} = Agent.start_link(fn -> 42 end)
      iex> Agent.get_and_update(pid, fn(state) -> {state, state + 1} end)
      42
      iex> Agent.get(pid, fn(state) -> state end)
      43
  """
```

 Imo the most underrated feature of elixir. Doc tests allow you to write iex example sessions in the documentation of a method. These will be executed during test runs and check if they still return the same values/still pass. They are also part of the awesome generated documentation. No more out of date/slightly wrong code samples in the documentation! I have entire modules that only rely on their doctests, which is pretty awesome if you ask me. Also, contributing doc tests to libraries is a pretty great way to provide both documentation and tests. E.g. once upon a time I wanted to learn about the Agent module, but it didn't click right away, so I made a [PR to elixir with some nice doctests to help future generations](https://github.com/elixir-lang/elixir/pull/5583).

### A good language to learn

In the end, elixir is a good language to learn. It contains many great concepts that can make your coding lives easier and more enjoyable and all of that lives in a nice and accessible syntax. Even if you can't use it at work straight away, learning these concepts will influence and improve your code. I experienced the same when I learned and read a couple of books about Clojure, I never wrote it professionally but it improved my Ruby code. You might ask "Should we all go and write Elixir now?". No. There are many great languages and there are no silver bullets. The eco system is still growing for instance. I'm also not a fan of rewriting all applications. Start small. See if you like it and if it works for you. Lastly, if this has peaked your interest I have a whole talk up that focuses on the great explicit features of elixir and explains them in more detail: ["Elixir & Phoenix - fast, concurrent and explicit"](https://pragtob.wordpress.com/2016/11/24/video-elixir-phoenix-fast-concurrent-and-explicit/) edit1: Clarified that the bleacher report blog post is mostly about performance with little else edit2: Fixed that you gotta specify the template by name, not the view [1] It's sort of like Traveling Salesman, put together with Knapsack and then you also need to decide what goes where. In short: a very hard problem to solve. ↑
