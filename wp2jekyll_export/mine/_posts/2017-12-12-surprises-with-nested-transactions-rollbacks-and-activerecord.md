---
layout: post
permalink: https://pragtob.wordpress.com/2017/12/12/surprises-with-nested-transactions-rollbacks-and-activerecord/
title: Surprises with Nested Transactions,  Rollbacks and ActiveRecord
description: None
date: 2017-12-12 16:52:06 -0000
last_modified_at: 2017-12-12 16:52:06 -0000
publish: true
pin: false
categories:
- Ruby
- Software Engineering
tags:
- ActiveRecord
- database
- nested transactions
- Rails
- transactions
---
Lately I acquired a new hobby. I went around and asked experience Rails developers, whom I respect and value a lot, how many users the following script would create: https://gist.github.com/pragtobgists/0ab874d6e707c85d95f7e27cb2e8ee64 The result should be the same on pretty much any database and any Rails version. For the sake of argument you can assume Rails 5.1 and Postgres 9.6 (what I tested it with). So, how many users _does_ it create? No one from more than a hand full of people I asked got the answer right (including myself). **The answer is 2**.

## Wait, WHAT?

Yup you read that right. It creates 2 users, the rollback is effectively useless here. Ideally this should create one user (Kotori), but as some people know nested transactions isn't really a thing that databases support (save for MS-SQL apparently). People, whom I asked and knew this, then guessed 0 because well if I can't rollback a part of it, better safe than sorry and roll all of it back, right? Well, sadly the inner transaction rescues the rollback and then the outer transaction happily commits all of it. :( Before you get all worried - if an exception is raised and not caught the outer transaction can't commit and hence 0 users are created as expected.

## A fix

So, what can we do? When opening a transaction, we can pass `requires_new: true` to the transaction which will emulate a "real" nested transaction using savepoints: https://gist.github.com/pragtobgists/70fb6eb60eaf4f421b4088ca5ac2b0b2 As you'd expect this creates just **one** user.

## Nah, doesn't concern me I'd never write code like this!

Sure, you probably straight up won't write code like this in a file. However, split across multiple files - I think so. You have one unit of business logic that you want to run in a transaction and then you start reusing it in another method that's also wrapped in another transaction. Happens more often than you think. Plus it can happen even more often than that as **every save operation is wrapped in its own transaction** (for good reasons). That means, as soon as you save anything inside a transaction or you save/update records as part of a callback **you might run into this problem**. Here's a small example highlighting the problem: https://gist.github.com/pragtobgists/d680bbf6fe7aa2ec96d488ce73c7016b As you probably expect by now this creates 2 users. And yes, I checked - if you run create with `rollback: true` outside of the transaction no user is created. Of course, you shouldn't raise rollbacks in callbacks but I'm sure that _someone somewhere does it_. In case you want to play with this, all of these examples (+ more) are up at my [rails playground](https://github.com/PragTob/rails_playground/tree/master/scripts).

## The saddest part of this surprise...

Unless you stumbled across this before, chances are this is at least somewhat surprising to you. If you knew this before, kudos to you. The saddest part is that **this shouldn't be a surprise to anyone** though. A lot of what is written here is **part of the[official documentation](http://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html#module-ActiveRecord::Transactions::ClassMethods-label-Nested+transactions), including the exact example I used.** It introduces the example with the following wonderful sentence:

> For example, the following behavior may be surprising:

As far as I can tell this documentation with the example has [been there for more than 9 years](https://github.com/rails/rails/commit/e916aa7ea1613be966959c05ad41d13fee55a683), and [fxn added the above sentence about 7 years ago](https://github.com/rails/rails/commit/d38644f4a9eead2f9d9ed96e10fb67430de31789). Why do I even blog about this when it's in the official documentation all along? I think this deserves more attention and more people should know about it to avoid truly bad surprises. The fact that nobody I asked knew the answer encouraged me to write this. We should all take care to read the documentation of software we use more, we _might find something interesting you know._ What do we learn from this? **READ THE DOCUMENTATION!!!!**
