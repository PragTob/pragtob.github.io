---
layout: post
title: You may not need GenServers and Supervision Trees
description: None
date: 2019-04-24 17:26:23 -0000
last_modified_at: 2019-04-25 06:46:51 -0000
publish: true
pin: false
categories:
- Elixir
- Uncategorized
tags:
- elixr
- Erlang
- GenServer
- process
- supervision tree
---
The thought that people seem to think of GenServers and supervision trees in the elixir/erlang world as too essential deterring people from using these languages has been brewing in my mind for quite some time. In fact I have [written about it before in Elixir Forum](https://elixirforum.com/t/you-may-not-need-genservers-and-supervision-trees/12947). This is a summary and extended version of that (including some choice replies) to give it more visibility. It feels like we talk so much about GenServers etc. that people who come to Elixir feel like they _need to_ use them or they are not “ _really_ ” using Elixir. I fear that it keeps people out of the elixir community because all this just seems so complicated. However, you can write great applications without ever writing them _yourself_. I emphasize _yourself_ because a lot of the libraries you'll use (phoenix, ecto etc.) already have their supervision trees and their processes - you're standing on the shoulders of giants truly. Still, I hear people say something to the tune of “We’re still using this like Rails - we should use GenServers” - without any need or concrete reasoning. Having something as simple as rails (in parts, let's not derail about rails here) but at the same time fully parallel and more efficient is a huge boon to my mind. I feel like **hardly anyone ever highlights this**. I've been programming elixir since ~2015. I've never written a production GenServer or supervision tree (and I have multiple applications in production and multiple published libraries). I simply didn't encounter these problems or the eco system took care of it for me. Still I felt _somewhat inadequate_ because of it, as everyone seem to already be talking about these. Which is also understandable, they are unique, they solve hard problems - there's lots to learn and share knowledge. I've had this thought that often you don't really need GenServers and supervision trees in my head for a long time (~2016) but was too afraid to voice it. Maybe I just don't understand it enough? Maybe I need to learn more about them? Everyone always talks about them, I'm sure enlightenment will come to me some time soon! I finally nervously wrote the aforementioned [Elixir Forum thread](https://elixirforum.com/t/you-may-not-need-genservers-and-supervision-trees/12947) in 2018. My nervousness went down a notch after José Valim, creator of elixir somewhat hyper productive and omnipresent, liked the post within ~15 minutes of its creation. Also most people were really supportive, hence I'm happy to share this more openly, sorry for the delay a lot had been going on in my life ;) Be mindful that I don't say you _don't need_ them - I'm merely saying that you can build significant and great elixir applications without writing your own GenServers and supervision trees. It's of course still a topic worth learning.

## GenServers? Supervision Trees? Processes?

If you've ever watched a talk about elixir or erlang you're likely to have heard about these. They're one of the _"killer features"_ of erlang and elixr. They give you that famed parallelism backed by the actor model, reliability and that whole _"Let it crash! (and restart in a known good state)"._ Both GenServer and Supervisor are [behaviours](https://elixir-lang.org/getting-started/typespecs-and-behaviours.html) showing a process "how to behave" and they both ship with Erlang/OTP.

## So what's the problem with Genservers and Supervision Trees?

GenServers, supervisors etc. are great technologies that help you solve problems. They’re one of the things that is most special & unique about elixir & erlang. As a result lots of conference talks, blog posts etc. focus on them and it seems everyone wants to use them. Through the big focus on them in the community it sometimes feels like you can't be a _"real"_ elixir/erlang programmer until you've used and mastered them. However, do you **need them all the time?** At least while using a framework (like Phoenix), chances are **you don’t**. The hidden detail of course is that **you are using GenServers and friends without even knowing it** \- Phoenix runs every request and every channel[1] in their own processes. [Ecto](https://github.com/elixir-ecto/ecto) has its own pool for your database connections. It’s already parallelized and you don’t need to take care of it. That’s the beauty of it. What I’m saying is that in the standard situation the **eco system takes care of you**. Building a relatively standard CRUD web application with Phoenix? No need. Just using channels for a chat like applications in Phoenix? You’re good. Of course, you don't need them until you really do. I like how [Jordan put it](https://elixirforum.com/t/you-may-not-need-genservers-and-supervision-trees/12947/3?u=pragtob):

> I agree that you, 99% of the time you do not need to use anything otp related but when you are in that 1% its really a game changer that makes elixir as great as it is.

## The Bad and the Ugly

It's not like using GenServers and friends makes everything instantly better. Quite the opposite, **it can make your code both harder to understand and slower**. Sometimes the introduction of processes just complicates the code, what could have been a simple interaction is now obfuscated through a bunch of GenServer calls. Through trying to use these concepts you can also essentially grind your application to a halt performance wise. To take an example from the excellent _[Adopting Elixir](https://pragprog.com/book/tvmelixir/adopting-elixir),_ which also covers this topic:

> A new developer team started building their Phoenix applications. They had always heard GenServers could be treated like microservices but even tinier. This “wisdom” led them to push all of their database access control to GenServers . (…) performance was abysmal. Under high-enough load, some pages took 3 seconds to render because they built a bottleneck where none existed. They defeated Ecto connection pools because all access happened through a single process. In essence, they made it easy to create global, mutable variables in Elixir. They essentially crippled the single biggest advantage of functional languages, for no gain whatsoever.

## When to GenServer?

[Adopting Elixir](https://pragprog.com/book/tvmelixir/adopting-elixir) again provides some guidance as to what to best use processes for:

> * Model state accessed by multiple processes.
> * Run multiple tasks concurrently.
> * Gracefully handle clean startup and exit concerns.
> * Communicate between servers.
>

They especially highlight that GenServers aren't to be used for code organization. Robert Virding (one of the creators of Erlang) also [chimed in](https://elixirforum.com/t/you-may-not-need-genservers-and-supervision-trees/12947/17?u=pragtob) and his response is so measured that I want to quote it in full:

> I think the most important thing to understand and to use properly is the **concurrency** in the problem/solution/system. Using GenServers and other behaviours is just one way of doing the concurrency but it is not the only way. They are tools and like all tools they need to be used in the right way. The problem is to get the right level of concurrency which suites your problem and your solution to that problem. Too much concurrency means you will be doing excess work to no real gain, and too little concurrency means you will be making your system too sequential. Now, as has been pointed out, many packages like Phoenix already provide a pretty decent level of concurrency which is suitable for many types of applications, at least the ones they were intended for. They will do this automatically so you don’t have to think about it in most cases, but it is still there. Understanding that is necessary so you can work out how much concurrency you need to explicitly add if any. Unfortunately because it is all managed for you “invisibly underneath” many don’t realise that is it there.

While people agree in general, there are also some that say that most systems can benefit from a GenServer and supervision tree. As [Saša Jurić points out](https://elixirforum.com/t/you-may-not-need-genservers-and-supervision-trees/12947/21?u=pragtob):

> With a lot of hand waving, I’d say that GenServers are OTPs built-in building block for building responsive services, Tasks are the same for non-responsive ones, and supervision tree is the built-in service manager like systemd or upstart. In the past 10+ years of my backend side experience, I’ve worked on small to medium systems, and all of them needed all of these technical approaches.

He also has a fairly extensive blog post on the topic of when to reach for these tools and when not to: [To spawn, or not to spawn](https://www.theerlangelist.com/article/spawn_or_not). In the end, I'm also not an expert on GenServers and Supervision Trees - as I said I never wrote a production one. Still learning and still growing. I think knowing them well gives you a good basis to make informed decisions on when to use them and when not to.

## Abstractions

But you came to Elixir for the parallelism! So you need GenServers right? No. Elixir core and the community have been very good at providing easy to use solutions to write fully parallel programs without having to write your own GenServers and supervision trees. There are [gen_stage](https://github.com/elixir-lang/gen_stage), [flow](https://github.com/plataformatec/flow) and [broadway](https://github.com/plataformatec/broadway), but somewhat more importantly a couple of these are built-ins like [Task](https://hexdocs.pm/elixir/Task.html) (do something in parallel easily) and [Agent](https://hexdocs.pm/elixir/Agent.html#content) (share state through a process). Want to geocode the pick up and drop off addresses of a shipment in parallel and then wait until both have finished? Say no more: https://gist.github.com/PragTob/36aae079055dfcc2af523f8644f0b018

## Learning

Although I'm saying you don't _need it_ and can write applications without it just fine, it's a fascinating and interesting topic that can make you a better programmer without ever writing your own supervision trees even. And as I said, education is key to know when to reach for them and when not to. So here are a couple of books I can recommend to up your knowledge:

* [The Little Elixir & OTP Guide Book](https://www.manning.com/books/the-little-elixir-and-otp-guidebook) \- my personal favorite, in it the author takes you through writing implementations of [poolboy](https://hex.pm/packages/poolboy) starting with a simple one, showing what shortcomings it has and then extending on it building a complicated supervision tree but you get the reasoning to go along with it to see for what feature what level of complexity is needed. A fascinating read for me.
* [Adopting Elixir](https://pragprog.com/book/tvmelixir/adopting-elixir) \- covers many aspects as mentioned before but is especially good at what to use these concepts for and what not to use them for (and is an interesting read overall if you consider to get your company into elixir)
* [Elixir in Action](https://www.manning.com/books/elixir-in-action-second-edition) \- Saša Jurić is one of the most knowledgeable people I can think of about this topic, hence I quoted him before, and a significant part of the book is dedicated to it too. A second edition came out earlier this year so it's also all up to date.
* [Functional Web Development with Elixir, OTP, and Phoenix](https://pragprog.com/book/lhelph/functional-web-development-with-elixir-otp-and-phoenix) \- build a simple game, first with simple functions, then develop a GenServer interface to it with some supervisors and then wire it all up in a Phoenix App - good introduction and especially good at showing some solid debugging work.
* [Programming Phoenix](https://pragprog.com/book/phoenix14/programming-phoenix-1-4) \- introductory book I wish everyone writing a phoenix application read first, as it also covers why things are done in a certain way and it's by the authors of the framework which gives a unique perspective. It also has the aforementioned information of what is already parallelized etc. It also includes a pretty cool use case for a supervised GenServer (getting suggestions from an external service and ranking them).
* [Designing Elixir Systems with OTP](https://pragprog.com/book/jgotp/designing-elixir-systems-with-otp) \- this is shaping up to be a great resource on GenServers, Supervision Trees and OTP in general. I haven't read it yet, but James, Bruce and PragProg have all my trust plus I read some early praise already.

## Final Thoughts

Well, **you don't need GenServers and supervision trees to start with writing elixir applications!** Go out there, write an application, play with it, have fun, call yourself an elixir programmer (because you _are_!). Still, learn about OTP to expand your mind and to know where to look when you encounter a problem where a supervision tree could help you. When discussing this in Elixir Forum, [Dimitar also came up with a good thought](https://elixirforum.com/t/you-may-not-need-genservers-and-supervision-trees/12947/27?u=pragtob): Maybe the OTP is what pulls people in and helps them discover all those other nice things?

> I came for OTP. I stayed for the functional programming.

As a community, I think we should make it clearer that you _don’t have to use GenServers_ and that doing so might _actually be harmful_. Of course all those conference talks about how to use them, distributed systems etc. are very cool but every now and then give me a talk about how a business succeeded by writing a fairly standard Phoenix application. _Don't over complicate things_. I’m not saying you shouldn’t learn about GenServers. You should. But know when to use them and when not to. Lastly, if you disagree I want you to scream at me and teach me the error of my ways ![:smiley:](https://elixirforum.com/images/emoji/apple/smiley.png?v=5)   [1]Technically the web server of phoenix cowboy doesn't use GenServers and supervision trees for normal http request handling but their own thing, they have a similar functionality though so it still holds true that you don't need to roll your own. Thanks to [Hubert for pointing that out](https://twitter.com/hubertlepicki/status/1121114981561438208). edit1: Correctly mention new edition of Elixir in Action, be more specific about Cowboy Processes and include a thought in closing paragraph. Thanks go to Saša, Hubert and Dimitar.
