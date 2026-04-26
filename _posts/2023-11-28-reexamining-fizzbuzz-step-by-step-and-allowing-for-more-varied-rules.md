---
layout: post
title: Reexamining FizzBuzz Step by Step - and allowing for more varied rules
description: None
date: 2023-11-28 15:17:46 -0000
last_modified_at: 2024-04-30 12:22:21 -0000
publish: true
pin: false
image:
  path: https://pragtob.wordpress.com/wp-content/uploads/2023/11/screenshot-from-2023-11-28-16-16-34.png
categories:
- Beginner
- Ruby
- Software Engineering
tags:
- coding challenge
- exercise
- FizzBuzz
- Programming
- ruby
- solution
---
Last week I found myself at my old RailsGirls/code curious project group the [rubycorns](https://rubycorns.club) coaching a beginner through the [FizzBuzz](https://wiki.c2.com/?FizzBuzzTest) coding challenge. It was a lot of fun and I found myself itching to implement it again myself as I came up with some ideas about a nice solution given a requirement for arbitrary or changing rules to the game.

I've also been working on blog posts helping people interview processes, the next of which will be about Technical Challenges/Code challenges (due to be published tomorrow! edit: [Published now!](https://pragtob.wordpress.com/2023/11/29/interviewing-tips-technical-challenges-coding-more/)). This is a little extension for that blog post, as an example of going through and improving a coding challenge.

To be clear, I don’t endorse FizzBuzz as a coding challenge. In my opinion something closer to your domain is much more valuable. However, it is (probably) **the most well known coding challenge** so I wanted to examine it a bit. It is also **deceptively simple** , and so deserves some consideration.

So, in this blog post let's start with what FizzBuzz is and then let's **iteratively go through writing and improving it.** Towards the end we'll also talk about **possible extensions** of the task and how to deal with them. The examples here will be in Ruby, but are easy to transfer to any other programming language. If you're only here for the code, you can check out the [repo](https://github.com/PragTob/fizz_buzz).

## The FizzBuzz Challenge

The challenge, inspired by a children's game, originated from the blog post ["Using FizzBuzz to Find Developers who Grok Coding"](https://imranontech.com/2007/01/24/using-fizzbuzz-to-find-developers-who-grok-coding/) by Imran Ghory back in 2007 - the intent being to come up with a question as simple as possible to check if people can write code.

The problem goes as follows:

> Write a program that prints the numbers from 1 to 100. But for multiples of three print “Fizz” instead of the number and for the multiples of five print “Buzz”. For numbers which are multiples of both three and five print “FizzBuzz”.

Simple enough, right? Well, I think it actually checks for some interesting properties and is a good basis for a conversation. To get started, let's check out a basic solution.

## Basic Solution

https://gist.github.com/PragTob/5c5367c99c1f4dc628a25292e40f140f

That one does the job perfectly fine. It prints out the numbers as requested. It also helps to illustrate some of the difficulties with the challenge:

First off, **printing out the results** is interesting as it is notoriously hard to test (while possible given the correct helpers). It should push a good programmer towards separating the output concern from the business logic concern. So, a good solution should usually feature a separate function `fizz_buzz(number)` that given any number `number` either returns the number itself or `”FizzBuzz”` etc. according to the rules. This is wonderfully easy to test, but many struggle initially to make that separation of concerns. We'll get to that in a second.

What I don’t like about the challenge is that it requires knowledge about the [modulo](https://en.wikipedia.org/wiki/Modulo) operator, as it isn’t commonly used, but you need it to check whether a number is actually divisible. Anyhow, there will be a lot of code like: `number % 3 == 0`. To avoid repetition and instead speak in the language of the domain**it’s much better to extract this functionality into a function`divisible_by?(number, divisor)`**. Makes the code read nicer and removes inherent duplication.

Speaking of the division, the order in which you check the conditions (namely, being divisible by 3 and 5, or 15, before the individual checks) is crucial for the program to work and I’ve seen more than one senior engineer stumble upon this.

With that in mind, let's improve the challenge!

## We need to go back

First off, while the previous solution is "perfectly" fine, I'd probably never write it as it's hard to test - it's just a script to run and everything is printed to the console. And since I'm a TDD kind of person, that won't do! I usually start, as teased before, by just implementing a function `fizz_buzz(number)` \- that's the core of the business logic. The iteration and printing out are just secondary aspects to me, so let's start there:

https://gist.github.com/PragTob/8bd3d8aad74c702ce514b8df76ae6b33

Much better, and it's tested! You may think that the test generation from the hash is overdone, but I love how easy it is to adjust and modify test cases. No ceremony, I just add an input and an expected output. Also, yes - tests. When solving a coding challenge tests should usually be a part of it unless you're explicitly told not to. Testing is an integral skill after all.

Ok, let's make it a full solution.

## Full FizzBuzz

Honestly, all that is required to turn it into a full FizzBuzz solution is a simple loop and output. What is a bit fancier is the integration test I added to go along with it:

https://gist.github.com/PragTob/66a7ab89786bf8b265d77226078f873d

Simple isn't it? You may argue that the integration test is too much, but when I can write an integration test as easy as this I prefer to do it. When I write code that generates files, like PAIN XML, I also love to have a full test that makes sure when given the same inputs we get the same outputs. This has the helpful side effect that even minor changes become very apparent in the pull request diff.

Anyhow, the other thing that we see is that our **separation of concerns** with the `fizz_buzz(number)` function pushed us to here is that there is **only a single`puts` statement**. We separated the output concern from the business logic. Should we want to change the output - perhaps it should be uploaded to an SFTP sever - then there is a single point for us to adjust that in. Of course we could also use [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection) to make the method of delivery easier to change, but without a hint that we might need it this is likely overdone. Especially since I'd still want to keep the full integration test we just wrote, programs have a tendency to break in the most unanticipated ways.

## Keeping up with the Domain

The other thing I complained about initially was the usage of the modulo operator. Truth be told, I only wrote the initial version like this for demonstration purposes - that one has to go. I don't want to think about what "modulo a number equals 0" means. Whether or not something is divisible is something I understand and can work with. It also removes a fair bit of duplication:

https://gist.github.com/PragTob/f31482c9b0d35158c6933253adc524b4

Much better! There is a small optimization here, where we only check the divisibility twice instead of 4 times. It doesn't fully matter, but when I see the exact same code being run twice in a method and I can remove it without impacting readability I love to do it.

I consider this a good solution. However, now is where the fun of many coding challenges starts - **what extension points are there?**

## Extension Points

Many coding challenges have potential extension points baked in. Some extra features, or, what I almost prefer dealing with, uncertainty and how that might affect software design.

How certain are we that we need the first 100 numbers? How certain are we that we want to print it out on the console? Is there a possibility that we’ll get a 3rd number like 7 and how would that work? How certain are we that it’s the numbers 3, 5 and the words Fizz and Buzz?

**Depending on the answers to these question you could go, adjust the challenge to make these easier to change.** And with answers I don't mean you making them up, but in case of a live coding challenge you talking to your interviewers to see what they think. A common case for instance would be that the numbers and strings may change while we’re certain it will be 2 numbers and 2 distinct strings - "product is still trying to figure out the exact numbers and text and they might change in the future as we're experimenting in the space".

Let's run with that for now - we think it will always be 2 numbers but we're not sure what 2 numbers and we're also not sure about Fizz and Buzz. What do we do now?

## Going Constants

One of the easiest solutions to this is to extract the relevant values to constants or even into a config.

https://gist.github.com/PragTob/0c5c01e55b14dc1cd96a62af61fb409b

Right, so that got a lot **longer** and frankly also a bit **more confusing**. However, it is now immediately apparent where to change the values. That said, we also kept the "FizzBuzz" naming for the constants which may get extra confusing if we changed the text to something like "Zazz". It's always a **tradeoff** , the **previous version was definitely more readable**. We did get rid of "Magic numbers" and "Magic Strings". Sadly, due to the nature of the challenge, they are also still very magical as there is no inherent reasoning to them 😅

Something bugs me with this solution though, and that's the reason why I actually went and implemented it myself again (and wrote this post): There is an **obvious relation between`FIZZ_NUMBER` and `FIZZ_TEXT` **but from a code point of view **they are completely separate data structures** only held together by naming conventions and their usage together.

## Working With Rules

Ideally we'd want**a data structure to hold both the text to be outputted and the number that triggers it together**. There's a gazillion ways you could go about this. You could simply use maps, arrays or tuples to hold that data together. As we're doing Ruby right now, I decided to create an object that holds the rule and can apply itself to a rule - either returning its configured text or `nil`.

https://gist.github.com/PragTob/537bb657dee52ba30e5a81c7333291f2

Now, that's quite different! Does it work? Well, yes - and the beauty of it is that so far we haven't altered our API at all so all of these were internal refactorings that work with exactly the same set of tests. Yes, technically this adds additional optional parameters, we'll get to these later 😉

The most interesting thing about this is that **the rule of "if it is divisible by both do X" is gone**. Turns out, that rule isn't really needed:

* if it is divisible by 3 add "Fizz" to the output
* if it is divisible by 5 add "Buzz" to the output
* if it is divisible by neither, just print out the number itself

That works just as well. It means that the order in which we store rules in our `DEFAULT_RULES` array matters (so we don't end up with "BuzzFizz"). Of course we need to verify this with our stakeholders/interviewers, but let's say they agree here. Now, can we allow for even more flexibility with the rules?

## Flexible Rules

Now our "stakeholders" might come back and say well, you know what we're not so sure about just having 2 numbers and their respective outputs. It may be more, it may be less! The good news? **This already completely works with our implementation above**. However, we should still **test it**. You can take a look at all the test I wrote over [here](https://github.com/PragTob/fizz_buzz/blob/main/spec/fizz_buzz_spec.rb), I'll just post the tests here for adding a 3rd rule: 7 and Zazz!

https://gist.github.com/PragTob/95a22ffcc9a3ff8c0813e90804e906a5

As per usual, testing all the different edge cases here is a fun exercise:

* What is the behavior if no rules are passed?
* What happens if the exact same rule is applied twice?
* Can I change the order to make it "BuzzFizz"?

What I also like about this solution is that the rules aren't actually hard coded but are injected from the outside. That allows us to easily test our system against many different rule configurations. It also allows us to run many different rule configurations in the same system - each user of our FizzBuzz platform could have their own settings for FizzBuzz!

## Closing Out

That's quite a bit of changes we went through here. I want to stress, that you shouldn't start with the more complex solution as it is definitely harder to understand. **Y** ou **A** in't **G** onna **N** eed **I** t.However, if there are actual additional requirements or credible uncertainty it might be worth it. I ended up implementing it because I wanted to translate that relationship between "3" and "Fizz" **explicitly into a data structure** , as it feels like an inherent part of the domain. The other properties of it were almost just a by-product.

You can check out the whole code on [github](https://github.com/PragTob/fizz_buzz) and let me know what you think.

Of course, we haven't handled all extension points here:

* The range of 1 to 100 is still hard coded, however that is easily remedied if necessary (by passing the range in as a parameter)
* Our choice of the implementation of `Rule` hard coded the assumption that rules only ever check the divisibility by a number. We couldn't easily produce a rule that says "for every odd number output 'Odd'". Instead of providing `Rule` with just a number, we could instead use an anonymous function to make it even more configurable. However, don't ever forget you ain't gonna need it - even in a coding challenge. Overengineering is also often bad, hence the conversation with your stakeholders/interviewers is important as for what are "sensible" extension points.
* The output mechanism is still just `puts`, as mentioned earlier dependency injecting an object with a specific output method instead would make that more configurable and quite easily so.

Naturally, naming is important and could see some improvement here. However, with completely made up challenges having good naming becomes nigh impossible.

Anyhow, I hope you enjoyed this little journey through FizzBuzz and that it may have been helpful to you. I certainly enjoyed writing that solution 😁

Edit: Earlier versions of the code samples featured bitwise-and (`&`) instead of the proper and operator (`&&`) - both work in this context (hence the tests passed) but you should definitely be using `&&`. Thanks to my friend [Jesse Herrick](https://github.com/JesseHerrick) for pointing that out. Yes the featured image is still wrong. I won't fix it.
