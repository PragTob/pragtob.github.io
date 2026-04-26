---
layout: post
permalink: https://pragtob.wordpress.com/2017/11/14/are-comments-a-code-smell-yes-no-it-depends/
title: Are comments a code smell? Yes! No? It Depends.
description: None
date: 2017-11-14 16:00:19 -0000
last_modified_at: 2017-11-14 21:40:50 -0000
publish: true
pin: false
categories:
- Software Engineering
tags:
- code
- code smell
- comments
- it depends
- readable
- refactoring
- software engineering
---
Most people are either firmly on the "Yes!" or the "No!" side when it comes to discussing comments and their status as a code smell. But, as with most question worth asking the correct answer rather is an **"It depends"**. I got to re-examine this topic lately triggered by a tweet and a discussion with Devon: https://twitter.com/PragTob/status/919886284440694784 So, let's start unwrapping these layers, shall we?

## Important distinction: Comments vs. Documentation

One of the first points on the list is understanding what a comment is and what it is not. For me documentation isn't a comment, in most languages (unfortunately) documentation happens to be represented as a comment. Thankfully some languages, such as [elixir](http://elixir-lang.github.io/getting-started/module-attributes.html#as-annotations), [Clojure](https://clojure.org/reference/special_forms) and [Rust](https://doc.rust-lang.org/book/first-edition/documentation.html), have a separate construct for documentation to make this obvious and facilitate working with documentation. I don't think _everything_ should be documented. However, libraries definitely need documentation (if you want people using them that is). I've also grown increasingly fond of documentation in application code, especially as projects grow. At Liefery core modules have a top level "module" comment describing the business context, language, important collaborators etc. It has proven invaluable. One of my favorites is the description of the shipment state machine that for each state shortly summarizes what it means - keeping all those in your head has proven quite difficult. Plus, it's a gift for new developers getting into the code base. Of course documentation still suffers one of the major drawback of comments - it can become outdated. Much less so if documentation rather provides context than describing in detail what happens. So, documentation for me isn't a comment. Next up - what's this code smell thing?

## What's a Code Smell?

In short a code smell is an indication that something _could_ be wrong with this code. Or to let the creators of the term, Kent Beck (whose idea the term was) and Martin Fowler, tell it in [Refactoring](https://martinfowler.com/books/refactoring.html):

> (...) describing the "when" of refactoring in terms of smells. (...) we have learned to look for certain structures in the code that suggest (sometimes they scream for) the possibility of refactoring.

Does this description fit comments? Well, comments made the "original" list of code smells, with the following reasoning:

> (...) comments often are used as a deodorant. It's surprising how often you look at thickly commented code and notice that the comments are there because the code is bad.

They go on to explain what should be done instead of comments:

> When you feel the need to write a comment, first try to refactor the code so that any comment becomes superfluous.

That is exactly in line with my view of code comments. There is so much more that you can do to make your code more readable instead of resorting to a comment. **Comments should be a last resort.** To further explore this, let's take a look at one of my favorite distinctions when it comes to "good" comments versus "bad" comments.

## WHAT versus WHY comments

I like to think of comments in 2 categories:

* **WHAT** comments describe _what_ the code does, these can be high level but sometimes they also tell you every little thing the code does ("iterates over, then... uses result to")
* **WHY** comments clarify _why_ some code is like it is giving you a peek into the past why a decision was made

Let's start with the **WHAT** \- what comments can almost always be replaced by more expressive code. Most of this has to do with proper naming and concepts, which is why it isn't uncommon for me to spend an extended period of time on these. Hell, (coincidentally) [Devon and I even spent hours on defining "Scenarios" in benchee.](https://pragtob.wordpress.com/2017/10/25/released-benchee-0-10-html-csv-and-json-plugins/) Variables, methods, classes, modules... all of these communicate through their name. So spending a good time naming them helps a lot. Often it is also the right call to extract one of these to keep the line count small and manageable while **naming the concept you just extracted** to help the understanding of the overall code. Let's take a look at one of my favorite examples: https://gist.github.com/pragtobgists/052de512b4a9dee1503924b3870fd944 Let this stand in for every long method you ever came across where the method body was broken into sections by comments. Extract 3 methods, name them somewhat like the comments. Enjoy shorter methods, meaningful names, concepts and reusability. I've even seen [people advocating for this style of long methods with comments](https://dev.to/bugfenderapp/the-importance-of-quality-comments). Easy to say, I'm not a fan. The article says _"The more complex the code, the more comments it_ _should have."_ and my colleague [Tiago](https://twitter.com/tiagotex) probably responded best to that:

> You should make the code less complex not add more comments.

Another example I wish I made up, but it's real (I only ported it from JavaScript to Ruby): https://gist.github.com/pragtobgists/399bfd4369f514a44bb091e95b3444c5 As a first step just rename your parameters to whatever understandable name was commented above (also how does _l_ translate to _time per step_?). Afterwards, look for a bigger concept you might be missing and aggregate the needed data into it so you trim the number of parameters down. All in all, a _WHAT_ style comment to my mind is a declaration of _defeat_ \- it's an "I tried everything but I can't make this code be readable by itself" You can be sure, if I get there I first consult a colleague about it and if we can't come up with something I'll isolate the complexity and then be sad about my defeat. With all of that about what comments, how about **WHY** comments? They can help us with things that can hardly be expressed in code. Let's take a little example from the great [shoes](https://github.com/shoes/shoes4) project: https://gist.github.com/pragtobgists/0d24edc25f5e3892d586ea3a05e173b1 While the _puts_ statements communicates some of it, it is important to emphasize how dangerous not rescuing here is. The comment also helps establish context and points to where one could find more information about this. This is an excellent use case for a comment and thankfully Kent Beck and Martin Fowler agree (again from the Refactoring book):

> A comment is a good place to say why you did something. This kind of information helps future modifiers, especially forgetful ones.

There is an argument to be made that such information should be kept in the version control system and not in a comment. It is true: the commit message should definitely reflect this, ideally with an easy to produce link both to the ticket and pull request. However, a commit message alone is not enough to my mind. Tracking down a commit that introduced a change in an older code base can be quite hard (ever tried changing all strings from single quotes to double quotes? ;) ) and you can't expect everyone to always look at the history of every line of code they change. A comment acts a warning sign in places like these. In short: **WHY** comments "**yay** "! **WHAT** comments "**nay** "!

## Context matters

Before we get to the final "verdict" there's one more aspect I'd like to examine: the context of your application. That context might greatly influence the need for comments. Another CRUD application like the ones you built before? Probably doesn't need many comments. That new machine learning micro service written in Python and deployed with docker while no one in your team has done any of these things before? Yup, that probably needs a couple of more comments. New business domain, new framework, new language, something out of your comfort zone, experience level of developers - all of these can justify more comments to be written. Those can give context, link to resources, WHAT comments describing on a high level what's going on and so on. For instance, our route planning code has quite a few more comments explaining the used algorithms and data structures on a high level than the rest of the code base.

## Yadda yadda - are comments a code smell or not?

As already established - it's not as black and white as some people make it seem. To get back to the original twitter conversation that started all this: https://twitter.com/devoncestes/status/919897183834574848 For a shorter answer, I think Robert Martin also puts it quite well and succinct in [Clean Code](https://www.goodreads.com/book/show/3735293-clean-code):

> The proper use of comments is to compensate for our failure to express ourself in code.

What about me? Well, if you asked me "Are comments a code smell?" on the street the answer would probably be _"Yes"_ , the better answer would be _"It depends."_ and the good answer short of this blog post would be something along the lines of:

> There's a difference between documentation, which is often good, and comments. WHY comments highlighting reasoning are valuable. WHAT comments explaining the code itself can often be replaced by more expressive code. Only when I admit defeat will I write a WHAT comment.

(these days this even fits in a single tweet ;) ) edit: As friends happily [pointed](https://twitter.com/plexus/status/930512058508021760) [out](https://twitter.com/Argorak/status/930512391355453440), documentation is also a construct different from code comments in clojure and rust. Added that in.
